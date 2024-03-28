import json
import os

class EGTSCMBGLNode:
    JSON_FILE_PATH = '../json/egtscglds.json'  
    @classmethod
    def load_options(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, cls.JSON_FILE_PATH)
        directory = os.path.dirname(json_file_path)
        
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                try:
                    cls.options = json.load(f)
                except json.JSONDecodeError:
                    print("模板文件格式错误，将为你创建一个新的模板文件。")
                    cls.options = {}
        else:
            print("模板文件不存在，将为你创建一个新的模板文件。")
            cls.options = {}
            cls.save_options()
    @classmethod
    def save_options(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, cls.JSON_FILE_PATH)
        directory = os.path.dirname(json_file_path)
        
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(cls.options, f, ensure_ascii=False, indent=4)

    @classmethod
    def INPUT_TYPES(cls):
        cls.load_options()  
        keys_list = list(cls.options.keys())  
        default_key = keys_list[0] if keys_list else '无'  
        return {
            "optional": {
                "读取模板": (keys_list, {"default": default_key}),
                "新建模板名": ("STRING", {"default": "请输入名称"}),
                "新建提示词内容": ("STRING", {"default": "请输入内容"}),
                "功能选择": (["读取模板", "新建模板", "删除读取模板"], {"default": "读取模板"}),
            },
            "required": {
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("文本",)
    FUNCTION = "process_action"
    CATEGORY = "2🐕/提示词大师/模板管理"

    def process_action(self, 读取模板='无', 新建模板名='请输入名称', 新建提示词内容='请输入内容', 功能选择='读取模板'):
        self.load_options()
        if 功能选择 == '新建模板':
            print("2🐕已为你保存成功,更多SD教程尽在B站@灵仙儿和二狗子")
            self.options[新建模板名] = 新建提示词内容
            self.save_options()
            
            self.load_options()
            return ("2🐕已为你保存成功,更多SD教程尽在B站@灵仙儿和二狗子",)
        elif 功能选择 == '删除读取模板':
            if 读取模板 in self.options:
                print("2🐕已为你删除成功,更多SD教程尽在B站@灵仙儿和二狗子")
                del self.options[读取模板]
                self.save_options()
                
                self.load_options()
                return ("2🐕已为你删除成功,更多SD教程尽在B站@灵仙儿和二狗子",)
            else:
                return ("2🐕已为你检查该模板不存在,更多SD教程尽在B站@灵仙儿和二狗子",)
                print("2🐕为你已检查该模板不存在,更多SD教程尽在B站@灵仙儿和二狗子")
        elif 功能选择 == '读取模板':
            if not 读取模板 or 读取模板 not in self.options:
                print("2🐕已为你检查该模板不存在,更多SD教程尽在B站@灵仙儿和二狗子")
                return ("2🐕已为你检查该模板不存在,更多SD教程尽在B站@灵仙儿和二狗子",)
            else:
                
                print(f"2🐕已为你成功读取模板，模板内容如下,更多SD教程尽在B站@灵仙儿和二狗子：")
                print(self.options[读取模板])
                
                return (self.options[读取模板],)
        else:
            return ("2🐕不清楚你的神操作,更多SD教程尽在B站@灵仙儿和二狗子",)
            print("2🐕不清楚你的神操作,更多SD教程尽在B站@灵仙儿和二狗子")






# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
