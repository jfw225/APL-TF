from torch import device

from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer

from pipeline.pipeline import Pipeline


class AnnotateImage(Pipeline):
    """Pipeline task for image annotation."""

    def __init__(self, dst, metadata_name, instance_mode=ColorMode.IMAGE):
        self.dst = dst
        self.metadata_name = metadata_name
        self.metadata = MetadataCatalog.get(metadata_name)
        self.instance_mode = instance_mode
        self.cpu_device = device("cpu")

        super().__init__()
