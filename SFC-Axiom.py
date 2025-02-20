import turtle
import matplotlib.pyplot as plt
import collections as cl
import numpy as np
from PIL import Image
from copy import deepcopy
import cv2 as cv

image = cv.imread("ro2.jpeg")
print(image.shape)


class curve:

    def __init__(self, arestas):

        self.a = arestas

    def print_curve(self):
        turtle.speed(0)
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()

        for start, end in self.a.items():
            turtle.goto(end[0] * 10, end[1] * 10)

        turtle.done()


def hilbert(stg: str) -> str:
    stg = stg.replace("a", "+Bf-AfA-fB+")
    stg = stg.replace("b", "-Af+BfB+fA-")
    return stg.lower()


Si = "a"
iters = 8

for _ in range(iters):
    Si = hilbert(Si)


def percorrer(stg: str) -> curve:

    arestas = cl.defaultdict()
    pointer = np.array([0, 0])
    dir = np.array([0, 1])
    next = pointer + dir

    for char in stg:
        if char == "+":
            dir = np.array([dir[1], -dir[0]])

        elif char == "-":
            dir = np.array([-dir[1], dir[0]])

        elif char == "f":
            next = pointer + dir
            arestas[tuple(pointer)] = tuple(next)
            pointer = next

    return arestas


def percorrer_img(
    curv: curve,
    img,
    n=1000,
):
    list_img = []
    im_pointer = np.array([0, 0])
    cv_pointer = (0, 0)

    while cv_pointer in curv.a.keys():

        img[im_pointer[0], im_pointer[1]] = [0, 0, 0]

        next_pointer = curv.a[cv_pointer]
        dir = np.array(next_pointer) - np.array(cv_pointer)

        im_pointer += dir
        cv_pointer = next_pointer

        if n == 1000:
            img_atual = deepcopy(img)
            list_img.append(img_atual)
            n = 0
        n += 1

    return list_img


crv = curve(percorrer(Si))

a = percorrer_img(crv, image)

for i in range(len(a)):
    cv.imwrite(f"image_gif/im{i}.jpeg", a[i])

print(a)

# crv.print_curve()
