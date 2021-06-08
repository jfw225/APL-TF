from pipeline.pipeline import Pipeline
from multiprocessing import Process, Queue, cpu_count
import torch

from time import sleep


def some_function(data):
    print("Current Data: " + str(data))
    sleep(.1)
    return data * data


class AsyncWorker:
    """The asynchronous worker."""

    class _Worker(Process):
        def __init__(self, task_queue, result_queue):
            self.task_queue = task_queue
            self.result_queue = result_queue

            super().__init__(daemon=True)

        def run(self):
            while (task := self.task_queue.get()) != Pipeline.Stop:
                data = task
                result = some_function(data)  # replace this with analysis
                self.result_queue.put(result)

    def __init__(self, num_gpus: int = 0, num_cpus: int = 0):
        num_gpus = min(torch.cuda.device_count(), num_gpus)
        num_cpus = min(cpu_count(), num_cpus)
        assert num_gpus > 0 or num_cpus > 0, "Must specify number of gpus or cpus"

        self.inx = self.outx = 0

        self.task_queue = Queue()
        self.result_queue = Queue()
        self.workers = list()

        # Create GPU Workers
        for gpuid in range(num_gpus if num_gpus >= 0 else 0):
            pass

        # Create CPU Workers
        for _ in range(num_cpus if num_cpus >= 0 else 0):
            self.workers.append(
                AsyncWorker._Worker(self.task_queue, self.result_queue)
            )

        # Start the Jobs
        for w in self.workers:
            w.start()

    def put(self, data):
        self.inx += 1
        self.task_queue.put(data)

    def get(self):
        self.outx += 1
        return self.result_queue.get()

    def ready(self):
        return not self.result_queue.empty()

    def is_idle(self):
        return self.inx == self.outx and self.task_queue.empty() and self.result_queue.empty()

    def shutdown(self):
        for _ in self.workers:
            self.task_queue.put(Pipeline.Stop)
