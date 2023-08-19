import cv2
import skimage.segmentation as seg

from .methods._dbscan import main as _dbscan
from .methods._k_means import main as _k_means
from .methods._selective_search import main as _selective_search
from .methods._watershed import main as _watershed
from .pre_seg import (
    bounding_boxes_from_segmentation,
    extract_relevant_segments,
    merge_neighbors,
)
from .pre_seg import register as __register__
from .pre_seg import segment

__all__ = [
    "segment",
    "extract_relevant_segments",
    "bounding_boxes_from_segmentation",
    "merge_neighbors",
]


# Register methods
__register__(_dbscan, name="dbscan")
__register__(_k_means, name="k_means")
__register__(_selective_search, name="selective_search")
__register__(_watershed, name="watershed")
__register__(func=seg.slic, transform=None, name="slic")
__register__(func=seg.quickshift, transform=None, name="quickshift")
__register__(
    func=seg.felzenszwalb,
    name="felzenszwalb",
)
__register__(
    func=seg.chan_vese,
    transform=lambda x: cv2.cvtColor(x, cv2.COLOR_RGB2GRAY),
    name="chan_vese",
)
