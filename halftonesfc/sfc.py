#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# Space Filling Curves
# ------------------------------------------------------------------------------
# usage examples:
#
# sfc.py --curve peano --order 2
# sfc.py --curve hilbert --order 3
# sfc.py --curve lebesgue --order 4
# ------------------------------------------------------------------------------
# usage: sfc.py [-h] [--curve curve] [--order order]
#
# options:
#   -h, --help     show this help message and exit
#   --curve curve  type of space filling curve (hilbert, peano, lebesgue)
#   --order order  order of the space filling curve (1, 2, 3, ...)
# ------------------------------------------------------------------------------

import argparse
import matplotlib.pyplot as plt
import turtle


def peano(i, order):
    """
    Return the coordinates (x, y) of i-th point of the Peano curve of given order.

    References: https://people.csail.mit.edu/jaffer/Geometry/PSFC
    https://codeforces.com/blog/entry/115590

    Parameters:
    -----------
    i : int
        The index of the point of Peano curve
    order : int
        The order of the peano curve.

    Returns:
    --------
    (x, y) : tuple of int
        The coordinates (x, y) of i-th point.
    """

    # find correct order
    for n in range(order):
        if max(i,2) < 3**(2*n):
            order = n
            break


    # convert the number to base 3
    digits = []
    for _ in range(2 * order):
        digits.append(i % 3)
        i //= 3
    digits.reverse()

    # filter the digits into two lists x and y
    a = []
    for _ in range(order):
        a.append([digits[2*_], digits[2*_+1]])

    # apply the inverse peano flip transformations
    R1, R2 = 0, 0
    tam = order
    for column in range(0,tam): #lines of a
        for line in range(0,2): #columns of a

            #build R1:
            R1 = 0
            for j in range(0,column+1): #R1 column
                for k in range(0,line): #R1 line
                    R1 += a[j][k]

            #build R2:
            R2 = 0
            for j in range(0,column): #R2 column
                for k in range(line+1,2): #R2 line
                    R2 += a[j][k]

            #check for the inverse peanos:
            if (R1 % 2 == 1) and a[column][line] != 1:
                a[column][line] = 2 - a[column][line]
            if (R2 % 2 == 1) and a[column][line] != 1:
                a[column][line] = 2 - a[column][line]

    x, y = 0, 0

    for _ in range(len(a)):
        base = (3**(order-_-1))
        x += base * a[_][0]
        y += base * a[_][1]

    return (x, y)


def hilbert(i, order):
    """
    Compute the (x, y) coordinates of the i-th point on a Hilbert curve of a given order.

    Reference: https://thecodingtrain.com/challenges/c3-hilbert-curve

    Parameters:
    -----------
    i : int
        The index of the point on the Hilbert curve.
    order : int
        The order of the Hilbert curve. The curve will cover a 2^order x 2^order grid.

    Returns:
    --------
    (x, y) : tuple of int
        The (x, y) coordinates of the i-th point on the Hilbert curve.
    """

    if i > (2**(2*order))-1 :
        raise ValueError("Number can't be bigger than the number of divisions")

    points = [
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 0),
    ]

    index = i & 3
    x, y = points[index]

    for j in range(1, order):
        i = i >> 2
        shift = 2**j
        index = i & 3

        if (index == 0):
            x, y = y, x
        elif (index == 1):
            x, y = x, y + shift
        elif (index == 2):
            x, y = x + shift, y + shift
        elif (index == 3):
            x, y = 2 * shift - 1 - y, shift - 1 - x

    return (x, y)


def lebesgue(i, order):
    """
    Compute the (x, y) coordinates of the i-th point on a Lesbegue curve of a given order.

    Parameters:
    -----------
    i : int
        The index of the point on the Lesbegue curve.
    order : int
        The order of the Lesbegue curve.  The curve will cover a 4^order x 4^order grid.

    Returns:
    --------
    (x, y) : tuple of int
        The (x, y) coordinates of the i-th point on the Lesbegue curve.
    """

    if i >= (4**order):
        raise ValueError(f"Index i must be less than 4^{order} = {4**order}.")

    def binary(num,size):
      '''
      num - número que queremos converter para binário
      size - tamanho do binário, se o número for menor que 2ˆsize, o binário terá zeros a esquerda

      ex: binary(10,5) = 01010
      '''
      return f"{num:0{size}b}"

    x, y = 0, 0

    binary_num = binary(i,order*2)

    for k in range(order):
        bits = binary_num[2*k : 2*(k+1)]

        shift = 2**(order - k - 1)

        if bits == "01":
            y += shift
        elif bits == "10":
            x += shift
        elif bits == "11":
            x += shift
            y += shift

    return (x,y)
def Sierpinski(iterations, step_size):
    def generate_l_system(iterations, axiom, rules):
        current = axiom
        for _ in range(iterations):
            next_str = []
            for char in current:
                next_str.append(rules.get(char, char))
            current = ''.join(next_str)
        return current

    def draw_l_system(t, l_string, angle, step_size):
        points = [t.position()]  # Store initial position
        for cmd in l_string:
            if cmd == 'F':
                t.forward(step_size)
                points.append(t.position())
            elif cmd == '+':
                t.left(angle)
            elif cmd == '-':
                t.right(angle)
        return points

    def get_curve_coordinates(iterations=4, step_size=3):
        axiom = "F--XF--F--XF"
        rules = {'X': 'XF+F+XF--F--XF+F+X'}
        angle = 45

        l_string = generate_l_system(iterations, axiom, rules)

        pen = turtle.Turtle()
        pen.speed(0)
        pen.hideturtle()
        pen.penup()
        
        # Start at center (0,0) for better normalization
        pen.goto(0, 0)
        pen.setheading(45)
        pen.pendown()
        
        points = draw_l_system(pen, l_string, angle, step_size)
        
        # Normalize coordinates to 1x1 square
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Calculate scaling factor
        width = max_x - min_x
        height = max_y - min_y
        scale = max(width, height) or 1.0  # Prevent division by zero
        
        normalized = [(
            (x - min_x) / scale,
            (y - min_y) / scale
        ) for x, y in points]
        
        # Return coordinates rounded to 6 decimal places
        return [(round(nx, 6), round(ny, 6)) for nx, ny in normalized]
    return get_curve_coordinates(iterations, step_size)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    default = {
        'curve': 'peano',
        'order': 3,
    }

    parser.add_argument('--curve', metavar='curve', type=str,
                        default=default['curve'],
                        help='type of space filling curve (hilbert, peano, lebesgue)')
    parser.add_argument('--order', metavar='order', type=int,
                        default=default['order'],
                        help='order of the space filling curve (1, 2, 3, ...)')
    args = parser.parse_args()

    curve = args.curve
    order = args.order

    if curve == 'hilbert':
        n = 2**order
        space_filling_curve = [hilbert(i, order) for i in range(n * n)]
    elif curve == 'peano':
        n = 3**order
        space_filling_curve = [peano(i, order) for i in range(n * n)]
    elif curve == 'lebesgue':
        n = 2**order
        space_filling_curve = [lebesgue(i, order) for i in range(n * n)]
    else:
        raise ValueError('invalid curve type, choose from (hilbert, peano, lebesgue)')

    fig, ax = plt.subplots()

    x = [x + 0.5 for x, y in space_filling_curve]
    y = [y + 0.5 for x, y in space_filling_curve]

    ax.plot(x, y)

    ax.set_xticks(range(n + 1))
    ax.set_yticks(range(n + 1))

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')

    plt.grid(True)
    plt.title(f"Space Filling Curves - {default['curve']} curve - order {default['order']}")

    plt.show()
