from typing import Tuple, Dict, Any
import torch
import numpy as np
from PIL import Image, ImageOps
import cv2


def tensor_to_pil(img_tensor, batch_index=0):
    
    img_tensor = img_tensor[batch_index].unsqueeze(0)
    i = 255. * img_tensor.cpu().numpy()
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
    return img


def pil_to_tensor(image):
    
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image).unsqueeze(0)
    if len(image.shape) == 3:  
        image = image.unsqueeze(-1)
    return image

class EGSCQYBHDQYYNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "迁移图": ("IMAGE",),  
                "目标图": ("IMAGE",),  
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("result_image",)
    FUNCTION = "transfer_saturation"
    CATEGORY = "2🐕/图像/色彩处理"
class EGSCQYBHDQYYNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "迁移图": ("IMAGE",),
                "目标图": ("IMAGE",),
            },
            "optional": {
                "迁移强度": ("FLOAT", {
                    "default": 50,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "precision": 100,
                    "display": "slider"
                }),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("result_image",)
    FUNCTION = "transfer_saturation"
    CATEGORY = "2🐕/图像/色彩处理"
    def transfer_saturation(self, 迁移图, 目标图, 迁移强度=50):
        source_pil = tensor_to_pil(迁移图)
        target_pil = tensor_to_pil(目标图)
        source_size = source_pil.size
        target_size = target_pil.size
        
        if source_size != target_size:
            source_pil = ImageOps.fit(source_pil, target_size, Image.LANCZOS)
            source_np = np.array(source_pil)
        else:
            source_np = np.array(source_pil)
        
        target_np = np.array(target_pil)
        
        source_hsv = cv2.cvtColor(source_np, cv2.COLOR_RGB2HSV)
        target_hsv = cv2.cvtColor(target_np, cv2.COLOR_RGB2HSV)
        
        # 根据迁移强度调整饱和度
        saturation_adjusted = (1 - 迁移强度 / 100) * target_hsv[:, :, 1] + (迁移强度 / 100) * source_hsv[:, :, 1]
        
        matched_target_hsv = target_hsv.copy()
        matched_target_hsv[:, :, 1] = np.clip(saturation_adjusted, 0, 255)  # 确保饱和度值在0到255之间
        
        matched_target_rgb = cv2.cvtColor(matched_target_hsv, cv2.COLOR_HSV2RGB)
        
        matched_target_pil = Image.fromarray(np.clip(matched_target_rgb * 255, 0, 255).astype(np.uint8))
        
        result_tensor = pil_to_tensor(matched_target_pil)
        
        return (result_tensor,)
