class EGXZRYHT:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "选择数量": ("FLOAT", {
                        "default": 1,
                        "min": 1,
                        "max": 6,
                        "step": 1,
                        "display": "slider"
                    }),
                },
                "optional": {}
        }
    RETURN_TYPES = ("INT",)
    FUNCTION = "run"
    CATEGORY = "2🐕/数字"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self, 选择数量):
        # 将浮点数转换为整数
        scaled_number = int(选择数量)
        return (scaled_number,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
