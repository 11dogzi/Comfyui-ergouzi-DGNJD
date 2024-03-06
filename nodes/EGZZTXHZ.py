import torch
from PIL import Image
import numpy as np
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
def image2mask(image_pil):
    # Convert image to grayscale
    image_pil = image_pil.convert("L")
    # Convert grayscale image to binary mask
    threshold = 128
    mask_array = np.array(image_pil) > threshold
    return Image.fromarray((mask_array * 255).astype(np.uint8))
def mask2image(mask_pil):
    color_map = {0: (0, 0, 0),
                 255: (255, 255, 255)}
    color_image = Image.new('RGB', mask_pil.size, color=color_map[0])
    for x in range(mask_pil.width):
        for y in range(mask_pil.height):
            color_image.putpixel((x, y), color_map[mask_pil.getpixel((x, y))])
    return color_image
class EGTXZZZHNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "输入遮罩": ("MASK", {}),
                "输入图像": ("IMAGE", {}),
            },
        }
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("转换图像", "转换遮罩")
    FUNCTION = "convert_input"
    CATEGORY = "2🐕/遮罩"
    def convert_input(self, 输入图像=None, 输入遮罩=None):
        if 输入图像 is None and 输入遮罩 is None:
            default_image = Image.new('L', (256, 256), color=255)
            default_mask = Image.new('L', (256, 256), color=0)
            image_tensor = pil2tensor(default_image)
            mask_tensor = pil2tensor(default_mask)
            return [image_tensor, mask_tensor]
        
        elif 输入图像 is not None:
            input_image_pil = tensor2pil(输入图像)
            转换遮罩_pil = image2mask(input_image_pil)
            转换图像_pil = input_image_pil
        elif 输入遮罩 is not None:
            input_mask_pil = tensor2pil(输入遮罩)
            转换图像_pil = mask2image(input_mask_pil)
            转换遮罩_pil = input_mask_pil
        
        转换图像_tensor = pil2tensor(转换图像_pil)
        转换遮罩_tensor = pil2tensor(转换遮罩_pil)
        
        return [转换图像_tensor, 转换遮罩_tensor]
