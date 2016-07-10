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

    f = open('FeaturesDB/features.csv', 'wb')

    # write header
    #header = 'label'
    #for k in range(4 * 18):
    #    header += ',' + str(k)
    #f.write(header + '\n')
    header = 'label'
    for i in range(40):
        header = header + ',' + str(i)
    f.write(header + '\n')

    features_vectors_total = []
    for (dirpath, dirnames, filenames) in walk(args.path):
        for filename in filenames:
            label = dirpath.split('#')[1]
            #if int(label) == 1:
            #    break
            image_path = dirpath + '/' + filename

            pre_processor = preprocessing.PreProcessFingerImage(
                image_path)
            pre_processor.process_image()
            image = pre_processor.get_preprocessed_image()

            image_fft = fft_enchance_image.enhance_image(image, 25, 0, 0.444)

            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
            image_fft = clahe.apply(image_fft)

            image_fft = image_binarization.binarization(image_fft, 170)


            image_gabor = gabor_enhance_image.gabor_enhance_image(
                image, 3, 3.9, 8.9, 1.4)


            image_result = image_gabor + image_fft
            for i in range(image_result.shape[0]):
                for j in range(image_result.shape[1]):
                    if (image_result[i, j] > 255):
                        image_result[i, j] = 255
                    else:
                        image_result[i, j] = 0

            image = image_binarization.binarization(image_result, 170)

            image = bwmorph_thin.bwmorph_thin(1 - image / 255, 20)
            image = (255 - image * 255).astype('uint8')


            minuteas_array = feature_extraction.minuteas_extraction(image)
            features_vector = feature_extraction.generate_features_vectors(
                minuteas_array)

            print label
            counter = 0
            f.write(label)
            for feature in features_vector:
                if counter == 10:
                    break
                image_features = ',{},{},{},{}'.format(feature[0], feature[1], feature[2], feature[3])
                f.write(image_features)
                counter += 1

            while counter != 10:
                image_features = ',{},{},{},{}'.format(0, 0, 0, 0)
                f.write(image_features)
                counter += 1
            f.write('\n')
    f.close()
if __name__ == '__main__':
    main()
