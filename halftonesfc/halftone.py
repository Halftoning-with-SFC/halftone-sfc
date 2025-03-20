import random
import cv2
import numpy as np

from .sfc import peano, hilbert, lebesgue


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


def edge_enhancement(image, strength=1, blur=1):

    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=blur)
    enhanced = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)

    return enhanced

def halftoning(image, curve, cluster_size, separate = False, monocrome=False, distribution="standard"):
    """

    Parameters:
    -----------
    image : numpy.ndarray
        The input image.
    curve : str
        The curve to use for the space filling curve.
        Options: 'hilbert', 'peano', 'lebesgue'
    cluster_size : int
        The size of the clusters to use for the space filling curve.
    separate : boolean
        To determiine whether you want to return each halftone separated or the whole halftone.
        Default: False
    monocrome : boolean
        To determiine whether you want the monocrome halftoned image or not.
        Default: False
    distribution : str
        type of distribuition for the clusters
        Default: standard
        Options: 'standard', 'ordered', 'random'
    Returns:
        numpy.ndarray or list of numpy.ndarrays
    """

    # Extrair os canais (b, g, ou r) ou o canal único ativo da imagem
    if image.shape[2] == 3 or not monocrome:
        # Se a imagem tem 3 canais, extrai os canais (B, G, ou R)
        blue_active_channel = cv.split(image)[0] # blue
        green_active_channel = cv.split(image)[1] # green
        red_active_channel = cv.split(image)[2] # red
        channels = [blue_active_channel, green_active_channel, red_active_channel]
    else:
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        # Se a imagem já é monocromática, usar diretamente
        monocrome_channel = image
        channels = [monocrome_channel]

    space_filling_curve = generate_space_filling_curve(channels[0], curve, cluster_size) #create the sfc for the channels halftoning
    
    halftone_list = [] # to append the finished halftones

    for active_channel in channels:

        halftone = np.zeros_like(active_channel)
        n_clusters = len(space_filling_curve) // cluster_size
        clusters = np.array_split(space_filling_curve, n_clusters)

        intensity_accumulator = np.int32(0)

        for cluster in clusters:
            sort_cluster = []
            for x, y in cluster:
                intensity_accumulator += active_channel[y, x]
                sort_cluster.append([active_channel[y, x], x, y])

            if distribution == 'ordered':
                sort_cluster.sort(reverse=True)
            elif distribution == 'random':
                random.shuffle(sort_cluster)


            blacks = intensity_accumulator // 255
            intensity_accumulator = intensity_accumulator % 255

            for x, y in cluster:
                halftone[y, x] = 0

            for i in range(blacks):
                halftone[sort_cluster[i][2], sort_cluster[i][1]] = 255

    halftone_list.append(halftone)
    
    if separate:
      return halftone_list
    else:
      halftone = cv.merge(halftone_list)
    
    return halftone
