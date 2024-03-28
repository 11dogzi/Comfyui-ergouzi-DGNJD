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

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
