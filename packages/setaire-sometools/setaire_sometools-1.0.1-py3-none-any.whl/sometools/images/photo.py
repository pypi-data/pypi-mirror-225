'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-03-02 14:43:57
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-03-02 14:59:53
 # @ Description:
 '''


import numpy as np
import cv2
from ..utils.decorator import Command


def get_frontalfaces(img: cv2.Mat) -> cv2.Mat:
    """获取正脸位置

    Args:
        img (cv2.Mat): 灰度图

    Returns:
        cv2.Mat: [x, y, w, h]
    """
    faceCascade = cv2.CascadeClassifier(
        '/usr/local/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(img, 1.3, 5)
    if isinstance(faces, tuple):
        return np.empty(shape=(0, 4), dtype=np.int16)
    return faces


@Command
def gen_residence_permit_photo(file: str, out: str):
    """生成居住证申请照片
            居住证 证件照 尺寸 358 x 441
            14kb < 大小 < 28kb

    Args:
        file (str): 原始照片
        out (str): 保存为
    """

    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x, y, w, h = get_frontalfaces(gray)[0]

    Xrate = 358 / 253
    Yrate = 441 / 253

    ww = int(w * Xrate)
    hh = int(h * Yrate)

    startX = max(int(x - (ww - w) // 2), 0)
    startY = max(int(y - (hh - h) // 3), 0)

    target = img[startY:startY+hh, startX:startX+ww]

    res = cv2.resize(target, (358, 441), interpolation=cv2.INTER_AREA)

    cv2.imwrite(out, res, [cv2.IMWRITE_JPEG_QUALITY, 85])
