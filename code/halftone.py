#! /usr/bin/env python3
# --------------------------------------------------------------------------------------------------
# Digital Halftoning with Space Filling Curves
#
# Implementation of:
#   Digital Halftoning with Space Filling Curves, Luiz Velho and Jonas de Miranda Gomes
#   Special Interest Group on Computer Graphics and Interactive Techniques (SIGGRAPH), 1991
# --------------------------------------------------------------------------------------------------
# usage examples:
#
# halftone.py --image data/input/araras.png --curve peano --cluster_size 4
# halftone.py --image data/input/impa.png --curve hilbert --cluster_size 8
# halftone.py --image data/input/araras.png --curve sierpinksi --cluster_size 6
# --------------------------------------------------------------------------------------------------
# usage: halftone.py [-h] [--image image] [--curve curve] [--cluster_size cluster_size]
#
# options:
#   -h, --help                   show this help message and exit
#   --image image                path to the input image
#   --curve curve                type of space filling curve (hilbert, peano, sierpinski)
#   --cluster_size cluster_size  size of the cluster for halftoning
# --------------------------------------------------------------------------------------------------

import argparse
import cv2
import numpy as np
from sfc import peano, hilbert, sierpinski


def generate_space_filling_curve(image, curve):
    log = lambda x, b : np.log(x) / np.log(b)

    if curve == 'hilbert':
        order = np.ceil(np.log2(max(image.shape))).astype(int)
        n = 2**order
        space_filling_curve = [hilbert(i, order) for i in range(n * n)]
    elif curve == 'peano':
        order = np.ceil(log(max(image.shape), 3)).astype(int)
        n = 3**order
        space_filling_curve = [peano(i, order) for i in range(n * n)]
    elif curve == 'sierpinski':
        order = np.ceil(log(max(image.shape), 2)).astype(int)
        n = 2**order
        space_filling_curve = [sierpinski(i, order) for i in range(n * n)]
    else:
        raise ValueError('invalid curve type, choose from (hilbert, peano, sierpinski)')

    height, width = image.shape
    space_filling_curve = [(x, y) for x, y in space_filling_curve if x < width and y < height]

    return space_filling_curve


def gammma_correction(image):

    #TODO: Implement gamma correction

    return image


def edge_enhancement(image):

    #TODO: Implement gamma correction

    return image


def halftoning(image, curve, cluster_size):
    halftone = np.zeros_like(image)

    space_filling_curve = generate_space_filling_curve(image, curve)
    n_clusters = len(space_filling_curve) // cluster_size
    clusters = np.array_split(space_filling_curve, n_clusters)

    intensity_accumulator = np.int32(0)

    for cluster in clusters:
        for x, y in cluster:
            intensity_accumulator += image[y, x]

        for x, y in cluster:
            if intensity_accumulator >= 255:
                halftone[y, x] = 255
                intensity_accumulator -= 255
            else:
                halftone[y, x] = 0

    return halftone


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    default = {
        'image': 'data/input/araras.png',
        'curve': 'hilbert',
        'cluster_size': 4,
    }

    parser.add_argument('--image', metavar='image', type=str,
                        default=default['image'],
                        help='path to the input image')
    parser.add_argument('--curve', metavar='curve', type=str,
                        default=default['curve'],
                        help='type of space filling curve (hilbert, peano, sierpinski)')
    parser.add_argument('--cluster_size', metavar='cluster_size', type=int,
                        default=default['cluster_size'],
                        help='size of the cluster for halftoning')
    args = parser.parse_args()

    image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    curve = args.curve
    cluster_size = args.cluster_size

    gamma_image = gammma_correction(image)
    edge_image = edge_enhancement(gamma_image)
    halftone_image = halftoning(edge_image, curve, cluster_size)

    cv2.imwrite(f"data/output/{curve}_{cluster_size}_{args.image.split('/')[-1]}", halftone_image)
