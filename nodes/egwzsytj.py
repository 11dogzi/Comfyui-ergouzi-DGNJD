import numpy as np
import torch
import os
from PIL import Image, ImageDraw, ImageOps, ImageFont

颜色_mapping = {
    "白色": (255, 255, 255),
    "黑色": (0, 0, 0),
    "红色": (255, 0, 0),
    "绿色": (0, 255, 0),
    "蓝色": (0, 0, 255),
    "黄色": (255, 255, 0),
    "青色": (0, 255, 255),
    "品红": (255, 0, 255),
    "橙色": (255, 165, 0),
    "紫色": (128, 0, 128),
    "粉色": (255, 192, 203),
    "棕色": (160, 85, 15),
    "灰色": (128, 128, 128),
    "浅灰": (211, 211, 211),
    "深灰": (102, 102, 102),
    "橄榄绿": (128, 128, 0),
    "酸橙色": (0, 128, 0),
    "鸭绿色": (0, 128, 128),
    "海军蓝": (0, 0, 128),
    "紫褐色": (128, 0, 0),
    "紫红色": (255, 0, 128),
    "浅绿色": (0, 255, 128),
    "银色": (192, 192, 192),
    "金色": (255, 215, 0),
    "青绿色": (64, 224, 208),
    "淡紫色": (230, 230, 250),
    "蓝紫色": (238, 130, 238),
    "珊瑚红": (255, 127, 80),
    "靛蓝色": (75, 0, 130),    
}

COLORS = ["自定义", "白色", "黑色", "红色", "绿色", "蓝色", "黄色",
          "青色", "品红", "橙色", "紫色", "粉色", "棕色", "灰色",
          "浅灰", "深灰", "橄榄绿", "酸橙色", "鸭绿色", "海军蓝", "紫褐色",
          "紫红色", "浅绿色", "银色", "金色", "青绿色", "淡紫色",
          "蓝紫色", "珊瑚红", "靛蓝色"]

ALIGN_OPTIONS = ["居中", "上", "下"]                 
ROTATE_OPTIONS = ["按文本 居中", "按图像 居中"]
JUSTIFY_OPTIONS = ["居中", "左", "右"]
PERSPECTIVE_OPTIONS = ["上", "下", "左", "右"]

def 竖向初始位置_text(竖向初始位置, img_height, text_height, text_pos_y, margins):
    if 竖向初始位置 == "居中":
        text_plot_y = img_height / 2 - text_height / 2 + text_pos_y
    elif 竖向初始位置 == "上":
        text_plot_y = 0 + text_pos_y
    elif 竖向初始位置 == "下":
        text_plot_y = img_height - text_height + text_pos_y
    return text_plot_y

def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height

def 横向初始位置_text(横向初始位置, img_width, line_width, margins):
    if 横向初始位置 == "左":
        text_plot_x = 0 + margins
    elif 横向初始位置 == "右":
        text_plot_x = img_width - line_width - margins
    elif 横向初始位置 == "居中":
        text_plot_x = img_width/2 - line_width/2 + margins
    return text_plot_x

def 六进制_to_rgb(六进制_颜色):
    六进制_颜色 = 六进制_颜色.lstrip('#')  # Remove the '#' character, if present
    r = int(六进制_颜色[0:2], 16)
    g = int(六进制_颜色[2:4], 16)
    b = int(六进制_颜色[4:6], 16)
    return (r, g, b)

def get_颜色_values(颜色, 颜色_六进制, 颜色_mapping):
    
    if 颜色 == "自定义":
        颜色_rgb = 六进制_to_rgb(颜色_六进制)
    else:
        颜色_rgb = 颜色_mapping.get(颜色, (0, 0, 0))  # Default to 黑色 if the 颜色 is not found
    return 颜色_rgb

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)) 

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

def draw_masked_text(text_mask, text,
                     font_name, font_size, font_opacity,
                     margins, 行间距,
                     横向偏移, 竖向偏移,
                     竖向初始位置, 横向初始位置,
                     rotation_angle, rotation_options):
    
    text_mask = Image.new('RGBA', text_mask.size, (255, 255, 255, 0))  # 创建一个带有Alpha通道的白色图像
    draw = ImageDraw.Draw(text_mask)
    
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(resolved_font_path, size=font_size)
    
    image_width = text_mask.size[0]
    
    image_height = text_mask.size[1]
    
    text_lines = text.split('\n')
    
    max_text_width = 0
    max_text_height = 0
    for line in text_lines:
        w, h = draw.textsize(line, font=font)
        max_text_width = max(max_text_width, w)
        max_text_height = max(max_text_height, h + 行间距)
    
    text_x = 横向偏移
    text_y = 竖向偏移
    
    text_plot_y = 竖向初始位置_text(竖向初始位置, image_width, max_text_height * len(text_lines), text_y, margins)
    text_plot_x = 横向初始位置_text(横向初始位置, image_width, max_text_width, margins) + text_x
    
    for line in text_lines:
        w, h = draw.textsize(line, font=font)
        current_y = text_plot_y
        draw.text((text_plot_x, current_y), line, font=font, fill=(255, 255, 255, font_opacity))
        text_plot_y += h + 行间距
    
    if rotation_angle != 0:
        if rotation_options == "按文本 居中":
            rotated_text_mask = text_mask.rotate(rotation_angle, center=(text_x + max_text_width / 2, text_y / 2))
        elif rotation_options == "按图像 居中":    
            rotated_text_mask = text_mask.rotate(rotation_angle, center=(image_width / 2, image_height / 2))
    else:
        rotated_text_mask = text_mask
    
    return rotated_text_mask

class EGYSZTNode:
    @classmethod
    def INPUT_TYPES(s):
        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        
        return {"required": {
                    "背景生成宽度": ("INT", {"default": 512, "min": 64, "max": 20000}),
                    "背景生成高度": ("INT", {"default": 512, "min": 64, "max": 20000}),
                    "text": ("STRING", {"multiline": True, "default": "请输入需要生成的水印文字,本插件字体均为网络公开资源字体，仅供学习交流使用，如需商用请自行更换商用字体，字体存放路径为Comfyui-ergouzi-DGNJD\fonts文件夹，更多SD教程尽在B站灵仙儿和二狗子🐕"}),
                    "选择字体": (file_list,),
                    "字体大小": ("INT", {"default": 50, "min": 1, "max": 1024}),
                    "字体颜色": (COLORS,),
                    "背景颜色": (COLORS,),
                    "竖向初始位置": (ALIGN_OPTIONS,),
                    "横向初始位置": (JUSTIFY_OPTIONS,),
                    "文字页边距": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                    "行间距": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                    "横向偏移": ("INT", {"default": 0, "min": -20000, "max": 20000}),
                    "竖向偏移": ("INT", {"default": 0, "min": -20000, "max": 20000}),
                    "旋转角度": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                    "旋转中心": (ROTATE_OPTIONS,),
                    "字体透明度": ("INT", {
                        "default": 255, 
                        "min": 0, 
                        "max": 255, 
                        "display": "slider"
                     }),
                },
                "optional": {
                    "字体_颜色_六进制": ("STRING", {"multiline": False, "default": "#000000"}),
                    "背景_颜色_六进制": ("STRING", {"multiline": False, "default": "#000000"}),
                    "输入原图": ("IMAGE", {}),
                }
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("输出图像",)
    FUNCTION = "draw_text"
    CATEGORY = "2🐕/水印大师"
    def draw_text(self, 背景生成宽度, 背景生成高度, text,
                  选择字体, 字体大小, 字体颜色,
                  背景颜色,
                  文字页边距, 行间距,
                  横向偏移, 竖向偏移,
                  竖向初始位置, 横向初始位置,
                  旋转角度, 旋转中心,
                  字体_颜色_六进制='#000000', 背景_颜色_六进制='#000000', 输入原图=None,
                  字体透明度=255):
        font_opacity = 字体透明度
        text_颜色 = get_颜色_values(字体颜色, 字体_颜色_六进制, 颜色_mapping)
        bg_颜色 = get_颜色_values(背景颜色, 背景_颜色_六进制, 颜色_mapping)
        if 输入原图 is not None:
            back_输入原图 = tensor2pil(输入原图)  # Assuming tensor2pil converts a tensor to PIL Image
            size = back_输入原图.size
        else:
            size = (背景生成宽度, 背景生成高度)
            back_输入原图 = Image.new('RGB', size, bg_颜色)
        text_输入原图 = Image.new('RGB', size, text_颜色)
        text_mask = Image.new('L', back_输入原图.size)
        rotated_text_mask = draw_masked_text(text_mask, text, 选择字体, 字体大小, font_opacity,
                                             文字页边距, 行间距,  # 确保传递了行间距参数
                                             横向偏移, 竖向偏移,
                                             竖向初始位置, 横向初始位置,
                                             旋转角度, 旋转中心)
        输入原图_out = Image.composite(text_输入原图, back_输入原图, rotated_text_mask)
        return (pil2tensor(输入原图_out),)
NODE_CLASS_MAPPINGS = { "EG-YSZT-ZT" : EGYSZTNode }
NODE_DISPLAY_NAME_MAPPINGS = { "EG-YSZT-ZT" : "2🐕文字水印添加" }


