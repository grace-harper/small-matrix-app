# Getting Started 

## Running the App
### Option 1:
 - Pyinstaller  
    - https://www.pyinstaller.org/  
    - Only works with Python3.5 - 3.7!  
    - Can compile on any platform
    - Clone this repo to where you want it installed
    ```$ pip install -r requirements.txt     
        $ cd ./matrix_app 
        $ pyinstaller ./main.py
        $ ./dist/main/main
   ```
    - Please note: The online instructions say to run `pyinstaller yourfile.py` 
    but if you need to run it as a module because you have multipled python versions
     going one, then try ` python3 -m PyInstaller main.py ` in order to compile.

## Matrix Calculator App 
- This app allows you to enter (or randomly generate) two matrices, A and B (no larger than 10x10), and then multiply them to 
create a third matrix C.   
- From here you have the option to save just A,B,C, or to calculate
some interesting stats (min, max, mean, cumulative product along a given axis) on C and add those stats to
your saved run.   
- All runs are saved in a local directory, SavedRuns. Each run includes either just A,B, and C (if the stats were not saved)
or A, B, C and all calculated stats.   
- The user can name each run as they want.  
- If a user wishes to review a run, they may go to the list of saved runs and choose to display a saved run. 
All saved runs are saved to a local directory and, if the app configurations/location 
 are not changed, will be available even if the app is closed and reopened
  


## Design Decisions

#### Architecture
###### MVC-ish Architecture 
   - The DatabaseModel is the gatekeeper to the database. Any data permanently stored to disk is saved to disk 
    and loaded from disk via this class. Unlike other MVCs (https://www.learnpyqt.com/courses/model-views/modelview-architecture/), 
    the DatabaseModel itself holds no data and does not serve as a cache. Instead, because the app is small and low-volume, any 
    data deemed permanent is immediately written to disk. (Adding caching before writing to disk would improve scalability if the app volume ever did increase.)
   - If some data has not been saved to disk, it is stored in the current widget in which it was created. This design 
    decision came about because I originally did not want the database being responsible for holding unsaved, potentially temporary data that a different widget 
    was currently presenting to the user. (In hindsight, while this current design is functional, instead using the DatabaseModel 
    as a source of truth for the current data state of the app and letting all other widgets pull from it would have been a better design.)
   

###### MainWindow Widget Manager 
   'page' is used to refer to whichever widget is set as the central widget to the MainWindow (QMainWindow). 'screen' is used to refer to what the user sees when they look at the app.
   - There was limited documentation online for screen changing. Searching through the anki code (https://github.com/ankitects/anki) it appeared they acheive different 
   screens by having multiple QMainWindows managed by a window manager they developed. However this design seemed due in large part to a need to preserve the state of different screens 
    as a user went back and forth between them - which is not a use case for this app.
    https://www.learnpyqt.com/ explained that it is best to minimize parentless widgets (in which QMainWindow are included)
    However, different "screens" were needed to provide a friendlier user experience. Since these screens could not be QMainWindows, a new approach was designed: 
        - There is one MainWindow class 
    inherited from QMainWindow that serves as a "Widget Page Manager" so to speak. There are several classes (HomeScreenPage, SavedRunsPage, etc.) each of which inherits from QtWidgets.QWidget and is
    designed to be a screen. The MainWindow sets it's central widget to be whatever page the user should be on.
        - If given the chance to remake the app, it seems to me a good choice to make a Page class that could serve as a parent to all pages (homescreen, display, etc.).
    If nothing else, it would allow for better organization of the code. Through polymorphism, it might provide a cleaner solution to changing screen. 
   - Any parentless widget will be garbage collected and any screen, if revisited by the user, should not have the same data as when the user left it.
    Thus, it was okay to make a new instantiation of a given page class for each screen switch. 
   - Any buttons pushes on a page widget that led to a screen change has to be connected by the MainWindow. Any other events were handled by the widget that created the event. 
        - A better design would avoid having the MainWindow wire any buttons from a different widget. Perhaps each page could import the necessary methods or if there is a signal
        in PyQt5 that could alert MainWindow to a specific hard-coded value, that evaluates to the next page.
        
###### Error Handling (given our Widget Manager)
   - The Error Handling was an experimental combination of Golang-style errors (nothing is raised nor thrown, just returned) and Pythonic exceptions. The goal was to 
   differentiate the change in flow by having widgets return errors (to the MainWindow usually) if they wished to keep control of the screen - and raising exceptions if 
    they required action on the part of another widget/window. 
   - Rules:
        - Any error that could be handled within a given widget was handled by that widget. 
        - All other errors became exceptions
   - Example: There is a button in a Page 1 widget to which the MainWindow has connected a transition method (transitioning from Page 1 to Page 2). If the button push fails in an anticipated way,
   Page 1 will return an error to the MainWindow, which will do nothing (not transition to Page 2). And, Page 1 will generate and display the pop-up error box for that error (and continue to be on the screen).  
   - Example: If something happens that the widget is unable to handle, for example the DatabaseModel fails to instantiate on startup, that is thrown as an exception and the MainWindow will take over.  
   In this particular example, the MainWindow would display an error pop up box which, when OK was pressed, would close the app. 
   
   
 
#### Testing
   - All tests are located in `./test` 
        - To run a particular test: 
            - ```cd test```
            - ```python3 -m unittest <testname>```
        - To run all tests:   
            - ```cd test```
            - ```python3 -m unittest discover .```
            
                 
    

   
