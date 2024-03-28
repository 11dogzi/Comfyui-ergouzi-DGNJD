import torch
class EGSZCGJS:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入数字1": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "operation": (["+", "-", "x", "÷"], {}),
                "输入数字2": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            }
        }
    RETURN_TYPES = ("INT", "FLOAT", "STRING")
    RETURN_NAMES = ("输出整数", "输出浮点", "输出文本")
    FUNCTION = "compute"
    CATEGORY = "2🐕/数字"
    
    def compute(self, 输入数字1, 输入数字2, operation):
        try:
            输入数字1 = float(输入数字1)
            输入数字2 = float(输入数字2)
        except ValueError:
            return (None, None, "Invalid input. Please enter a number.")
        
        if operation == "+":
            result = 输入数字1 + 输入数字2
        elif operation == "-":
            result = 输入数字1 - 输入数字2
        elif operation == "x":
            result = 输入数字1 * 输入数字2
        elif operation == "÷":
            if 输入数字2 == 0:
                return (None, None, "Cannot divide by zero.")
            result = 输入数字1 / 输入数字2
        else:
            return (None, None, "Invalid operation.")
        
        if result.is_integer():
            输出文本 = str(int(result))
        else:
            输出文本 = str(result)
        
        return (int(result), float(result), 输出文本)
# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
