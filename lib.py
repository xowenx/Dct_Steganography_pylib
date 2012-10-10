import numpy as np
from scipy.fftpack import dct, idct
import Image


def write_to_image(path, text):
    x1, x2, x3, y1, y2, y3 = [4, 5, 3, 3, 5, 4]
    index = 0
    D = 5
    img = Image.open(path)
    img.getdata()
    bitext = text_to_binary(text)
    bitext = bitext + '0000000000000000'
    r, g, b = [np.array(x) for x in img.split()]
    lx, ly = r.shape()
    for x in xrange(0, lx - 2, 8):
        for y in xrange(0, ly - 2, 8):
            if index == len(bitext) - 1:
                break
            metric = r[x:x + 8, y:y + 8].astype('float')
            metric = dct(metric, norm='ortho')
            if bitext[index] == 1:
                metric[x1, y1] = max(metric[x1, y1], metric[x3, y3] + D + 1)
                metric[x2, y2] = max(metric[x2, y2], metric[x3, y3] + D + 1)
            else:
                metric[x1, y1] = min(metric[x1, y1], metric[x3, y3] - D - 1)
                metric[x2, y2] = min(metric[x2, y2], metric[x3, y3] - D - 1)
            index = index + 1
            metric = idct(metric, norm='ortho')
            r[x:x + 8, y:y + 8] = metric.astype('uint8')
    im = Image.merge("RGB", [Image.fromarray(x) for x in [r, g, b]])
    im.save('%s_writed' % path)


def text_to_binary(text):
    return ''.join(['%08d' % int(bin(ord(c))[2:]) for c in text])


def binary_to_text(text):
    tmp = [text[k: k + 8] for k in xrange(0, len(text), 8)]
    return ''.join([chr(int(c, 2)) for c in tmp])
