import torch
import numpy as np
from PIL import Image, ImageOps

def tensor_to_pil(img_tensor, batch_index=0):
    img_tensor = img_tensor[batch_index].unsqueeze(0)
    i = 255. * img_tensor.cpu().numpy()
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
    return img

def batch_tensor_to_pil(img_tensor):
    return [tensor_to_pil(img_tensor, i) for i in range(img_tensor.shape[0])]

def pil_to_tensor(image):
    image = np.array(image).astype(np.float32) / 255.0
    image_channels = image.shape[0]
    if image_channels == 1:  # If the image is grayscale, convert to RGB
        image = image.repeat(3, axis=0)
    image = torch.from_numpy(image).unsqueeze(0)
    return image

def batched_pil_to_tensor(images):
    return torch.cat([pil_to_tensor(image) for image in images], dim=0)


class EGTMTX:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            },
            "optional": {
                "遮罩反转": (["no", "yes"],),
            },
        }

    RETURN_TYPES = ('IMAGE',)
    RETURN_NAMES = ("透明图像",)

    FUNCTION = "apply_mask"

    CATEGORY = "2🐕/图像"

    def apply_mask(self, image, mask, 遮罩反转="no"):
        image_pil = batch_tensor_to_pil(image)[0]

        mask_pil = batch_tensor_to_pil(mask)[0]
        
        image_size = image_pil.size
        mask_size = mask_pil.size

        if image_size != mask_size:
            mask_pil = mask_pil.resize(image_size, Image.LANCZOS)

        if 遮罩反转 == "yes":
            mask_pil = ImageOps.invert(mask_pil)

        transparent = Image.new('RGBA', image_pil.size)
        transparent.paste(image_pil, (0, 0), mask_pil)

        transparent_tensor = pil_to_tensor(transparent)

        transparent_tensor = transparent_tensor.unsqueeze(0)

        return transparent_tensor


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
