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
import random

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


def gammma_correction(image, gamma):
    
    img_normalized = image / 255.0
    gamma_corrected = np.power(img_normalized, gamma)
    gamma_corrected = (gamma_corrected * 255).astype(np.uint8)

    return gamma_corrected


def edge_enhancement(image, alpha, beta):
    
    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=beta)
    enhanced = cv2.addWeighted(image, 1 + alpha, blurred, -alpha, 0)
    enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)

    #: Implement gamma correction

    return enhanced


def halftoning(image, curve, cluster_size, distribution):
    halftone = np.zeros_like(image)

    space_filling_curve = generate_space_filling_curve(image, curve)
    n_clusters = len(space_filling_curve) // cluster_size
    clusters = np.array_split(space_filling_curve, n_clusters)

    intensity_accumulator = np.int32(0)

    for cluster in clusters:
        sort_cluster = []
        for x, y in cluster:
            intensity_accumulator += image[y, x]
            sort_cluster.append([image[y, x], x, y])
        
        if distribution == 'ordered':
            sort_cluster.sort(reverse=True)
        
        if distribution == 'random':
            random.shuffle(sort_cluster)

        blacks = intensity_accumulator//255
        intensity_accumulator = intensity_accumulator%255

        for x, y in cluster:
                halftone[y, x] = 0

        for i in range(blacks):
            halftone[sort_cluster[i][2], sort_cluster[i][1]] = 255

    return halftone


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    default = {
        'image': 'data/input/araras.png',
        'curve': 'hilbert',
        'cluster_size': 4,
        'distribution' : 'standart'
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
    parser.add_argument('--distribution', metavar='distribution', type=str,
                        default=default['distribution'],
                        help='how blacks are distributed within the cluster ( standart, ordered, random )')
    args = parser.parse_args()

    image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    curve = args.curve
    cluster_size = args.cluster_size
    distribution = args.distribution
    
    Alpha = 1.0
    Gamma = 1.0
    Beta = 1.0

    gamma_image = gammma_correction(image, Gamma)
    edge_image = edge_enhancement(gamma_image, Alpha, Beta)
    halftone_image = halftoning(edge_image, curve, cluster_size, distribution)

    cv2.imwrite(f"data/output/{curve}_{cluster_size}_{distribution}_{args.image.split('/')[-1]}", halftone_image)
