# TODO bad practise
import sys
sys.path.append("..")

import cv2
import numpy as np
import argparse
import bwmorph_thin
from imageprocess import *


def generate_features_vectors(minuteas_array):
    prev_coord_x = 0
    prev_coord_y = 0
    features_vectors = []

    for i in np.arange(len(minuteas_array)):
        next_coord_x = minuteas_array[i][0]
        next_coord_y = minuteas_array[i][1]
        if (prev_coord_x != 0) and (prev_coord_y != 0):

            # generate feature
            a = next_coord_x - prev_coord_x
            b = next_coord_y - prev_coord_y
            d_next = np.sqrt(a**2 + b**2)
            ang = np.degrees(np.arctan2(b, a))
            #print "%s, %s, %0.1f, %0.2f" % (prev_coord_x, prev_coord_y, d_next, ang)
            features_vectors.append([prev_coord_x,prev_coord_y,d_next,ang])
        prev_coord_x = next_coord_x
        prev_coord_y = next_coord_y

    return features_vectors

def minuteas_extraction(image):
    #TODO  normalize image to 0s and 1s, handle that without forcing
    image_thinned = bwmorph_thin.bwmorph_thin(1 - image / 255, 10)

    minuteas = []
    clone = 1 - image_thinned * 1
    clone = cv2.merge((clone, clone, clone))

    # alterar o stepSize
    for (x, y, window) in image_process_utils.sliding_window(1 - image_thinned * 1, stepSize=3, windowSize=(3, 3)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != 3 or window.shape[1] != 3:
            continue

        if (window[1, 1] == 0) and (np.sum(window) <= 5):
            minuteas.append(np.array([x, y]))

    return minuteas


def main():
    parser = argparse.ArgumentParser(
        description='Extract Features')
    parser.add_argument(
        "image_path", help="Specify image path location")

    args = parser.parse_args()

    pre_processor = preprocessing.PreProcessFingerImage(args.image_path)
    pre_processor.process_image()
    image = pre_processor.get_preprocessed_image()
    image = fft_enchance_image.enhance_image(image, 30, 0, 0.35)
    image = image_binarization.binarization(image, 200)
    minuteas_array = minuteas_extraction(image)
    features_vector = generate_features_vectors(minuteas_array)
    for vector in features_vector:
        print "%s,%s,%0.1f,%0.1f" % (vector[0],vector[1],vector[2],vector[3])

if __name__ == '__main__':
    main()
