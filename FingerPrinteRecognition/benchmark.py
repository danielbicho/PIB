import numpy as np
import cv2
import argparse
from imageprocess import *
from fingerprint import *
from os import walk


def main():
    parser = argparse.ArgumentParser(
        description='Read fingerprint images and benchmark preprocessing phase.')
    parser.add_argument(
        "path", help="Specify the images path location")

    args = parser.parse_args()

#    f = open('FeaturesDB/features.csv', 'ab')

    for (dirpath, dirnames, filenames) in walk(args.path):
        for filename in filenames:
            label = dirpath.split('#')[1]
            image_path = dirpath + '/' + filename

            pre_processor = preprocessing.PreProcessFingerImage(
                image_path)

            # display original image

            original_image = pre_processor.get_original_image()
            cv2.imshow('O' + str(filename), original_image)

            pre_processor.process_image()
            image = pre_processor.get_preprocessed_image()

            #image = cv2.GaussianBlur( image, (3,3), 0);
            kernel = np.ones((3,3),np.float32)/9
            image = cv2.filter2D(image,-1,kernel)

            # bilateralFilter
            #image = cv2.bilateralFilter(image,9,100,100)

            # low pass band
            image = frequency_filters.low_pass_filter(image, 170)
            image_fft = fft_enchance_image.enhance_image(image, 30, 0, 0.35)

            #gaussian_3 = cv2.GaussianBlur(image, (3,3), 10.0)
            #image = cv2.add(image, 255 - gaussian_3)
            image_gabor = gabor_enhance_image.gabor_enhance_image(image, 3, 3.9, 8.9, 1.4)

            image_result = image_fft + image_gabor
            for i in range(image_result.shape[0]):
                for j in range(image_result.shape[1]):
                    if (image_result[i,j] > 255):
                        image_result[i,j] = 255
                    else:
                        image_result[i,j] = 0

            #image = image_binarization.binarization(image, 170)
            #image = cv2.adaptiveThreshold(image.astype('uint8'),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,-1)
            cv2.imshow('Result' + filename, image_result)
            cv2.waitKey()

            #image = bwmorph_thin.bwmorph_thin(1 - image / 255,20)
            #image = 255 - image * 255
            #cv2.imshow(filename, image.astype('uint8'))

#            minuteas_array = feature_extraction.minuteas_extraction(image)
#            features_vector = feature_extraction.generate_features_vectors(
#                minuteas_array)
if __name__ == '__main__':
    main()
