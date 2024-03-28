import os
import requests
import hashlib
import json
import re
class EGWBRYPJ:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "文本1": ("STRING", {"multiline": True}),
                "文本2": ("STRING", {"multiline": True}),
                "文本3": ("STRING", {"multiline": True}),
                "文本4": ("STRING", {"multiline": True}),
                "文本5": ("STRING", {"multiline": True}),
                "拼接字符": ("STRING", {"default": ""}),
                "排除字符": ("STRING", {"default": ""}),
                "排除单词": ("STRING", {"default": ""})  # 新增排除单词输入
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('concatenated_text',)
    FUNCTION = "concatenate_text"
    CATEGORY = "2🐕/文本"
    
    def concatenate_text(self, 文本1, 文本2, 文本3, 文本4, 文本5, 拼接字符="", 排除字符="", 排除单词="", seed=0):
        """将用户输入的文本拼接后输出字符串结果。"""
        texts = [文本1, 文本2, 文本3, 文本4, 文本5]
                
        concatenated_text = 拼接字符.join(filter(None, texts))
        
        # 处理排除字符
        if 排除字符:
            exclude_chars = 排除字符.split(',')
            exclude_chars = [char.strip() for char in exclude_chars if char.strip()]
            for char in exclude_chars:
                concatenated_text = concatenated_text.replace(char, "")
        
        # 处理排除单词
        if 排除单词:
            exclude_words = 排除单词.split(',')
            exclude_words = [word.strip() for word in exclude_words if word.strip()]
            for word in exclude_words:
                pattern = r'(?<!\w)' + re.escape(word) + r'(?!\w)'
                concatenated_text = re.sub(pattern, '', concatenated_text)
        
        concatenated_text = re.sub(r'(\W)\1+', r'\1', concatenated_text)
        concatenated_text = re.sub(r'^[，,]+', '', concatenated_text)
        concatenated_text = re.sub(r'[，,]+$', '', concatenated_text)
        
        return (concatenated_text,)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
