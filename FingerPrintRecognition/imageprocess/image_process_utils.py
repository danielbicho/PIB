import cv2
import numpy as np

def unsharp_masking(image, k):

    image_filtered = cv2.GaussianBlur(image,(7,7),1)
    cv2.imshow('blured', image_filtered)
    mask = image - image_filtered
    cv2.imshow('mask', mask)
    image_result = image + k * mask
    return image_result



def block_process_overlap(a, blocksize, overlap, filt, args):
    b = np.empty(a.shape)

    for row in range(0, a.shape[0] - overlap, blocksize - overlap ):
        for col in range(0, a.shape[1] - overlap, blocksize - overlap ):
            b[col:col + blocksize, row:row + blocksize] = (
                filt(a[col:col + blocksize, row:row + blocksize], *args))
    return b


def block_process(a, blocksize, filt, args):
    b = np.empty(a.shape)
    for row in xrange(0, a.shape[0], blocksize):
        for col in xrange(0, a.shape[1], blocksize):
            b[col:col + blocksize, row:row + blocksize] = (
                filt(a[col:col + blocksize, row:row + blocksize], *args))
    return b

def crop_image_sides( image, width ,height):
     a = int(1 + np.floor(image.shape[0] * width))
     b = int(image.shape[0] - np.floor(image.shape[0] * width))
     c = int(1 + np.floor(image.shape[1] * height))
     d = int(image.shape[1] - np.floor(image.shape[1] * height))
     return image[a:b,c:d]

def crop_around_center(image, width, height):
    """
    Given a NumPy / OpenCV 2 image, crops it to the given width and height,
    around it's centre point
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if(width > image_size[0]):
        width = image_size[0]

    if(height > image_size[1]):
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]

def contrast_streching(image):

    image = image.astype('uint8')
    high = np.max(image)
    low = np.min(image)

    x = np.linspace(0,255,256);

    declive = 255./(high - low);
    ordenada = - declive * low;

    # build LUT table
    table = declive * x + ordenada;
    table[0:low] = 0;
    table[high:256] = 255;

    table = np.array([table.astype('uint8')])
    image_enchanted = cv2.LUT(image,table)

    return image_enchanted

def binarize_mean(img):

    mean = np.mean(img) - 10

    img_binarize = np.empty([img.shape[0], img.shape[1]])

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] >= mean:
                img_binarize[i,j] = 1
            else:
                img_binarize[i,j] = 0
    return img_binarize

def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for x in xrange(0, image.shape[0], stepSize):
        for y in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[ y:y + windowSize[0],x:x + windowSize[1]])

def invertChannels(img):
    b,g,r = cv2.split(img) # split channels
    return cv2.merge((r,g,b)) # merge in rgb order to display with matplotlib


# power law tranformation
def power_law_lut(c, g):
    table = np.zeros(256,'uint8')

    table = np.array([( c * (i / 255.0) ** g) * 255 for i in np.arange(0, 256)]).astype("uint8")

    return np.array([table.astype('uint8')])


# mean square error
def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    return err
