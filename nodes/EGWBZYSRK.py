import torch
class EGZYWBKNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "自由输入": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            }
        }
    RETURN_TYPES = ("INT", "FLOAT", "STRING")
    RETURN_NAMES = ("整数", "浮点", "文本")
    FUNCTION = "convert_number_types"
    CATEGORY = "2🐕/文本"
    def convert_number_types(self, 自由输入):
        try:
            float_num = float(自由输入)
            int_num = int(float_num)
            str_num = 自由输入
        except ValueError:
            return (None, None, 自由输入)
        return (int_num, float_num, str_num)
# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
