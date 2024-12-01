from typing import Tuple, Dict, Any
import torch
from PIL import Image, ImageDraw
import numpy as np
import math

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class GridMosaicNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "批次图像": ("IMAGE",),
                "行数": ("INT", {"default": 2, "min": 1, "max": 16}),
                "列数": ("INT", {"default": 2, "min": 1, "max": 16}),
                "接缝颜色": ("COLOR", {"default": "#ffffff"}),
                "接缝宽度": ("INT", {"default": 2, "min": 0, "max": 50}),
                "随机排序": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "随机种子": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("拼接结果",)
    FUNCTION = "create_grid_mosaic"
    CATEGORY = "2🐕/图像/拼接"

    def create_grid_mosaic(self, 批次图像, 行数, 列数, 接缝颜色, 接缝宽度, 随机排序, 随机种子=None):
        if len(批次图像.shape) == 3:  # 单张图片
            批次图像 = 批次图像.unsqueeze(0)
        batch_size = 批次图像.shape[0]
        
        # 添加随机排序逻辑
        if 随机排序:
            if 随机种子 is not None:
                generator = torch.Generator().manual_seed(随机种子)
                indices = torch.randperm(batch_size, generator=generator)
            else:
                indices = torch.randperm(batch_size)
            批次图像 = 批次图像[indices]
        
        first_image = tensor2pil(批次图像[0])
        width, height = first_image.size
        grid_rows = 行数
        grid_cols = 列数
        canvas_width = width * grid_cols + 接缝宽度 * (grid_cols + 1)
        canvas_height = height * grid_rows + 接缝宽度 * (grid_rows + 1)
        final_image = Image.new('RGB', (canvas_width, canvas_height), 接缝颜色)
        for idx in range(min(batch_size, grid_rows * grid_cols)):
            row = idx // grid_cols
            col = idx % grid_cols
            x = col * (width + 接缝宽度) + 接缝宽度
            y = row * (height + 接缝宽度) + 接缝宽度
            current_image = tensor2pil(批次图像[idx])
            if current_image.size != (width, height):
                current_image = current_image.resize((width, height), Image.LANCZOS)
            final_image.paste(current_image, (x, y))
        result_tensor = pil2tensor(final_image)
        return (result_tensor,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用 