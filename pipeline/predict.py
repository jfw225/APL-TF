from pipeline.pipeline import Pipeline

from detectron2.engine.defaults import DefaultPredictor


class Predict(Pipeline):
    def __init__(self, cfg):
        self.predictor = DefaultPredictor(cfg)

        super().__init__()

    def is_working(self):
        """ Returns False because predictions are done linearly. """

        return False

    def map(self, data):
        image = data["image"]
        predictions = self.predictor(image)
        data["predictions"] = predictions

        return data

    def cleanup(self):
        pass
