from typing import Tuple, Dict, Any
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from scipy.ndimage import binary_dilation, binary_erosion

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class EGZZSSKZNODE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入遮罩": ("MASK",),
                "扩展收缩大小": ("INT", {"default": 0, "min": -1000, "max": 1000, "step": 1}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("遮罩",)
    FUNCTION = "mask_expand_shrink"
    CATEGORY = "2🐕/遮罩"

    def mask_expand_shrink(self, 输入遮罩, 扩展收缩大小):
        输入遮罩 = tensor2pil(输入遮罩)
        expand_shrink_value = 扩展收缩大小
        
        mask_array = np.array(输入遮罩) > 0  
        
        if expand_shrink_value > 0:
            expanded_mask_array = binary_dilation(mask_array, iterations=expand_shrink_value)
        elif expand_shrink_value < 0:
            expanded_mask_array = binary_erosion(mask_array, iterations=-expand_shrink_value)
        else:
            expanded_mask_array = mask_array
        
        expanded_mask = Image.fromarray((expanded_mask_array * 255).astype(np.uint8))
        
        expanded_mask_tensor = pil2tensor(expanded_mask)
        
        return (expanded_mask_tensor, )






# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
