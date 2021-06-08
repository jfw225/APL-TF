from pipeline import Pipeline

class TestPipe1(Pipeline):
    def __init__(self):
        super().__init__()

    def map(self, data):
        return data ** .5