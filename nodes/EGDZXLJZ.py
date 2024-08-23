import os
from PIL import Image
import numpy as np
import torch
import tkinter as tk
from tkinter import messagebox

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
    RETURN_NAMES = ('image_tensor', 'filename_prefix',)
    FUNCTION = "get_image"
    CATEGORY = "2🐕/训练"

    def __init__(self):
        self.current_index = 0
        self.image_filenames = []
        self.images_cache = {}
        self.last_input_folder = None

    def load_image_filenames(self, input_folder):
        if input_folder != self.last_input_folder:
            self.image_filenames = []
            self.images_cache.clear()
            self.current_index = 0
            self.last_input_folder = input_folder
            
        self.image_filenames = [
            filename for filename in os.listdir(input_folder)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ]

    def get_image(self, input_folder, seed):
        try:
            if os.path.isdir(input_folder):
                if not self.image_filenames or input_folder != self.last_input_folder:
                    self.load_image_filenames(input_folder)

                if self.current_index >= len(self.image_filenames):
                    self.current_index = 0
                    root = tk.Tk()
                    root.withdraw()
                    root.attributes('-topmost', True)  # 确保窗口总是在最前面

                    def on_continue():
                        root.destroy()

                    def on_end():
                        root.destroy()
                        raise RuntimeError("已取消当前任务")

                    if messagebox.askokcancel(
                        "Processing Complete",
                        "2狗提醒最帅的你，本次文件夹处理已完成，是否继续循环"
                    ):
                        on_continue()
                    else:
                        on_end()

                selected_filename = self.image_filenames[self.current_index]
                img_path = os.path.join(input_folder, selected_filename)

                if selected_filename not in self.images_cache:
                    image = Image.open(img_path).convert('RGBA')
                    self.images_cache[selected_filename] = image
                else:
                    image = self.images_cache[selected_filename]

                self.current_index += 1

                image_rgba = image
                image_np = np.array(image_rgba).astype(np.float32) / 255.0
                image_tensor = torch.from_numpy(image_np)[None, :, :, :]
                filename_prefix = os.path.splitext(selected_filename)[0]
                return (image_tensor, filename_prefix)

        except Exception as e:
            print(f"Error processing images, please reset the node: {e}")
        return None, None
