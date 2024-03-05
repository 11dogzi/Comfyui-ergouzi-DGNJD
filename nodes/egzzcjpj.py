import torch
from PIL import Image
import numpy as np
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
def resize_mask(mask_pil, target_size):
    return mask_pil.resize(target_size, Image.LANCZOS)
class EGZZHBCJNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_mask": ("MASK",),
                "source_mask": ("MASK",),
                "operation": (["merge", "crop"], {}),
            },
        }
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("result_mask",)
    FUNCTION = "mask_operation"
    CATEGORY = "2🐕/遮罩"
    def mask_operation(self, source_mask, target_mask, operation):
        source_mask_pil = tensor2pil(source_mask)
        target_mask_pil = tensor2pil(target_mask)
        source_mask_pil = resize_mask(source_mask_pil, target_mask_pil.size)      
        source_mask_array = np.array(source_mask_pil) > 0
        target_mask_array = np.array(target_mask_pil) > 0
        
        if operation == "merge":
            result_mask_array = np.logical_or(source_mask_array, target_mask_array)
        elif operation == "crop":
            result_mask_array = np.logical_and(target_mask_array, np.logical_not(source_mask_array))
        
        result_mask = Image.fromarray((result_mask_array * 255).astype(np.uint8))
        
        result_mask_tensor = pil2tensor(result_mask)
        
        return (result_mask_tensor, )
