#!/usr/bin/python

import math
from glob import glob
from PIL import Image

def phash(im):
    im = im.resize((32, 32)).convert('L')
    seq = [sum(im.getpixel((x, y)) *
               math.cos(math.pi / 32 * (x + .5) * u) *
               math.cos(math.pi / 32 * (y + .5) * v)
               for x in range(32) for y in range(32))
           for v in range(8) for u in range(8)]
    avg = sum(seq[1:]) / (len(seq) - 1)
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, seq)),
                  0)

def diff(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

if __name__ == '__main__':
    target = phash(Image.open('target.png'))

    candidates = glob('images/[0-9][0-9].*')
    candidates = dict((f, phash(Image.open(f))) for f in candidates)

    diffs = dict()
    for c in candidates:
        diffs[c] = diff(target, candidates[c])

    for c in sorted(diffs, key=diffs.__getitem__):
        print c, diffs[c]
