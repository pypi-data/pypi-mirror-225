import logging
from functools import lru_cache
from pathlib import Path
from typing import Callable

import torch
import torch.nn as nn

from explainer.base import BaseExplainableModel
from explainer.util.filehandling import download_url, get_working_dir

from .object_model.cam import Cam
from .object_model.prm.resnet import PRM
from .object_model.ViT import ViT
from .parts_model.resnet_based import ResNetParts

MODELS = {}


def _register_model(model: Callable, weight_url: str = None, **default_kwargs):
    """Register a model.

    Args:
        model (nn.Module): Model to register.
        weight_url (str, optional): URL to download the model weights from.
            Defaults to None.
        kwargs: Additional arguments that must be passed to the constructor.
    """
    if model.__name__ in MODELS:
        raise ValueError(f"Model {model.__name__} already registered.")

    MODELS[model.__name__] = {
        "model": model,
        "weight_url": weight_url,
        "defaults": default_kwargs,
    }


_register_model(
    Cam,
    weight_url="https://tu-dortmund.sciebo.de/s/2UeO47mYjEx5YKt/download",
    num_classes=20,
)

_register_model(PRM, weight_url=None, num_classes=20)

_register_model(
    ViT,
    weight_url="https://tu-dortmund.sciebo.de/s/jFdXY3k0uVIb1XS/download",
    num_classes=20,
    pretrained_vit="base",
    method="gradient_rollout",
)

_register_model(
    ResNetParts,
    weight_url="https://tu-dortmund.sciebo.de/s/7fAxd4RMPcg1drr/download",
    num_classes=194,
)


def list_models():
    """List all registered models.

    Returns:
        list: List of registered models.
    """
    return list(MODELS.keys())


def _init_model(
    model_handle: Callable,
    device: torch.device,
    weight_url: str = None,
    force_download=False,
    **kwargs,
) -> BaseExplainableModel:
    model = model_handle(**kwargs)
    model_name = model_handle.__name__

    expected_file_path: Path = get_working_dir() / "models" / f"{model_name}.pth"

    download_required = not expected_file_path.exists() or force_download
    if download_required:
        if expected_file_path.exists():
            expected_file_path.unlink()
        try:
            download_url(weight_url, expected_file_path)
        except Exception as e:
            logging.error(f"Could not download weights for {model_name}.")
            logging.error(e)

    if expected_file_path.exists():
        state_dict = torch.load(expected_file_path, map_location=device)
        model.load_state_dict(state_dict)
    else:
        logging.warning(f"No weights available for {model_name}.")

    try:
        model.unfreeze()  # unfreeze all layers
    except AttributeError:
        pass

    model.to(device)
    model.eval()

    return model


@lru_cache(maxsize=1)
def get_model(model_name: str, device: torch.device, **kwargs):
    """Get a registered model.

    Args:
        model_name (str): Name of the model.
        device (torch.device): Device to use.
        kwargs: Additional arguments to pass to the model constructor. These
            overwrite the default arguments.

    Raises:
        ValueError: If model is not registered.

    Returns:
        nn.Module: Model.
    """

    model_dict = MODELS.get(model_name)
    if model_dict is None:
        raise ValueError(f"Model {model_name} not registered.")

    model_handle = model_dict["model"]
    weight_url = model_dict["weight_url"]
    defaults_kwargs = model_dict["defaults"]

    defaults_kwargs.update(kwargs)  # overwrite default kwargs with passed kwargs

    return _init_model(model_handle, device, weight_url, **defaults_kwargs)
