import comfy
import torch
import nodes
class EGPCZH:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images_batch1": ("IMAGE",),
                "images_batch2": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "doit"
    CATEGORY = "2🐕/图像"

    def doit(self, images_batch1, images_batch2):
        # Check and adjust the size of images in the second batch
        for i, image in enumerate(images_batch2):
            if image.shape[1:] != images_batch1[0].shape[1:]:
                images_batch2[i] = comfy.utils.common_upscale(image.movedim(-1, 1), 
                                                             images_batch1[0].shape[2], 
                                                             images_batch1[0].shape[1], 
                                                             "lanczos", "center").movedim(1, -1)

        # Combine the two batches
        combined_batch = torch.cat((images_batch1, images_batch2), dim=0)

        return (combined_batch,)