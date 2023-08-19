from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Union

from PIL import Image
import cv2 as cv
import numpy as np


@dataclass(frozen=True)
class Part:
    img: Image = field(repr=False)
    relevancy: Union[int, float]
    labels: dict
    rect: tuple  # x,y,w,h --> probably some checks needed to confirm this

    def __post_init__(self):
        # sanity checks
        assert isinstance(self.img, Image.Image), type(self.img)
        assert isinstance(self.relevancy, (float, int)), type(self.relevancy)
        assert isinstance(self.labels, dict), type(self.labels)
        assert isinstance(self.rect, tuple), type(self.rect)
        assert len(self.rect) == 4, len(self.rect)

    def to_disk(self, path: Path):
        parts_string = ""
        for class_, parts in self.labels.items():
            parts_string += f"{class_}({','.join(parts)})_"

        self.img.save(path / "tmp" / f"{parts_string}_{int(self.relevancy)}.png")


@dataclass(frozen=True)
class Object:
    heatmap: np.ndarray = field(repr=False)
    label: str
    parts: List[Part]

    def __post_init__(self):
        # sanity checks
        assert isinstance(self.heatmap, np.ndarray)
        assert isinstance(self.label, str)
        assert isinstance(self.parts, list)

    def to_disk(self, path: Path):
        heatmap = Image.fromarray((self.heatmap.astype(np.float32)) * 255)
        heatmap = heatmap.convert("RGB")
        heatmap.save(path / "tmp" / "heatmap.png")
        for part in self.parts:
            part.to_disk(path)

    def get_cam(self, np_img: np.ndarray, image_weight: float = 0.5) -> Image:
        cam = _show_cam_on_image(
            img=np_img,
            mask=self.heatmap,
            use_rgb=True,
            image_weight=image_weight,
        )

        return Image.fromarray(cam)


@dataclass(frozen=True)
class Result:
    img: Image
    objects: List[Object]

    def __post_init__(self):
        # sanity checks
        assert isinstance(self.img, Image.Image)
        assert isinstance(self.objects, list)

    def to_disk(self, path: Path):
        self.img.save(path / "tmp" / "original.png")
        for obj in self.objects:
            cam = obj.get_cam(np_img=np.array(self.img))
            cam.save(path / "tmp" / f"{obj.label}_cam.png")
        for obj in self.objects:
            obj.to_disk(path)

    def as_dict(self):
        return asdict(self)


# Credit: https://github.com/jacobgil/pytorch-grad-cam/blob/master/pytorch_grad_cam/utils/image.py#L33
def _show_cam_on_image(
    img: np.ndarray,
    mask: np.ndarray,
    use_rgb: bool = False,
    colormap: int = cv.COLORMAP_JET,
    image_weight: float = 0.5,
) -> np.ndarray:
    """This function overlays the cam mask on the image as an heatmap.
    By default the heatmap is in BGR format.

    :param img: The base image in RGB or BGR format. Values are expected to be RGB or BGR in range [0, 255].
    :param mask: The cam mask. Values should be in the range [0, 1] and same height and width as the 'img'.
    :param use_rgb: Whether to use an RGB or BGR heatmap, this should be set to True if 'img' is in RGB format.
    :param colormap: The OpenCV colormap to be used.
    :param image_weight: The final result is image_weight * img + (1-image_weight) * mask.
    :returns: The default image with the cam overlay.
    """
    img = np.float32(img) / 255  # Scale to range [0, 1].
    heatmap = cv.applyColorMap(np.uint8(255 * mask), colormap)
    if use_rgb:
        heatmap = cv.cvtColor(heatmap, cv.COLOR_BGR2RGB)
    heatmap = np.float32(heatmap) / 255

    if np.max(img) > 1:
        raise Exception("The input image should np.float32 in the range [0, 1]")

    if image_weight < 0 or image_weight > 1:
        raise Exception(
            f"image_weight should be in the range [0, 1].\
                Got: {image_weight}"
        )

    cam = (1 - image_weight) * heatmap + image_weight * img
    cam = cam / np.max(cam)
    return np.uint8(255 * cam)
