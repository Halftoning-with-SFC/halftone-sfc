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
# cli.py --image data/input/araras.png --curve peano --cluster_size 4
# cli.py --image data/input/impa.png --curve hilbert --cluster_size 8
# cli.py --image data/input/araras.png --curve sierpinksi --cluster_size 6
# --------------------------------------------------------------------------------------------------
# usage: cli.py [-h] [--image image] [--curve curve] [--cluster_size cluster_size]
#
# options:
#   -h, --help                   show this help message and exit
#   --in_image in_image          path to the input image
#   --curve curve                type of space filling curve (hilbert, peano, lebesgue)
#   --cluster_size cluster_size  size of the cluster for halftoning
#   --out_image out_image        path to the output image
#   --distribution distribution  how blacks are distributed within the cluster (standard, ordered, random)
#   --strength strength  strength value for edge enhancement (default: 1.0)
#   --blur blur  blur value for edge enhancement (default: 1.0)
#   --gamma gamma  Gamma value for gamma correction (default: 1.0)
# --------------------------------------------------------------------------------------------------

import argparse
import os
import cv2

from .halftone import edge_enhancement, gammma_correction, halftoning


def main():
    parser = argparse.ArgumentParser(description="Halftoning with Space-Filling Curves")

    default = {
        'curve': 'hilbert',
        'cluster_size': 4,
        'distribution' : 'standard',
        'strength': 1.0,
        'blur': 1.0,
        'gamma': 1.0
    }

    valid_curves = {'hilbert', 'peano', 'lebesgue'}
    valid_distributions = {'standard', 'ordered', 'random'}

    parser.add_argument('--in_image', metavar='in_image', type=str, required=True,
                        help='path to the input image')
    parser.add_argument('--curve', metavar='curve', type=str,
                        default=default['curve'],
                        help='type of space filling curve (hilbert, peano, lebesgue)')
    parser.add_argument('--cluster_size', metavar='cluster_size', type=int,
                        default=default['cluster_size'],
                        help='size of the cluster out_image halftoning')
    parser.add_argument('--out_image', metavar='out_image', type=str,
                        help='path to the output image')
    parser.add_argument('--distribution', metavar='distribution', type=str,
                        default=default['distribution'],
                        help='how blacks are distributed within the cluster (standard, ordered, random)')
    parser.add_argument('--strength', type=float, default=default['strength'],
                        help='strength value for edge enhancement (default: 1.0)')
    parser.add_argument('--blur', type=float, default=default['blur'],
                        help='blur value for edge enhancement (default: 1.0)')
    parser.add_argument('--gamma', type=float, default=default['gamma'],
                        help='Gamma value for gamma correction (default: 1.0)')
    
    args = parser.parse_args()

    args.in_image = os.path.abspath(args.in_image)

    if not os.path.isfile(args.in_image):
        print(f"Error: Input image '{args.in_image}' not found.")
        return

    if args.curve not in valid_curves:
        print(f"Error: Invalid curve '{args.curve}'. Choose from {valid_curves}.")
        return

    if args.distribution not in valid_distributions:
        print(f"Error: Invalid distribution '{args.distribution}'. Choose from {valid_distributions}.")
        return
        
    if args.out_image is None:
        filename = os.path.basename(args.in_image)
        args.out_image = os.path.join(os.getcwd(), f"{args.curve}_{args.cluster_size}_{args.distribution}_{args.strength}_{args.blur}_{args.gamma}_{filename}")

    output_dir = os.path.dirname(args.out_image)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(args.in_image, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Error: Failed to read image '{args.in_image}'. Make sure it is a valid image file.")
        return
    
    curve = args.curve
    cluster_size = args.cluster_size
    distribution = args.distribution

    gamma_image = gammma_correction(image, args.gamma)
    edge_image = edge_enhancement(gamma_image, args.strength, args.blur)

    halftone_image = halftoning(edge_image, curve, cluster_size, distribution)

    cv2.imwrite(args.out_image, halftone_image)
    print(f"Output saved to: {args.out_image}")

if __name__ == '__main__':
    main()

