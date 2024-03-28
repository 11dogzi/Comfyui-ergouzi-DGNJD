import torch
import torch.nn.functional as F

class EGZZBSYH:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK", {}),
            },
            "optional": {
                "kernel_size": ("INT", {"default": 50, "min": 3, "max": 200, "step": 2}),
                "sigma": ("FLOAT", {"default": 15.0, "min": 0.1, "max": 200.0, "step": 0.1}),
                "shrink_pixels": ("INT", {"default": 0, "min": 0, "max": 50, "step": 1}),
                "expand_pixels": ("INT", {"default": 0, "min": 0, "max": 50, "step": 1}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("遮罩",)
    FUNCTION = "gaussian_blur_edge"
    CATEGORY = "2🐕/遮罩/模糊羽化"
    def gaussian_blur_edge(self, mask, kernel_size=5, sigma=1.0, shrink_pixels=0, expand_pixels=0):
        
        binary_mask = (mask > 0.5).float()
        
        if shrink_pixels > 0:
            
            eroded_mask = F.max_pool2d(binary_mask.unsqueeze(0), kernel_size=shrink_pixels+1, stride=1, padding=shrink_pixels//2)
            binary_mask = eroded_mask.squeeze(0)
        elif expand_pixels > 0:
            
            
            expand_kernel = torch.ones(1, 1, expand_pixels*2+1, expand_pixels*2+1).to(mask.device) / (expand_pixels*2+1)**2
            expanded_mask = F.conv2d(binary_mask.unsqueeze(0), expand_kernel, padding=expand_pixels)
            binary_mask = expanded_mask.squeeze(0)
        
        x = torch.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
        x_grid = x.repeat(kernel_size).view(kernel_size, kernel_size)
        y_grid = x_grid.t()
        gaussian_kernel = torch.exp(-(x_grid**2 + y_grid**2) / (2 * sigma**2))
        gaussian_kernel /= gaussian_kernel.sum()
        
        kernel = gaussian_kernel.view(1, 1, kernel_size, kernel_size).repeat(1, 1, 1, 1).to(mask.device)
        
        blurred_mask = F.conv2d(binary_mask.unsqueeze(0), kernel, padding=kernel_size // 2, groups=1).squeeze(0)
        return (blurred_mask,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
