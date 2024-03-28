import torch
import torch.nn.functional as F

class EGZZBYYHNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入遮罩": ("MASK", {}),
            },
            "optional": {
                "模糊权重": ("INT", {"default": 50, "min": 1, "max": 1000, "step": 2}),
                "边缘模糊大小": ("INT", {"default": 50, "min": 1, "max": 1000, "step": 1}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("遮罩",)
    FUNCTION = "gaussian_blur_edge"
    CATEGORY = "2🐕/遮罩/模糊羽化"

    def gaussian_blur_edge(self, 输入遮罩, 模糊权重=5, 边缘模糊大小=1):
        binary_mask = (输入遮罩 > 0.5).float()
        
        sigma_float = 边缘模糊大小 / 10.0
        
        kernel_size_half = 模糊权重 // 2
        x = torch.linspace(-kernel_size_half, kernel_size_half, 模糊权重)
        x_grid = x.repeat(模糊权重).view(模糊权重, 模糊权重)
        y_grid = x_grid.t()
        gaussian_kernel = torch.exp(-(x_grid**2 + y_grid**2) / (2 * sigma_float**2))
        gaussian_kernel /= gaussian_kernel.sum()
        kernel = gaussian_kernel.view(1, 1, 模糊权重, 模糊权重).repeat(1, 1, 1, 1).to(输入遮罩.device)
        blurred_mask = F.conv2d(binary_mask.unsqueeze(0), kernel, padding=kernel_size_half, groups=1).squeeze(0)
        return (blurred_mask,)



# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
