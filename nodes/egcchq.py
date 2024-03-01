import torch
from typing import Tuple

class EGTXCCHQ:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            
            "required": {
                "输入图像": ("IMAGE", {}), 
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("宽度", "高度") 
    FUNCTION = "get_image_size"
    CATEGORY = "2🐕/图像/常规处理" 

    def get_image_size(self, 输入图像: torch.Tensor) -> Tuple[int, int]:
        if len(image_in.shape) == 4:
            height, width = 输入图像.shape[1], 输入图像.shape[2]
        else:
            height, width = 输入图像.shape[-2], 输入图像.shape[-1]
        return (width, height)

NODE_CLASS_MAPPINGS = { "EG_TX_CCHQ" : EGTXCCHQ }
NODE_DISPLAY_NAME_MAPPINGS = { "EG_TX_CCHQ" : "2🐕图像尺寸获取" } 
