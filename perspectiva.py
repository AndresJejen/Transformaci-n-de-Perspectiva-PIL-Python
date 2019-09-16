import numpy
import sys
from PIL import Image


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

img = Image.open(sys.argv[1])
width, height = img.size
m = -0.5
xshift = abs(m) * width
new_width = width + int(round(xshift))

coeffs = find_coeffs(
        [(0, 0), (width, 0), (new_width, height), (xshift, height)],
        [(0, 0), (width, 0), (width, height), (0, height)])

img = img.transform((new_width, height), Image.PERSPECTIVE,coeffs, Image.BICUBIC)
img.save(sys.argv[2])

coeffs = find_coeffs(
        [(0, 0), (width, 0), (width, height), (0, height)],
        [(0, 0), (width, 0), (new_width, height), (xshift, height)])

img.transform((width, height), Image.PERSPECTIVE, coeffs,Image.BICUBIC).save(sys.argv[3])