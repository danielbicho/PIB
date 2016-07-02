import numpy as np
import cv2
import argparse
from imageprocess import *
from fingerprint import *
from os import walk


def main():
    parser = argparse.ArgumentParser(
        description='Read fingerprint images and enroll them.')
    parser.add_argument(
        "path", help="Specify the images path location")

    args = parser.parse_args()

    #pre_processor = preprocessing.PreProcessFingerImage(args.image_path)
    # pre_processor.process_image()
    #image = pre_processor.get_preprocessed_image()
    #image = fft_enchance_image.enhance_image(image,25,0,0.222)

    f = open('FeaturesDB/features.csv', 'ab')

    # write header
    header = 'label'
    for k in range(4 * 18):
        header += ',' + str(k)
    f.write(header + '\n')

    features_vectors_total = []
    for (dirpath, dirnames, filenames) in walk(args.path):
        for filename in filenames:
            label = dirpath.split('#')[1]
            image_path = dirpath + '/' + filename
            pre_processor = preprocessing.PreProcessFingerImage(
                image_path)
            pre_processor.process_image()
            image = pre_processor.get_preprocessed_image()
            image = fft_enchance_image.enhance_image(image, 30, 0, 0.35)
            image = image_binarization.binarization(image, 170)
            minuteas_array = feature_extraction.minuteas_extraction(image)
            features_vector = feature_extraction.generate_features_vectors(
                minuteas_array)

            image_features = label
            for i in range(18):
                image_features += ',{},{},{},{}'.format(
                    features_vector[i][0], features_vector[i][1], features_vector[i][2], features_vector[i][3])

            f.write(image_features + '\n')

    f.close()
if __name__ == '__main__':
    main()
