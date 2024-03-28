import torch
def common_upscale(samples, width, height, 缩放方法, 裁剪):
        if 裁剪 == "center":
            old_width = samples.shape[3]
            old_height = samples.shape[2]
            old_aspect = old_width / old_height
            new_aspect = width / height
            x = 0
            y = 0
            if old_aspect > new_aspect:
                x = round((old_width - old_width * (new_aspect / old_aspect)) / 2)
            elif old_aspect < new_aspect:
                y = round((old_height - old_height * (old_aspect / new_aspect)) / 2)
            s = samples[:,:,y:old_height-y,x:old_width-x]
        else:
            s = samples

        if 缩放方法 == "bislerp":
            return bislerp(s, width, height)
        elif 缩放方法 == "lanczos":
            return lanczos(s, width, height)
        else:
            return torch.nn.functional.interpolate(s, size=(height, width), mode=缩放方法)

class EGTXSFBLSNode:
    缩放方法s = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    裁剪方式 = ["disabled", "center"]
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image": ("IMAGE",),
                             "width": ("INT", {"default": 512, "min": 0, "max": 10000, "step": 1}),
                             "height": ("INT", {"default": 512, "min": 0, "max": 10000, "step": 1}),
                             "裁剪": (s.裁剪方式,)},
                "optional": {"缩放方法": (s.缩放方法s,),
                             "锁定比例": ("BOOLEAN", {"default": False}),
                             }
                }
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES =('图像', '宽度', '高度')
    FUNCTION = "upscale"
    CATEGORY = "2🐕/图像"
    def upscale(self, image, 缩放方法, width, height, 裁剪, 锁定比例=False):
        if width == 0 and height == 0:
            s = image
            return_width = image.shape[3]
            return_height = image.shape[2]
        else:
            samples = image.movedim(-1,1)
            original_width, original_height = samples.shape[3], samples.shape[2]
            original_aspect = original_width / original_height
            if not 锁定比例:
                if width == 0:
                    width = original_width
                if height == 0:
                    height = original_height
            else:
                if width != 0 and height != 0:
                    if width > height:
                        height = max(1, round(width / original_aspect))
                    else:
                        width = max(1, round(height * original_aspect))
                elif width != 0 and height == 0:
                    height = max(1, round(width / original_aspect))
                elif width == 0 and height != 0:
                    width = max(1, round(height * original_aspect))
            s = common_upscale(samples, width, height, 缩放方法, 裁剪)
            s = s.movedim(1,-1)
            return_width = width
            return_height = height
        return (s, return_width, return_height)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
