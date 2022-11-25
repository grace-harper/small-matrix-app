"""small_matrix_app.matrix_app.all_exceptions.py"""

# Used in return values to indicated failure
# Used in exceptions to indicate loss of control
class FailureMessage(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        def __str__(self):
            return "ERROR: " + message


# End process
class CriticalFailure(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return "Critical Failure Error Encountered: " + self.message


# Db Choked
class InternalDbError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return "DB ERROR: " + self.message
