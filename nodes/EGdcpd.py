class FindFirstMatchNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入文本": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "查找单词": ("STRING", {
                    "multiline": True,
                    "default": "man,woman,girl"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("匹配单词",)
    FUNCTION = "find_first_match"
    CATEGORY = "2🐕/文本"
    NAME = "查找首个匹配词"

    def find_first_match(self, 输入文本, 查找单词):
        word_list = [word.strip() for word in 查找单词.split(',')]
        first_positions = {}
        for word in word_list:
            pos = 输入文本.find(word)
            if pos != -1:
                first_positions[word] = pos
        if not first_positions:
            return ("",)
        first_match = min(first_positions.items(), key=lambda x: x[1])[0]
        return (first_match,)

NODE_CLASS_MAPPINGS = {
    "FindFirstMatchWord": FindFirstMatchNode
}
