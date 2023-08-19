import copy
import logging
import time
from typing import List

import numpy as np
import torch
from PIL import Image
from torch import nn
from torchvision import transforms

from explainer.base.base_explainable_model import ExplainedInput
from explainer.grabcut.grabcut import relevantAreaMask
from explainer.models import get_model
from explainer.part_extr import extract_parts as part_extraction
from explainer.pre_seg import extract_relevant_segments, merge_neighbors, segment
from explainer.util.filehandling import clear_temporary_files
from explainer.util.return_types import Object, Part, Result


def _init_cuda(device_id, torch_seed):
    torch.random.manual_seed(torch_seed)

    if torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        if device_id == "cpu":
            logging.warning("Running on CPU, despite CUDA being available!")
    else:
        if device_id != "cpu":
            logging.warning("CUDA not available, running on CPU!")
        device_id = "cpu"
    device = torch.device(device_id)

    return device


def _pascal_transform(img: Image, size=(224, 224)):
    return transforms.Compose(
        [
            transforms.Resize(size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )(img)


def _timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        time_delta_ms = (end - start) * 1000
        logging.debug(f"@_timeit: {func.__name__} took {time_delta_ms:.2f} ms")
        return result

    return wrapper


@_timeit
def _run_object_model(
    img: Image, object_model: str, device: torch.device, **kwargs
) -> ExplainedInput:
    model = get_model(
        model_name=object_model,
        device=device,
        **kwargs,
    )

    logging.debug(f"Model: {model.__class__.__name__} device: {model.device()}")

    _categories = [
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "diningtable",
        "dog",
        "horse",
        "motorbike",
        "person",
        "pottedplant",
        "sheep",
        "sofa",
        "train",
        "tvmonitor",
    ]

    idx_to_name = {i: c for i, c in enumerate(_categories)}

    # preprocess image
    img = copy.deepcopy(img)  # don't modify the original image

    img = _pascal_transform(img)
    img = img.unsqueeze(0)
    img = img.to(device)

    assert (
        model.device() == img.device
    ), f"Model device: {model.device()} != image device: {img.device}"

    # run model
    out = model.explain(img)[0]

    return out, idx_to_name


def _extract_parts(
    heatmap: np.ndarray,
    img: np.ndarray,
    n_segments: int = 1000,  # number of segments in initial segmentation
    compactness: int = 10,  # compactness of segmentation
    grabcut: bool = False,
    extraction_method="threshold",  # No grabcut: Method for selecting relevant segments. Options "threshold", "top_k_segments"
    threshold=0.35,  # No grabcut: Threshold when using method "threshold"
    num_segments=10,  # No grabcut: Number of segments when using method "top_k_segments"
    thresh_fgd=0.8,  # With grabcut: threshold for sure foreground
    thresh_bgd=0.4,  # With grabcut: threshold for sure background
    seg_method="slic",  # "felzenszwalb" # "slic" # "watershed" # "quickshift
    merge_method="louvain",  # "normalized_graph_cut" # "greedy_modularity" # "girvan_newman" # "louvain"
    num_parts=5,  # only relevant for  "normalized_graph_cut" and "girvan_newman"
):
    if grabcut:
        relevant_area = relevantAreaMask(img, heatmap, thresh_bgd, thresh_fgd)

        seg_img = segment(
            img=img,
            method=seg_method,
            n_segments=n_segments,
            compactness=compactness,
            mask=relevant_area,
        )
        seg_img[seg_img == 1] = 0

        relevant_segments = merge_neighbors(seg_img, heatmap, merge_method, num_parts)
    else:
        seg_img = segment(
            img=img,
            method=seg_method,
            n_segments=n_segments,
            compactness=compactness,
        )

        relevant_segments = extract_relevant_segments(
            segmentation=seg_img,
            heatmap=heatmap,
            evaluation_method="mean",
            merge_neightbors=True,
            num_pixels=-1,
            extraction_method=extraction_method,
            threshold=threshold,
            num_segments=num_segments,
            partition_method=merge_method,
            num_parts=num_parts,
        )

    parts = part_extraction(
        segmentation=relevant_segments,
        image=img,
        heatmap=heatmap,
        cut=True,
        replace="blur",
    )

    return parts


@_timeit
def extract_parts(np_img, heatmap, **kwargs):
    use_grabcut = kwargs.get("grabcut", False)
    segmentation_method = kwargs.get("seg_method", "slic")

    exctracted_parts: List[tuple] = _extract_parts(
        heatmap,
        np_img,
        grabcut=use_grabcut,
        seg_method=segmentation_method,
        n_segments=200 if use_grabcut else 1000,
    )

    return exctracted_parts


def _run_parts_model(img: Image, parts_model, device, **kwargs):
    model = get_model(
        model_name=parts_model,
        device=device,
        **kwargs,
    )

    img = copy.deepcopy(img)  # don't modify the original image
    img = _pascal_transform(img, size=(128, 128))
    img = img.unsqueeze(0)
    img = img.to(device)

    _parts = {
        "aeroplane": ["body", "stern", "lwing", "rwing", "tail", "engine", "wheel"],
        "bicycle": [
            "fwheel",
            "bwheel",
            "saddle",
            "handlebar",
            "chainwheel",
            "headlight",
        ],
        "bird": [
            "head",
            "leye",
            "reye",
            "beak",
            "torso",
            "neck",
            "lwing",
            "rwing",
            "lleg",
            "lfoot",
            "rleg",
            "rfoot",
            "tail",
        ],
        "boat": [],
        "bottle": ["cap", "body"],
        "bus": [
            "frontside",
            "leftside",
            "rightside",
            "backside",
            "roofside",
            "leftmirror",
            "rightmirror",
            "fliplate",
            "bliplate",
            "door",
            "wheel",
            "headlight",
            "window",
        ],
        "car": [
            "frontside",
            "leftside",
            "rightside",
            "backside",
            "roofside",
            "leftmirror",
            "rightmirror",
            "fliplate",
            "bliplate",
            "door",
            "wheel",
            "headlight",
            "window",
        ],
        "cat": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "nose",
            "torso",
            "neck",
            "lfleg",
            "lfpa",
            "rfleg",
            "rfpa",
            "lbleg",
            "lbpa",
            "rbleg",
            "rbpa",
            "tail",
        ],
        "chair": [],
        "cow": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "muzzle",
            "lhorn",
            "rhorn",
            "torso",
            "neck",
            "lfuleg",
            "lflleg",
            "rfuleg",
            "rflleg",
            "lbuleg",
            "lblleg",
            "rbuleg",
            "rblleg",
            "tail",
        ],
        "table": [],
        "dog": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "nose",
            "torso",
            "neck",
            "lfleg",
            "lfpa",
            "rfleg",
            "rfpa",
            "lbleg",
            "lbpa",
            "rbleg",
            "rbpa",
            "tail",
            "muzzle",
        ],
        "horse": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "muzzle",
            "lfho",
            "rfho",
            "lbho",
            "rbho",
            "torso",
            "neck",
            "lfuleg",
            "lflleg",
            "rfuleg",
            "rflleg",
            "lbuleg",
            "lblleg",
            "rbuleg",
            "rblleg",
            "tail",
        ],
        "motorbike": ["fwheel", "bwheel", "handlebar", "saddle", "headlight"],
        "person": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "lebrow",
            "rebrow",
            "nose",
            "mouth",
            "hair",
            "torso",
            "neck",
            "llarm",
            "luarm",
            "lhand",
            "rlarm",
            "ruarm",
            "rhand",
            "llleg",
            "luleg",
            "lfoot",
            "rlleg",
            "ruleg",
            "rfoot",
        ],
        "pottedplant": ["pot", "plant"],
        "sheep": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "muzzle",
            "lhorn",
            "rhorn",
            "torso",
            "neck",
            "lfuleg",
            "lflleg",
            "rfuleg",
            "rflleg",
            "lbuleg",
            "lblleg",
            "rbuleg",
            "rblleg",
            "tail",
        ],
        "sofa": [],
        "train": [
            "head",
            "hfrontside",
            "hleftside",
            "hrightside",
            "hbackside",
            "hroofside",
            "headlight",
            "coach",
            "cfrontside",
            "cleftside",
            "crightside",
            "cbackside",
            "croofside",
        ],
        "tvmonitor": [
            "screen",
            "frame",
        ],  # NOTE: frame was missing in the paper! See https://github.com/pmeletis/panoptic_parts/blob/v2.0/panoptic_parts/specs/dataset_specs/ppp_datasetspec.yaml for correct version
    }

    _idx_to_name = {}

    _idx = 0
    for class_, _parts in _parts.items():
        for _part in _parts:
            _idx_to_name[_idx] = (class_, _part)
            _idx += 1

    with torch.no_grad():
        out = model(img)[0]

    out = nn.Sigmoid()(out)
    out = out.squeeze().cpu().numpy()
    class_labels = np.argwhere(out > 0.5).flatten().tolist()

    class_labels = (
        [_idx_to_name[idx] for idx in class_labels] if len(class_labels) else []
    )

    # organize parts by class
    class_labels_organized = {class_: [] for class_, _ in class_labels}
    for class_, part_ in class_labels:
        class_labels_organized[class_].append(part_)

    return class_labels_organized


@_timeit
def _process_explaination(label, heatmap, img, class_map: dict):
    label_name = class_map[label]

    np_img = np.array(img)

    heatmap = heatmap.unsqueeze(0) if len(heatmap.shape) == 2 else heatmap

    assert (
        len(heatmap.shape) == 3
    ), f"heatmap.shape = {heatmap.shape} != (1, H, W) or (C, H, W)"

    heatmap = transforms.Resize((np_img.shape[0], np_img.shape[1]), antialias=True)(
        heatmap
    )
    heatmap = heatmap.squeeze().numpy(force=True)

    return label_name, heatmap, np_img


@_timeit
def _process_parts(exctracted_parts, parts_model, device, **kwargs):
    """
    Outer loop for processing parts.

    Args:
        exctracted_parts (list): List of tuples (part_img, relevancy).
        device (str): Device to use.
        kwargs: Additional arguments.

    Returns:
        list: List of Part objects.
    """

    _parts_collecter = []

    for i, (part_img, relevancy, rect) in enumerate(exctracted_parts):
        part_img = Image.fromarray(part_img)

        part_labels = _run_parts_model(
            part_img,
            parts_model,
            device,
            **kwargs,
        )

        _parts_collecter.append(
            Part(
                img=part_img,
                relevancy=relevancy,
                labels=part_labels,
                rect=rect,
            )
        )

    return _parts_collecter


@_timeit
def run(
    img: Image.Image,
    device: str,
    debug: bool,
    object_model: str,
    object_model_kwargs: dict,
    parts_model: str,
    parts_model_kwargs: dict,
    seed: int,
    segmentation_kwargs: dict,
    **kwargs,
) -> Result:
    # clear the temporary files
    clear_temporary_files()

    # init devices and random state
    device = _init_cuda(device_id=device, torch_seed=seed)
    np.random.seed(seed)  # set seed for numpy

    # run object model and get explained input
    explained_input, class_map = _run_object_model(
        img,
        object_model,
        device,
        **object_model_kwargs,
    )

    _object_collecter = []

    for label, heatmap in explained_input:
        # do some preprocessing on the explained input
        _tmp = _process_explaination(label, heatmap, img, class_map)
        label_name: str = _tmp[0]  # for example: "person"
        heatmap: np.ndarray = _tmp[1]  # 2D-array with values in range [0, 1]
        np_img: np.ndarray = _tmp[2]  # RBG values in range [0, 255]

        extracted_parts = extract_parts(
            heatmap=heatmap,
            np_img=np_img,
            **segmentation_kwargs,
        )

        collected_parts: List[Part] = _process_parts(
            extracted_parts, parts_model, device, **parts_model_kwargs
        )

        _object_collecter.append(
            Object(
                label=label_name,
                heatmap=heatmap,
                parts=collected_parts,
            )
        )

    return Result(img=img, objects=_object_collecter)
