# coding=utf-8
import argparse
from os import walk

import cv2
import numpy as np

from fingerprint import *
from imageprocess import *


def writeHeader(f, min_minucias):
    header = 'label'
    for i in range(min_minucias * 4):
        header = header + ',' + str(i)
    f.write(header + '\n')

def main():
    parser = argparse.ArgumentParser(
        description='Read fingerprint images and enroll them.')
    parser.add_argument(
        "path", help="Specify the images path location")

    args = parser.parse_args()

    f = open('FeaturesDB/features.csv', 'wb')

    minuteas_numbers = []
    features_vectors = []
    labels = []

    for (dirpath, dirnames, filenames) in walk(args.path):
        for filename in filenames:
            label = dirpath.split('#')[1]
            labels.append(label)
            image_path = dirpath + '/' + filename

            ###########################################################
            # pre processamento de imagem
            pre_processor = preprocessing.PreProcessFingerImage(
                image_path)
            pre_processor.process_image()
            image = pre_processor.get_preprocessed_image()

            ###########################################################
            # Aplicação do metodo FFT
            image_fft = fft_enchance_image.enhance_image(image, 15, 0, 0.444)

            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
            image_fft = clahe.apply(image_fft)

            image_fft = image_binarization.binarization(image_fft, 170)

            ## Visualização
            cv2.namedWindow('FFT', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('FFT', 200, 200)
            cv2.imshow('FFT', image_fft)
            ###########################################################

            ###########################################################
            # Aplicação dos filtros de Gabor
            image_gabor = gabor_enhance_image.gabor_enhance_image(
                image, 3, 3.9, 8.9, 1.4)
            # 3,6,8.9,1
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

            #### Apenas Gabor
            # image_result = image_gabor
            # showImage( image_result, 'gabor1')
            # cv2.normalize(image_result, image_result, 0, 255, cv2.NORM_MINMAX)
            # showImage( image_result, 'gabor2')
            # image_result = image_binarization.binarization(image_result, 200)
            # showImage( image_result, 'gabor3')
            ####
            ### Apenas FFT
            #             image_result = image_fft
            ###

            image_result = image_binarization.binarization(image_result, 170)

            image_thin = bwmorph_thin.bwmorph_thin(1 - image_result / 255, 20)
            image_thin_show = np.uint8(255 - image_thin * 255)

            cv2.namedWindow('Thinning', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Thinning', 200, 200)
            cv2.imshow('Thinning', image_thin_show)
            ###########################################################

            ###########################################################
            ## Extração de minucias
            #
            # coordenadas (x,y) das bifurcações
            minuteas_array = feature_extraction.minuteas_extraction(1 - image_thin)

            # guardar o numero de minucias encontradas em cada iteração
            minuteas_numbers.append(len(minuteas_array))

            # geração de feature (d,ang,x,y)
            vector = feature_extraction.generate_features_vectors(minuteas_array)
            features_vectors.append(vector)
            ###########################################################

            image_color = cv2.merge((image, image, image))
            image_thin_inspect = cv2.merge((image_thin_show, image_thin_show, image_thin_show))

            for minutea in minuteas_array:
                cv2.rectangle(image_color, (minutea[0] - 2, minutea[1] - 2), (minutea[0] + 2, minutea[1] + 2),
                              (0, 255, 0), 1)
                cv2.rectangle(image_thin_inspect, (minutea[0] - 2, minutea[1] - 2), (minutea[0] + 2, minutea[1] + 2),
                              (0, 255, 0), 1)

            cv2.namedWindow('TDetected', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('TDetected', 200, 200)
            cv2.imshow('TDetected', image_thin_inspect)

            cv2.namedWindow('Detected', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Detected', 200, 200)
            cv2.imshow('Detected', image_color)

            cv2.waitKey()
            cv2.destroyAllWindows()

    ###########################################################
    ## Escrever para ficheiro csv
    #
    min_minucias = np.min(minuteas_numbers) - 1
    header = 'label'
    for i in range(min_minucias * 4):
        header = header + ',' + str(i)
    f.write(header + '\n')

    i = 0
    changeLabel = labels[0]
    labelNbr = 0
    for vector in features_vectors:
        print labels[i]
        counter = 0
        if changeLabel == labels[i]:
            labelNbr += 1
        else:
            labelNbr = 1
        changeLabel = labels[i]
        ff = open('FeaturesDB/' + str(labels[i]) + str(labelNbr) + '.dat', 'wb')
        writeHeader(ff, min_minucias)
        f.write(labels[i])
        ff.write(labels[i])
        i += 1
        for feature in vector:
            if counter == min_minucias:
                break
            image_features = ',{},{},{},{}'.format(feature[0], feature[1], feature[2], feature[3])
            f.write(image_features)
            ff.write(image_features)
            counter += 1
        f.write('\n')
        ff.write('\n')
        ff.close()
    f.close()
    ###########################################################


if __name__ == '__main__':
    main()
