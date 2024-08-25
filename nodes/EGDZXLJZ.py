import os
from PIL import Image
import numpy as np
import torch

class SequentialImageLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_folder": ("STRING", {}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ('IMAGE', 'STRING',)
    OUTPUT_IS_LIST = (True, True)
    FUNCTION = "get_images"
    CATEGORY = "2🐕/训练"

    def __init__(self):
        self.image_filenames = []
        self.images_cache = {}
        self.last_input_folder = None

    def load_image_filenames(self, input_folder):
        if input_folder != self.last_input_folder:
            self.image_filenames = []
            self.images_cache.clear()
            self.last_input_folder = input_folder
            
        self.image_filenames = [
            filename for filename in os.listdir(input_folder)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ]

    def get_images(self, input_folder, seed):
        try:
            if os.path.isdir(input_folder):
                if not self.image_filenames or input_folder != self.last_input_folder:
                    self.load_image_filenames(input_folder)

                if not self.image_filenames:
                    raise RuntimeError("No images found in the specified folder.")

                images = []
                filename_prefixes = []

                for selected_filename in self.image_filenames:
                    img_path = os.path.join(input_folder, selected_filename)

                    if selected_filename not in self.images_cache:
                        image = Image.open(img_path).convert('RGBA')
                        self.images_cache[selected_filename] = image
                    else:
                        image = self.images_cache[selected_filename]

                    image_np = np.array(image).astype(np.float32) / 255.0
                    image_tensor = torch.from_numpy(image_np)[None, :, :, :]
                    images.append(image_tensor)
                    filename_prefixes.append(os.path.splitext(selected_filename)[0])

                return (images, filename_prefixes)

        except Exception as e:
            return None, None

