from pytorch_grad_cam import EigenGradCAM, GradCAM, GradCAMPlusPlus, XGradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
import torch
import torch.nn as nn
from torchvision import models
from torchvision.models.resnet import ResNet50_Weights

from explainer.base import BaseExplainableModel, BaseModel, ExplainedInput


class Cam(BaseModel, BaseExplainableModel):
    def __init__(self, num_classes, **kwargs):
        super().__init__()
        self.pretrained = models.resnet50(weights=ResNet50_Weights.DEFAULT)

        self.pretrained.fc = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, num_classes),
        )

        self._frozen = False

        self.freeze()

    def forward(self, x):
        return self.pretrained(x)

    def freeze(self):
        # freeze all layers except the last one
        self._frozen = True
        for param in self.pretrained.parameters():
            param.requires_grad = False

        for param in self.pretrained.fc.parameters():
            param.requires_grad = True

    def unfreeze(self):
        if self._frozen:
            self._frozen = False
            for param in self.pretrained.parameters():
                param.requires_grad = True

    def _explain(self, x):
        frozen = self._frozen
        self.unfreeze()

        if x.ndim == 3:
            # add batch dimension
            x = x.unsqueeze(0)

        class_indices = self._classify(x)
        heatmaps = self._explain_cam(x, class_indices)

        if frozen:
            self.freeze()

        return [
            ExplainedInput(
                input_tensor=x[i],
                predicted_labels=class_indices[i],
                explanations=heatmaps[i],
                use_logits=True,
            )
            for i in range(x.shape[0])
        ]

    def _classify(self, x):
        """
        Perform multi-label binary classification on x

        Returns:
            List of class-indices that are predicted to be present in x
        """
        with torch.no_grad():
            logits = self.forward(x)
            probs = torch.nn.functional.sigmoid(logits)
            probs = (probs > 0.5).type(torch.int64)

        class_indices = []

        for p in probs:
            tmp = p.nonzero().flatten().tolist()
            class_indices.append(tmp)

        return class_indices

    def _explain_cam(self, x, targets):
        target_layers = [self.pretrained.layer4[-1]]

        maps = []
        for i in range(x.shape[0]):
            tmp = []
            x_i = x[i].unsqueeze(0)
            for target in targets[i]:
                heatmap = cam(
                    model=self,
                    input_tensor=x_i,
                    category_index=target,
                    target_layers=target_layers,
                    aug_smooth=True,
                    eigen_smooth=True,
                )
                tmp.append(torch.from_numpy(heatmap))
            maps.append(tmp)
        return maps


def cam(
    model,
    input_tensor,
    category_index,
    target_layers,
    method="gradcam",
    aug_smooth=False,
    eigen_smooth=False,
):
    methods = {
        "gradcam": GradCAM,
        "gradcam++": GradCAMPlusPlus,
        "xgradcam": XGradCAM,
        "eigengradcam": EigenGradCAM,
    }

    device = next(model.parameters()).device.type
    use_cuda = device == "cuda"
    cam = methods[method](
        model=model,
        target_layers=target_layers,
        use_cuda=use_cuda,
    )

    targets = [ClassifierOutputTarget(category_index)]
    heatmap = cam(
        input_tensor=input_tensor,
        targets=targets,
        eigen_smooth=aug_smooth,
        aug_smooth=eigen_smooth,
    )
    return heatmap
