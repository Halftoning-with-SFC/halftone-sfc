#!/usr/bin/python3.11

import turtle
import collections as cl
import numpy as np


class Curve:
    def __init__(self, edges) -> None:
        self.a = edges

    def print_curve(self):
        turtle.speed(0)
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()

        for _, end in self.a.items():
            turtle.goto(
                end[0] * 10, end[1] * 10
            ) # multiply for better view

        turtle.done()


def hilbert(stg: str) -> str:
    stg = stg.replace("a", "+Bf-AfA-fB+")
    stg = stg.replace("b", "-Af+BfB+fA-")
    return stg.lower()


Si = "a"
iters = 10

for _ in range(iters):
    Si = hilbert(Si)


def traverse(stg: str) -> Curve:
    edges = cl.defaultdict()
    pointer = np.array([0, 0])
    dir = np.array([0, 1])
    next = pointer + dir

    print(stg)

    for char in stg:
        if char == "+":
            dir = np.array([dir[1], -dir[0]])

        elif char == "-":
            dir = np.array([-dir[1], dir[0]])

        elif char == "f":
            next = pointer + dir
            edges[tuple(pointer)] = tuple(next)
            pointer = next

    print(edges)
    return edges


curv = Curve(traverse(Si))

curv.print_curve()
