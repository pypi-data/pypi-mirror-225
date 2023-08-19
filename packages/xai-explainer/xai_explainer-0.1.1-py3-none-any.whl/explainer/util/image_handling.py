import copy
import logging
from pathlib import Path
from re import I
from typing import Union

from PIL import Image
import cv2 as cv
import numpy as np
import torch
from torch import nn
from torchvision import transforms

"""
WIP - not used yet
"""


class GeneralizedImage:
    def __init__(
        self, img: Union[Image.Image, np.ndarray, torch.Tensor, "GeneralizedImage"]
    ):
        self._pil_img: Image.Image = self._to_pil(
            img
        )  # inernal representation of the image

    def _to_pil(
        self, img: Union[Image.Image, np.ndarray, torch.Tensor, "GeneralizedImage"]
    ) -> Image.Image:
        """
        Convert the image to a PIL image.
        """
        if not isinstance(
            img, (Image.Image, np.ndarray, torch.Tensor, GeneralizedImage)
        ):
            raise ValueError(
                f"Image type {type(img)} not supported. Supported types are: Image.Image, np.ndarray, torch.Tensor, GeneralizedImage."
            )

        if isinstance(img, GeneralizedImage):
            return img.to_pil()

        if isinstance(img, Image.Image):
            assert img.mode == "RGB"
            assert img.size[0] > 0
            assert img.size[1] > 0
            _arr = np.array(img)
            assert (
                0 <= _arr.min() <= _arr.max() <= 255
            ), f"Image values must be in [0, 255]."

            if _arr.max() <= 1:
                logging.warning("Image values are in [0, 1]. Converting to [0, 255].")
                _arr = _arr * 255
                img = Image.fromarray(_arr.astype(np.uint8))

            return img

        if isinstance(img, torch.Tensor):
            img = img.numpy(force=True)

            if img.shape[0] == 1:
                img = img.squeeze(0)  # remove batch dimension

            img = np.transpose(img, (1, 2, 0))  # CHW -> HWC

        if isinstance(img, np.ndarray):
            if img.max() <= 1:
                img = img * 255
            assert img.max() <= 255
            assert img.min() >= 0
            img = img.astype(np.uint8)

            return Image.fromarray(img)

    def normalize(self, mean, std, inplace=False, **kwargs) -> "GeneralizedImage":
        _img = self.to_tensor()
        _img = transforms.functional.normalize(_img, mean, std, **kwargs)
        if inplace:
            self._pil_img = self._to_pil(_img)
            return self
        else:
            return GeneralizedImage(self._pil_img.normalize(mean, std, **kwargs))

    def resize(self, size, inplace=False, **kwargs) -> "GeneralizedImage":
        if inplace:
            self._pil_img = self._pil_img.resize(size, **kwargs)
            return self
        else:
            return GeneralizedImage(self._pil_img.resize(size, **kwargs))

    def to_tensor(self, add_batch_dim=False) -> torch.Tensor:
        pass

    def to_numpy(self) -> np.ndarray:
        pass

    def to_pil(self) -> Image.Image:
        return copy.deepcopy(self._pil_img)

    def show(self):
        self._pil_img.show()

    @property
    def shape(self):
        return self._pil_img.size

    @property
    def size(self):
        return self._pil_img.size
