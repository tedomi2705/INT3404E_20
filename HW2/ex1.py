import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import os


def read_img(img_path):
    """
    Read grayscale image
    Inputs:
    img_path: str: image path
    Returns:
    img: cv2 image
    """
    return cv2.imread(img_path, 0)


def padding_img(img, filter_size=3):
    """
    The surrogate function for the filter functions.
    The goal of the function: replicate padding the image such that when applying the kernel with the size of filter_size, the padded image will be the same size as the original image.
    WARNING: Do not use the exterior functions from available libraries such as OpenCV, scikit-image, etc. Just do from scratch using function from the numpy library or functions in pure Python.
    Inputs:
        img: cv2 image: original image
        filter_size: int: size of square filter
    Return:
        padded_img: cv2 image: the padding image
    """
    height, width = img.shape
    padding_size = filter_size // 2
    # Create a padded image with zeros
    padded_img = np.zeros(
        (height + 2 * padding_size, width + 2 * padding_size), dtype=img.dtype
    )

    # Copy the original image into the center of the padded image
    padded_img[
        padding_size : padding_size + height, padding_size : padding_size + width
    ] = img

    # Replicate padding for borders
    padded_img[:padding_size, padding_size : padding_size + width] = img[0, :]  # Top
    padded_img[padding_size + height :, padding_size : padding_size + width] = img[
        height - 1, :
    ]  # Bottom
    padded_img[:, :padding_size] = padded_img[
        :, padding_size : padding_size + 1
    ]  # Left
    padded_img[:, padding_size + width :] = padded_img[
        :, padding_size + width - 1 : padding_size + width
    ]  # Right

    return padded_img


def mean_filter(img, filter_size=3):
    """
    Smoothing image with mean square filter with the size of filter_size. Use replicate padding for the image.
    WARNING: Do not use the exterior functions from available libraries such as OpenCV, scikit-image, etc. Just do from scratch using function from the numpy library or functions in pure Python.
    Inputs:
        img: cv2 image: original image
        filter_size: int: size of square filter,
    Return:
        smoothed_img: cv2 image: the smoothed image with mean filter.
    """
    padded_img = padding_img(img, filter_size)

    smoothed_img = np.zeros_like(img)
    height, width = padded_img.shape
    pad_size = filter_size // 2

    for x in range(pad_size, height - pad_size):
        for y in range(pad_size, width - pad_size):
            neighborhood = padded_img[x : x + filter_size, y : y + filter_size]
            median_value = np.mean(neighborhood)
            smoothed_img[x - pad_size, y - pad_size] = median_value

    return smoothed_img


def median_filter(img, filter_size=3):
    """
    Smoothing image with median square filter with the size of filter_size. Use replicate padding for the image.
    WARNING: Do not use the exterior functions from available libraries such as OpenCV, scikit-image, etc. Just do from scratch using function from the numpy library or functions in pure Python.
    Inputs:
        img: cv2 image: original image
        filter_size: int: size of square filter
    Return:
        smoothed_img: cv2 image: the smoothed image with median filter.
    """
    padded_img = padding_img(img, filter_size)
    smoothed_img = np.zeros_like(img)
    height, width = padded_img.shape
    pad_size = filter_size // 2

    for x in range(pad_size, height - pad_size):
        for y in range(pad_size, width - pad_size):
            neighborhood = padded_img[x : x + filter_size, y : y + filter_size]
            median_value = np.median(neighborhood)
            smoothed_img[x - pad_size, y - pad_size] = median_value

    return smoothed_img


def psnr(gt_img, smooth_img):
    """
    Calculate the PSNR metric
    Inputs:
        gt_img: cv2 image: groundtruth image
        smooth_img: cv2 image: smoothed image
    Outputs:
        psnr_score: PSNR score
    """
    gt_img = gt_img.astype(np.float64)
    smooth_img = smooth_img.astype(np.float64)

    mse = np.mean(np.square(gt_img - smooth_img))

    max_pixel = np.max(gt_img)

    psnr_score = 20 * np.log10(max_pixel) - 10 * np.log10(mse)

    return psnr_score


def show_res(before_img, after_img):
    """
    Show the original image and the corresponding smooth image
    Inputs:
        before_img: cv2: image before smoothing
        after_img: cv2: corresponding smoothed image
    Return:
        None
    """
    plt.figure(figsize=(12, 9))
    plt.subplot(1, 2, 1)
    plt.imshow(before_img, cmap="gray")
    plt.title("Before")

    plt.subplot(1, 2, 2)
    plt.imshow(after_img, cmap="gray")
    plt.title("After")
    plt.show()


if __name__ == "__main__":
    img_noise = "ex1_images/noise.png"  # <- need to specify the path to the noise image
    img_gt = "ex1_images/ori_img.png"  # <- need to specify the path to the gt image
    img = read_img(img_noise)
    gt = read_img(img_gt)
    filter_size = 3

    # Mean filter
    mean_smoothed_img = mean_filter(img, filter_size)
    show_res(img, mean_smoothed_img)
    print("PSNR score of mean filter: ", psnr(gt, mean_smoothed_img))

    # Median filter
    median_smoothed_img = median_filter(img, filter_size)
    show_res(img, median_smoothed_img)
    print("PSNR score of median filter: ", psnr(gt, median_smoothed_img))