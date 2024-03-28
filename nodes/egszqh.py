NAMESPACE='2🐕按数字选择切换'

def is_context_empty(ctx):
  """Checks if the provided ctx is None or contains just None values."""
  return not ctx or all(v is None for v in ctx.values())

def get_category(sub_dirs = None):
    if sub_dirs is None:
        return NAMESPACE
    else:
        return "{}/utils".format(NAMESPACE)

def get_name(name):
    return '{} ({})'.format(name, NAMESPACE)

class AnyType(str):
  """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

  def __ne__(self, __value: object) -> bool:
    return False


any_type = AnyType("*")


def is_none(value):
  """Checks if a value is none. Pulled out in case we want to expand what 'None' means."""
  if value is not None:
    if isinstance(value, dict) and 'model' in value and 'clip' in value:
      return is_context_empty(value)
  return value is None


class EGXZQHNode:
  """The any switch. """

  NAME = get_name("选择输出")
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
        "选择": (["1", "2", "3", "4", "5", "6"],)
      },
    }

  RETURN_TYPES = (any_type,)
  RETURN_NAMES = ('输出',)
  FUNCTION = "switch"
  CATEGORY = "2🐕/选择"

  def switch(self, 输入01=None, 输入02=None, 输入03=None, 输入04=None, 输入05=None, 输入06=None, 选择=None):
    """Chooses the item to output based on the user's selection."""
    if 选择 is not None:
        if 选择 == "1":
            return (输入01,)
        elif 选择 == "2":
            return (输入02,)
        elif 选择 == "3":
            return (输入03,)
        elif 选择 == "4":
            return (输入04,)
        elif 选择 == "5":
            return (输入05,)
        elif 选择 == "6":
            return (输入06,)
        else:
            return (None,)


# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用
