import cv2
import numpy as np
import image_process_utils
import argparse

class PreProcessFingerImage():

    def __init__(self, image_path):
        img = cv2.imread(image_path)
        self.image = img
        self.image_pre = None

    def process_image(self):
        # crop image
        image_pre = image_process_utils.crop_around_center(self.image, 150, 150)

        # convert to grayscale
        b,g,r = cv2.split(image_pre)
        image_pre = image_pre[:,:,0]

        # contrast streching
        image_pre = image_process_utils.contrast_streching(image_pre)

        # adptative histogram equalizer
        clahe = cv2.createCLAHE()
        image_pre = clahe.apply(image_pre)

        self.image_pre = image_pre

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
    image = pre_processor.get_preprocessed_image()
    
    cv2.imshow('Pre Processed Image', image)
    cv2.waitKey()

if __name__ == '__main__':
    main()
