import os
from pathlib import Path
import cv2
import numpy as np

def find_slider_x(bg_path, tgt_path):
    bg = cv2.imdecode(np.fromfile(bg_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    tpl = cv2.imdecode(np.fromfile(tgt_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if bg is None or tpl is None:
        print("图片读取失败，路径：", bg_path, tgt_path)
        return None
    bg_edge = cv2.Canny(bg, 100, 200)
    tpl_edge = cv2.Canny(tpl, 100, 200)
    result = cv2.matchTemplate(bg_edge, tpl_edge, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    x = max_loc[0]     
    return x