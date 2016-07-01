import cv2
import numpy as np
import image_process_utils
import preprocessing
import argparse
import fft_enchance_image


def binarization(image, threshold):
    ret, image_binarized = cv2.threshold(
        image.astype('uint8'), threshold, 255, cv2.THRESH_BINARY)
    return image_binarized

def main():
    parser = argparse.ArgumentParser(
        description='Binariza fingerprint image specifying the threshold.')
    parser.add_argument(
        "image_path", help="Specify image path location")

    args = parser.parse_args()

    pre_processor = preprocessing.PreProcessFingerImage(args.image_path)
    pre_processor.process_image()
    image = pre_processor.get_preprocessed_image()
    image = fft_enchance_image.enhance_image(image,25,0,0.222)

    for t in np.arange(1,255,10):
        image_binarized = binarization(image,t)
        cv2.imshow('Binarized image with threshold=' + str(t), image_binarized)
        cv2.waitKey()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
