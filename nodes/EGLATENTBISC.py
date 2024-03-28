import torch
class Args:
    def __init__(self):
        self.gpu_only = False
args = Args()
def intermediate_device():
    if args.gpu_only:
        return get_torch_device()
    else:
        return torch.device("cpu")
class EGKLATENT:
    选择比例s = {
        "1:1": (1, 1),
        "3:2": (3, 2),
        "16:9": (16, 9),
        "2:3": (2, 3),
        "9:16": (9, 16)
    }

    def __init__(self):
        self.device = intermediate_device()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"width": ("INT", {"default": 512, "min": 16, "max": 4096, "step": 8}),
                             "height": ("INT", {"default": 512, "min": 16, "max": 4096, "step": 8}),
                             "批次": ("INT", {"default": 1, "min": 1, "max": 4096}),
                             "选择比例": (list(s.选择比例s.keys()), {"default": "1:1"}),
                             "启用比例": ("BOOLEAN", {"default": False})
                             }}

    RETURN_TYPES = ("LATENT", "INT", "INT")
    RETURN_NAMES = ('LATENT', 'width', 'height')
    FUNCTION = "generate"
    CATEGORY = "2🐕/Latent"

    def generate(self, width, height, 批次=1, 选择比例="1:1", 启用比例=False):
        if 选择比例 not in self.选择比例s.keys():
            raise ValueError(f"Invalid 选择比例 value: {选择比例}. Valid 选择比例s are: {', '.join(self.选择比例s.keys())}")
        if not 启用比例:
            latent = torch.zeros([批次, 4, int(height // 8), int(width // 8)], device=self.device)
            return ({"samples": latent}, width, height)
        if width == height:
            max_dim = width
            选择比例_width, 选择比例_height = self.选择比例s[选择比例]
            if 选择比例_width >= 选择比例_height:
                width = max_dim
                height = int(max_dim * 选择比例_height / 选择比例_width)
            else:
                height = max_dim
                width = int(max_dim * 选择比例_width / 选择比例_height)
        else:
            max_dim = max(width, height)
            选择比例_width, 选择比例_height = self.选择比例s[选择比例]
            if width == max_dim:
                new_height = int(max_dim * 选择比例_height / 选择比例_width)
                height = new_height
            elif height == max_dim:
                new_width = int(max_dim * 选择比例_width / 选择比例_height)
                width = new_width

        latent = torch.zeros([批次, 4, int(height // 8), int(width // 8)], device=self.device)
        return ({"samples": latent}, width, height)

# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
