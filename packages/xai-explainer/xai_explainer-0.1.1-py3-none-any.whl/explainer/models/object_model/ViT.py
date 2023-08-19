import logging
from typing import List, Optional

from pytorch_grad_cam import EigenGradCAM, GradCAM, GradCAMPlusPlus, XGradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from timm.models.vision_transformer import Block, PatchEmbed, VisionTransformer
import torch
from torchvision import transforms

from explainer.base import BaseExplainableModel, BaseModel, ExplainedInput


class ViT(BaseModel, BaseExplainableModel):
    def __init__(
        self,
        num_classes=1000,
        method="gradient_rollout",
        pretrained_vit: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Args:
            num_classes: Number of classes to classify
            method: Method to use for explaining the model
            pretrained: Name of the pretrained model to use. If None, a new model is created. Must be one of ["tiny", "small", "base"]

        """
        super().__init__()

        _img_size = 224

        self._frozen = False

        if pretrained_vit:
            try:
                if pretrained_vit not in ["tiny", "small", "base"]:
                    raise ValueError(
                        "pretrained_vit must be one of [tiny, small, base]"
                    )
                model_name = f"deit_{pretrained_vit}_patch16_{_img_size}"
                self.vit = torch.hub.load(
                    "facebookresearch/deit:main", model_name, pretrained=True
                )
            except:
                fallback_model = "deit_tiny_patch16_224"
                logging.warning(
                    "Could not load pretrained model. Falling back to {}".format(
                        fallback_model
                    )
                )
                self.vit = torch.hub.load(
                    "facebookresearch/deit:main", fallback_model, pretrained=True
                )

            self.vit.head = torch.nn.Linear(
                self.vit.head.in_features, num_classes
            )  # Replace the last layer

            # Freeze all layers except the last one
            self.freeze()

        else:
            self.vit = VisionTransformer(
                img_size=224,
                patch_size=16,
                in_chans=3,
                num_classes=num_classes,
                global_pool="token",
                embed_dim=192,
                depth=12,
                num_heads=12,
                mlp_ratio=4.0,
                qkv_bias=True,
                init_values=None,
                class_token=True,
                no_embed_class=False,
                pre_norm=False,
                fc_norm=None,
                drop_rate=0.0,
                attn_drop_rate=0.0,
                drop_path_rate=0.0,
                weight_init="",
                embed_layer=PatchEmbed,
                norm_layer=None,
                act_layer=None,
                block_fn=Block,
            )

        self.transform = transforms.Compose(
            [
                transforms.Resize((_img_size, _img_size), antialias=True),
                transforms.Lambda(
                    lambda x: transforms.ToTensor()(x)
                    if not isinstance(x, torch.Tensor)
                    else x
                ),
            ]
        )

        self._method = method

        # Disable fused attention for gradient rollout
        # https://github.com/jacobgil/vit-explain/issues/23
        if self._method in ["gradient_rollout", "attention_rollout"]:
            for block in self.vit.blocks:
                block.attn.fused_attn = False

    def forward(self, x):
        x = self.transform(x)
        logits = self.vit(x)
        return logits

    def freeze(self):
        self._frozen = True
        for param in self.vit.parameters():
            param.requires_grad = False
        for param in self.vit.head.parameters():
            param.requires_grad = True

    def unfreeze(self):
        if self._frozen:
            self._frozen = False
            for param in self.vit.parameters():
                param.requires_grad = True

    def _explain(self, x):
        """
        Classify x and return heatmaps for each class/category
        """
        frozen = self._frozen
        self.unfreeze()
        self.train(True)

        if x.ndim == 3:
            # add batch dimension
            x = x.unsqueeze(0)

        class_indices = self._classify(x)

        # heatmaps = self._explain_cam(x, targets)
        if self._method == "cam":
            heatmaps = self._explain_cam(x, class_indices)
        elif self._method == "gradient_rollout":
            heatmaps = self._explain_grad_rollout(x, class_indices)
        elif self._method == "attention_rollout":
            heatmaps = self._explain_attention_rollout(x, class_indices)
        else:
            raise ValueError("Unknown method: {}".format(self._method))

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

    def _classify(self, x) -> List[List[int]]:
        """
        Perform multi-label binary classification on x

        Returns:
            List of class-indices that are predicted to be present in x
        """
        with torch.no_grad():
            logits = self.forward(x)
            probs = torch.sigmoid(logits)
            probs = (probs > 0.5).type(torch.int64)

        class_indices = []

        for p in probs:
            tmp = p.nonzero().flatten().tolist()
            class_indices.append(tmp)

        return class_indices

    def _explain_cam(self, x, targets):
        target_layers = [self.vit.blocks[-1].norm1]

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

    def _explain_grad_rollout(self, x, targets):
        """
        Explain the model using gradient rollout

        Args:
            x: Input tensor
            targets: List of target indices

        """
        maps = []

        if not hasattr(self, "_grad_rollout"):
            self._grad_rollout = VITAttentionGradRollout(model=self, discard_ratio=0.9)

        for i in range(x.shape[0]):
            tmp = []
            x_i = x[i].unsqueeze(0)

            assert x_i.ndim == 4, f"{x_i.ndim = } != 4"

            for target in targets[i]:
                heatmap = self._grad_rollout(input_tensor=x_i, category_index=target)
                tmp.append(heatmap)
            maps.append(tmp)

        return maps

    def _explain_attention_rollout(self, x, targets):
        """
        Explain the model using gradient rollout

        Args:
            x: Input tensor

        """
        maps = []

        if not hasattr(self, "_attn_rollout"):
            self._attn_rollout = VITAttentionRollout(model=self, discard_ratio=0.9)

        for i in range(x.shape[0]):
            tmp = []
            x_i = x[i].unsqueeze(0)

            assert x_i.ndim == 4, f"{x_i.ndim = } != 4"

            heatmap = self._attn_rollout(input_tensor=x_i)

            if len(targets[i]) > 1:
                logging.warning(
                    "Attention rollout returns the same heatmap for all targets"
                )

            for target in targets[i]:
                tmp.append(heatmap)
            maps.append(tmp)

        return maps


class VITAttentionGradRollout:
    def __init__(self, model, attention_layer_name="attn_drop", discard_ratio=0.9):
        self.model = model
        self.discard_ratio = discard_ratio

        for name, module in self.model.named_modules():
            if attention_layer_name in name:
                module.register_forward_hook(self.get_attention)
                module.register_full_backward_hook(self.get_attention_gradient)

        self.attentions = []
        self.attention_gradients = []

    def _reset(self):
        self.attentions = []
        self.attention_gradients = []

    def get_attention(self, module, input, output):
        self.attentions.append(output.cpu())

    def get_attention_gradient(self, module, grad_input, grad_output):
        self.attention_gradients.append(grad_input[0].cpu())

    def __call__(self, input_tensor, category_index):
        self._reset()
        self.model.zero_grad()
        output = self.model(input_tensor)
        device = next(self.model.parameters()).device.type
        category_mask = torch.zeros(output.size(), device=device)
        category_mask[:, category_index] = 1
        loss = (output * category_mask).sum()
        loss.backward()

        return self.grad_rollout(
            self.attentions, self.attention_gradients, self.discard_ratio
        )

    @staticmethod
    def grad_rollout(attentions, gradients, discard_ratio):
        result = torch.eye(attentions[0].size(-1))
        with torch.no_grad():
            for attention, grad in zip(attentions, gradients):
                weights = grad
                attention_heads_fused = (attention * weights).mean(axis=1)
                attention_heads_fused[attention_heads_fused < 0] = 0

                # Drop the lowest attentions, but
                # don't drop the class token
                flat = attention_heads_fused.view(attention_heads_fused.size(0), -1)
                _, indices = flat.topk(int(flat.size(-1) * discard_ratio), -1, False)
                # indices = indices[indices != 0]
                flat[0, indices] = 0

                I = torch.eye(attention_heads_fused.size(-1))
                a = (attention_heads_fused + 1.0 * I) / 2
                a = a / a.sum(dim=-1)
                result = torch.matmul(a, result)

        # Look at the total attention between the class token,
        # and the image patches
        mask = result[0, 0, 1:]
        # In case of 224x224 image, this brings us from 196 to 14
        width = int(mask.size(-1) ** 0.5)
        mask = mask.reshape(width, width)
        mask = mask / mask.max()
        return mask


def reshape_transform(tensor, height=14, width=14):
    result = tensor[:, 1:, :].reshape(tensor.size(0), height, width, tensor.size(2))

    # Bring the channels to the first dimension,
    # like in CNNs.
    result = result.transpose(2, 3).transpose(1, 2)
    return result


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
        reshape_transform=reshape_transform,
    )

    targets = [ClassifierOutputTarget(category_index)]

    heatmap = cam(
        input_tensor=input_tensor,
        targets=targets,
        eigen_smooth=eigen_smooth,
        aug_smooth=aug_smooth,
    )

    return heatmap


class VITAttentionRollout:
    def __init__(
        self,
        model,
        attention_layer_name="attn_drop",
        head_fusion="mean",
        discard_ratio=0.9,
    ):
        self.model = model
        self.head_fusion = head_fusion
        self.discard_ratio = discard_ratio
        for name, module in self.model.named_modules():
            if attention_layer_name in name:
                module.register_forward_hook(self.get_attention)

        self.attentions = []

    def get_attention(self, module, input, output):
        self.attentions.append(output.cpu())

    def __call__(self, input_tensor):
        self.attentions = []
        with torch.no_grad():
            output = self.model(input_tensor)

        return self.rollout(self.attentions, self.discard_ratio, self.head_fusion)

    @staticmethod
    def rollout(attentions, discard_ratio, head_fusion):
        result = torch.eye(attentions[0].size(-1))
        with torch.no_grad():
            for attention in attentions:
                if head_fusion == "mean":
                    attention_heads_fused = attention.mean(axis=1)
                elif head_fusion == "max":
                    attention_heads_fused = attention.max(axis=1)[0]
                elif head_fusion == "min":
                    attention_heads_fused = attention.min(axis=1)[0]
                else:
                    raise "Attention head fusion type Not supported"

                # Drop the lowest attentions, but
                # don't drop the class token
                flat = attention_heads_fused.view(attention_heads_fused.size(0), -1)
                _, indices = flat.topk(int(flat.size(-1) * discard_ratio), -1, False)
                indices = indices[indices != 0]
                flat[0, indices] = 0

                I = torch.eye(attention_heads_fused.size(-1))
                a = (attention_heads_fused + 1.0 * I) / 2
                a = a / a.sum(dim=-1)

                result = torch.matmul(a, result)

        # Look at the total attention between the class token,
        # and the image patches
        mask = result[0, 0, 1:]
        # In case of 224x224 image, this brings us from 196 to 14
        width = int(mask.size(-1) ** 0.5)
        mask = mask.reshape(width, width)
        mask = mask / mask.max()
        return mask
