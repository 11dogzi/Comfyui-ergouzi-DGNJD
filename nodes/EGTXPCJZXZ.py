import comfy
import torch
import nodes
class EGPCTXLZ:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
                "image5": ("IMAGE",),
                "image6": ("IMAGE",)
            },
            "optional": {
                "batch_size": ("INT", {"default": 6, "min": 1, "max": 6, "step": 1})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "doit"
    CATEGORY = "2🐕/图像"

    def doit(self, image1, image2, image3, image4, image5, image6, batch_size=6):
        images = [image2, image3, image4, image5, image6]

        # Use only the selected number of images
        images = images[:batch_size-1]

        for image2 in images:
            if image1.shape[1:] != image2.shape[1:]:
                image2 = comfy.utils.common_upscale(image2.movedim(-1, 1), image1.shape[2], image1.shape[1], "lanczos", "center").movedim(1, -1)
            image1 = torch.cat((image1, image2), dim=0)
        
        return (image1,)
