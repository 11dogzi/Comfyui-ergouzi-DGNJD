from typing import Tuple, Dict, Any
import torch
from PIL import Image, ImageDraw
import numpy as np
import math
import random

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def center_crop_resize(image, target_width, target_height):
    if isinstance(image, torch.Tensor):
        image = tensor2pil(image)
    target_ratio = target_width / target_height
    current_ratio = image.width / image.height
    
    if current_ratio > target_ratio:
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        image = image.crop((left, 0, left + new_width, image.height))
    elif current_ratio < target_ratio:
        new_height = int(image.width / target_ratio)
        top = (image.height - new_height) // 2
        image = image.crop((0, top, image.width, top + new_height))
    return image.resize((target_width, target_height), Image.LANCZOS)

class NineGridMosaicNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "图像1": ("IMAGE",),
                "行数": ("INT", {"default": 3, "min": 1, "max": 16}),
                "列数": ("INT", {"default": 3, "min": 1, "max": 16}),
                "接缝颜色": ("COLOR", {"default": "#ffffff"}),
                "接缝宽度": ("INT", {"default": 2, "min": 0, "max": 50}),
                "随机排序": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "随机种子": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "图像2": ("IMAGE",),
                "图像3": ("IMAGE",),
                "图像4": ("IMAGE",),
                "图像5": ("IMAGE",),
                "图像6": ("IMAGE",),
                "图像7": ("IMAGE",),
                "图像8": ("IMAGE",),
                "图像9": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("九宫格结果",)
    FUNCTION = "create_nine_grid"
    CATEGORY = "2🐕/图像/拼接"

    def create_nine_grid(self, 图像1, 行数, 列数, 接缝颜色, 接缝宽度, 随机排序, 随机种子=None, 图像2=None, 图像3=None, 图像4=None, 
                        图像5=None, 图像6=None, 图像7=None, 图像8=None, 图像9=None):
        images = [img for img in [图像1, 图像2, 图像3, 图像4, 图像5, 图像6, 图像7, 图像8, 图像9] if img is not None]
        
        if 随机排序:
            if 随机种子 is not None:
                random.seed(随机种子)
            random.shuffle(images)
        
        image_count = len(images)
        first_image = tensor2pil(图像1)
        width, height = first_image.size
        canvas_width = width * 列数 + 接缝宽度 * (列数 + 1)
        canvas_height = height * 行数 + 接缝宽度 * (行数 + 1)
        final_image = Image.new('RGB', (canvas_width, canvas_height), 接缝颜色)
        for idx in range(min(image_count, 行数 * 列数)):
            row = idx // 列数
            col = idx % 列数
            x = col * (width + 接缝宽度) + 接缝宽度
            y = row * (height + 接缝宽度) + 接缝宽度
            current_image = tensor2pil(images[idx])
            current_image = center_crop_resize(current_image, width, height)
            final_image.paste(current_image, (x, y))
        result_tensor = pil2tensor(final_image)
        
        return (result_tensor,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用 