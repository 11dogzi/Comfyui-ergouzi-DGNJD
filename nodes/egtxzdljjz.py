from PIL import Image, ImageSequence
import numpy as np
import torch
import os
class EGJZRYTX:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {}),
                "fill_color": (["None", "white", "gray", "black"], {}),
                "smooth": ("BOOLEAN", {"default": True})
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }
    RETURN_TYPES = ('IMAGE', 'MASK',)
    FUNCTION = "get_transparent_image"
    CATEGORY = "2🐕/图像"
    
    def get_transparent_image(self, file_path, smooth, seed, fill_color):
        try:
            if os.path.isdir(file_path):
                images = []
                for filename in os.listdir(file_path):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        img_path = os.path.join(file_path, filename)
                        image = Image.open(img_path).convert('RGBA')
                        images.append(image)
                
                if not images:
                    return None, None
                
                target_size = images[0].size
                
                resized_images = []
                for image in images:
                    if image.size != target_size:
                        image = image.resize(target_size, Image.BILINEAR)
                    resized_images.append(image)
                
                batch_images = np.stack([np.array(img) for img in resized_images], axis=0).astype(np.float32) / 255.0
                batch_tensor = torch.from_numpy(batch_images)
                
                mask_tensor = None
                
                return batch_tensor, mask_tensor        
            else:
                file_path = file_path.strip('"')
                image = Image.open(file_path)
                if image is not None:
                    image_rgba = image.convert('RGBA')
                    image_rgba.save(file_path.rsplit('.', 1)[0] + '.png')
            
                    mask = np.array(image_rgba.getchannel('A')).astype(np.float32) / 255.0
                    if smooth:
                        mask = 1.0 - mask
                    mask_tensor = torch.from_numpy(mask)[None, None, :, :]
            
                    if fill_color == 'white':
                        for y in range(image_rgba.height):
                            for x in range(image_rgba.width):
                                if image_rgba.getpixel((x, y))[3] == 0:
                                    image_rgba.putpixel((x, y), (255, 255, 255, 255))
                    elif fill_color == 'gray':
                        for y in range(image_rgba.height):
                            for x in range(image_rgba.width):
                                if image_rgba.getpixel((x, y))[3] == 0:
                                    image_rgba.putpixel((x, y), (128, 128, 128))
                    elif fill_color == 'black':
                        for y in range(image_rgba.height):
                            for x in range(image_rgba.width):
                                if image_rgba.getpixel((x, y))[3] == 0:
                                    image_rgba.putpixel((x, y), (0, 0, 0))
                    elif fill_color == 'None':
                        pass
                    else:
                        raise ValueError("Invalid fill color specified.")
            
                    image_np = np.array(image_rgba).astype(np.float32) / 255.0
                    image_tensor = torch.from_numpy(image_np)[None, :, :, :]
            
                    return (image_tensor, mask_tensor)
            
        except Exception as e:
            print(f"2🐕温馨提示处理图像时出错请重置节点：{e}")
        return None, None




# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
