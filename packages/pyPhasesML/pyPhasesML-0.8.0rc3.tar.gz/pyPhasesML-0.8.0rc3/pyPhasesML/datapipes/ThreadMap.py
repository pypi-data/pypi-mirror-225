import threading
import queue
from pyPhasesML.datapipes.DataPipe import DataPipe

class ThreadMap(DataPipe):
    def __init__(self, datapipe: DataPipe, numThreads=2, preloadCount=3):
        super().__init__(datapipe)
        self.numThreads = numThreads
        self.queue = queue.Queue(maxsize=preloadCount)
        self.threads = []
        self.preloaded = 0

        self.start()
    
    def start(self):
        # Create and start worker threads
        for _ in range(self.numThreads):
            thread = threading.Thread(target=self._loadData)
            thread.start()
            self.threads.append(thread)
        return self

    def close(self):
        # Signal threads to exit
        for _ in range(self.numThreads):
            self.queue.put(None)
        # Wait for threads to finish
        for thread in self.threads:
            thread.join()

    def _loadData(self):
        for data in self.datapipe:
            self.queue.put(data)
            self.preloaded += 1

    def __getitem__(self, index):
        r = self.queue.get()
        self.preloaded -= 1
        return r
