import cv2
import numpy as np
import image_process_utils
import frequency_filters
import argparse


class PreProcessFingerImage():

    def __init__(self, image_path):
        img = cv2.imread(image_path)
        self.image = img
        self.image_pre = None

    def process_image(self):
        # convert to grayscale
        image_pre = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # crop image banners
        image_pre = image_process_utils.crop_around_center(image_pre, 150, 150)
        #image_pre = image_process_utils.crop_image_sides( image_pre, 0, 0.12)

        # filter with blpf
        dft = cv2.dft(np.float32(image_pre), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        dft_filtered = frequency_filters.blpf(dft_shift, 70, 20)
        f_ishift = np.fft.ifftshift(dft_filtered)
        image_pre = cv2.idft(
            f_ishift, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

        # convert to uint8
        #image_pre = cv2.convertScaleAbs(image_pre)

        # contrast streching
        image_pre = image_process_utils.contrast_streching(image_pre)

        # histogram equalizer
        #image_pre = cv2.equalizeHist(image_pre)

        # adptative histogram equalizer
        #clahe = cv2.createCLAHE()
        #image_pre = clahe.apply(image_pre)

        self.image_pre = image_pre

    def get_original_image(self):
        return self.image

    def get_preprocessed_image(self):
        return self.image_pre

    def get_original_image(self):
        return self.image


def main():
    parser = argparse.ArgumentParser(
        description='Pre process image to finger print recgonition.')
    parser.add_argument(
        "image_path", help="Specify image path location")

    args = parser.parse_args()

    pre_processor = PreProcessFingerImage(args.image_path)
    pre_processor.process_image()
    image_original = pre_processor.get_original_image()
    cv2.imshow('Original Image', image_original)

    image = pre_processor.get_preprocessed_image()

    cv2.imshow('Pre Processed Image', image)
    cv2.waitKey()

if __name__ == '__main__':
    main()
