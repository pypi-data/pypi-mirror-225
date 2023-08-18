from pyPhasesML.datapipes.DataPipe import DataPipe


class DatasetXY(DataPipe):
    def __init__(self, X, Y):
        self.datapipe = list(zip(X, Y))

