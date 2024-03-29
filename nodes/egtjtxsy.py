import os
import numpy as np
import torch
import sys
from PIL import Image, ImageOps
from torchvision import transforms as T
from torchvision.transforms import functional as TF




my_dir = os.path.dirname(os.path.abspath(__file__))
custom_nodes_dir = os.path.abspath(os.path.join(my_dir, '.'))
comfy_dir = os.path.abspath(os.path.join(my_dir, '..'))
sys.path.append(comfy_dir)

from nodes import MAX_RESOLUTION


def tensor2pil(image: torch.Tensor) -> Image.Image:
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


def pil2tensor(image: Image.Image) -> torch.Tensor:
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def common_upscale(samples, 缩放宽度, 缩放高度, upscale_method, crop):
        if crop == "center":
            old_缩放宽度 = samples.shape[3]
            old_缩放高度 = samples.shape[2]
            old_aspect = old_缩放宽度 / old_缩放高度
            new_aspect = 缩放宽度 / 缩放高度
            x = 0
            y = 0
            if old_aspect > new_aspect:
                x = round((old_缩放宽度 - old_缩放宽度 * (new_aspect / old_aspect)) / 2)
            elif old_aspect < new_aspect:
                y = round((old_缩放高度 - old_缩放高度 * (old_aspect / new_aspect)) / 2)
            s = samples[:,:,y:old_缩放高度-y,x:old_缩放宽度-x]
        else:
            s = samples

        if upscale_method == "bislerp":
            return bislerp(s, 缩放宽度, 缩放高度)
        elif upscale_method == "lanczos":
            return lanczos(s, 缩放宽度, 缩放高度)
        else:
            return torch.nn.functional.interpolate(s, size=(缩放高度, 缩放宽度), mode=upscale_method)


class EGCPSYTJNode:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入原图": ("IMAGE",),
                "输入水印": ("IMAGE",),
                "缩放模式": (["None", "保持比例铺满", "按照缩放倍数缩放", "按照输入宽高缩放"],),
                "缩放方法": (["nearest-exact", "bilinear", "area"],),
                "缩放倍数": ("FLOAT", {"default": 1, "min": 0.01, "max": 16.0, "step": 0.1}),
                "缩放宽度": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                "缩放高度": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                "初始位置": (["居中", "上", "下", "左", "右", "上 左", "上 右", "下 左", "下 右"],),
                "横向位移": ("INT", {"default": 0, "min": -48000, "max": 48000, "step": 10}),
                "竖向位移": ("INT", {"default": 0, "min": -48000, "max": 48000, "step": 10}),
                "旋转度数": ("INT", {"default": 0, "min": -180, "max": 180, "step": 5}),
                "水印透明度": ("FLOAT", {"default": 0, "min": 0, "max": 100, "step": 5, "display": "slider"}),
            },
            "optional": {"水印遮罩": ("MASK",),}
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_输入水印"
    CATEGORY = "2🐕/水印大师"

    def apply_输入水印(self, 输入原图, 输入水印, 缩放模式, 缩放方法, 缩放倍数,
                            缩放宽度, 缩放高度, 横向位移, 竖向位移, 旋转度数, 水印透明度, 初始位置, 水印遮罩=None):

        
        size = 缩放宽度, 缩放高度
        location = 横向位移, 竖向位移
        mask = 水印遮罩

        
        if 缩放模式 != "None":
            
            输入水印_size = 输入水印.size()
            输入水印_size = (输入水印_size[2], 输入水印_size[1])
            if 缩放模式 == "保持比例铺满":
                h_ratio = 输入原图.size()[1] / 输入水印_size[1]
                w_ratio = 输入原图.size()[2] / 输入水印_size[0]
                ratio = min(h_ratio, w_ratio)
                输入水印_size = tuple(round(dimension * ratio) for dimension in 输入水印_size)
            elif 缩放模式 == "按照缩放倍数缩放":
                输入水印_size = tuple(int(dimension * 缩放倍数) for dimension in 输入水印_size)
            elif 缩放模式 == "按照输入宽高缩放":
                输入水印_size = (size[0], size[1])

            samples = 输入水印.movedim(-1, 1)
            输入水印 =common_upscale(samples, 输入水印_size[0], 输入水印_size[1], 缩放方法, False)
            输入水印 = 输入水印.movedim(1, -1)
            
        输入水印 = tensor2pil(输入水印)

         
        输入水印 = 输入水印.convert('RGBA')
        输入水印.putalpha(Image.new("L", 输入水印.size, 255))

        
        if mask is not None:
            
            mask = tensor2pil(mask)
            mask = mask.resize(输入水印.size)
            
            输入水印.putalpha(ImageOps.invert(mask))

        
        输入水印 = 输入水印.rotate(旋转度数, expand=True)

        
        r, g, b, a = 输入水印.split()
        a = a.point(lambda x: max(0, int(x * (1 - 水印透明度 / 100))))
        输入水印.putalpha(a)  
        
        输入原图_缩放宽度, 输入原图_缩放高度 = 输入原图.size()[2], 输入原图.size()[1]
        输入水印_缩放宽度, 输入水印_缩放高度 = 输入水印.size
        
        
        横向位移_int = None
        竖向位移_int = None
        
        if 初始位置 == "居中":
            横向位移_int = int(横向位移 + (输入原图_缩放宽度 - 输入水印_缩放宽度) / 2)
            竖向位移_int = int(竖向位移 + (输入原图_缩放高度 - 输入水印_缩放高度) / 2)
        elif 初始位置 == "上":
            横向位移_int = int(横向位移 + (输入原图_缩放宽度 - 输入水印_缩放宽度) / 2)
            竖向位移_int = 竖向位移  
        elif 初始位置 == "下":
            横向位移_int = int(横向位移 + (输入原图_缩放宽度 - 输入水印_缩放宽度) / 2)
            竖向位移_int = int(竖向位移 + 输入原图_缩放高度 - 输入水印_缩放高度)
        elif 初始位置 == "左":
            竖向位移_int = int(竖向位移 + (输入原图_缩放高度 - 输入水印_缩放高度) / 2)
            横向位移_int = 横向位移  
        elif 初始位置 == "右":
            横向位移_int = int(横向位移 + 输入原图_缩放宽度 - 输入水印_缩放宽度)
            竖向位移_int = int(竖向位移 + (输入原图_缩放高度 - 输入水印_缩放高度) / 2)
        elif 初始位置 == "上 左":
            pass  
        elif 初始位置 == "上 右":
            横向位移_int = int(输入原图_缩放宽度 - 输入水印_缩放宽度 + 横向位移)  
            竖向位移_int = 竖向位移  
        elif 初始位置 == "下 左":
            横向位移_int = 横向位移  
            竖向位移_int = int(输入原图_缩放高度 - 输入水印_缩放高度 + 竖向位移) 
        elif 初始位置 == "下 右":
            横向位移_int = int(横向位移 + 输入原图_缩放宽度 - 输入水印_缩放宽度)
            竖向位移_int = int(竖向位移 + 输入原图_缩放高度 - 输入水印_缩放高度)
        
        if 横向位移_int is not None and 竖向位移_int is not None:
            
            location = 横向位移_int, 竖向位移_int
        else:
            
            location = 横向位移, 竖向位移

        
        输入原图_list = torch.unbind(输入原图, dim=0)

        
        processed_输入原图_list = []
        for tensor in 输入原图_list:
            
            image = tensor2pil(tensor)

            
            if mask is None:
                image.paste(输入水印, location)
            else:
                image.paste(输入水印, location, 输入水印)

            
            processed_tensor = pil2tensor(image)

            
            processed_输入原图_list.append(processed_tensor)

        
        输入原图 = torch.stack([tensor.squeeze() for tensor in processed_输入原图_list])

        
        return (输入原图,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
