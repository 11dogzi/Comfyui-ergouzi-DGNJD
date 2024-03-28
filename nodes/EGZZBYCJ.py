from PIL import Image
import torch
import numpy as np
import cv2

def tensor_to_pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil_to_tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class EGZZRH:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
            }
        }
    
    RETURN_TYPES = ('MASK', 'IMAGE')  # Both outputs are tensors
    FUNCTION = "mask_edge_detection"
    CATEGORY = "2🐕/遮罩/细化处理"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False, False)  # Both outputs are single items, not lists
    def mask_edge_detection(self, mask):
        print('Edge Detection', mask.shape)
        mask_pil = tensor_to_pil(mask)
        
        edges = cv2.Canny(np.array(mask_pil), 100, 200)
        edges_pil = Image.fromarray(edges)
        
        edges_tensor = pil_to_tensor(edges_pil)
        
        return (edges_tensor, edges_tensor)  # Return mask tensor and image tensor



# 本套插件版权所属B站@灵仙儿和二狗子，仅供学习交流使用，未经授权禁止一切商业性质使用


