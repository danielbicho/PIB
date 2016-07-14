import cv2
import numpy as np
import image_process_utils
import preprocessing
import argparse


def filter_fft(block, k):
    dft = cv2.dft(np.float32(block), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_tmp = dft * np.absolute(dft)**k
    block_back = cv2.idft(dft_tmp)
    block_back = cv2.magnitude(block_back[:, :, 0], block_back[:, :, 1])
    return block_back


def enhance_image(image, window, overlap, k):
    image_enhanced = image_process_utils.block_process_overlap(
        image, window, overlap, filter_fft, (k,))

    # Normalize values 0 a 255
    print "FFT Minimum value: %s; Maximum value: %s" % (np.min(image_enhanced), np.max(image_enhanced))
    image_enhanced *= 255.0 / image_enhanced.max()

    # Convert for uint8
    image_enhanced = image_enhanced.astype('uint8')

    return image_enhanced

def main():
    parser = argparse.ArgumentParser(
        description='Enhance fingerprint image with diferent parameters.')
    parser.add_argument(
        "image_path", help="Specify image path location")

    args = parser.parse_args()

    pre_processor = preprocessing.PreProcessFingerImage(args.image_path)
    pre_processor.process_image()
    image_pre = pre_processor.get_preprocessed_image()

    #gaussian_3 = cv2.GaussianBlur(image, (9,9), 10.0)
    #unsharp_image = cv2.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)

    dft = cv2.dft(np.float32(image_pre), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    dft_filtered = preprocessing.frequency_filters.blpf(dft_shift, 70, 20)
    f_ishift = np.fft.ifftshift(dft_filtered)
    image_pre = cv2.idft(
        f_ishift, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

    for k in np.linspace(0, 2, 5):
        for window in [20, 25, 35, 40, image_pre.shape[0]]:
            image_fft = enhance_image(image_pre, window, 2, k)
            cv2.imshow('FF Enhanced Image with k=' + str(k) +
                       ' window=' + str(window), image_fft)
            cv2.waitKey()
            cv2.destroyAllWindows()
            # matplotlib
            #plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
            #plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
            #plt.show()

if __name__ == '__main__':
    main()
