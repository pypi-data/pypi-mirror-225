from .DataPipe import DataPipe
from .BatchMap import BatchMap
from .ShuffleMap import ShuffleMap
from .ThreadMap import ThreadMap


class DataLoader:
    @staticmethod
    def build(
        data: DataPipe,
        batchSize=1,
        onlyFullBatches=False,
        numThreads=1,
        shuffle=False,
        shuffleSeed=None,
        mapBatchToXY=True,
        torch=False,
        torchCuda=False,
    ):
        if shuffle:
            data = ShuffleMap(data, seed=shuffleSeed)

        if batchSize > 1:
            data = BatchMap(data, batchSize, onlyFullBatches, toXY=mapBatchToXY)

        if torch:
            from .TorchMap import TorchMap

            data = TorchMap(data, cuda=torchCuda)

        if numThreads > 1:
            data = ThreadMap(data, numThreads=numThreads)

        return data
