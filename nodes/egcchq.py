import torch
from typing import Tuple

class EGTXCCHQ:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            # 必选输入
            "required": {
                "image_in": ("IMAGE", {}), 
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("宽度", "高度") 
    FUNCTION = "get_image_size"
    CATEGORY = "2🐕/图像" 

    def get_image_size(self, image_in: torch.Tensor) -> Tuple[int, int]:
        if len(image_in.shape) == 4:
            height, width = image_in.shape[1], image_in.shape[2]
        else:
            height, width = image_in.shape[-2], image_in.shape[-1]
        return (width, height)

NODE_CLASS_MAPPINGS = { "EG_TX_CCHQ" : EGTXCCHQ }
NODE_DISPLAY_NAME_MAPPINGS = { "EG_TX_CCHQ" : "2🐕图像尺寸获取" } 
