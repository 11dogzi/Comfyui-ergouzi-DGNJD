import numpy as np
import scipy.ndimage
import torch

def fill_holes(input_mask):
    input_mask = input_mask.reshape((-1, input_mask.shape[-2], input_mask.shape[-1]))
    out = []
    for m in input_mask:
        output = m.numpy()
        output = scipy.ndimage.binary_fill_holes(output).astype(output.dtype)
        output = torch.from_numpy(output)
        out.append(output)
    return torch.stack(out, dim=0)

def keep_specific_component(mask, target_label):
    labeled_mask, num_components = scipy.ndimage.label(mask)
    kept_mask = (labeled_mask == target_label).astype(mask.dtype)
    return kept_mask

def keep_largest_component(mask):
    labeled_mask, num_components = scipy.ndimage.label(mask)
    sizes = scipy.ndimage.sum(mask, labeled_mask, range(1, num_components + 1))
    largest_component = sizes.argmax() + 1
    kept_mask = (labeled_mask == largest_component).astype(mask.dtype)
    return kept_mask

class EGJFZZTC:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入遮罩": ("MASK",),
                "是否填充": ("BOOLEAN", {"default": True}),
                "保留最大区域": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "目标标签": ("INT", {"default": -1, "min": -1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("遮罩",)
    FUNCTION = "run"
    CATEGORY = "2🐕/遮罩/细化处理"

    def run(self, 输入遮罩, 是否填充, 保留最大区域, 目标标签=-1):
        if 是否填充:
            filled_mask = fill_holes(输入遮罩)
        else:
            filled_mask = 输入遮罩

        if 保留最大区域:
            selected_mask = torch.from_numpy(keep_largest_component(filled_mask.numpy()))
        elif 目标标签 >= 0:
            selected_mask = torch.from_numpy(keep_specific_component(filled_mask.numpy(), 目标标签))
        else:
            selected_mask = filled_mask

        return (selected_mask,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
