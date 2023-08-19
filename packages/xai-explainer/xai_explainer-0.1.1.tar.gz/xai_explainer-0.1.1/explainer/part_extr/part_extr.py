from typing import List, Optional, Tuple

import cv2 as cv
import numpy as np


def extract_parts(
    segmentation: np.ndarray,
    image: np.ndarray,
    heatmap: np.ndarray,
    cut: bool = True,
    replace: str = "zero",
) -> List[tuple]:
    """
    Computes all parts of a segmentation sorted by the heatmap

    Parameters
    ----------
    segmentation : np.ndarray
        Segmentation to be processed. Must be a 2D array of integers.
    image : np.ndarray
        Image to be processed. Must be a 2D array of integers with the same shape as segmentation
    heatmap : np.ndarray
        Heatmap to be processed. Must be a 2D array of integers with the same shape as segmentation
    cut : bool
        If true, the parts will be cut along the bounding box of the segment. Otherwise every part will be the same shape as the image. By default True
    replace : str
        Defines how pixels which do not belong to the segment are replaced. The options are:
        "mean": pixels are replace with the mean of the segment
        "zero": pixels are replaced with zero, default value
        "blur": pixels are blurred
        If there is any other value, pixels are not replaced.

    Returns
    -------
    List[tuple]
        List of tuples containing the part, the relevance and the bounding box of the part. Sorted by relevance.
    """

    parts = []

    for segment_id in np.unique(segmentation):
        if segment_id == 0:
            continue  # background

        part = extract_part(segmentation, image, segment_id, cut, replace)

        mask = (segmentation == segment_id).astype(np.uint8)  # shape: (H, W)
        part_heatmap = np.where(mask, heatmap, 0)
        relevance = float(part_heatmap.sum())

        rect = cv.boundingRect(
            mask
        )  # x,y,w,h = cv.boundingRect(cnt), https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html

        parts.append((part, relevance, rect))

    sorted_parts = sorted(parts, key=lambda x: x[1], reverse=True)
    return sorted_parts


def extract_part(
    segmentation: np.ndarray,
    image: np.ndarray,
    segment_id: int,
    cut: bool = True,
    replace: str = "zero",
) -> np.ndarray:
    """
    Computes the part of a specified segment

    Parameters
    ----------
    segmentation : np.ndarray
        Segmentation to be processed. Must be a 2D array of integers.
    image : np.ndarray
        Image to be processed. Must be a 3D array of integers.
    segment_id : id
        Id of the segment
    cut : bool
        If true, the parts will be cut along the bounding box of the segment. Otherwise every part will be the same shape as the image. By default True
    replace : str
        Defines how pixels which do not belong to the segment are replaced. The options are:
        "mean": pixels are replace with the mean of the segment
        "zero": pixels are replaced with zero, default value
        "blur": pixels are blurred
        If there is any other value, pixels are not replaced.

    Returns
    -------
    np.ndarray
        part
    """
    assert (
        segmentation.shape[0] == image.shape[0]
        and segmentation.shape[1] == image.shape[1]
    )

    # cut bounding box of this segment if cut == True
    part_img = 0
    part_seg = 0
    if cut:
        segment = segmentation == segment_id
        segment = segment.astype(np.uint8)

        x_min = np.min(np.where(segment)[1])
        x_max = np.max(np.where(segment)[1])
        y_min = np.min(np.where(segment)[0])
        y_max = np.max(np.where(segment)[0])

        part_img = image[y_min : y_max + 1, x_min : x_max + 1]
        part_seg = segmentation[y_min : y_max + 1, x_min : x_max + 1]
    else:
        part_img = np.copy(image)
        part_seg = segmentation

    # replace other pixels if replace is specified
    in_segment = np.repeat(part_seg == segment_id, 3, 1)
    in_segment = np.reshape(in_segment, (part_seg.shape[0], part_seg.shape[1], 3))

    if replace == "mean":
        mean = np.mean(part_img, axis=(0, 1), where=in_segment)
        fill = np.full_like(part_img, mean)
        part_img = np.multiply(part_img, in_segment)
        fill = np.multiply(fill, np.invert(in_segment))
        part_img = part_img + fill
    elif replace == "zero":
        part_img = np.multiply(part_img, in_segment)
    elif replace == "blur":
        fill = part_img
        for i in range(0, 10):
            fill = cv.blur(fill, (5, 5))
        fill = np.multiply(fill, np.invert(in_segment))
        part_img = np.multiply(part_img, in_segment)
        part_img = part_img + fill

    return part_img
