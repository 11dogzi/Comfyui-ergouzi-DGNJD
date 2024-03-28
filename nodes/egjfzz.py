import numpy as np
import scipy.ndimage
import torch

def grow(输入遮罩, expand, tapered_corners):
    c = 0 if tapered_corners else 1
    kernel = np.array([[c, 1, c],
                            [1, 1, 1],
                            [c, 1, c]])
    输入遮罩 = 输入遮罩.reshape((-1, 输入遮罩.shape[-2], 输入遮罩.shape[-1]))
    out = []
    for m in 输入遮罩:
        output = m.numpy()
        for _ in range(abs(expand)):
            if expand < 0:
                output = scipy.ndimage.grey_erosion(output, footprint=kernel)
            else:
                output = scipy.ndimage.grey_dilation(output, footprint=kernel)
        output = torch.from_numpy(output)
        out.append(output)
    return torch.stack(out, dim=0)

def combine(destination, source, x, y):
    output = destination.reshape((-1, destination.shape[-2], destination.shape[-1])).clone()
    source = source.reshape((-1, source.shape[-2], source.shape[-1]))

    left, top = (x, y,)
    right, bottom = (min(left + source.shape[-1], destination.shape[-1]), min(top + source.shape[-2], destination.shape[-2]))
    visible_width, visible_height = (right - left, bottom - top,)

    source_portion = source[:, :visible_height, :visible_width]
    destination_portion = destination[:, top:bottom, left:right]

    
    output[:, top:bottom, left:right] = destination_portion - source_portion

    output = torch.clamp(output, 0.0, 1.0)

    return output

class EGJFZZSC:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            
            "required": {
                "输入遮罩": ("MASK",),
                "生成宽度": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 666,
                    "step": 1
                }),
                "平滑边缘开关": ("BOOLEAN", {"default": True}),
            },
            
            "optional": {}
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("生成接缝遮罩",)
    FUNCTION = "run"
    CATEGORY = "2🐕/遮罩/细化处理"

    def run(self, 输入遮罩, 生成宽度, 平滑边缘开关):
        m1 = grow(输入遮罩, 生成宽度, 平滑边缘开关)
        m2 = grow(输入遮罩, -生成宽度, 平滑边缘开关)
        m3 = combine(m1, m2, 0, 0)

        return (m3,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
