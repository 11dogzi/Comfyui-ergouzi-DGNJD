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
from .nodes.egtxzdljjz import EGJZRYTX
from .nodes.egtxcglj import EGTXLJNode
from .nodes.egtxystz import EGHTYSTZNode
from .nodes.egtxwhlj import EGWHLJ
from .nodes.egzzcjpj import EGZZHBCJNode
from .nodes.EGJDFDHT import EGRYHT
from .nodes.EGSZJDYS import EGSZCGJS
from .nodes.EGSZHZ import EGSSRYZH
from .nodes.EGWBZYSRK import EGZYWBKNode
from .nodes.EGZZTXHZ import EGTXZZZHNode
from .nodes.EGJBCHBMQ import EGJBCH
from .nodes.EGLATENTBISC import EGKLATENT
from .nodes.EGTXSFBLS import EGTXSFBLSNode
from .nodes.EGTXSXJZ import EGLJJZTXDZ
from .nodes.EGZZTXYSJ import EGTXFT
from .nodes.EGZZJDYH import EGZZMH
from .nodes.EGZZJDYHHT import EGZZMHHT
from .nodes.EGZZTMTX import EGTMTX
from .nodes.EGZZFQTC import EGJFZZTC
from .nodes.EGZZBYCJ import EGZZRH
from .nodes.EGJUCHCYQ import EGCYQJB
from .nodes.egtscdssrjknode import EGTSCDSSRJKNode
from .nodes.EGDZXLJZ import SequentialImageLoader
from .nodes.EGXLWBBC import SaveTextToFile

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
    "EG_TX_JZRY" : EGJZRYTX,
    "EG_TX_LJ" : EGTXLJNode,
    "EG_HT_YSTZ" : EGHTYSTZNode,
    "EG_TX_WHLJ" : EGWHLJ,
    "EG_ZZHBCJ" : EGZZHBCJNode,
    "EG_RY_HT" : EGRYHT,
    "EG_SZ_CGJS" : EGSZCGJS,
    "EG_SS_RYZH" : EGSSRYZH,
    "EG_ZY_WBK" : EGZYWBKNode,
    "EG_TXZZ_ZH" : EGTXZZZHNode,
    "ER_JBCH": EGJBCH,
    "EG_TX_SFBLS" : EGTXSFBLSNode,
    "EG_K_LATENT" : EGKLATENT,
    "EG_LJ_JZTXDZ" : EGLJJZTXDZ,
    "EG_FSFT" : EGTXFT,
    "EG_ZZ_MH" : EGZZMH,
    "EG_ZZ_MHHT" : EGZZMHHT,
    "EG_ZZ_TMTX" : EGTMTX,
    "EG_JF_ZZTC" : EGJFZZTC,
    "EG_ZZ_RH" : EGZZRH,
    "EG_CYQ_JB" : EGCYQJB,
    "EG_TSCDS_SRJK" : EGTSCDSSRJKNode,
    "SequentialImageLoader": SequentialImageLoader,
    "SaveTextToFile": SaveTextToFile,
}

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
    "EG_TX_JZRY" : "2🐕加载任意图像",
    "EG_TX_LJ" : "2🐕常规滤镜",
    "EG_HT_YSTZ" : "2🐕调整图像颜色",
    "EG_TX_WHLJ" : "2🐕网红滤镜",
    "EG_ZZHBCJ" : "2🐕遮罩任意裁剪拼接",
    "EG_RY_HT" : "2🐕权重滑条",
    "EG_SZ_CGJS" : "2🐕+-x÷常规计算",
    "EG_SS_RYZH" : "2🐕整数浮点字符串格式转换",
    "EG_ZY_WBK" : "2🐕自由输入框",
    "EG_TXZZ_ZH" : "2🐕互转遮罩图像",
    "ER_JBCH": "2🐕重绘模式选择内补编码器",
    "EG_TX_SFBLS" : "2🐕图像缩放比例锁",
    "EG_K_LATENT" : "2🐕空Latent比例生成器",
    "EG_LJ_JZTXDZ" : "2🐕单张顺序随机加载图像",
    "EG_FSFT" : "2🐕图像选择加载",
    "EG_ZZ_MH" : "2🐕遮罩边缘快速模糊",
    "EG_ZZ_MHHT" : "2🐕遮罩边缘滑条快速模糊",
    "EG_ZZ_TMTX" : "2🐕透明图像裁剪",
    "EG_JF_ZZTC" : "2🐕遮罩分块填充",
    "EG_ZZ_RH" : "2🐕遮罩边缘检测",
    "EG_CYQ_JB" : "2🐕局部重绘采样器",
    "EG_TSCDS_SRJK" : "2🐕提示词大师素人极客类",
    "SequentialImageLoader": "2🐕单张加载训练集图像",
    "SaveTextToFile": "2🐕训练tag保存"
}
