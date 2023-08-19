import cv2
import numpy as np
import segmentation_models_pytorch as smp
import skimage.segmentation as seg
import torch

model = smp.Unet(
    encoder_name="resnet34",  # choose encoder, e.g. mobilenet_v2 or efficientnet-b7
    encoder_weights="imagenet",  # use `imagenet` pre-trained weights for encoder initialization
    in_channels=3,  # model input channels (1 for gray-scale images, 3 for RGB, etc.)
    classes=2,  # model output channels (number of classes in your dataset)
)


def segment(img: np.ndarray) -> np.ndarray:
    """Segmentation function

    Args:
        img (np.ndarray): input image

    Returns:
        np.ndarray: segmented image
    """


def _prepare_img(img) -> np.ndarray:
    """
    Convert image to 8-bit unsigned integer.

    Args:
        img: RGB-image to convert

    Returns:
        img: converted image
    """

    if img.max() <= 1:
        img *= 255
        img = np.array(img, dtype=np.uint8)
    else:
        img = np.array(img, dtype=np.uint8)

    return img


def main():
    img_path = r"C:\Users\Raphael\Desktop\PASCAL_Dataset\VOCdevkit\VOC2012\JPEGImages\2007_000256.jpg"
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))
    tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float()
    out = model(tensor)
    out = out.squeeze(0).permute(1, 2, 0).detach().numpy()
    out = np.argmax(out, axis=2) + 1
    mask = out.astype(np.uint8)
    print(out)
    fig = seg.mark_boundaries(img, mask)
    fig = _prepare_img(fig)
    fig = cv2.cvtColor(fig, cv2.COLOR_RGB2BGR)
    cv2.imshow("", fig)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
