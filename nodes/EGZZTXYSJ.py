import importlib.util
import os
from pathlib import Path
current_file_path = Path(__file__).resolve()
current_directory = current_file_path.parent
folder_paths_directory = current_directory.parent.parent.parent / "folder_paths.py"
spec = importlib.util.spec_from_file_location("folder_paths", str(folder_paths_directory))
folder_paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(folder_paths)
from folder_paths import *
from PIL import Image, ImageOps, ImageSequence, PngImagePlugin
from PIL.ExifTags import TAGS
import numpy as np
import torch
import json
import hashlib

class EGTXFT:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True}),
                     "load_alpha": (["RGB", "RGBA"], {"default": "RGB", "widget": "select"}),}
                }

    CATEGORY = "2🐕/图像"

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    FUNCTION = "load_image"
    def get_metadata_text(self, img):
        pnginfo_data = img.info
        if not pnginfo_data:
            return "No metadata found in the image."
        metadata_text = ""
        for key, value in pnginfo_data.items():
            try:
                if not isinstance(value, (str, bytes, bytearray)):
                    value = str(value)
                value = json.loads(value)
                if isinstance(value, dict):
                    value = json.dumps(value, indent=4)
            except (json.JSONDecodeError, TypeError):
                pass
            metadata_text += f"{key}: {value}\n"
        return metadata_text.strip()
    def load_image(self, image, load_alpha):
        image_path = folder_paths.get_annotated_filepath(image)
        img = Image.open(image_path)
        metadata_text = self.get_metadata_text(img)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            if load_alpha == "RGBA" and 'A' in i.getbands():
                image = i.convert("RGBA")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
            else:
                image = i.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.ones((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))
        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]
        return (output_image, output_mask, metadata_text)
    

    @classmethod
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
