from typing import Tuple, Dict, Any
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from skimage import exposure


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
                "source_image": ("IMAGE",),  
                "target_image": ("IMAGE",),  
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("result_image",)
    FUNCTION = "transfer_color"
    CATEGORY = "2🐕/图像/色彩处理"

    def transfer_color(self, source_image, target_image):
        
        source_pil = tensor_to_pil(source_image)
        target_pil = tensor_to_pil(target_image)
        
        source_np = np.array(source_pil)
        target_np = np.array(target_pil)
        
        matched_target_np = np.empty_like(target_np)
        for i in range(source_np.shape[-1]):  
            matched_target_np[:, :, i] = exposure.match_histograms(
                target_np[:, :, i], source_np[:, :, i]
            )
        
        matched_target_pil = Image.fromarray(matched_target_np)
        
        result_tensor = pil_to_tensor(matched_target_pil)
        return (result_tensor,)

NODE_CLASS_MAPPINGS = { "EG_SCQY_QBQY": EGSCQYQBQYNode }
NODE_DISPLAY_NAME_MAPPINGS = { "EG_SCQY_QBQY": "2🐕常规颜色迁移" }
