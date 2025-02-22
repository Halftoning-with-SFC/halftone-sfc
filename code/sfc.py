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
    Retorna as coordenadas (x, y) do i-ésimo ponto na curva de Peano de ordem order.

    Parâmetros:
    -----------
    i : int
        O índice do ponto na curva de Peano.
    order : int
        A ordem da curva de Peano.

    Retorna:
    --------
    (x, y) : tuple of int
        As coordenadas (x, y) do i-ésimo ponto.
    """
    # Converte o número i para a base 3
    digits = []
    for _ in range(2 * order):
        digits.append(i % 3)
        i //= 3
    digits.reverse()
    print(f'digitos = {digits}')

    # Separa os dígitos em duas listas (x e y)
    a = []
    for _ in range(order):
        a.append([digits[2*_], digits[2*_+1]])

    print(f'matriz = {a}')

    # Aplica as transformações inversas
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
        x += a[_][0]
        y += a[_][1]

    return (x, y)

'''
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

    points = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 1),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2)
    ]
    
    #tem que testar pra ver se isso ta funcinando certo

    if i > (3**(2*order))-1 : #se o número for maior do que o número de quadrados que existem
        raise ValueError("Number can't be bigger than the number of divisions")

    index = i % 9  
    x, y = points[index]

    for j in range(1, order):
        i = i // 9  
        shift = 3**j  
        index = i % 9  

        if index == 0:
            x, y = y, x
        elif index == 1:
            x, y = x, y + shift
        elif index == 2:
            x, y = x + shift, y + shift
        elif index == 3:
            x, y = x + shift, y - shift
        elif index == 4:
            x, y = x + shift, y
        elif index == 5:
            x, y = x - shift, y + shift
        elif index == 6:
            x, y = x - shift, y - shift
        elif index == 7:
            x, y = x - shift, y
        elif index == 8:
            x, y = 2 * shift - 1 - y, shift - 1 - x

    return (x, y)
'''


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

    if i > (2**(2*order))-1 : #se o número for maior do que o número de quadrados que existem
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


def lesbegue(i, order):
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

    if i >= (4**order): #se o número for maior do que o número de quadrados que existem
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
        # Extrai o par de bits atual
        bits = binary_num[2*k : 2*(k+1)]

        # Calcula o deslocamento com base na ordem atual
        shift = 2**(order - k - 1)

        if bits == "01":
            y += shift
        elif bits == "10":
            x += shift
        elif bits == "11":
            x += shift
            y += shift

    return (x,y)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    default = {
        'curve': 'peano',
        'order': 2,
    }

    parser.add_argument('--curve', metavar='curve', type=str,
                        default=default['curve'],
                        help='type of space filling curve (hilbert, peano, lesbegue)')
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
    elif curve == 'lesbegue':
        n = 2**order
        space_filling_curve = [lesbegue(i, order) for i in range(n * n)]
    else:
        raise ValueError('invalid curve type, choose from (hilbert, peano, lesbegue)')

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
