#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# Space Filling Curves
# ------------------------------------------------------------------------------
# usage examples:
#
# sfc.py --curve peano --order 2
# sfc.py --curve hilbert --order 3
# sfc.py --curve sierpinski --order 4
# ------------------------------------------------------------------------------
# usage: sfc.py [-h] [--curve curve] [--order order]
#
# options:
#   -h, --help     show this help message and exit
#   --curve curve  type of space filling curve (hilbert, peano, sierpinski)
#   --order order  order of the space filling curve (1, 2, 3, ...)
# ------------------------------------------------------------------------------

import argparse
import matplotlib.pyplot as plt


def peano(i, order):
    """
    Compute the (x, y) coordinates of the i-th point on a Peano curve of a given order.

    Parameters:
    -----------
    i : int
        The index of the point on the Peano curve.
    order : int
        The order of the Peano curve. The curve will cover a 3^order x 3^order grid.

    Returns:
    --------
    (x, y) : tuple of int
        The (x, y) coordinates of the i-th point on the Peano curve.
    """

    # TODO Implement Peano curve

    return (0, 0)


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


def sierpinski(i, order):
    """
    Compute the (x, y) coordinates of the i-th point on a Sierpinski curve of a given order.

    Parameters:
    -----------
    i : int
        The index of the point on the Sierpinski curve.
    order : int
        The order of the Sierpinski curve.  The curve will cover a 4^order x 4^order grid.

    Returns:
    --------
    (x, y) : tuple of int
        The (x, y) coordinates of the i-th point on the Sierpinski curve.
    """

    # TODO Implement Sierpinski curve

    return (0, 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    default = {
        'curve': 'hilbert',
        'order': 4,
    }

    parser.add_argument('--curve', metavar='curve', type=str,
                        default=default['curve'],
                        help='type of space filling curve (hilbert, peano, sierpinski)')
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
    elif curve == 'sierpinski':
        n = 4**order
        space_filling_curve = [sierpinski(i, order) for i in range(n * n)]
    else:
        raise ValueError('invalid curve type, choose from (hilbert, peano, sierpinski)')

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
    plt.title('Space Filling Curves')

    plt.show()
