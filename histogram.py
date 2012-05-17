#!/usr/bin/python

from glob import glob
from PIL import Image

def phash(im):
    return im.resize((100, 100)).convert('P').histogram()

def diff(h1, h2):
    acc = 0
    for a, b in zip(h1, h2):
        acc += abs(a - b)
    return acc

if __name__ == '__main__':
    target = phash(Image.open('target.png'))

    candidates = glob('images/[0-9][0-9].*')
    candidates = dict((f, phash(Image.open(f))) for f in candidates)

    diffs = dict()
    for c in candidates:
        diffs[c] = diff(target, candidates[c])

    for c in sorted(diffs, key=diffs.__getitem__):
        print c, diffs[c]
