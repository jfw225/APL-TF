
from pipeline.pipeline import Pipeline


class Predict(Pipeline):
    def __init__(self, source):
        super().__init__(source=source)
