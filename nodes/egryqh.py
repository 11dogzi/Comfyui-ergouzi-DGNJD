NAMESPACE='2🐕无限制递归切换'

def is_context_empty(ctx):
  return not ctx or all(v is None for v in ctx.values())

def get_category(sub_dirs = None):
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


class EGRYQHNode:

  NAME = get_name("Any Switch")
  CATEGORY = get_category()

  @classmethod
  def INPUT_TYPES(cls):  
    return {
      "required": {},
      "optional": {
        "输入01": (any_type,),
        "输入02": (any_type,),
        "输入03": (any_type,),
        "输入04": (any_type,),
        "输入05": (any_type,),
        "输入06": (any_type,),
      },
    }

  RETURN_TYPES = (any_type,)
  RETURN_NAMES = ('输出',)
  FUNCTION = "switch"
  CATEGORY = "2🐕/选择"

  def switch(self, 输入01=None, 输入02=None, 输入03=None, 输入04=None, 输入05=None,输入06=None):
    any_value = None
    if not is_none(输入01):
      any_value = 输入01
    elif not is_none(输入02):
      any_value = 输入02
    elif not is_none(输入03):
      any_value = 输入03
    elif not is_none(输入04):
      any_value = 输入04
    elif not is_none(输入05):
      any_value = 输入05
    elif not is_none(输入06):
      any_value = 输入06
    return (any_value,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
