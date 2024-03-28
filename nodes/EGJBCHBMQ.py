import torch
import math


class EGJBCH:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE",),
            "vae": ("VAE",),
            "mask": ("MASK",),
            "遮罩延展": ("INT", {"default": 6, "min": 0, "max": 64, "step": 1}),
            "重绘模式": (["原图", "填充"],),
        }}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "encode"
    CATEGORY = "2🐕/Latent"

    def encode(self, vae, image, mask, 遮罩延展=6, 重绘模式="填充"):
        x = (image.shape[1] // 8) * 8
        y = (image.shape[2] // 8) * 8
        mask = torch.nn.functional.interpolate(mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])),
                                               size=(image.shape[1], image.shape[2]), mode="bilinear")
        if 重绘模式 == "填充":
            image = image.clone()
            if image.shape[1] != x or image.shape[2] != y:
                x_offset = (image.shape[1] % 8) // 2
                y_offset = (image.shape[2] % 8) // 2
                image = image[:, x_offset:x + x_offset, y_offset:y + y_offset, :]
                mask = mask[:, :, x_offset:x + x_offset, y_offset:y + y_offset]
        # grow mask by a few image to keep things seamless in latent space
        if 遮罩延展 == 0:
            mask_erosion = mask
        else:
            kernel_tensor = torch.ones((1, 1, 遮罩延展, 遮罩延展))
            padding = math.ceil((遮罩延展 - 1) / 2)
            mask_erosion = torch.clamp(torch.nn.functional.conv2d(mask.round(), kernel_tensor, padding=padding), 0, 1)

        m = (1.0 - mask.round()).squeeze(1)
        if 重绘模式 == "填充":
            for i in range(3):
                image[:, :, :, i] -= 0.5
                image[:, :, :, i] *= m
                image[:, :, :, i] += 0.5
        t = vae.encode(image)
        return ({"samples": t, "noise_mask": (mask_erosion[:, :, :x, :y].round())},)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
