import random
import cv2
import numpy as np

from halftonesfc.sfc import peano, hilbert, lebesgue


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
    elif curve == 'lebesgue':
        order = np.ceil(log(max(image.shape), 2)).astype(int)
        n = 2**order
        space_filling_curve = [lebesgue(i, order) for i in range(n * n)]
    else:
        raise ValueError('invalid curve type, choose from (hilbert, peano, lebesgue)')

    height, width = image.shape
    space_filling_curve = [(x, y) for x, y in space_filling_curve if x < width and y < height]

    return space_filling_curve


def gammma_correction(image, gamma=1):

    img_array = np.array(image)

    img_normalized = img_array / 255.0
    gamma_corrected = np.power(img_normalized, gamma)
    gamma_corrected = (gamma_corrected * 255).astype(np.uint8)

    return image


def edge_enhancement(image, alpha=1, beta=1):

    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=beta)
    enhanced = cv2.addWeighted(image, 1 + alpha, blurred, -alpha, 0)
    enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)

    return enhanced


def halftoning(image, curve, cluster_size, distribution="standard"):
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

        elif distribution == 'random':
            random.shuffle(sort_cluster)

        blacks = intensity_accumulator//255
        intensity_accumulator = intensity_accumulator%255

        for x, y in cluster:
                halftone[y, x] = 0

        for i in range(blacks):
            halftone[sort_cluster[i][2], sort_cluster[i][1]] = 255

    return halftone