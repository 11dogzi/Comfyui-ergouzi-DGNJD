import requests
import hashlib
import json

NAMESPACE = '2🐕百度API翻译'
APPID_API_KEY_FILE = 'baidukey.json'

def get_category(sub_dirs=None):
    if sub_dirs is None:
        return NAMESPACE
    else:
        return "{}/{}".format(NAMESPACE, sub_dirs)
def get_name(name):
    return '{} ({})'.format(name, NAMESPACE)
class EGBDAPINode:
    NAME = get_name("翻译")
    CATEGORY = get_category()
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "免费百度API申请网站https://fanyi-api.baidu.com/?ext_channel=Aldtype&fr=pcHeader \n申请后在下方输入APP ID与密钥。\n仅第一次需要输入即可自动保存。\n更多SD教程尽在B站@灵仙儿和二狗子🐕"
                }),
            },
            "optional": {
                "appid": ("STRING", {}),
                "api_key": ("STRING", {}),
                "翻译模式": (["zh-en", "en-zh"],)
            },
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('文本',)
    FUNCTION = "translate"
    CATEGORY = "2🐕/文本"
    def __init__(self, appid=None, api_key=None):
        self.appid = appid
        self.api_key = api_key
        self.load_credentials()
    def load_credentials(self):
        try:
            with open(APPID_API_KEY_FILE, 'r') as f:
                credentials = json.load(f)
                self.appid = credentials.get('appid', self.appid)
                self.api_key = credentials.get('api_key', self.api_key)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error decoding JSON credentials. Using default values.")
    def save_credentials(self):
        with open(APPID_API_KEY_FILE, 'w') as f:
            json.dump({'appid': self.appid, 'api_key': self.api_key}, f)
    def translate(self, text, appid=None, api_key=None, 翻译模式="zh-en"):
        
        if appid:
            self.appid = appid
            self.save_credentials()
        if api_key:
            self.api_key = api_key
            self.save_credentials()
        
        if not self.appid or not self.api_key:
            return ("Translation failed - missing appid or api_key",)
        
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        
        salt = '123456'  
        sign = self.calculate_sign(text, salt, self.appid, self.api_key)
        params = {
            'q': text,
            'appid': self.appid,
            'salt': salt,
            'sign': sign
        }
        
        params['from'], params['to'] = 翻译模式.split('-')
        
        response = requests.get(url, params=params)
        
        print(response.text)
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                
                if "error_code" in response_json:
                    return ("Translation failed - error code: {}".format(response_json["error_code"]),)
                
                translation = response_json["trans_result"][0]["dst"]
                return (translation,)
            except KeyError as e:
                return ("Translation failed - KeyError: {}".format(e),)
        else:
            return ("Translation failed - status code: {}".format(response.status_code),)
    def calculate_sign(self, query, salt, appid, api_key):
        sign = f"{appid}{query}{salt}{api_key}"
        sign = sign.encode('utf-8')
        sign = hashlib.md5(sign).hexdigest()
        return sign


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
