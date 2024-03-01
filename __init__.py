from .nodes.egbdfy import EGBDAPINode
from .nodes.egcchq import EGTXCCHQ
from .nodes.egcgysqy import EGSCQYQBQYNode
from .nodes.egcjpjnode import EGCJPJNode
from .nodes.egjfzz import EGJFZZSC
from .nodes.egjxfz import EGJXFZNODE
from .nodes.egryqh import EGRYQHNode
from .nodes.egszqh import EGXZQHNode
from .nodes.egtjtxsy import EGCPSYTJNode
from .nodes.egtscdscjnode import EGTSCDSCJLNode
from .nodes.egtscdsdgnode import EGTSCDSDGLNode
from .nodes.egtscdsfgnode import EGTSCDSFGLNode
from .nodes.egtscdsjtnode import EGTSCDSJTLNode
from .nodes.egtscdsqtnode import EGTSCDSQTLNode
from .nodes.egtscdsrwnode import EGTSCDSRWLNode
from .nodes.egtscdssjdiy import EGSJNode
from .nodes.egtscdswpnode import EGTSCDSWPLNode
from .nodes.egtscdszlnode import EGTSCDSZLLNode
from .nodes.egtscmb import EGTSCMBGLNode
from .nodes.egtxljbc import EGTXBCLJBCNode
from .nodes.egwbpj import EGWBRYPJ
from .nodes.egwbsjpj import EGWBSJPJ
from .nodes.egysbhd import EGSCQYBHDQYYNode
from .nodes.egysblld import EGYSQYBLLDNode
from .nodes.egysqyld import EGYSQYBBLLDNode
from .nodes.egyssxqy import EGSCQSXQYNode
from .nodes.egzzbsyh import EGZZBSYH
from .nodes.egzzcjnode import EGTXZZCJNode
from .nodes.egzzhsyh import EGZZHSYH
from .nodes.egzzhtkz import EGZZKZHTNODE
from .nodes.egzzkzyh import EGZZSSKZNODE
from .nodes.egzzmhnode import EGZZBYYHNode
from .nodes.egwzsytj import EGYSZTNode
from .nodes.egwbksh import EGWBKSH

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "EG_FX_BDAPI": EGBDAPINode,
    "EG_TX_CCHQ": EGTXCCHQ,
    "EG_SCQY_QBQY": EGSCQYQBQYNode,
    "EG_TX_CJPJ": EGCJPJNode,
    "EG_JF_ZZSC": EGJFZZSC,
    "EG_JXFZ_node": EGJXFZNODE,
    "EG_WXZ_QH": EGRYQHNode,
    "EG_XZ_QH": EGXZQHNode,
    "EG_CPSYTJ": EGCPSYTJNode,
    "EG_TSCDS_CJ": EGTSCDSCJLNode,
    "EG_TSCDS_DG": EGTSCDSDGLNode,
    "EG_TSCDS_FG": EGTSCDSFGLNode,
    "EG_TSCDS_JT": EGTSCDSJTLNode,
    "EG_TSCDS_QT": EGTSCDSQTLNode,
    "EG_TSCDS_RW": EGTSCDSRWLNode,
    "EG_SJ" : EGSJNode,
    "EG_TSCDS_WP": EGTSCDSWPLNode,
    "EG_TSCDS_ZL": EGTSCDSZLLNode,
    "EG_TSCMB_GL": EGTSCMBGLNode,
    "EG_TX_LJBC": EGTXBCLJBCNode,
    "EG_TC_Node": EGWBRYPJ,
    "EG_SJPJ_Node" : EGWBSJPJ,
    "EG_SCQY_BHDQY": EGSCQYBHDQYYNode,
    "EG_YSQY_BLLD": EGYSQYBLLDNode,
    "EG_YSQY_BBLLD": EGYSQYBBLLDNode,
    "EG_SCQY_SXQY": EGSCQSXQYNode,
    "EG_ZZ_BSYH": EGZZBSYH,
    "ER_TX_ZZCJ": EGTXZZCJNode,
    "EG_ZZ_HSYH": EGZZHSYH,
    "EG_ZZKZ_HT_node": EGZZKZHTNODE,
    "EG_ZZ_SSKZ": EGZZSSKZNODE,
    "EG_ZZ_BYYH": EGZZBYYHNode,
    "EG-YSZT-ZT" : EGYSZTNode,
    "EG_WB_KSH": EGWBKSH,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "EG_FX_BDAPI" : "2🐕百度API翻译",
    "EG_TX_CCHQ" : "2🐕图像尺寸获取",
    "EG_SCQY_QBQY" : "2🐕常规颜色迁移",
    "EG_TX_CJPJ" : "2🐕图像裁剪数据拼接",
    "EG_JF_ZZSC" : "2🐕接缝遮罩生成器",
    "EG_JXFZ_node" : "2🐕图像镜像翻转",
    "EG_WXZ_QH" : "2🐕无限制递归切换",
    "EG_XZ_QH" : "2🐕按数字选择切换",
    "EG_CPSYTJ" : "2🐕添加成品水印图像",
    "EG_TSCDS_CJ" : "2🐕提示词大师场景类",
    "EG_TSCDS_DG" : "2🐕提示词大师灯光类",
    "EG_TSCDS_FG" : "2🐕提示词大师风格类",
    "EG_TSCDS_JT" : "2🐕提示词大师镜头类",
    "EG_TSCDS_QT" : "2🐕提示词大师其它类",
    "EG_TSCDS_RW" : "2🐕提示词大师人物类",
    "EG_SJ" : "2🐕任选种类随机提示词",
    "EG_TSCDS_WP" : "2🐕提示词大师物品类",
    "EG_TSCDS_ZL" : "2🐕提示词大师质量类",
    "EG_TSCMB_GL" : "2🐕提示词模板管理大师",
    "EG_TX_LJBC" : "2🐕指定图像保存路径",
    "EG_TC_Node" : "2🐕文本任意拼接",
    "EG_SJPJ_Node" : "2🐕文本随机拼接",
    "EG_SCQY_BHDQY" : "2🐕图像饱和度迁移",
    "EG_YSQY_BLLD" : "2🐕图像迁移保留亮度",
    "EG_YSQY_BBLLD" : "2🐕图像迁移亮度",
    "EG_SCQY_SXQY" : "2🐕图像色相迁移",
    "EG_ZZ_BSYH" : "2🐕遮罩白色区域边缘模糊羽化",
    "ER_TX_ZZCJ" : "2🐕图像遮罩区域裁剪",
    "EG_ZZ_HSYH" : "2🐕遮罩黑色区域边缘模糊羽化",
    "EG_ZZKZ_HT_node" : "2🐕遮罩滑条扩展收缩",
    "EG_ZZ_SSKZ" : "2🐕遮罩扩展收缩",
    "EG_ZZ_BYYH" : "2🐕遮罩边缘模糊羽化",
    "EG-YSZT-ZT" : "2🐕文字水印添加",
    "EG_WB_KSH": "2🐕显示文本",
}
