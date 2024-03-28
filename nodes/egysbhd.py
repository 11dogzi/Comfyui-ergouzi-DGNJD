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
                "source_image": ("IMAGE",),  
                "target_image": ("IMAGE",),  
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("result_image",)
    FUNCTION = "transfer_saturation"
    CATEGORY = "2🐕/图像/色彩处理"
    def transfer_saturation(self, source_image, target_image):
        source_pil = tensor_to_pil(source_image)
        target_pil = tensor_to_pil(target_image)
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
        
        matched_target_hsv = target_hsv.copy()
        matched_target_hsv[:, :, 1] = source_hsv[:, :, 1]
        
        matched_target_rgb = cv2.cvtColor(matched_target_hsv, cv2.COLOR_HSV2RGB)
        
        matched_target_pil = Image.fromarray(np.clip(matched_target_rgb * 255, 0, 255).astype(np.uint8))
        
        result_tensor = pil_to_tensor(matched_target_pil)
        
        return (result_tensor,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
