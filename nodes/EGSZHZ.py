NAMESPACE='2🐕整数浮点字符串格式转换'
def is_context_empty(ctx):
    return not ctx or all(v is None for v in ctx.values())
def get_category(sub_dirs=None):
    if sub_dirs is None:
        return NAMESPACE
    else:
        return "{}/utils".format(NAMESPACE)
def get_name(name):
    return '{} ({})'.format(name, NAMESPACE)
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
any_type = AnyType("*")
def is_none(value):
    if value is not None:
        if isinstance(value, dict) and 'model' in value and 'clip' in value:
            return is_context_empty(value)
    return value is None
def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return None
def convert_to_str(value):
    return str(value)
class EGSSRYZH:
    NAME = get_name("Any Switch")
    CATEGORY = get_category()
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"任意输入": (any_type,)},
            "optional": {},
        }
    RETURN_TYPES = (any_type, any_type, any_type)
    RETURN_NAMES =('整数', '浮点', '文本')
    FUNCTION = "switch"
    CATEGORY = "2🐕/数字"
    def switch(self, 任意输入=None):
        if 任意输入 is None:
            return (None, None, None)
        
        int_output = convert_to_int(任意输入)
        float_output = convert_to_float(任意输入)
        str_output = convert_to_str(任意输入)
        
        return (int_output, float_output, str_output)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
