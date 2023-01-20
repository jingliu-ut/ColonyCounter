#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 16:42:57 2022

@author: ernestiu
"""
import numpy as np
from skimage import io, filters, img_as_float
import matplotlib.pyplot as plt
from skimage.morphology import disk, white_tophat, reconstruction
import os
from skimage.feature import peak_local_max
import scipy.ndimage as ndimage
import glob
import pandas as pd


def get_files():
    '''
    Get all the .tif files in the Inputs folder
    :return: a list of file names
    '''
    files = []
    os.chdir(os.path.join(home_dir, "Inputs"))
    for f in glob.glob("*.tif"):
        files.append(f)
    return files


def analyze(file):
    '''
    Analyze a given file. Save the analyzed image into the output folder and
    the count number into the output_dict
    :param file: name of file to be analyzed
    :return: None
    '''
    image_name = file.split(".")[0]

    # Raw image
    colony_img_raw = io.imread(file)

    #Smooth the image
    # (sigma determines the level of smoothing. Large sigma value corresponds
    # to more smoothing)
    colony_img = filters.gaussian(colony_img_raw, sigma=0.3, preserve_range=True)

    # This section aims to identify the plate boundary and remove it from the
    # analysis
    # Thresholding
    plate_mask = colony_img > filters.threshold_triangle(colony_img)
    # Fill holes
    plate_mask = ndimage.binary_fill_holes(plate_mask)
    # Erode by using a large structuring element
    # (disk() determines of size of disk for the erosion)
    plate_mask = ndimage.binary_erosion(plate_mask,
                                        structure=disk(50),
                                        iterations=1)

    # Apply the mask onto the image
    colony_img[np.where(plate_mask==False)] = 0

    # Apply top hat reconstruction
    top_hat_img = top_hat_recon(colony_img, colony_size)

    # Identify the colonies on the plate
    # (min_distance specifies the minimum distance between two colonies)
    coordinates = peak_local_max(top_hat_img,
                                 exclude_border=True,
                                 threshold_rel=0.1,
                                 min_distance=min_distance)

    #Plotting
    plt.rcParams["figure.dpi"] = 150
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.imshow(colony_img_raw, cmap='gray')
    plt.plot(coordinates[:, 1], coordinates[:, 0], 'r.', markersize=2, alpha=0.3)
    plt.savefig(output_dir + '/' + image_name + ' results.png',
                bbox_inches='tight', pad_inches=0)

    output_dict['Name'].append(image_name)
    output_dict['Count'].append(len(coordinates))

    print(f"The number of colonies for {image_name} is: {len(coordinates)}")


def top_hat_recon(img, colony_size):
    '''
    This function applies a top hat transformation to the img followed by an
    image reconstruction. This removes background signal and highlight the
    colonies.
    :param img: 2d array
    :param colony_size: size of colony
    :return: transformed_img: 2d array
    '''
    # selem specifies the colony size
    top_hat = white_tophat(img, selem=disk(colony_size))
    top_hat_float = img_as_float(top_hat.copy())
    seed = np.copy(top_hat_float)
    seed[1:-1, 1:-1] = top_hat_float.min()
    mask = top_hat_float
    recon = reconstruction(seed, mask, method='dilation')
    transformed_img = (top_hat - recon).astype(img.dtype)
    return transformed_img


def main():
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    files = get_files()

    for f in files:
        # Print progress
        print(f"Analyzing {files.index(f) + 1} out of {len(files)}")
        analyze(f)

    print(f"Saving outputs to Output.csv")
    output_data = pd.DataFrame(output_dict)
    output_data.to_csv(os.path.join(output_dir, "Output.csv"), index=False)


if __name__ == '__main__':
    home_dir = os.getcwd()
    output_dir = os.path.join(home_dir, "Outputs")
    output_dict = {'Name': [], 'Count': []}

    # Parameters
    colony_size = 5
    min_distance = 2

    main()


