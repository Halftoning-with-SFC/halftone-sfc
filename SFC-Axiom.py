import turtle
import matplotlib.pyplot as plt
import collections as cl
import numpy as np


class curve:

    def __init__(self, arestas):

        self.a = arestas

    def print_curve(self):
        turtle.speed(0)
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()

        for start, end in self.a.items():
            turtle.goto(
                end[0] * 10, end[1] * 10
            )  # Multiplicamos para visualização melhor

        turtle.done()


def hilbert(stg: str) -> str:
    stg = stg.replace("a", "+Bf-AfA-fB+")
    stg = stg.replace("b", "-Af+BfB+fA-")
    return stg.lower()


Si = "a"
iters = 10

for _ in range(iters):
    Si = hilbert(Si)


def percorrer(stg: str) -> curve:

    arestas = cl.defaultdict()
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
            arestas[tuple(pointer)] = tuple(next)
            pointer = next

    print(arestas)
    return arestas


curv = curve(percorrer(Si))

curv.print_curve()
