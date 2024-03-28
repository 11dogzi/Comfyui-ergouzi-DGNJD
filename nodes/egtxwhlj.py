import os
import numpy as np
from PIL import Image
import torch
from typing import Union, List
import subprocess
try:
    import pilgram
except ImportError:
    subprocess.check_call(['pip', 'install', 'pilgram'])
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
class EGWHLJ:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "style": ([
                    "1977",
                    "aden",
                    "brannan",
                    "brooklyn",
                    "clarendon",
                    "earlybird",
                    "gingham",
                    "hudson",
                    "inkwell",
                    "kelvin",
                    "lark",
                    "lofi",
                    "maven",
                    "mayfair",
                    "moon",
                    "nashville",
                    "perpetua",
                    "reyes",
                    "rise",
                    "slumber",
                    "stinson",
                    "toaster",
                    "valencia",
                    "walden",
                    "willow",
                    "xpro2"
                ],),
            },
            "optional": {
                "All": ("BOOLEAN", {"default": False}),
            },
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_style_filter"
    CATEGORY = "2🐕/图像/滤镜"
    def image_style_filter(self, image, style, All=False):
        if All:
            tensors = []
            for img in image:
                for filter_name in self.INPUT_TYPES()['required']['style'][0]:
                    if filter_name == "1977":
                        tensors.append(pil2tensor(pilgram._1977(tensor2pil(img))))
                    elif filter_name == "aden":
                        tensors.append(pil2tensor(pilgram.aden(tensor2pil(img))))
                    elif filter_name == "brannan":
                        tensors.append(pil2tensor(pilgram.brannan(tensor2pil(img))))
                    elif filter_name == "brooklyn":
                        tensors.append(pil2tensor(pilgram.brooklyn(tensor2pil(img))))
                    elif filter_name == "clarendon":
                        tensors.append(pil2tensor(pilgram.clarendon(tensor2pil(img))))
                    elif filter_name == "earlybird":
                        tensors.append(pil2tensor(pilgram.earlybird(tensor2pil(img))))
                    elif filter_name == "gingham":
                        tensors.append(pil2tensor(pilgram.gingham(tensor2pil(img))))
                    elif filter_name == "hudson":
                        tensors.append(pil2tensor(pilgram.hudson(tensor2pil(img))))
                    elif filter_name == "inkwell":
                        tensors.append(pil2tensor(pilgram.inkwell(tensor2pil(img))))
                    elif filter_name == "kelvin":
                        tensors.append(pil2tensor(pilgram.kelvin(tensor2pil(img))))
                    elif filter_name == "lark":
                        tensors.append(pil2tensor(pilgram.lark(tensor2pil(img))))
                    elif filter_name == "lofi":
                        tensors.append(pil2tensor(pilgram.lofi(tensor2pil(img))))
                    elif filter_name == "maven":
                        tensors.append(pil2tensor(pilgram.maven(tensor2pil(img))))
                    elif filter_name == "mayfair":
                        tensors.append(pil2tensor(pilgram.mayfair(tensor2pil(img))))
                    elif filter_name == "moon":
                        tensors.append(pil2tensor(pilgram.moon(tensor2pil(img))))
                    elif filter_name == "nashville":
                        tensors.append(pil2tensor(pilgram.nashville(tensor2pil(img))))
                    elif filter_name == "perpetua":
                        tensors.append(pil2tensor(pilgram.perpetua(tensor2pil(img))))
                    elif filter_name == "reyes":
                        tensors.append(pil2tensor(pilgram.reyes(tensor2pil(img))))
                    elif filter_name == "rise":
                        tensors.append(pil2tensor(pilgram.rise(tensor2pil(img))))
                    elif filter_name == "slumber":
                        tensors.append(pil2tensor(pilgram.slumber(tensor2pil(img))))
                    elif filter_name == "stinson":
                        tensors.append(pil2tensor(pilgram.stinson(tensor2pil(img))))
                    elif filter_name == "toaster":
                        tensors.append(pil2tensor(pilgram.stinson(tensor2pil(img))))
                    elif filter_name == "valencia":
                        tensors.append(pil2tensor(pilgram.valencia(tensor2pil(img))))
                    elif filter_name == "walden":
                        tensors.append(pil2tensor(pilgram.walden(tensor2pil(img))))
                    elif filter_name == "willow":
                        tensors.append(pil2tensor(pilgram.willow(tensor2pil(img))))
                    elif filter_name == "xpro2":
                        tensors.append(pil2tensor(pilgram.xpro2(tensor2pil(img))))
            tensors = torch.cat(tensors, dim=0)
            return (tensors, )
        else:
            tensors = []
            for img in image:
                if style == "1977":
                    tensors.append(pil2tensor(pilgram._1977(tensor2pil(img))))
                elif style == "aden":
                    tensors.append(pil2tensor(pilgram.aden(tensor2pil(img))))
                elif style == "brannan":
                    tensors.append(pil2tensor(pilgram.brannan(tensor2pil(img))))
                elif style == "brooklyn":
                    tensors.append(pil2tensor(pilgram.brooklyn(tensor2pil(img))))
                elif style == "clarendon":
                    tensors.append(pil2tensor(pilgram.clarendon(tensor2pil(img))))
                elif style == "earlybird":
                    tensors.append(pil2tensor(pilgram.earlybird(tensor2pil(img))))
                elif style == "gingham":
                    tensors.append(pil2tensor(pilgram.gingham(tensor2pil(img))))
                elif style == "hudson":
                    tensors.append(pil2tensor(pilgram.hudson(tensor2pil(img))))
                elif style == "inkwell":
                    tensors.append(pil2tensor(pilgram.inkwell(tensor2pil(img))))
                elif style == "kelvin":
                    tensors.append(pil2tensor(pilgram.kelvin(tensor2pil(img))))
                elif style == "lark":
                    tensors.append(pil2tensor(pilgram.lark(tensor2pil(img))))
                elif style == "lofi":
                    tensors.append(pil2tensor(pilgram.lofi(tensor2pil(img))))
                elif style == "maven":
                    tensors.append(pil2tensor(pilgram.maven(tensor2pil(img))))
                elif style == "mayfair":
                    tensors.append(pil2tensor(pilgram.mayfair(tensor2pil(img))))
                elif style == "moon":
                    tensors.append(pil2tensor(pilgram.moon(tensor2pil(img))))
                elif style == "nashville":
                    tensors.append(pil2tensor(pilgram.nashville(tensor2pil(img))))
                elif style == "perpetua":
                    tensors.append(pil2tensor(pilgram.perpetua(tensor2pil(img))))
                elif style == "reyes":
                    tensors.append(pil2tensor(pilgram.reyes(tensor2pil(img))))
                elif style == "rise":
                    tensors.append(pil2tensor(pilgram.rise(tensor2pil(img))))
                elif style == "slumber":
                    tensors.append(pil2tensor(pilgram.slumber(tensor2pil(img))))
                elif style == "stinson":
                    tensors.append(pil2tensor(pilgram.stinson(tensor2pil(img))))
                elif style == "toaster":
                    tensors.append(pil2tensor(pilgram.stinson(tensor2pil(img))))
                elif style == "valencia":
                    tensors.append(pil2tensor(pilgram.valencia(tensor2pil(img))))
                elif style == "walden":
                    tensors.append(pil2tensor(pilgram.walden(tensor2pil(img))))
                elif style == "willow":
                    tensors.append(pil2tensor(pilgram.willow(tensor2pil(img))))                    
                elif style == "xpro2":
                    tensors.append(pil2tensor(pilgram.xpro2(tensor2pil(img))))
                else:
                    tensors.append(img)
            tensors = torch.cat(tensors, dim=0)
            return (tensors, )  

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
