from pickle import NONE
from telnetlib import OUTMRK
import latent_preview
import comfy.samplers
import comfy.sample
import torch
import math
import base64
from colorama import Fore
from typing import Tuple, Dict, Any
from PIL import Image, ImageFilter
import numpy as np
from torchvision import transforms
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
def batch_tensor_to_pil(img_tensor):
    return [tensor2pil(img_tensor, i) for i in range(img_tensor.shape[0])]
def batched_pil_to_tensor(images):
    return torch.cat([pil2tensor(image) for image in images], dim=0)




def common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
    latent_image = latent["samples"]
    if disable_noise:
        noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
    else:
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

    noise_mask = None
    if "noise_mask" in latent:
        noise_mask = latent["noise_mask"]

    callback = latent_preview.prepare_callback(model, steps)
    disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
    out = latent.copy()
    out["samples"] = samples
    return (out, )

def mask2image(input_mask_pil):
    input_mask_tensor = pil2tensor(input_mask_pil)
    result_tensor = input_mask_tensor.expand(-1, 3, -1, -1)
    return result_tensor

statement = 'Ouino+mUgeabtOWkmuWunei0teaXtuWFie+8jOWOu+WBmuabtOacieaEj+S5ieeahOS6i+aDhe+8jOi/meaJjeaYr0FJLS0tLS0tLS1C56uZQOeBteS7meWEv+WSjOS6jOeLl+WtkA=='
EGSMWBA = base64.b64decode(statement.encode('utf-8')).decode('utf-8')
tstatement='Q29tZnl1aS1lcmdvdXppLURHTkpE'
EGSMWBB = base64.b64decode(tstatement.encode('utf-8')).decode('utf-8')

red_part = EGSMWBB
yellow_part = EGSMWBA.replace(red_part, "")
print(Fore.RED + red_part + Fore.YELLOW + yellow_part + Fore.RESET)

class EGCYQJB:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "model": ("MODEL",),
            "image": ("IMAGE",),
            "vae": ("VAE",),
            "mask": ("MASK",),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
            "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01}),
            "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
            "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
            "positive": ("CONDITIONING", ),
            "negative": ("CONDITIONING", ),
            "denoise": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
            "重绘模式": (["原图", "填充"],),
            "遮罩延展": ("INT", {"default": 6, "min": 0, "max": 64, "step": 1}),
            "仅局部重绘": ("BOOLEAN", {"default": True}),
            "局部重绘大小": ("INT", {"default": 512, "min": 0, "max": 2048, "step": 1}),
            "重绘区域扩展": ("INT", {"default": 50, "min": 0}),
            "遮罩羽化":("INT", {"default": 5, "min": 0, "max": 100, "step": 1}),
            "TEXT":("STRING", {"default":"2🐕出品，必出精品"}),
        }}

    RETURN_TYPES = ("LATENT", "IMAGE", "IMAGE","MASK")
    RETURN_NAMES = ('LATENT', '结果图像', '采样图', '采样遮罩')
    FUNCTION = "sample"
    CATEGORY = "2🐕/局部重绘采样器"

    def mask_crop(self, image, mask, 重绘区域扩展, 局部重绘大小=0):
        image_pil = tensor2pil(image)
        mask_pil = tensor2pil(mask)
        mask_array = np.array(mask_pil) > 0
        coords = np.where(mask_array)
        if coords[0].size == 0 or coords[1].size == 0:
            return (image, None, mask)
        x0, y0, x1, y1 = coords[1].min(), coords[0].min(), coords[1].max(), coords[0].max()
        x0 -= 重绘区域扩展
        y0 -= 重绘区域扩展
        x1 += 重绘区域扩展
        y1 += 重绘区域扩展
        x0 = max(x0, 0)
        y0 = max(y0, 0)
        x1 = min(x1, image_pil.width)
        y1 = min(y1, image_pil.height)
        cropped_image_pil = image_pil.crop((x0, y0, x1, y1))
        cropped_mask_pil = mask_pil.crop((x0, y0, x1, y1))
        if 局部重绘大小 > 0:
            min_size = min(cropped_image_pil.size)
            if min_size < 局部重绘大小 or min_size > 局部重绘大小:
                scale_ratio = 局部重绘大小 / min_size
                new_size = (int(cropped_image_pil.width * scale_ratio), int(cropped_image_pil.height * scale_ratio))
                cropped_image_pil = cropped_image_pil.resize(new_size, Image.LANCZOS)
                cropped_mask_pil = cropped_mask_pil.resize(new_size, Image.LANCZOS)

        cropped_image_tensor = pil2tensor(cropped_image_pil)
        cropped_mask_tensor = pil2tensor(cropped_mask_pil)
        qtch = image
        qtzz = mask
        return (cropped_image_tensor, cropped_mask_tensor, (y0, y1, x0, x1) ,qtch ,qtzz )

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
        return {"samples": t, "noise_mask": (mask_erosion[:, :, :x, :y].round())}, None
    def paste_cropped_image_with_mask(self, original_image, cropped_image, crop_coords, mask, MHmask, 遮罩羽化):
        y0, y1, x0, x1 = crop_coords
        original_image_pil = tensor2pil(original_image)
        cropped_image_pil = tensor2pil(cropped_image)
        mask_pil = tensor2pil(mask)
        crop_width = x1 - x0
        crop_height = y1 - y0
        crop_size = (crop_width, crop_height)

        cropped_image_pil = cropped_image_pil.resize(crop_size, Image.LANCZOS)
        mask_pil = mask_pil.resize(crop_size, Image.LANCZOS)

        mask_binary = mask_pil.convert('L')
        mask_rgba = mask_binary.convert('RGBA')
        blurred_mask = mask_rgba
        transparent_mask = mask_binary
        blurred_mask = mask_binary
        cropped_image_pil = cropped_image_pil.convert('RGBA')
        original_image_pil = original_image_pil.convert('RGBA')
        original_image_pil.paste(cropped_image_pil, (x0, y0), mask=blurred_mask)
        ZT_image_pil=original_image_pil.convert('RGB')
        IMAGEEE = pil2tensor(ZT_image_pil)        
        mask_ecmhpil= tensor2pil(MHmask)   
        mask_ecmh = mask_ecmhpil.convert('L')
        mask_ecrgba = tensor2pil(MHmask)   
        maskecmh = None
        if 遮罩羽化 is not None:
            if 遮罩羽化 > -1:
                maskecmh = mask_ecrgba.filter(ImageFilter.GaussianBlur(遮罩羽化))
        dyzz = pil2tensor(maskecmh)
        maskeccmh = pil2tensor(maskecmh)
        destination = original_image
        source = IMAGEEE
        dyyt = source
        multiplier = 8
        resize_source = True
        mask = dyzz
        destination = destination.clone().movedim(-1, 1)
        source=source.clone().movedim(-1, 1)
        source = source.to(destination.device)
        if resize_source:
            source = torch.nn.functional.interpolate(source, size=(destination.shape[2], destination.shape[3]), mode="bilinear")

        source = comfy.utils.repeat_to_batch_size(source, destination.shape[0])
        x=0
        y=0
        x = int(x)
        y = int(y)  
        x = max(-source.shape[3] * multiplier, min(x, destination.shape[3] * multiplier))
        y = max(-source.shape[2] * multiplier, min(y, destination.shape[2] * multiplier))

        left, top = (x // multiplier, y // multiplier)
        right, bottom = (left + source.shape[3], top + source.shape[2],)

        if mask is None:
            mask = torch.ones_like(source)
        else:
            mask = mask.to(destination.device, copy=True)
            mask = torch.nn.functional.interpolate(mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])), size=(source.shape[2], source.shape[3]), mode="bilinear")
            mask = comfy.utils.repeat_to_batch_size(mask, source.shape[0])
        visible_width, visible_height = (destination.shape[3] - left + min(0, x), destination.shape[2] - top + min(0, y),)

        mask = mask[:, :, :visible_height, :visible_width]
        inverse_mask = torch.ones_like(mask) - mask

        source_portion = mask * source[:, :, :visible_height, :visible_width]
        destination_portion = inverse_mask  * destination[:, :, top:bottom, left:right]

        destination[:, :, top:bottom, left:right] = source_portion + destination_portion
        zztx = destination.movedim(1, -1)
        return zztx,dyzz,dyyt


    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, image, vae, mask, 遮罩延展=6, 重绘模式="填充", denoise=1.0, 仅局部重绘=False, 重绘区域扩展=0, 局部重绘大小=0, 遮罩羽化=1, TEXT="2🐕出品，必出精品" ):
        original_image = image
        hqccimage = tensor2pil(image)
        sfmask = tensor2pil(mask)
        sfhmask = sfmask.resize(hqccimage.size, Image.LANCZOS)
        mask = pil2tensor(sfhmask)
        
        MHmask = mask
        
        if 仅局部重绘:
            image, mask, crop_coords,bytx, byzz = self.mask_crop(image, mask, 重绘区域扩展, 局部重绘大小)
            latent_image, _ = self.encode(vae, image, mask, 遮罩延展, 重绘模式)
            samples = common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
            decoded_image = vae.decode(samples[0]["samples"])
            final_image,dyzz,dyyt = self.paste_cropped_image_with_mask(original_image, decoded_image, crop_coords, mask, MHmask, 遮罩羽化)
            return (samples[0], final_image,decoded_image,dyzz)
        else:
            bytx, byzz, crop_coords,image, mask = self.mask_crop(image, mask, 重绘区域扩展, 局部重绘大小)
            latent_image, _ = self.encode(vae, image, mask, 遮罩延展, 重绘模式)
            samples = common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
            decoded_image = vae.decode(samples[0]["samples"])
            
            mask_ecrgba = tensor2pil(mask)   
            
            maskecmh = None
            if 遮罩羽化 is not None:
                if 遮罩羽化 > -1:
                    maskecmh = mask_ecrgba.filter(ImageFilter.GaussianBlur(遮罩羽化))
            dyzz = pil2tensor(maskecmh)
            maskeccmh = pil2tensor(maskecmh)
            mask = maskeccmh
            destination = original_image
            source = decoded_image       
            multiplier = 8
            resize_source = True
            mask = dyzz
            destination = destination.clone().movedim(-1, 1)
            source=source.clone().movedim(-1, 1)
            source = source.to(destination.device)
            if resize_source:
                source = torch.nn.functional.interpolate(source, size=(destination.shape[2], destination.shape[3]), mode="bilinear")

            source = comfy.utils.repeat_to_batch_size(source, destination.shape[0])
            x=0
            y=0
            x = int(x)
            y = int(y)  
            x = max(-source.shape[3] * multiplier, min(x, destination.shape[3] * multiplier))
            y = max(-source.shape[2] * multiplier, min(y, destination.shape[2] * multiplier))

            left, top = (x // multiplier, y // multiplier)
            right, bottom = (left + source.shape[3], top + source.shape[2],)

            if mask is None:
                mask = torch.ones_like(source)
            else:
                mask = mask.to(destination.device, copy=True)
                mask = torch.nn.functional.interpolate(mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])), size=(source.shape[2], source.shape[3]), mode="bilinear")
                mask = comfy.utils.repeat_to_batch_size(mask, source.shape[0])
            visible_width, visible_height = (destination.shape[3] - left + min(0, x), destination.shape[2] - top + min(0, y),)
            mask = mask[:, :, :visible_height, :visible_width]
            inverse_mask = torch.ones_like(mask) - mask
            source_portion = mask * source[:, :, :visible_height, :visible_width]
            destination_portion = inverse_mask  * destination[:, :, top:bottom, left:right]
            destination[:, :, top:bottom, left:right] = source_portion + destination_portion
            zztx = destination.movedim(1, -1)
            return (samples[0], zztx, decoded_image, dyzz)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用