import numpy as np
import cv2
import argparse
import preprocessing

def low_pass_filter(image, freq_cut):
    dft = cv2.dft(np.float32(image),flags = cv2.DFT_COMPLEX_OUTPUT)
    radius = freq_cut

    H = np.ones_like(dft)
    for i in range(dft.shape[0]):
        for j in range(dft.shape[1]):
            if np.sqrt(i**2 + j**2) >= radius:
                H[i,j] = 0

    fimage = dft * H

    image_enhanced = cv2.idft(fimage, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    return image_enhanced


def high_pass_filter(image, freq_cut):
    dft = cv2.dft(np.float32(image),flags = cv2.DFT_COMPLEX_OUTPUT)
    radius = freq_cut

    H = np.ones_like(dft)
    for i in range(dft.shape[0]):
        for j in range(dft.shape[1]):
            if np.sqrt(i**2 + j**2) <= radius:
                H[i,j] = 0

    fimage = dft * H

    image_enhanced = cv2.idft(fimage, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    return image_enhanced

def main():
    parser = argparse.ArgumentParser(description='Display Image Spectrum')
    parser.add_argument('image_path', help="Specify image path location")

    args = parser.parse_args()



    pre_processor = preprocessing.PreProcessFingerImage(args.image_path)
    pre_processor.process_image()
    image = pre_processor.get_preprocessed_image()
    cv2.imshow('Control Image',image)
    cv2.waitKey()

    for i in np.arange(1,200,5):
        image_enhanced = high_pass_filter(image, i)
        cv2.imshow('LPF ' + str(i), image_enhanced)
        cv2.waitKey()

    for i in np.arange(1,100,5):
        image_enhanced = high_pass_filter(image, i)
        cv2.imshow('HPF ' + str(i), image_enhanced)
        cv2.waitKey()


if __name__ == '__main__':
    main()
