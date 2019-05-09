from cStringIO import StringIO
from PIL import Image
import numpy as np


def numpy2png(data):
    """
    transform the numpy to bytes info of png file
    :param data:
    :return:
    """
    temp_file = StringIO()
    img = Image.fromarray(data[:, :, ::-1])
    img.save(temp_file, format="PNG")
    image_data = temp_file.getvalue()
    return image_data


if __name__ == '__main__':
    numpy2png(None)