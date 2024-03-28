import json
import os
import random

class EGTSCDSWPLNode:
    JSON_FILE_PATH = 'options.json'
    CATEGORY_KEYS = ['物品', '花卉', '食物', '印刷材质', '物理材质']

    def __init__(self):
        self.load_json()
    def load_json(self):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        
        json_dir = os.path.join(parent_dir, 'json')
        
        json_file_path = os.path.join(json_dir, self.JSON_FILE_PATH)
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                self.options = json.load(f)
        except Exception as e:
            print(f"读取JSON文件时出错: {e}")  

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                **cls.get_input_types_from_keys(cls.CATEGORY_KEYS),
                "是否随机": (["是", "否"], {"default": "否"}),
                "seed": ("INT", {"default": 0,"min": -1125899906842624,"max": 1125899906842624}),
            }
        }

    @staticmethod
    def get_input_types_from_keys(keys):
        input_types = {}
        for key in keys:
            input_types[key] = (tuple(EGTSCDSWPLNode.get_options_keys(key)), {"default": "无"})
            input_types[f"{key}权重"] = ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2, "step": 0.1, "display": "slider"})
        return input_types

    @staticmethod
    def get_options_keys(key):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        json_dir = os.path.join(parent_dir, 'json')  
        json_file_path = os.path.join(json_dir, EGTSCDSWPLNode.JSON_FILE_PATH)
    
        with open(json_file_path, 'r', encoding='utf-8') as f:
            options = json.load(f)
            return list(options[key].keys())

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "2🐕/提示词大师/固定类"

    def generate_prompt(self, **kwargs):
        prompt_parts = {}
        for key in self.CATEGORY_KEYS:
            if key in kwargs and kwargs[key] in self.options[key] and kwargs[key] != "无":
                weight_key = f"{key}权重"
                weight = kwargs[weight_key] if weight_key in kwargs and kwargs[weight_key] is not None else 1
                if weight != 1:
                    prompt_parts[key] = f"({self.options[key][kwargs[key]]}:{weight:.1f})"
                else:
                    prompt_parts[key] = self.options[key][kwargs[key]]
        
            if kwargs.get("是否随机") == "是":
                可选 = list(self.options[key].keys())
                可选.remove("无")
                随机选择 = random.choice(可选)
                weight_key = f"{key}权重"
                weight = kwargs[weight_key] if weight_key in kwargs and kwargs[weight_key] is not None else 1
                if weight != 1:
                    prompt_parts[key] = f"({self.options[key][随机选择]}:{weight:.1f})"
                else:
                    prompt_parts[key] = self.options[key][随机选择]
        
        prompt_parts = {k: v for k, v in prompt_parts.items() if v}
        prompt = ','.join(prompt_parts.values()).strip()
        prompt += ','
        return (prompt,) if prompt else ('',)








# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
