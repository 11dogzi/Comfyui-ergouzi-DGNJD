import os
from PIL import Image
import numpy as np
import torch

class EGLJJZTXDZ:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入路径": ("STRING", {}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "切换随机输出": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ('IMAGE',)
    FUNCTION = "get_transparent_image"
    CATEGORY = "2🐕/图像"
    
    def __init__(self):
        self.current_index = 0

    def get_transparent_image(self, 输入路径, seed, 切换随机输出=False):
        try:
            if os.path.isdir(输入路径):
                images = []
                for filename in os.listdir(输入路径):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        img_path = os.path.join(输入路径, filename)
                        image = Image.open(img_path).convert('RGBA')
                        images.append(image)
                if 切换随机输出:
                    import random
                    selected_image = random.choice(images)
                else:
                    selected_image = images[self.current_index % len(images)]
                    self.current_index += 1
                    
                image_rgba = selected_image
                image_np = np.array(image_rgba).astype(np.float32) / 255.0
                image_tensor = torch.from_numpy(image_np)[None, :, :, :]
                
                return (image_tensor,)
        
        except Exception as e:
            print(f"2🐕温馨提示处理图像时出错请重置节点：{e}")
        return None,










# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
