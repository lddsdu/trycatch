# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

import cv2
import numpy as np


if __name__ == '__main__':
    im = np.ones((100, 100, 3), dtype="uint8")
    im = im * 200
    pil_im = Image.fromarray(im)
    draw = ImageDraw.Draw(pil_im)
    font = ImageFont.truetype("xiaowei.ttf", 20, encoding="utf-8")
    # decode --->  utf-8  ->  unicode
    draw.text((0, 0), "字体下载".decode("utf8"), (0, 0, 0), font= font)
    im = np.array(pil_im)
    cv2.imshow("video", im)
    cv2.waitKey(1000)


def drawtext(xy, text, font_size, color, data):
    """
    zhong wen
    :param xy: location
    :param text:  the text data
    :param font_size:
    :param color:  text color
    :param data: numpy.ndarray
    :return:
    """
    pil_im = Image.fromarray(data)
    draw = ImageDraw.Draw(pil_im)
    font = ImageFont.truetype("facerecoModule/xiaowei.ttf", font_size, encoding="utf-8")
    if not isinstance(text, unicode):
        text = text.decode("utf-8")
    draw.text(xy, text, color, font)
    return np.array(pil_im)