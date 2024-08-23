import os

class SaveTextToFile:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"multiline": False, "default": ""}),
                "filename_prefix": ("STRING", {"multiline": False, "default": "output"}),
                "text": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_info",)
    FUNCTION = "save_text"

    CATEGORY = "2🐕/训练"

    def save_text(self, folder, filename_prefix, text):
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, f"{filename_prefix}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        file_info = (
            f"保存的文件夹路径：{folder}\n"
            f"保存的txt文件名称：{filename_prefix}.txt\n"
            f"保存的文件内容：{text}"
        )
        
        print(f"2🐕已成功为你保存文本文件{file_path}，更多免费教程尽在B站@灵仙儿和二狗子")
        return (file_info,)
