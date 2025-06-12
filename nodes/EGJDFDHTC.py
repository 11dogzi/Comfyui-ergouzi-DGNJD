class EGRYHTC:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "浮点权重": ("FLOAT", {
                        "default": 0,
                        "min": 1,
                        "max": 10,
                        "step":1,
                        "display": "slider"
                    }),
                },
                "optional": {}
        }
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "run"
    CATEGORY = "2🐕/数字"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)
    def run(self, 浮点权重):
        scaled_number = 浮点权重
        return (scaled_number,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
