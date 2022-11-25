"""
small_matrix_app.matrix_app.db_widget.py
This widgets writes data to or loads data from disk
"""

import os

import h5py

from PyQt5 import QtWidgets

from typing import List

import numpy as np

from os import mkdir, remove, path, listdir
from os.path import isfile, join

from matrix_app.all_exceptions import (
    FailureMessage,
    CriticalFailure,
    InternalDbError,
)


class DisplayData:
    def __init__(self, label: str, data):
        """Class for have an organized way of keeping label with data """
        self.label = label
        self.data = data

    def __str__(self):
        return str(self.label) + ":\n" + str(self.data) + "\n"


class RunData:
    def __init__(
        self,
        run_name: str,
        matrices: List[DisplayData],
        stats: List[DisplayData],
        saved: bool = False,
        random: str = None,
    ):
        """
        Class for hold matrices and their stats
        Args:
        run_name -- name of the run
        matrices -- the two entered matrices and their product
        stats -- any calculated stats for a given run
        saved -- whether the run was previously saved
        """
        self.run_name = run_name
        self.matrices = matrices
        self.stats = stats
        self.saved = saved
        if random is None:
            self.random = ""
        else:
            self.random = random

    def __str__(self):
        basestr = self.run_name + ":\n Matrices:\n"
        for m in self.matrices:
            basestr += str(m)
        basestr += "Stats:\n"
        for s in self.stats:
            basestr += str(s)
        basestr += "Saved: " + str(self.saved) + "\n"
        return basestr


class DatabaseModel(QtWidgets.QWidget):
    MATRIX_GROUP = "matrices"
    STATS_GROUP = "stats"
    NO_STATS_RUN = "-No_Stats_Run"

    def __init__(self, DB_Name="SavedRuns", parent=None):
        """ Create DB and reads in any pre-existing data into relevant models"""
        super().__init__()
        self.db_name = DB_Name
        self._db_name_f = self.db_name + "/"
        self._past_runs = {}  # for loading the SavedRunsPage()
        self._past_runs_list = []
        self._set_up_db()

    def _set_up_db(self):
        if path.exists(self.db_name):
            if path.isdir(self.db_name):
                pass
            else:
                raise CriticalFailure(
                    "Cannot create DB, "
                    + self.db_name
                    + ", as there is a file that already exists with that name. "
                )
        else:
            mkdir(self.db_name)

        prev_run_files = [
            f
            for f in listdir(self._db_name_f)
            if isfile(join(self._db_name_f, f)) and f.endswith(".h5")
        ]
        for prf in prev_run_files:
            run_name = prf.split(".")[0].split("-")[
                0
            ]  # Doesn't matter is there is a run1-No_Stats_Run and a run1 because load will get the fullest version
            self._past_runs[run_name] = 1
            self._past_runs_list.append(run_name)

    def get_previous_runs(self):
        return list(self._past_runs.keys())

    def load_run(self, run_name: str) -> (RunData):
        """ Return data for a particular run"""
        run_data = RunData("", None, None)
        matrices = []
        stats = []
        run_file = self._db_name_f + run_name + ".h5"
        if not path.exists(run_file):
            run_file = self._db_name_f + run_name + self.NO_STATS_RUN + ".h5"
            if not path.exists(run_file):
                raise InternalDbError("ERROR: File does not exist")
        try:
            with h5py.File(run_file, "r") as hdf:
                matrix_group = hdf.get(self.MATRIX_GROUP)

                for mgi in list(matrix_group.keys()):
                    dd = DisplayData(mgi, np.array(matrix_group[mgi]))
                    matrices.append(dd)

                # Only get stats if stats were saved
                if not self.NO_STATS_RUN in run_file:
                    stats_group = hdf.get(self.STATS_GROUP)
                    for sgi in list(stats_group.keys()):
                        dd = DisplayData(sgi, np.array(stats_group[sgi]))
                        stats.append(dd)
        except Exception as e:
            raise InternalDbError(
                "ERROR: Could not read saved .h5 file. ERROR: " + str(e)
            )

        run_data.run_name = run_name
        run_data.matrices = matrices
        run_data.stats = stats
        run_data.saved = True
        return run_data

    def save_run(self, c_run: RunData) -> FailureMessage:
        """save data for a particular run to disk"""
        # error if run already exists
        run_name = c_run.run_name
        run_file = self._db_name_f + run_name + ".h5"
        if path.exists(run_file):
            return FailureMessage("ERROR: Saved File (all stats) already exists")

        if len(c_run.stats) < 1:
            run_file = self._db_name_f + run_name + self.NO_STATS_RUN + ".h5"
            if path.exists(run_file):
                return FailureMessage("ERROR: Saved File (no stats) already exists")
        if run_name in self._past_runs:
            if self._past_runs[run_name] != c_run.random:
                return FailureMessage(
                    "ERROR: Saved File already exists with that run name"
                )
        try:
            with h5py.File(run_file, "w") as hdf:
                matrix_group = hdf.create_group(self.MATRIX_GROUP)
                for m in c_run.matrices:
                    matrix_group.create_dataset(m.label, data=m.data)

                stats_group = hdf.create_group(self.STATS_GROUP)
                for s in c_run.stats:
                    stats_group.create_dataset(s.label, data=s.data)
            if self.NO_STATS_RUN not in run_file:
                if path.exists(self._db_name_f + run_name + self.NO_STATS_RUN + ".h5"):
                    os.remove(self._db_name_f + run_name + self.NO_STATS_RUN + ".h5")
        except Exception as e:
            if path.exists(run_file):
                os.remove(run_file)
            return FailureMessage("ERROR: Could not save file: " + str(e))
        self._past_runs[run_name] = c_run.random
        return None
