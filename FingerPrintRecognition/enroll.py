# coding=utf-8
import argparse
from os import walk

import cv2

from fingerprint import *
from imageprocess import *


def main():
    parser = argparse.ArgumentParser(
        description='Read fingerprint images and enroll them.')
    parser.add_argument(
        "path", help="Specify the images path location")

    args = parser.parse_args()

    f = open('FeaturesDB/features.csv', 'wb')

    header = 'label'
    for i in range(40):
        header = header + ',' + str(i)
    f.write(header + '\n')

    for (dirpath, dirnames, filenames) in walk(args.path):
        for filename in filenames:
            label = dirpath.split('#')[1]
            image_path = dirpath + '/' + filename

            ###########################################################
            # pre processamento de imagem
            pre_processor = preprocessing.PreProcessFingerImage(
                image_path)
            pre_processor.process_image()
            image = pre_processor.get_preprocessed_image()

            ###########################################################



            ###########################################################
            # Aplicação do metodo FFT
            image_fft = fft_enchance_image.enhance_image(image, 15, 0, 0.444)

            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
            image_fft = clahe.apply(image_fft)

            image_fft = image_process_utils.block_process_overlap(
                image_fft, 15, 0, cv2.adaptiveThreshold,
                (255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, -1,))

            cv2.imshow('FFT', image_fft)
            ###########################################################


            ###########################################################
            # Aplicação dos filtros de Gabor
            image_gabor = gabor_enhance_image.gabor_enhance_image(
                image, 3, 6, 8.9, 1.4)
            cv2.normalize(image_gabor, image_gabor, 0, 255, cv2.NORM_MINMAX)
            image_gabor = image_binarization.binarization(image_gabor, 130)
            cv2.imshow('GB', image_gabor)
            ###########################################################

            ###########################################################
            # Juntar FFT + Gabor
            #
            image_result = image_gabor + image_fft
            for i in range(image_result.shape[0]):
                for j in range(image_result.shape[1]):
                    if (image_result[i, j] > 255):
                        image_result[i, j] = 255
                    else:
                        image_result[i, j] = 0

            # image_result = image_gabor # apenas GABOR
            cv2.imshow('RS', image_result)
            ###########################################################
            cv2.waitKey()

            ###########################################################
            ## Binarização (O valor de threshold aqui não tem efeitos
            # image = image_binarization.binarization(image_result, 170)
            ###########################################################
            ## Thinning
            #
            image_thin = bwmorph_thin.bwmorph_thin(1 - image_result / 255, 20)
            image_thin = (255 - image_thin * 255).astype("uint8")
            cv2.imshow('Thinning', image_thin)
            ###########################################################


            ###########################################################
            ## Extração de minucias

            # coordenadas (x,y) das bifurcações
            minuteas_array = feature_extraction.minuteas_extraction(image_thin)
            print len(minuteas_array)
            # geração de feature (d,ang,x,y)
            features_vector = feature_extraction.generate_features_vectors(
                minuteas_array)
            ###########################################################



            ###########################################################
            ## Escrever para fichiro csv
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
            ###########################################################
    f.close()


if __name__ == '__main__':
    main()
