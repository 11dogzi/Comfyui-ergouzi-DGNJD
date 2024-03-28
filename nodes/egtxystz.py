import cv2
import numpy as np
import torch
from PIL import Image, ImageEnhance
class EGHTYSTZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "色温": ("FLOAT", {
                    "default": 0, 
                    "min": -100, 
                    "max": 100, 
                    "step": 100,
                    "precision": 5,
                    "display": "slider" 
                }),
                "色调": ("FLOAT", {
                    "default": 0, 
                    "min": -90, 
                    "max": 90, 
                    "step": 5,
                    "precision": 180,
                    "display": "slider" 
                }),
                "亮度": ("FLOAT", {
                    "default": 0, 
                    "min": -100, 
                    "max": 100, 
                    "step": 5,
                    "precision": 200,
                    "display": "slider" 
                }),
                "对比度": ("FLOAT", {
                    "default": 0, 
                    "min": -100, 
                    "max": 100, 
                    "step": 5,
                    "precision": 200,
                    "display": "slider" 
                }),
                "饱和度": ("FLOAT", {
                    "default": 0, 
                    "min": -100, 
                    "max": 100, 
                    "step": 5,
                    "precision": 200,
                    "display": "slider" 
                }),
                "明暗度": ("INT", {
                    "default": 1, 
                    "min": -0.2, 
                    "max": 2.2, 
                    "step": 0.1,
                    "precision": 200,
                    "display": "slider" 
                }),
                "模糊度": ("INT", {
                    "default": 0, 
                    "min": -200, 
                    "max": 200, 
                    "step": 1,
                    "precision": 200,
                    "display": "slider" 
                }),
            },
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "color_correct"
    CATEGORY = "2🐕/图像/滤镜"
    def color_correct(
        self,
        image: torch.Tensor,
        色温: float,
        色调: float,
        亮度: float,
        对比度: float,
        饱和度: float,
        明暗度: float,
        模糊度: float,
    ):
        batch_size, height, width, _ = image.shape
        result = torch.zeros_like(image)
        亮度 /= 100
        对比度 /= 100
        饱和度 /= 100
        色温 /= 100
        亮度 = 1 + 亮度
        对比度 = 1 + 对比度
        饱和度 = 1 + 饱和度
        for b in range(batch_size):
            tensor_image = image[b].numpy()
            modified_image = Image.fromarray((tensor_image * 255).astype(np.uint8))
            # 亮度
            modified_image = ImageEnhance.Brightness(modified_image).enhance(亮度)
            # 对比度
            modified_image = ImageEnhance.Contrast(modified_image).enhance(对比度)
            modified_image = np.array(modified_image).astype(np.float32)
            # 色温
            if 色温 > 0:
                modified_image[:, :, 0] *= 1 + 色温
                modified_image[:, :, 1] *= 1 + 色温 * 0.4
            elif 色温 < 0:
                modified_image[:, :, 2] *= 1 - 色温
            modified_image = np.clip(modified_image, 0, 255) / 255
            # 明暗度
            modified_image = np.clip(np.power(modified_image, 明暗度), 0, 1)
            # 饱和度
            hls_img = cv2.cvtColor(modified_image, cv2.COLOR_RGB2HLS)
            hls_img[:, :, 2] = np.clip(饱和度 * hls_img[:, :, 2], 0, 1)
            modified_image = cv2.cvtColor(hls_img, cv2.COLOR_HLS2RGB) * 255
            # 色调
            hsv_img = cv2.cvtColor(modified_image, cv2.COLOR_RGB2HSV)
            hsv_img[:, :, 0] = (hsv_img[:, :, 0] + 色调) % 360
            modified_image = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
            # 模糊度
            if 模糊度 > 0:
                modified_image = cv2.GaussianBlur(modified_image, (模糊度*2+1, 模糊度*2+1), 0)
            modified_image = modified_image.astype(np.uint8)
            modified_image = modified_image / 255
            modified_image = torch.from_numpy(modified_image).unsqueeze(0)
            result[b] = modified_image
        return (result,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
