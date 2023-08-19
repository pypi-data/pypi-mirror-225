import logging
from pathlib import Path
from typing import Union

from PIL import Image

import explainer._default_pipeline as _default_pipeline  # explicit import
import explainer.util.logger as logger
from explainer.util.return_types import Result


def _init_args(**kwargs):
    # Set defaults
    kwargs.setdefault("debug", False)
    kwargs.setdefault("device", "cpu")
    kwargs.setdefault("logging_level", logging.WARNING)
    kwargs.setdefault("object_model", "ViT")
    kwargs.setdefault("object_model_kwargs", {})
    kwargs.setdefault("parts_model", "ResNetParts")
    kwargs.setdefault("parts_model_kwargs", {})
    kwargs.setdefault("seed", 0)
    kwargs.setdefault("segmentation_kwargs", {})

    return kwargs


def _init_working_dir(working_dir) -> Path:
    from explainer.util.filehandling import setup_working_dir

    return setup_working_dir(working_dir)


# Right now only one pipeline is available, but this could be extended to
# include more pipelines in the future.
def run_pipeline(
    img: Image.Image,
    working_dir: Union[str, Path],
    **kwargs,
) -> Result:
    """
    Start the explainer process.

    Args:
        img (Image.Image): The image to explain.
        working_dir (Union[str, Path]): The working directory where local files are stored.
    Keyword Args:
        - debug (bool): Whether to run in debug mode. Default: False
        - device (str): The device to use. Default: "cpu"
        - logging_level (Union[str, int]): The logging level. Default: logging.WARNING
        - object_model (str): The object model to use. Default: "ViT"
        - object_model_kwargs (dict): Additional arguments for the object model. Default: {}
        - parts_model (str): The parts model to use. Default: "ResNetParts"
        - parts_model_kwargs (dict): Additional arguments for the parts model. Default: {}
        - seed (int): The seed to use. Default: 0
        - segmentation_kwargs (dict): Additional arguments for the segmentation method. Default: {}

    Returns:
        Result: The explanation, which can be converted to a dict using its "to_dict" method. See explainer.util.return_types.Result for more information.

    """

    # check input
    assert isinstance(
        img, Image.Image
    ), f"img must be of type PIL.Image.Image, but is {type(img)}"

    _init_working_dir(working_dir)

    kwargs = _init_args(**kwargs)
    logger.set_logging_level(kwargs.pop("logging_level"))

    # start explainer
    result = _default_pipeline.run(img=img, **kwargs)

    return result
