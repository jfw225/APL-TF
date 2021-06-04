from pipeline import Pipeline

class InputCapture(Pipeline):
    """Modify this class to change the input to the pipeline."""

    def __init__(self, source=list()):
        self.counter = 0
        self.results = list()

        super().__init__(source)

    def is_working(self):
        """Modify this to change the working condition."""

        return any(self.source)

    def input_ready(self):
        """Modify this to determine when to capture an input."""

        self.counter = (current_counter := self.counter) + 1

        return current_counter % 5 == 0 and any(self.source)

    def map(self, data):
        """Modify this to change what data is submitted to the pipe."""

        ## Use None to communicate to predictor that there is no new input but the pipe should continue if
        ##      there's an output waiting.

        data = self.source.popleft() if self.input_ready() else Pipeline.Empty

        return data

    def run(self, pl: Pipeline):
        """Modify this to change run functionality."""

        while self.is_working():
            result = pl.map(None)
            self.results.append(result)

        results = [r for r in self.results if r]

        return results

