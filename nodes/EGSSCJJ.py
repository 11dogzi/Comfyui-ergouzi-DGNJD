import torch
import random
import json

class EGSSCJJ:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "起始抽奖号": ("INT", {
                    "default": 0,
                    "min": -1000000,
                    "max": 1000000
                }),
                "结束抽奖号": ("INT", {
                    "default": 100,
                    "min": -1000000,
                    "max": 1000000
                }),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ("输出整数", "输出浮点", "输出文本")
    FUNCTION = "generate_random_int"
    CATEGORY = "2🐕/数字"
    
    def generate_random_int(self, 起始抽奖号, 结束抽奖号):
        if 起始抽奖号 > 结束抽奖号:
            起始抽奖号, 结束抽奖号 = 结束抽奖号, 起始抽奖号
        
        result = random.randint(起始抽奖号, 结束抽奖号)        
        return (result, float(result), str(result))
