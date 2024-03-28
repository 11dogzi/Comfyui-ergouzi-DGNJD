import torch
from PIL import Image
import numpy as np
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
def image2mask(image_pil, channel='red'):
    image_array = np.array(image_pil)
    image_tensor = torch.from_numpy(image_array).float() / 255.0
    if channel == 'red':
        mask_tensor = image_tensor[:, :, 0]
    elif channel == 'green':
        mask_tensor = image_tensor[:, :, 1]
    elif channel == 'blue':
        mask_tensor = image_tensor[:, :, 2]
    elif channel == 'alpha':
        if image_tensor.shape[2] == 4:
            mask_tensor = 1 - image_tensor[:, :, 3]
        else:
            mask_tensor = torch.zeros(image_tensor.shape[:2])
    else:
        raise ValueError("Invalid channel specified.")
    mask_array = mask_tensor.numpy() * 255
    mask_array = mask_array.astype(np.uint8)
    mask_pil = Image.fromarray(mask_array)
    return mask_pil
def mask2image(mask_pil):
    mask_array = np.array(mask_pil)
    mask_tensor = torch.from_numpy(mask_array).float() / 255.0
    mask_tensor = mask_tensor.unsqueeze(0).unsqueeze(0)
    result_tensor = mask_tensor.expand(-1, 3, -1, -1)
    result_array = result_tensor.squeeze().numpy() * 255
    result_array = result_array.transpose(1, 2, 0).astype(np.uint8)
    result_pil = Image.fromarray(result_array)
    return result_pil
class EGTXZZZHNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "输入遮罩": ("MASK", {}),
                "输入图像": ("IMAGE", {}),
                "选择通道": (["red", "green", "blue", "alpha"], {"default": "red"}),
            },
        }
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("转换图像", "转换遮罩")
    FUNCTION = "convert_input"
    CATEGORY = "2🐕/遮罩"
    def convert_input(self, 输入图像=None, 输入遮罩=None, 选择通道='red'):
        if 输入图像 is None and 输入遮罩 is None:
            default_image = Image.new('L', (256, 256), color=255)
            default_mask = Image.new('L', (256, 256), color=0)
            image_tensor = pil2tensor(default_image)
            mask_tensor = pil2tensor(default_mask)
            return [image_tensor, mask_tensor]
        
        elif 输入图像 is not None:
            input_image_pil = tensor2pil(输入图像)
            转换遮罩_pil = image2mask(input_image_pil, 选择通道)
            转换图像_pil = input_image_pil
        elif 输入遮罩 is not None:
            input_mask_pil = tensor2pil(输入遮罩)
            转换图像_pil = mask2image(input_mask_pil)
            转换遮罩_pil = input_mask_pil
        
        转换图像_tensor = pil2tensor(转换图像_pil)
        转换遮罩_tensor = pil2tensor(转换遮罩_pil)
        
        return [转换图像_tensor, 转换遮罩_tensor]

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
