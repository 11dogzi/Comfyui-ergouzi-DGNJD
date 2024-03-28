import numpy as np
import torch
from PIL import Image, ImageFilter

specific_filters = [
    'BLUR',
    'CONTOUR',
    'DETAIL',
    'EDGE_ENHANCE',
    'EDGE_ENHANCE_MORE',
    'EMBOSS',
    'FIND_EDGES',
    'GaussianBlur',
    'MaxFilter',
    'MedianFilter',
    'MinFilter',
    'ModeFilter',
    'SHARPEN',
    'SMOOTH',
    'SMOOTH_MORE',
    'UnsharpMask'
]


class EGTXLJNode:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_filter"
    CATEGORY = "2🐕/图像/滤镜"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "滤镜类型": (specific_filters,),
            },
        }
    
    def apply_filter(
        self,
        image: torch.Tensor,
        滤镜类型: str,
    ):
        if 滤镜类型 not in specific_filters:
            raise ValueError(f"Unknown filter type: {滤镜类型}")
    
        image_pil = Image.fromarray((image[0].numpy() * 255).astype(np.uint8))
    
        try:
            filter_instance = getattr(ImageFilter, 滤镜类型)
        except AttributeError:
            filter_method = getattr(image_pil, 滤镜类型)
            if callable(filter_method):
                filter_instance = filter_method()
            else:
                raise ValueError(f"Unknown filter type: {滤镜类型}")
    
        try:
            image_pil = image_pil.filter(filter_instance)
        except TypeError:
            filter_method = getattr(image_pil, 滤镜类型)
            if callable(filter_method):
                default_params = filter_method.__defaults__
                if default_params:
                    filter_instance = filter_method(*default_params)
                    image_pil = image_pil.filter(filter_instance)
                else:
                    raise TypeError(f"Filter {滤镜类型} requires arguments but no default parameters are provided.")
            else:
                raise TypeError(f"Unknown filter type: {滤镜类型}")
    
        image_tensor = torch.from_numpy(np.array(image_pil).astype(np.float32) / 255).unsqueeze(0)
    
        return (image_tensor,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
