import argparse

import cv2
import numpy as np
from skimage.segmentation import mark_boundaries

try:
    from . import segment
except ImportError:
    from __init__ import segment


def _prepare_img(img) -> np.ndarray:
    """
    Convert image to 8-bit unsigned integer.

    Parameters
    ----------
    img : np.ndarray
        RGB-image to convert

    Returns
    -------
    np.ndarray
        Converted image

    """
    if img.max() <= 1:
        img *= 255
        img = np.array(img, dtype=np.uint8)
    else:
        img = np.array(img, dtype=np.uint8)

    return img


def _demo(path, method) -> None:
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print(f"Segmenting image with {method}")
    print(f"Image shape: {img.shape}")
    segments = segment(img, method=method)
    fig = mark_boundaries(img, segments)
    fig = _prepare_img(fig)
    fig = cv2.cvtColor(fig, cv2.COLOR_RGB2BGR)
    cv2.imshow(f"Superpixels -- {method}", fig)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", type=str, required=True, help="path to image")
    parser.add_argument(
        "--method", type=str, default="slic", help="segmentation method"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = _parse_args()
    _demo(args.img, args.method)
