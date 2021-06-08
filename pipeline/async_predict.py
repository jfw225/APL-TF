from pipeline.pipeline import Pipeline
from pipeline.libs.async_predictor import AsyncWorker


class AsyncPredict(Pipeline):
    def __init__(self, num_gpus: int = 1, num_cpus: int = 1, queue_size: int = 3, ordered=True):
        self.predictor = AsyncWorker(num_gpus, num_cpus)

        super().__init__()

    def map(self, data):
        if data != Pipeline.Empty:
            self.predictor.put(data)

        return self.predictor.get() if self.predictor.ready() else Pipeline.Skip

        # return data if data else Pipeline.Skip
    def is_working(self):
        return not self.predictor.is_idle()

    def cleanup(self):
        self.predictor.shutdown()
