import random
class EGRandomWordNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "单词列表": ("STRING", {
                    "multiline": True,
                    "default": "word1,word2,word3"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": -1125899906842624,
                    "max": 1125899906842624
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("随机单词",)
    FUNCTION = "get_random_word"
    CATEGORY = "2🐕/文本"
    NAME = "随机选词"

    def get_random_word(self, 单词列表, seed):
        random.seed(seed)
        words = [word.strip() for word in 单词列表.split(',') if word.strip()]
        if not words:
            return ("",)
        selected_word = random.choice(words)
        
        return (selected_word,)
NODE_CLASS_MAPPINGS = {
    "RandomWord": EGRandomWordNode
}
