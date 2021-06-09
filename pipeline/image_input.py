import os
from collections import deque
from cv2 import imread

from pipeline.pipeline import Pipeline


class ImageInput(Pipeline):
    """ Pipeline task to capture images. """

    def __init__(self, path, valid_exts=(".jpg", ".png"), level=None, contains=None):
        self.valid_exts = valid_exts
        self.level = level
        self.contains = contains

        if os.path.isdir(path):
            images = self.images_from_dir(path)
        else:
            images = [path] if self.valid_extension(path) else []

        self.images = deque(images)

        super().__init__()

    def valid_extension(self, path):
        """ Returns True if path has a valid image extension. """
        return os.path.splitext(path)[-1] in self.valid_exts

    def images_from_dir(self, path: str) -> list[str]:
        """ Returns a list of paths to valid images. """

        images = list()
        for root, _, files in os.walk(path):
            for img in files:
                if self.valid_extension(img):
                    images.append(os.path.join(root, img))

        return images

    def is_working(self):
        """ Returns True if there are images yet to be captured. """

        return len(self.images) > 0

    def image_ready(self):
        """ Returns True if the next image is ready. """

        return True

    def map(self, _):
        """ Returns the image content and metadata of the next image in the input. """

        if not self.image_ready():
            return Pipeline.Skip

        image_file = self.images.popleft()
        image = imread(image_file)

        data = {
            "image_id": image_file,
            "image": image
        }

        return data
