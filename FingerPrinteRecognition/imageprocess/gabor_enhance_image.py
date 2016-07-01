import cv2
import numpy as np
import image_process_utils
import preprocessing
import argparse

def overlay_images(i1, i2):
    for i in range(i1.shape[0]):
        for j in range(i1.shape[1]):
            i1[i,j] += i2[i,j]
    return i1

def gabor_enhance_image(image, ksize, sigma, lambd, gamma):
    theta = [0, 11.2500, 22.5000, 33.7500, 45, 56.2500, 67.5000, 78.7500,
             90, 101.2500, 112.5000, 123.7500, 135, 146.2500, 157.5000, 168.7500]
    image_filtered = image

    #for theta in np.arange(0, np.pi, np.pi / 32):
    for i in np.arange(0,len(theta),2):
        kernel = cv2.getGaborKernel(
            (ksize, ksize), sigma, theta[i], lambd, gamma)
        fimage = cv2.filter2D(image, cv2.CV_8U, kernel)
        np.maximum(image_filtered, fimage, image_filtered)
        #image_filtered = image_filtered + fimage
        #image_filtered = overlay_images(image_filtered, fimage)
        cv2.imshow('Gabor contributions', fimage)
        cv2.waitKey()

    #image_filtered *= 255.0 / image_filtered.max()

    # Convert for uint8
    #image_filtered = image_filtered.astype('uint8')
    #cv2.imshow('Gabor filtered image', image_filtered)
    #cv2.waitKey()

    return image_filtered


def main():
    parser = argparse.ArgumentParser(
        description='Enhance fingerprint using gabor filter.')
    parser.add_argument(
        "image_path", help="Specify image path location")

    args = parser.parse_args()
    pre_processor = preprocessing.PreProcessFingerImage(args.image_path)
    pre_processor.process_image()
    image = pre_processor.get_preprocessed_image()

    cv2.imshow('Image Pre Processed', image)
    cv2.waitKey()

    image_enhanced = gabor_enhance_image(image, 3, 3.9, 8.9, 1.4)

    cv2.imshow('Last Gabor filtered image', image_enhanced)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
