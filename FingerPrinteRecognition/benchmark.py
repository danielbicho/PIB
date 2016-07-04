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
            cv2.imwrite('processed_images_results/' +
                        str(filename) + '_preprocessing.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            # inverter para trabalhar nas cristas
            image_gabor = gabor_enhance_image.gabor_enhance_image(
                image, 3, 3.9, 8.9, 1.4)
            #cv2.normalize(image_gabor,image_gabor, alpha=0, beta=255, dtype=cv2.CV_8UC1)

            cv2.imshow('Gabor Enhanced Image', image_gabor)
            cv2.imwrite('processed_images_results/' +
                        str(filename) + '_gabor.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            image_fft = fft_enchance_image.enhance_image(
                image, image.shape[0], 0, 0.15)

            cv2.imwrite('processed_images_results/' +
                        str(filename) + '_fft.jpg', image_fft, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            #image_fft = image_binarization.binarization(image_fft, 170)

            cv2.imshow('FFT Enhanced Image', image_fft)
            image_result = image_gabor + image_fft

            for i in range(image_result.shape[0]):
                for j in range(image_result.shape[1]):
                    if (image_result[i, j] > 255):
                        image_result[i, j] = 255
                    else:
                        image_result[i, j] = 0

            cv2.imshow('Result Enhanced Image', image_result)
            # Testar tecnicas de pos-processamento
            image = image_binarization.binarization(image_result, 170)

            cv2.imshow('binarization', image)
            #image = cv2.adaptiveThreshold(image.astype('uint8'),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,-1)
            cv2.imwrite('processed_images_results/' +
                        str(filename) + '_result.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            image = bwmorph_thin.bwmorph_thin(1 - image / 255, 20)
            image = (255 - image * 255).astype('uint8')
            cv2.imshow(filename, image)
            cv2.imwrite('processed_images_results/' +
                        str(filename) + '_thinned.jpg', image)

            minuteas_array = feature_extraction.minuteas_extraction(image)
            # convert image to 3 channel
            image_color = cv2.merge((image, image, image))

            for minutea in minuteas_array:
                cv2.rectangle(image_color, (minutea[0] - 2, minutea[1] - 2), (minutea[
                              0] + 2, minutea[1] + 2), (0, 255, 0), 1)

            cv2.imshow('Features Detected', image_color)
            cv2.imwrite('processed_images_results/' +
                        str(filename) + '_features.jpg', image_color, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            cv2.waitKey()

if __name__ == '__main__':
    main()
