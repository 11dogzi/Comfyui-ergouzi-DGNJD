from typing import Tuple, Dict, Any
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from skimage import exposure
from skimage.transform import resize


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

class EGSCQYQBQYNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "颜色图": ("IMAGE",),
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
    FUNCTION = "transfer_color"
    CATEGORY = "2🐕/图像/色彩处理"

    def transfer_color(self, 颜色图, 目标图, 迁移强度=50):
        source_pil = tensor_to_pil(颜色图)
        target_pil = tensor_to_pil(目标图)
    
        source_np = np.array(source_pil)
        target_np = np.array(target_pil)
    
        matched_target_np = np.empty_like(target_np)
        for i in range(source_np.shape[-1]):
            matched_target_np[:, :, i] = exposure.match_histograms(
                target_np[:, :, i], source_np[:, :, i]
            )
    
        result_np = (1 - 迁移强度 / 100) * target_np + (迁移强度 / 100) * matched_target_np
        result_pil = Image.fromarray(result_np.astype(np.uint8))
    
        result_tensor = pil_to_tensor(result_pil)
        return (result_tensor,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
