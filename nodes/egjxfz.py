from typing import Tuple, Dict, Any
import torch
from PIL import Image
import numpy as np
from torchvision import transforms


def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


class EGJXFZNODE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入图像": ("IMAGE",),
                "方向": (["水平", "垂直"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图像",)
    FUNCTION = "image_flip"
    CATEGORY = "2🐕/图像"

    def image_flip(self, 输入图像, 方向):
        batch_tensor = []
        for image in 输入图像:
            image = tensor2pil(image)
            if 方向 == '水平':
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif 方向 == '垂直':
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            batch_tensor.append(pil2tensor(image))
        batch_tensor = torch.cat(batch_tensor, dim=0)
        return (batch_tensor, )






# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
