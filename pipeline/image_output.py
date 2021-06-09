import os
import cv2

from pipeline.pipeline import Pipeline


class ImageOutput(Pipeline):
    """ Pipeline task that delivers the images to some output. """

    def __init__(self, src, path,
                 image_ext=".jpg", jpg_quality=None, png_compression=None):

        self.src = src
        self.path = path
        self.image_ext = image_ext

        # 0 - 100 (higher means better). Default is 95.
        self.jpg_quality = jpg_quality

        # 0 - 9 (higher means a smaller size and longer compression time). Default is 3.
        self.png_compression = png_compression

        super().__init__()

    def map(self, data):
        image = data[self.src]
        image_id = data["image_id"]

        # Prepare output for image based on image_id
        dirname, basename = os.path.split(image_id)

        dirname = os.path.join(self.path, dirname)
        os.makedirs(dirname, exist_ok=True)

        basename = os.path.splitext(basename)[0] + self.image_ext

        path = os.path.join(dirname, basename)

        if self.image_ext == ".jpg":
            cv2.imwrite(path, image,
                        (cv2.IMWRITE_JPEG_QUALITY, self.jpg_quality) if self.jpg_quality else None)
        elif self.image_ext == ".png":
            cv2.imwrite(path, image,
                        (cv2.IMWRITE_PNG_COMPRESSION, self.png_compression) if self.png_compression else None)
        else:
            raise Exception("Unsupported image format")

        return data
