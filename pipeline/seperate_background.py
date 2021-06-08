from pipeline.pipeline import Pipeline


class SeperateBackground(Pipeline):
    def __init__(self, source):
        super().__init__(source=source)
