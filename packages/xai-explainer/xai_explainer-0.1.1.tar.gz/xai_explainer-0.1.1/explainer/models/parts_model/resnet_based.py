import torch.nn as nn
from torchvision import models
from torchvision.models.resnet import ResNet50_Weights

from explainer.base import BaseModel


class ResNetParts(BaseModel):
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
