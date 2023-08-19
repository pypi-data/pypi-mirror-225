from fnmatch import fnmatch
from typing import Dict, Iterable, List, Optional, Tuple, Union

import cv2
from matplotlib import pyplot as plt
from matplotlib.colors import hsv_to_rgb
import numpy as np
from scipy import interpolate
from scipy.ndimage import center_of_mass
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

from explainer.base.base_explainable_model import BaseExplainableModel, ExplainedInput

from .modules import PeakResponseMapping

# from nest import register


def finetune(
    model: nn.Module,
    base_lr: float,
    groups: Dict[str, float],
    ignore_the_rest: bool = False,
    raw_query: bool = False,
) -> List[Dict[str, Union[float, Iterable]]]:
    """Fintune."""

    print("finetune------->> ", base_lr, groups, ignore_the_rest, raw_query)

    parameters = [
        dict(
            params=[],
            names=[],
            query=query if raw_query else "*" + query + "*",
            lr=lr * base_lr,
        )
        for query, lr in groups.items()
    ]
    rest_parameters = dict(params=[], names=[], lr=base_lr)
    for k, v in model.named_parameters():
        for group in parameters:
            if fnmatch(k, group["query"]):
                group["params"].append(v)
                group["names"].append(k)
            else:
                rest_parameters["params"].append(v)
                rest_parameters["names"].append(k)
    if not ignore_the_rest:
        parameters.append(rest_parameters)
    for group in parameters:
        group["params"] = iter(group["params"])
    return parameters


class FC_ResNet(nn.Module):
    def __init__(self, pretrained, num_classes, **kwargs):
        super(FC_ResNet, self).__init__()
        model = models.resnet50(pretrained)

        # feature encoding
        self.features = nn.Sequential(
            model.conv1,
            model.bn1,
            model.relu,
            model.maxpool,
            model.layer1,
            model.layer2,
            model.layer3,
            model.layer4,
        )

        # classifier
        num_features = model.layer4[1].conv1.in_channels
        self.classifier = nn.Sequential(
            nn.Conv2d(num_features, num_classes, kernel_size=1, bias=True)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class PRM(PeakResponseMapping, BaseExplainableModel):
    def __init__(self, num_classes, pretrained):
        BaseExplainableModel.__init__(self)
        PeakResponseMapping.__init__(
            self,
            enable_peak_stimulation=True,
            enable_peak_backprop=True,
            win_size=3,
            sub_pixel_locating_factor=8,
            filter_type="median",
        )

        self.backbone = FC_ResNet(pretrained, num_classes)
        self.add_module("backbone", self.backbone)

    def forward(self, input, class_threshold=0.2, peak_threshold=1, retrieval_cfg=None):
        x = super(PRM, self).forward(
            input,
            class_threshold=class_threshold,
            peak_threshold=peak_threshold,
            retrieval_cfg=retrieval_cfg,
        )
        return x

    def _classify(self, x) -> Tuple[List[List[int]], torch.Tensor]:
        """
        Perform multi-label binary classification on x

        Returns:
            List of class-indices that are predicted to be present in x
        """
        self.eval()
        if x is None:
            return
        output = self(x)
        if output is None:
            return
        pred = torch.sigmoid(output)
        pred = (pred > 0.5).type(torch.int64)

        class_indices = []

        for p in pred:
            tmp = p.nonzero().flatten().tolist()
            class_indices.append(tmp[:1])

        return class_indices, output

    def _explain(self, x):
        """
        Classify x and return heatmaps for each class/category
        """

        prm_list = []
        pred_list = []
        self.eval()

        class_names = [
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

        for i in range(x.shape[0]):
            input = x[i]

            if input.ndim == 3:
                input = input.unsqueeze(0)
            # prediction
            pred_list, pred = self._classify(input)
            pred_list = pred_list[:1]
            # pred = self(input)
            # print("input: ", input)
            print("predictions: ", pred)
            res = []

            for idx in range(len(class_names)):
                if pred.data[0, idx] > 0:
                    print(
                        "[class_idx: %d] %s (%.2f)"
                        % (idx, class_names[idx], pred[0, idx])
                    )
                    res.append(idx)

            # pred_list.append(pred)

            with torch.enable_grad():  # Enable gradient computation
                input.requires_grad = True
                self.inference()
                visual_cues = self(input)
            if visual_cues is None:
                print("No visual cues found!!!")
                pred_list.append([])
                prm_list.append([])
                continue

            (
                confidence,
                class_response_maps,
                class_peak_responses,
                peak_response_maps,
            ) = visual_cues
            print(
                "confidence: ",
                confidence.shape,
                "class_response_maps: ",
                class_response_maps.shape,
                "class_peak_responses: ",
                class_peak_responses,  # [idx, class_idx, x_peak, y_peak]
                "peak_response_maps: ",
                peak_response_maps.shape,
                sep="\n",
            )
            # get index of class with highest confidence
            _, class_idx = torch.max(confidence, dim=1)
            print(
                "Got",
                len(class_idx),
                "predicted classes and",
                len(peak_response_maps),
                "peak response maps",
            )
            # get (1,) tensor value
            class_item = class_idx.item()
            # plot
            num_plots = 2 + len(peak_response_maps)
            f, axarr = plt.subplots(1, num_plots, figsize=(num_plots * 4, 4))
            axarr[0].imshow(input.detach()[0].permute(1, 2, 0).cpu())
            axarr[0].set_title(f"Image ('{class_names[class_item]}')")
            axarr[0].axis("off")
            axarr[1].imshow(
                class_response_maps[0, class_item].cpu(), interpolation="none"
            )
            axarr[1].set_title('CRM("%s")' % class_names[class_item])
            axarr[1].axis("off")
            merged_peak_response_map = torch.zeros(224, 224).cpu()
            for idx, (prm, peak) in enumerate(
                sorted(
                    zip(peak_response_maps, class_peak_responses),
                    key=lambda v: v[-1][-1],
                )
            ):
                axarr[idx + 2].imshow(prm.cpu(), cmap=plt.cm.jet)
                axarr[idx + 2].set_title(
                    'Peak Response Map ("%s")' % (class_names[peak[1].item()])
                )
                axarr[idx + 2].axis("off")
                if peak[1].item() == class_idx:
                    merged_peak_response_map += prm.cpu()
            plt.show()

            # normalize and append merged prms
            merged_peak_response_map /= merged_peak_response_map.max()
            prm_list.append([merged_peak_response_map])

        # return an ExplainableInput for each input batch
        print("pred_list: ", pred_list, "prm_list: ", prm_list)
        explanations = [
            ExplainedInput(
                input_tensor=x[i],
                predicted_labels=pred_list[i],
                explanations=prm_list[i],
                use_logits=True,
            )
            for i in range(x.shape[0])
        ]
        return explanations
