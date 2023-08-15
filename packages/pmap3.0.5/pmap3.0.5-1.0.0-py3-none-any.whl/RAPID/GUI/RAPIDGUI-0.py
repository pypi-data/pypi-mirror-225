import os
import webbrowser
import ast
import copy
import glob
import time
from argparse import Namespace
from shutil import copyfile
from skimage import img_as_ubyte
import shutil
import stat
import configparser
import matplotlib
from matplotlib import patches
import networkx as nx
import pandas as pd
import seaborn as sns
import torch
import umap
import RAPID.GUI.GUIUtils as GUIUtils
from RAPID.spatialanalysis import KNN
from RAPID.network import IID_loss
from RAPID.Impressionist import runRAPIDzarr
from RAPID.network import objectmodels
from RAPID.util.utils import generate_colormap, denoise_img, preprocess, save_preprocess, run_pca
from RAPID.util.mst import prep_for_mst, generate_mst
from RAPID.network.model import load_checkpoint, weight_init, RAPIDMixNet
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QColor
from matplotlib.path import Path
from pandas import DataFrame
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel, QWidget, QGridLayout, QDockWidget, QAction, QAbstractScrollArea
from scipy.spatial import distance
from skimage import morphology, measure
from skimage.color import label2rgb
from sklearn.preprocessing import StandardScaler
from torch import optim
from vispy.color import ColorArray
from vispy.color import Colormap
import napari
from napari.layers import Image

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from numpy import math, unicode
import zarr
import cv2 as cv
from dask import array as da
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem
from scipy import ndimage as ndi, ndimage
from imageio import imread
import phenograph
import tifffile
import torch.nn as nn
import numpy as np
from magicgui import magicgui

### TODO: Test this (imaris files in particular).
#from napari_pims_bioformats import napari_get_reader
from napari_bioformats import napari_get_reader
from napari.utils.progress import progress
from napari.layers import Image
import io
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import gc
import vaex
import vaex.ml

gc.enable()

### TODO: Maybe add volumetric imaging in the documentation.


class RAPIDGUI():
    """
    Class containing all functions available in the RAPID GUI, as well as core functions/attributes.
    """

    ### TODO: Change variable names to be more standard
    def __init__(self):
        self.addedtable = False
        self.addwhenchecked = True
        self.editedimage = False
        self.hasloadedpixel = False
        self.imagehasbeenloaded = False
        self.loadingenv = False

        self.actionloggerpath = ""
        self.biaxialcount = 1
        self.displayselectedcount = 1
        self.editimagepath = ""
        self.index = 0
        self.listindex = 0
        self.mode = ""
        self.numclasses = 0
        self.numimgs = 0
        self.nummarkers = 0
        self.objecttraincount = 0
        self.pixeltraincount = 0
        self.res = 0
        self.segmentcount = 0
        self.selectedregioncount = 1
        self.tableimgcount = 0
        self.umapcount = 1

        self.annotatedclusters = []
        self.cellindices = []
        self.cellnums = []
        self.columnheaders = ['ID']
        self.combcellnums = []
        self.coordinates = []
        self.cortabs = []
        self.curimgs = []
        self.currentlyselectedcells = []
        self.currentlyselectedobjectclusters = []
        self.currentlyselectedpixelclusters = []
        self.datalist = []
        self.datanorm = []
        self.datavals = np.array([])
        self.editactions = []
        self.filenames = []
        self.flipimg = []
        self.fulltab = pd.DataFrame()
        self.greyobjects = []
        self.greypixels = []
        self.groupslist = []
        self.groupsnames = ['Individual']
        self.imageshapelist = []
        self.lowerbounds = []
        self.lowerboundslist = []
        self.markers = []
        self.maximageshape = np.array([])
        self.maxvalsobject = []
        self.maxvalspixel = []
        self.maxvalssegment = []
        self.mergedimagespaths = []
        self.mergememmarkers = []
        self.mergenucmarkers = []
        self.minvalsobject = []
        self.minvalspixel = []
        self.minvalssegment = []
        self.objectclusterdirectories = []
        self.objectclusterindices = []
        self.objectclusternums = []
        self.objectclusters = []
        self.objectcolor = []
        self.objectdatalist = []
        self.objectimgnames = []
        self.objectplots = []
        self.objecttrainlist = []
        self.order = []
        self.orders = []
        self.pixelbasedclusters = []
        self.pixelclusterdirectories = []
        self.pixelclusterindices = []
        self.pixelclustermarkers = []
        self.pixelclusternums = []
        self.pixelcolor = []
        self.Qtab = []
        self.sampleshapes = []
        self.segmentationindicesinumap = []
        self.segmentcounts = []
        self.segmentedimgpaths = []
        self.tabdata = []
        self.tableimagenames = ['None']
        self.tableorder = []
        self.umapplots = []
        self.upperbounds = []
        self.upperboundslist = []
        self.verticalheaderlabels = np.array([])
        self.xmins = []
        self.xmaxs = []
        self.ymins = []
        self.ymaxs = []

    def apply_contrast_limits(self, img, cl):
        """
        Apply both lower- and upper-bound thresholds to an image array.

        Args:
            img (numpy.ndarray): Array for image data having contrast limits applied to it.
            cl (iterable): List containing the lower and upper bound values for the contrast limits being applied.
        """
        lower = cl[0]
        upper = cl[1]
        img[img < lower] = lower
        img[img > upper] = upper
        img = (img - lower) / (upper - lower) * 255
        img[img < 0] = 0
        img[img > 255] = 255
        return img.astype(np.uint8)

    def apply_edits(self, editactions, imgindex=-1):
        """
        Apply any changes made in the Edit Image popup window.

        Args:
            editactions (list): Sequence of edits to be made for each image.
            imgindex (int, optional): Index of image to apply edits to. If -1, apply across all images (Default: -1).
        """
        imgnums = [i for i in range(self.numimgs) if not i == imgindex]
        for i in range(self.nummarkers):
            for edits in editactions:
                if edits[0][i] == "Gaussian":
                    for j in imgnums:
                        self.viewer.layers[i].data[j, :, :] = ndimage.gaussian_filter(
                            self.viewer.layers[i].data[j, :, :], [1, 1])
                elif edits[0][i] == "Median":
                    for j in imgnums:
                        self.viewer.layers[i].data[j, :, :] = ndimage.median_filter(self.viewer.layers[i].data[j, :, :],
                                                                                    [1, 1])
                elif edits[0][i] == "Denoise":
                    self.viewer.layers[i].data[imgnums, :, :] = np.moveaxis(
                        denoise_img(np.moveaxis(self.viewer.layers[i].data[imgnums, :, :], 0, -1).astype(float),
                                    [j for j in range(len(imgnums))]), -1, 0)
                elif edits[0][i] == "Binarize":
                    self.viewer.layers[i].data[imgnums, :, :] = np.moveaxis(
                        denoise_img(np.moveaxis(self.viewer.layers[i].data[imgnums, :, :], 0, -1).astype(float),
                                    [j for j in range(len(imgnums))]), -1, 0)
                    self.viewer.layers[i].data[imgnums, :, :][self.viewer.layers[i].data[imgnums, :, :] > 0] = 255
            if not imgindex == -1:
                self.viewer.layers[i].data[imgindex, :, :] = self.edit_viewer.layers[i].data

    def apply_RAPID_pixel(self, tab, args, colors, outpath=""):
        """
        Populate the viewer and the table with results from RAPID-P clustering.

        Args:
            tab (numpy.ndarray): Data being used to populate the table.
            args (Namespace): Additional user-defined parameters used for training.
            colors (numpy.ndarray): Array (#clusters x 3) of RGB values for each cluster.
            outpath (str): Path to folder where results will be saved.
        """
        if self.numimgs > 1:
            data = np.zeros((self.numimgs + 1, args.ncluster, tab.shape[1] - 2))
        else:
            data = np.zeros((self.numimgs, args.ncluster, tab.shape[1] - 2))
        for i in range(self.numimgs):
            data[i, :, :] = tab[args.ncluster * i:args.ncluster * (i + 1), 2:]
            self.tableimagenames.append(
                f"Pixel Cluster {self.pixeltraincount + 1} - {self.filenames[i].split('/')[-1]}")
            self.pixelclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
        if 'None' in self.tableimagenames:
            self.tableimagenames.remove('None')
        if self.numimgs > 1:
            self.tableimagenames.append(f"Pixel Cluster {self.pixeltraincount + 1} - Combined Average")
            self.pixelclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
            table = np.zeros((args.ncluster, tab.shape[1]))
            for i in range(args.ncluster):
                npixels = 0
                for j in range(self.numimgs):
                    npixels += tab[args.ncluster * j + i, 2]
                for j in range(self.numimgs):
                    table[i, 3:] += tab[args.ncluster * j + i, 3:] * float(tab[args.ncluster * j + i, 2] / npixels)
                table[i, 2] = npixels
            data[-1, :, :] = table[:, 2:]
            for i in range(self.numimgs + 1):
                minvals = []
                maxvals = []
                for j in range(data.shape[2] - 1):
                    minvals.append(np.min(data[i, :, j + 1]))
                    maxvals.append(np.max(data[i, :, j + 1]))
                self.minvalspixel.append(copy.deepcopy(minvals))
                self.maxvalspixel.append(copy.deepcopy(maxvals))
                self.lowerboundslist.append(copy.deepcopy(minvals))
                self.upperboundslist.append(copy.deepcopy(maxvals))
        elif self.numimgs == 1:
            minvals = []
            maxvals = []
            for j in range(data.shape[2] - 1):
                minvals.append(np.min(data[0, :, j + 1]))
                maxvals.append(np.max(data[0, :, j + 1]))
            self.minvalspixel.append(copy.deepcopy(minvals))
            self.maxvalspixel.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
        if not self.addedtable:
            self.lowerbounds = copy.deepcopy(self.minvalspixel[self.index])
            self.upperbounds = copy.deepcopy(self.maxvalspixel[self.index])
            self.update_table(data[0, :, :], self.lowerbounds, self.upperbounds, data.shape[1])
        clusterlist = []
        s = self.greypixels[-1].shape
        volimage = np.zeros((s[0], s[1], s[2], 3)).astype(np.uint8)
        # color = generate_colormap(args.ncluster + 1)
        for j in range(args.ncluster):
            mask = self.greypixels[-1] == j
            volimage[mask] = colors[j, :]
            if np.count_nonzero(volimage[mask]) > 0:
                clusterlist.append([j])
        self.order = []
        for i in range(data.shape[1]):
            self.order.append(i)
        for i in range(len(data)):
            self.datalist.append(data[i, :, :])
        self.pixelclusternums = copy.deepcopy(self.order)
        if outpath != "":
            for i in range(self.numimgs):
                if self.flipimg[i]:
                    saveimg = np.moveaxis(volimage[i, :, :, :], 0, 1)
                else:
                    saveimg = volimage[i, :, :, :]
                tifffile.imwrite(os.path.join(outpath, f"Pred_{self.filenames[i].split('/')[-1]}_Pred.tif"), saveimg)

        # Allow user to decide whether to add the labeled and/or colored image.
        selectimagesadded = GUIUtils.GreyColorImages()
        selectimagesadded.exec()
        if not selectimagesadded.OK:
            return

        # Add the segmented image(s) to the main GUI viewer window.
        self.set_invisible(self.viewer)
        if selectimagesadded.grey:
            self.viewer.add_image(self.greypixels[-1] + 1, name=f"Pixel Cluster IDs {self.pixeltraincount + 1}",
                                  blending="additive", contrast_limits=[0, np.max(self.greypixels[-1]) + 1])
        if selectimagesadded.color:
            self.viewer.add_image(volimage, name=f"Pixel Clusters {self.pixeltraincount + 1}", blending="additive")
        self.viewer.layers[-1].visible = True

        # Update any necessary variables.
        self.viewer.status = "RAPID clustering done"
        self.pixelbasedclusters.append(True)
        self.pixelcolor.append(colors)
        self.annotatedclusters.append([])
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Pixel Cluster {self.pixeltraincount + 1} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()

    def biaxial_gate(self):
        """
        Generate a biaxial plot according to cell markers and normalization algorithm defined by the user.
        """
        # User must first run object-based segmentation in order to generate a Biaxial Plot.
        if self.segmentcount == 0:
            GUIUtils.display_error_message("You must segment before running biaxial gating",
                                           "Biaxial gating cannot be done until the image has been segmented")
            return

        # Prompt user to select which cell markers to use as parameters for the plot and vertex coloring.
        biaxial = GUIUtils.BiaxialGate(self.markers, self.objectimgnames, self.objecttraincount > 0,
                                       self.groupsnames[1:])
        biaxial.exec()
        if not biaxial.OK:
            return
        curimg = biaxial.imageindex
        self.curimgs.append(curimg * self.numimgs)

        # Compile quantified cells from each individual image into one combined data array.
        numcells = 0
        for i in range(self.numimgs):
            numcells += self.Qtab[curimg * self.numimgs + i].shape[0]
        fullquantified = np.zeros((numcells, self.Qtab[curimg * self.numimgs].shape[1]))
        count = 0
        cellsperimage = []
        for i in range(self.numimgs):
            cellsincurrimg = []
            index1 = biaxial.dict.get(biaxial.chan1)
            index2 = biaxial.dict.get(biaxial.chan2)
            currentimage = self.Qtab[curimg * self.numimgs + i]
            for j in range(count, count + self.Qtab[curimg * self.numimgs + i].shape[0]):
                cellsincurrimg.append(j)
            fullquantified[count:count + currentimage.shape[0], :] = currentimage
            count += currentimage.shape[0]
            cellsperimage.append(cellsincurrimg)

        # Remove rows with NaN values from the data array
        removerows = np.unique(np.argwhere(np.isnan(fullquantified[:, [index2, index1]]))[:, 0])
        fullquantified = np.delete(fullquantified, removerows, axis=0)
        for i in range(self.numimgs):
            for cellnum in removerows:
                if cellnum in cellsperimage[i]:
                    cellsperimage[i].remove(cellnum)

        # Color data points on a red-blue gradient according to expression of a defined cell marker, if applicable.
        name = ""
        cols = np.zeros((len(fullquantified), 3)).astype(np.float)
        if biaxial.color != '---(Optional)---':
            colorindex = biaxial.dict.get(biaxial.color)
            max = np.percentile(fullquantified[:, colorindex], 97)
            min = np.min(fullquantified[:, colorindex])
            for i in range(len(fullquantified)):
                cols[i, 0] = (fullquantified[i, colorindex] - min) / (max - min)
                cols[i, 2] = 1.0 - (fullquantified[i, colorindex] - min) / (max - min)
            cols[cols > 1.0] = 1.0
            cols[cols < 0.0] = 0.0
            name = " (" + biaxial.color + ")"
        cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)

        # Perform any necessary normalization and define vertices that will be plotted on the biaxial scatterplot
        x = fullquantified[:, index1]
        y = fullquantified[:, index2]
        if biaxial.norm == "Log10":
            x = np.log10(x * 9.0 + 1.0)
            y = np.log10(y * 9.0 + 1.0)
        elif biaxial.norm == "Log2":
            x = np.log2(x + 1.0)
            y = np.log2(y + 1.0)
        x = np.append(x, [-0.05 * np.max(x), 1.05 * np.max(x)])
        y = np.append(y, [-0.05 * np.max(y), 1.05 * np.max(y)])

        # Use resulting points to generate a scatterplot and add it to the viewer.
        plt.figure(figsize=(10, 10))
        plt.scatter(x, y, s=1, c=cols)
        plt.show(block=False)
        plt.title("Biaxial Gate" + name)
        plt.xlabel(str(biaxial.chan1))
        plt.ylabel(str(biaxial.chan2))
        dir = GUIUtils.create_new_folder("Biaxial_", self.outputfolder)
        plt.savefig(os.path.join(dir, "Biaxial.png"), format="PNG", dpi=300)
        im = cv.imread(os.path.join(dir, "Biaxial.png"))
        im = np.asarray(im)
        im[:, :, [0, 2]] = im[:, :, [2, 0]]
        locs = np.where((im[:, :, 0] == 242) & (im[:, :, 1] == 255) & (im[:, :, 2] == 242))
        self.xmins.append(np.min(locs[0]))
        self.xmaxs.append(np.max(locs[0]))
        self.ymins.append(np.min(locs[1]))
        self.ymaxs.append(np.max(locs[1]))
        self.set_invisible(self.viewer)
        self.viewer.add_image(im, name=f"Biaxial {self.biaxialcount} ({biaxial.chan1} vs. {biaxial.chan2})",
                              blending="additive")

        # If given segmented image iteration has been clustered, check if the user elected to use clustering as
        # a basis for vertex coloring.
        if len(self.objecttrainlist[curimg]) > 0:
            # If the user is coloring according to cluster assignment, prompt to define which clustering
            # iteration is being used.
            if biaxial.colorbyindivclusters or biaxial.colorbycombclusters:
                if len(self.objecttrainlist[curimg]) > 1:
                    iteration = GUIUtils.ObjectTrainIteration(len(self.objecttrainlist[biaxial.imageindex]))
                    iteration.exec()
                    if not iteration.OK:
                        return
                    startindex = self.objecttrainlist[biaxial.imageindex][iteration.iteration]
                    GUIUtils.log_actions(self.actionloggerpath,
                                         f"Biaxial Gating: Axis 1 ({biaxial.chan1}), Axis 2 ({biaxial.chan2}), Color ({biaxial.color}), "
                                         f"Normalization ({biaxial.norm}), Segmentation Iteration ({biaxial.imageindex}), "
                                         f"Coloring ({biaxial.colorbyindivclusters}, {biaxial.colorbycombclusters}, {biaxial.colorbygroups}), "
                                         f"Iteration ({iteration.iteration})")
                else:
                    GUIUtils.log_actions(self.actionloggerpath,
                                         f"Biaxial Gating: Axis 1 ({biaxial.chan1}), Axis 2 ({biaxial.chan2}), Color ({biaxial.color}), "
                                         f"Normalization ({biaxial.norm}), Segmentation Iteration ({biaxial.imageindex}), "
                                         f"Coloring ({biaxial.colorbyindivclusters}, {biaxial.colorbycombclusters}, {biaxial.colorbygroups})")
                    startindex = self.objecttrainlist[biaxial.imageindex][0]
                clusternums = []
                for i in range(self.numimgs):
                    curclusternums = self.objectclusters[startindex * self.numimgs + i]
                    for n in curclusternums:
                        clusternums.append(n - 1)
                numclusters = len(np.unique(self.greyobjects[startindex])) - 1

            # If selected by user, add an additional stack of scatterplots with vertices colored red if
            # corresponding to a cell in the respective cluster, or blue otherwise.
            if biaxial.colorbyindivclusters:
                self.set_invisible(self.viewer)
                pathlist = []
                for i in range(numclusters):
                    plt.figure(figsize=(10, 10))
                    col = np.zeros((len(fullquantified), 3)).astype(np.float)
                    for j in range(len(fullquantified)):
                        if int(clusternums[j]) == i:
                            col[j, 0] = 1.0
                            col[j, 2] = 0.0
                        else:
                            col[j, 0] = 0.0
                            col[j, 2] = 1.0
                    col = np.append(col, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                    plt.scatter(x, y, s=1, c=col, marker='.')
                    ax = plt.gca()
                    plt.title(f"Cluster {i + 1}")
                    plt.xlabel(str(biaxial.chan1))
                    plt.ylabel(str(biaxial.chan2))
                    plt.savefig(os.path.join(dir, f"BiaxialCluster{i + 1}.png"), format="PNG", dpi=300)
                    pathlist.append(os.path.join(dir, f"BiaxialCluster{i + 1}.png"))
                imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
                self.viewer.add_image(imx,
                                      name=f"Biaxial {self.biaxialcount} ({biaxial.chan1} vs. {biaxial.chan2}) (Individual Clusters)",
                                      blending="additive")

            # If selected by user, add an additional scatterplot colored according to cluster assignment.
            if biaxial.colorbycombclusters:
                self.set_invisible(self.viewer)
                col_list = generate_colormap(numclusters + 1)
                cols = np.zeros((len(fullquantified), 3)).astype(np.float)
                for i in range(len(fullquantified)):
                    cols[i, :] = col_list[int(clusternums[i]), :] / np.array([255.0, 255.0, 255.0])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=cols, marker='.')
                ax = plt.gca()
                plt.title("Clusters")
                plt.xlabel(str(biaxial.chan1))
                plt.ylabel(str(biaxial.chan2))
                filename = os.path.join(dir, "BiaxialClusters.png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename, pilmode='RGB'),
                                      name=f"Biaxial {self.biaxialcount} ({biaxial.chan1} vs. {biaxial.chan2}) (Combined Clusters)",
                                      blending="additive")

        # If selected by user, add an additional scatterplot colored according to group assignment.
        if biaxial.colorbygroups != []:
            for ind in biaxial.colorbygroups:
                group = self.groupslist[ind + 1]
                imggroupnames = list(group.values())
                shufflelist = [list(group.keys()).index(name) for name in
                               [os.path.split(fn)[-1] for fn in self.filenames]]
                nameindices = list(set(imggroupnames))
                numgroups = len(nameindices)
                imagegroups = []
                for i in range(self.numimgs):
                    imagegroups.append(nameindices.index(imggroupnames[i]))
                imagegroups = [imagegroups[i] for i in shufflelist]
                self.set_invisible(self.viewer)
                col_list = generate_colormap(numgroups + 1)
                cols = np.zeros((len(fullquantified), 3)).astype(np.float)
                count = 0
                for i in range(self.numimgs):
                    for j in range(count, count + len(cellsperimage[i])):
                        cols[j, :] = col_list[imagegroups[i], :] / np.array([255.0, 255.0, 255.0])
                    count += len(cellsperimage[i])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=cols, marker='.')
                ax = plt.gca()
                plt.title(f"{biaxial.chan1} vs. {biaxial.chan2} ({self.groupsnames[ind + 1]})")
                plt.xlabel(str(biaxial.chan1))
                plt.ylabel(str(biaxial.chan2))
                filename = os.path.join(dir, "BiaxialGroups_" + self.groupsnames[ind + 1] + ".png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename, pilmode='RGB'),
                                      name=f"Biaxial {self.biaxialcount} ({biaxial.chan1} vs. {biaxial.chan2}) ({self.groupsnames[ind + 1]})",
                                      blending="additive")

        # Keep track of coordinates on Biaxial plot, and update variables.
        coordslist = []
        coords = np.hstack((np.expand_dims(x / np.max(x), 1), np.expand_dims(y / np.max(y), 1)))
        count = 0
        for i in range(self.numimgs):
            coordslist.append(coords[count:count + self.Qtab[curimg * self.numimgs + i].shape[0]].astype(np.float))
            count += self.Qtab[curimg * self.numimgs + i].shape[0]
        self.coordinates.append(coordslist)
        self.umapplots.append(False)
        self.biaxialcount += 1

    def change_folder(self):
        """
        Change the root directory path where results from the GUI will be saved.
        """
        dialog = QFileDialog()
        outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
        if outputfolder != "":
            outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
            os.rename(self.outputfolder, outputfolder)
            self.actionloggerpath = self.actionloggerpath.replace(self.outputfolder, outputfolder)
            self.editimagepath = self.editimagepath.replace(self.outputfolder, outputfolder)
            self.mergedimagespaths = [path.replace(self.outputfolder, outputfolder) for path in self.mergedimagespaths]
            self.objectclusterdirectories = [path.replace(self.outputfolder, outputfolder) for path in
                                             self.objectclusterdirectories]
            self.pixelclusterdirectories = [path.replace(self.outputfolder, outputfolder) for path in
                                            self.pixelclusterdirectories]
            self.segmentedimgpaths = [path.replace(self.outputfolder, outputfolder) for path in self.segmentedimgpaths]
            self.outputfolder = outputfolder
        return

    def colormap_group(self):
        """
        Load preset colormap options from a csv file to allow the user to assign custon colors to each cluster.
        """
        if self.mode == "Segmentation":
            GUIUtils.display_error_message("Must be displaying clustered image",
                                           "Please ensure that the currently selected table corresponds to clustering results.")

        ind = self.index
        if self.numimgs > 1:
            ind = int(self.index / (self.numimgs + 1))
        tabindex = ind
        if self.numimgs > 1:
            tabindex = (ind + 1) * (self.numimgs + 1) - 1

        if self.mode == "Pixel":
            nc = len(np.unique(self.greypixels[ind]))
        elif self.mode == "Object":
            nc = len(np.unique(self.greyobjects[ind])) - 1

        if nc < 57:
            colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color56.csv"
            colordf = pd.read_csv(colorcsvpath, index_col=0)
        elif 56 < nc < 142:
            colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color141.csv"
            colordf = pd.read_csv(colorcsvpath, index_col=0)
        else:
            colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color282.csv"
            colordf = pd.read_csv(colorcsvpath, index_col=0)

        imgnames = []
        for fname in self.filenames:
            name = fname.split("/")
            imgnames.append(name[-1])

        cmapwidget = GUIUtils.ColorAssign(nc, colordf, self.viewer)
        cmapwidget.exec()
        if not cmapwidget.OK:
            return

        if self.mode == "Pixel":
            self.pixelcolor[ind] = cmapwidget.newcolorlist
            data = self.datalist[tabindex]
            index = [f"RP-{i + 1}" for i in range(nc)]
            cols = self.fulltab.columns[3:]
        else:
            self.objectcolor[ind] = cmapwidget.newcolorlist
            data = self.objectdatalist[tabindex][:, 1:-4]
            index = [f"RO-{i + 1}" for i in range(nc)]
            cols = self.fulltab.columns[3:-4]

        scaler = MinMaxScaler()
        scaler.fit(data)
        my_data_scaled = scaler.transform(data).T

        # Cutoff the overflowing values
        my_data_scaled[my_data_scaled > 1] = 1
        my_data_scaled = pd.DataFrame(my_data_scaled)
        my_data_scaled.columns = index

        # Get the selected markers
        my_data_scaled.index = cols.values
        minhight = 4
        minwidth = 6
        ClusterDend = sns.clustermap(my_data_scaled + 0.001, col_cluster=True, linewidth=1, metric='cosine',
                                     cmap="vlag",
                                     row_cluster=True, yticklabels=True, xticklabels=True, vmin=0, vmax=1, cbar=False,
                                     figsize=(int(max(minhight, my_data_scaled.shape[1] * 0.8)),
                                              int(max(minwidth, my_data_scaled.shape[0] * 0.4))),
                                     linecolor='#799579')
        ClusterDend.ax_row_dendrogram.set_visible(False)
        ClusterDend.ax_col_dendrogram.set_visible(False)
        ClusterDend.cax.set_visible(False)
        for tick_label in ClusterDend.ax_heatmap.axes.get_xticklabels():
            if self.mode == "Pixel":
                tick_text = tick_label.get_text().replace(r"RP-", "")
                tick_label.set_color(self.pixelcolor[ind][int(tick_text) - 1, :] / 255)
                if self.pixelcolor[ind][int(tick_text) - 1, 0] == 255 and self.pixelcolor[ind][
                    int(tick_text) - 1, 1] == 255 and self.pixelcolor[ind][int(tick_text) - 1, 2] == 255:
                    tick_label.set_color("black")
            else:
                tick_text = tick_label.get_text().replace(r"RO-", "")
                tick_label.set_color(self.objectcolor[ind][int(tick_text) - 1, :] / 255)
                if self.objectcolor[ind][int(tick_text) - 1, 0] == 255 and self.objectcolor[ind][
                    int(tick_text) - 1, 1] == 255 and self.objectcolor[ind][int(tick_text) - 1, 2] == 255:
                    tick_label.set_color("black")

        if self.mode == "Pixel":
            plt.savefig(os.path.join(self.pixelclusterdirectories[ind], "ClusterHEATMAP.png"), dpi=300)
            np.save(os.path.join(self.pixelclusterdirectories[ind], "COLOR.npy"), self.pixelcolor[ind])
        else:
            plt.savefig(os.path.join(self.objectclusterdirectories[ind], "ClusterHEATMAP.png"), dpi=300)
            np.save(os.path.join(self.objectclusterdirectories[ind], "COLOR.npy"), self.objectcolor[ind])

    def count_visible_layers(self):
        """
        Count the number of layers in the main viewer window.

        :return: numvisible *(int)*: \n
            Number of layers in the main viewer window that are currently visible.
        """
        numvisible = 0
        for le in range(len(self.viewer.layers)):
            if self.viewer.layers[le].visible:
                numvisible += 1
        return numvisible

    def create_shape_path(self, verts, shapetype):
        """
        Connect a series of vertices into a shape.

        Args:
            verts (iterable): Coordinates for vertices being connected to form the shape.
            shapetype (str): Shape for the connected series of vertices.

        :return: path *(matplotlib.path.Path)*: \n
            The connected path of the vertices.
        """
        if shapetype != 'ellipse':
            path = Path(verts)
        else:
            centerx = (verts[0][0] + verts[2][0]) / 2
            centery = (verts[0][1] + verts[2][1]) / 2
            height = abs(verts[0][1] - verts[2][1])
            width = abs(verts[0][0] - verts[2][0])
            path = matplotlib.patches.Ellipse((centerx, centery), width, height)
        return path

    def create_table(self, data):
        """
        Add the contents of a data table in the table widget within teh RAPID GUI.

        Args:
            data (pandas.DataFrame): Dataset being displayed in the table.
        """
        headerList = []
        for n, key in enumerate(data.keys()):
            headerList.append(key)
        self.tablewidget = QTableWidget()
        numcols = len(data.keys())
        numrows = len(data[headerList[0]])
        self.tablewidget.setRowCount(numrows)
        self.tablewidget.setColumnCount(numcols)
        print(data.keys())
        for j, key in enumerate(data.keys()):
            for i, item in enumerate(data[key]):
                if data[headerList[j]][i] is not None and j == 1 and i >= 3 and not self.mode == "Segmentation":
                    val = int(data[headerList[j]][i])
                elif data[headerList[j]][i] is not None:
                    val = round(data[headerList[j]][i], 3)
                else:
                    val = data[headerList[j]][i]
                if math.isnan(val):
                    val = ""
                newitem = QTableWidgetItem(str(val))
                if i == 0:
                    if j == 0:
                        newitem = QTableWidgetItem("≥")
                elif i == 1:
                    if j == 0:
                        newitem = QTableWidgetItem("≤")
                elif j == 0 and i == 2:
                    newitem = QTableWidgetItem("")
                elif i == 2 and j == 1 and not (self.mode == "Segmentation"):
                    newitem = QTableWidgetItem("")
                    newitem.setBackground(QColor(0, 0, 0))
                elif i == 2 or j == 0:
                    newitem = QTableWidgetItem("")
                    if key not in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
                        newitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        newitem.setCheckState(QtCore.Qt.Unchecked)
                elif j == 1 and not (self.mode == "Segmentation"):
                    newitem.setBackground(QColor(0, 0, 0))
                else:
                    if self.mode == "Object" and numrows > 4:
                        minv = self.minvalsobject[self.index][j - 2]
                        maxv = self.maxvalsobject[self.index][j - 2]
                        numtabs = 1
                        if self.numimgs > 1:
                            numtabs += self.numimgs
                        trainindex = self.index // numtabs
                        tabnum = self.index % numtabs
                        for k in range(len(self.objecttrainlist)):
                            l = self.objecttrainlist[k]
                            if trainindex in l:
                                segmentindex = k * self.numimgs
                        if tabnum == self.numimgs:
                            maxsegment = []
                            for k in range(self.numimgs):
                                maxsegment.append(np.array(self.maxvalssegment[segmentindex + k]))
                            maxsegment = np.vstack(maxsegment)
                            maxsegment = list(np.amax(maxsegment, axis=0))
                        else:
                            maxsegment = self.maxvalssegment[segmentindex + tabnum]
                        adj = (data[key][i] - minv) / (maxv - minv) * maxsegment[j - 2] / np.max(
                            np.asarray(maxsegment[:-4]))
                    elif self.mode == "Segmentation" and numrows > 4:
                        minv = self.minvalssegment[self.index][j - 1]
                        maxv = self.maxvalssegment[self.index][j - 1]
                        adj = (data[key][i] - minv) / (maxv - minv)
                    elif self.mode == "Pixel":
                        minv = self.minvalspixel[self.index][j - 2]
                        maxv = self.maxvalspixel[self.index][j - 2]
                        adj = ((data[key][i] - minv) / (maxv - minv) * self.datanorm[j - 2]) / 255
                    else:
                        adj = 0.5
                    if math.isnan(adj):
                        adj = 0.5
                    if adj > 1.0:
                        adj = 1.0
                    if adj < 0.0:
                        adj = 0.0
                    newitem.setBackground(QColor(int(adj * 255), 0, int(255 - adj * 255)))
                if i < 3 or j == 0:
                    newitem.setBackground(QColor(0, 0, 0))
                newitem.setTextAlignment(Qt.AlignHCenter)
                font = QFont("Helvetica", pointSize=12, weight=QFont.Bold)
                newitem.setFont(font)
                newitem.setTextAlignment(Qt.AlignCenter)
                self.tablewidget.setItem(i, j, newitem)
        self.tablewidget.cellChanged.connect(self.on_cell_changed)
        self.tablewidget.setHorizontalHeaderLabels(headerList)
        self.tablewidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.resizeRowsToContents()
        style = "::section {""background-color: black; background-position: bottom center; }"
        self.tablewidget.horizontalHeader().setStyleSheet(style)
        self.tablewidget.verticalHeader().setStyleSheet(style)
        self.tablewidget.setMaximumHeight(self.tablewidget.rowHeight(4) * 14)

    def display_selected_cells(self):
        """
        Mask the image according to the cells within user-defined shapes overlaid on a Biaxial or UMAP plot.
        """
        # https://stackoverflow.com/questions/21339448/how-to-get-list-of-points-inside-a-polygon-in-python
        # Can only use display selected for UMAP or Biaxial gating.
        if self.biaxialcount == 1 and self.umapcount == 1:
            GUIUtils.display_error_message("No UMAP or biaxial gate output detected",
                                           "You must first generate a UMAP or biaxial-gate plot in order to select cells to be displayed")
            return

        # Select which plot is being used.
        it = 0
        if len(self.umapplots) > 1:
            selectplot = GUIUtils.BiaxialUMAPIterations(self.umapplots)
            selectplot.exec()
            if not selectplot.OK:
                return
            it = selectplot.iteration
        print(it)
        self.viewer.status = "Displaying selected cells"
        # self.display_selected(self.curimgs[it], self.xmins[it], self.xmaxs[it], self.ymins[it], self.ymaxs[it], self.coordinates[it])

        # Find the most recent shapes layer to define which vertices to use to define the shapes.
        ind = -1
        for i in reversed(range(len(self.viewer.layers))):
            if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and self.viewer.layers[i].visible:
                ind = i
                break

        # If no shapes have been drawn, prompt user to first draw a shape.
        if ind == -1:
            GUIUtils.display_error_message("Please draw a shape in the viewer first",
                                           "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
            return

        # Define the colors of each of the shapes, which will be coordinated with the selected cells.
        if len(self.viewer.layers[ind].data) == 1:
            cols = [np.array([1, 0, 0])]
        elif len(self.viewer.layers[ind].data) == 2:
            cols = [np.array([1, 0, 0]), np.array([0, 1, 1])]
        elif len(self.viewer.layers[ind].data) == 3:
            cols = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
        else:
            cols = generate_colormap(len(self.viewer.layers[ind].data) + 1) / 255.0
            cols = [cols[i] for i in range(len(cols) - 1)]

        # Keep track of masked images and percentages of cells that are selected in each shape.
        masklist = []
        percents = []
        type = [self.viewer.layers[ind].shape_type[i] for i in range(len(self.viewer.layers[ind].data))]
        curimg = self.curimgs[it]
        for shape in range(len(self.viewer.layers[ind].data)):
            # Find the vertices of the shapes relative to the scale of the plot, and the vertices within each
            # shape.
            verts = copy.deepcopy(self.viewer.layers[ind].data[shape])[:, -2:]
            verts[:, 0] = ((self.xmaxs[it] - verts[:, 0]) / (self.xmaxs[it] - self.xmins[it])) * 1.1 - 0.05
            verts[:, 1] = ((verts[:, 1] - self.ymins[it]) / (self.ymaxs[it] - self.ymins[it])) * 1.1 - 0.05
            verts[:, [0, 1]] = verts[:, [1, 0]]
            verts = [tuple(x) for x in verts.tolist()]
            p = self.create_shape_path(verts, type[shape])

            # Keep track of quantified cell marker expression for each selected cell.
            inclrows = []

            # Mask each image to filter out cells that aren't selected.
            masks = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]))

            # Keep track of the total number of cells and number of selected cells to calculate percentages.
            selectedcells = 0
            totalcells = 0
            for i in range(self.numimgs):
                # Add the number of total and selected cells in the image.
                totalcells += self.coordinates[it][i].shape[0]
                mask = p.contains_points(self.coordinates[it][i])
                rows = list(self.Qtab[curimg + i][mask, 0].astype(int))
                inclrows.append([x - 1 for x in rows])
                selectedcells += len(rows)

                # Mask the image for the selected cells.
                arr = copy.deepcopy(self.objectplots[curimg + i])
                arr[np.isin(self.objectplots[curimg + i], rows, invert=True)] = 0
                arr = self.method_searchsort(np.unique(arr), np.array([j for j in range(len(np.unique(arr)))]), arr)
                self.objectplots.append(arr)
                masks[i, :arr.shape[0], :arr.shape[1]][arr > 0] = 1

            # Make sure there is at least one cell selected.
            if selectedcells == 0:
                GUIUtils.display_error_message("No cells selected",
                                               "Make sure there is at lease one cell within the bounds of your shape")
                return

            else:
                # Keep track of the masked image to add to the viewer later.
                masklist.append(masks)

                # Keep track of min/max vals for each marker for the table for each image, as well as the
                # coordinates for each selected cell.
                mins = []
                maxs = []
                cortabs = []
                for i in range(self.numimgs):
                    # Re-index the selected cells and create a new table entry.
                    newentry = self.Qtab[curimg + i][inclrows[i], :]
                    for j in range(newentry.shape[0]):
                        newentry[j, 0] = j + 1
                    self.Qtab.append(newentry)

                    # Find the coordinates of only the selected cells.
                    cortabs.append([self.cortabs[int(curimg / self.numimgs)][i][j] for j in inclrows[i]])

                    # Find the min/max vals for each marker for the table for the current image.
                    minvals = []
                    maxvals = []
                    for j in range(self.Qtab[curimg + i].shape[1] - 1):
                        try:
                            minvals.append(np.min(self.Qtab[curimg + i][inclrows[i], j + 1]))
                            maxvals.append(np.max(self.Qtab[curimg + i][inclrows[i], j + 1]))
                        except:
                            minvals.append(0)
                            maxvals.append(0)
                    mins.append(copy.deepcopy(minvals))
                    maxs.append(copy.deepcopy(maxvals))

                    # Keep track of the orders of the cells and default to no cells being selected in the table.
                    self.orders.append(inclrows[i])
                    self.combcellnums.append(inclrows[i])
                    self.currentlyselectedcells.append([])

                # Keep track of the coordinates for each selected cell and the min/max values for each marker
                # for each cell in each image.
                self.cortabs.append(cortabs)
                minvals = []
                maxvals = []
                for i in range(len(mins[0])):
                    minvals.append(min([l[i] for l in mins]))
                    maxvals.append(max([l[i] for l in maxs]))
                for i in range(self.numimgs):
                    self.minvalssegment.append(copy.deepcopy(minvals))
                    self.maxvalssegment.append(copy.deepcopy(maxvals))
                    self.lowerboundslist.append(copy.deepcopy(minvals))
                    self.upperboundslist.append(copy.deepcopy(maxvals))

                # Keep track of the percentages of cells selected for each image.
                percent = round(float(selectedcells * 100 / totalcells), 2)
                percents.append(copy.deepcopy(percent))

                # Update the dropdown options for the sort table widget.
                for i in range(len(inclrows)):
                    imgname = f"Selected{self.displayselectedcount}-{i + 1} ({percent}%)"
                    self.tableimagenames.append(f"{imgname} - {self.tableimagenames[self.cellindices[i]]}")
                    self.cellindices.append(self.tableimgcount)
                    self.tableimgcount += 1

        # Update the shapes layer with shapes colored consistently with the displayed images.
        vertslist = [self.viewer.layers[ind].data[i] for i in range(len(self.viewer.layers[ind].data))]
        self.viewer.layers.pop(ind)
        self.viewer.add_shapes(vertslist, shape_type=type, edge_width=0, edge_color=cols, face_color=cols,
                               name="Selected Regions")
        self.set_invisible(self.viewer)

        # Add the selected cells from each image to the viewer.
        for i in range(len(masklist)):
            cmap = Colormap(ColorArray([(0, 0, 0), cols[i]]))
            imgname = f"Selected{self.displayselectedcount}-{i + 1} ({percents[i]}%)"
            self.viewer.add_image(masklist[i], name=imgname, blending="additive", colormap=cmap)
            self.objectimgnames.append(imgname)
            self.objecttrainlist.append([])
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Selected{self.displayselectedcount}-1 ({percents[0]}%) - {self.tableimagenames[self.cellindices[0]]}"
        self.displayselectedcount += 1
        self.sorttableimages.reset_choices()
        GUIUtils.log_actions(self.actionloggerpath, f"Displayed Selected: Plot ({it}), Shapes ({type}), "
                                                    f"Vertices ({vertslist})")

    def display_umap(self):
        """
        Generate a UMAP plot according to parameters defined by the user.
        """
        # User must first run object-based segmentation in order to generate a UMAP.
        if self.segmentcount == 0:
            GUIUtils.display_error_message("You must segment before running UMAP",
                                           "UMAP cannot be generated until the image has been segmented")
            return

        # Prompt user to select which cell markers to use as parameters for UMAP.
        umapmarkers = GUIUtils.RAPIDObjectParams(self.markers, True)
        umapmarkers.exec()
        if not umapmarkers.OK:
            return

        # Prompt user to define the parameters and coloring schemes used for the UMAP.
        setumapParams = GUIUtils.UMAPParameters(self.objecttraincount > 0, self.objectimgnames, self.groupsnames[1:])
        setumapParams.exec()
        if not setumapParams.OK:
            return

        # Count total number of cells in the segmented iteration being used across all images.
        numcells = 0
        curimg = setumapParams.imageindex
        self.curimgs.append(curimg * self.numimgs)
        for i in range(self.numimgs):
            numcells += self.Qtab[curimg * self.numimgs + i].shape[0]

        # Compile quantified cells from each individual image into one combined data array.
        currentimage = np.zeros((numcells, len(umapmarkers.markernums)))
        currentimage2 = np.zeros((numcells, self.Qtab[curimg * self.numimgs].shape[1]))
        count = 0
        col_list = generate_colormap(self.numimgs + 1)
        cols = np.zeros((numcells, 3)).astype(np.float)
        cellsperimage = []
        for i in range(self.numimgs):
            cellsincurrimg = []
            currentimage[count:count + self.Qtab[curimg * self.numimgs + i].shape[0], :] = self.Qtab[
                                                                                               curimg * self.numimgs + i][
                                                                                           :, umapmarkers.markernums]
            currentimage2[count:count + self.Qtab[curimg * self.numimgs + i].shape[0], :] = self.Qtab[
                curimg * self.numimgs + i]
            for j in range(count, count + self.Qtab[curimg * self.numimgs + i].shape[0]):
                cellsincurrimg.append(j)
                cols[j, :] = col_list[i, :] / np.array([255.0, 255.0, 255.0])
            count += self.Qtab[curimg * self.numimgs + i].shape[0]
            cellsperimage.append(cellsincurrimg)

        # Apply UMAP algorithm and remove rows with NaN values.
        reducer = umap.UMAP(min_dist=setumapParams.min_dist, n_neighbors=setumapParams.n_neighbors,
                            metric=setumapParams.distance)
        mapper = reducer.fit_transform(currentimage)
        removerows = np.unique(np.argwhere(np.isnan(mapper))[:, 0])
        mapper = np.delete(mapper, removerows, axis=0)
        for i in range(self.numimgs):
            for cellnum in removerows:
                if cellnum in cellsperimage[i]:
                    cellsperimage[i].remove(cellnum)

        # Color data points according to image ID.
        cols = np.delete(cols, removerows, axis=0)
        cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)

        # Use resulting points to generate a scatterplot and add it to the viewer.
        y = (mapper[:, 0] - np.min(mapper[:, 0])) / (np.max(mapper[:, 0]) - np.min(mapper[:, 0]))
        x = (mapper[:, 1] - np.min(mapper[:, 1])) / (np.max(mapper[:, 1]) - np.min(mapper[:, 1]))
        x = np.append(x, [-0.05, 1.05])
        y = np.append(y, [-0.05, 1.05])
        plt.figure(figsize=(10, 10))
        plt.scatter(x, y, s=1, c=cols, marker='.')
        plt.title("UMAP")
        plt.xlabel("UMAP 1")
        plt.ylabel("UMAP 2")
        # ax = plt.gca()
        plt.xticks([], [])
        plt.yticks([], [])
        dir = GUIUtils.create_new_folder("UMAP_", self.outputfolder)
        plt.savefig(os.path.join(dir, "UMAP.png"), format="PNG", dpi=300)
        im = cv.imread(os.path.join(dir, "UMAP.png"))
        imarray = np.asarray(im)
        locs = np.where((imarray[:, :, 0] == 242) & (imarray[:, :, 1] == 255) & (imarray[:, :, 2] == 242))
        self.xmins.append(np.min(locs[0]))
        self.xmaxs.append(np.max(locs[0]))
        self.ymins.append(np.min(locs[1]))
        self.ymaxs.append(np.max(locs[1]))
        self.set_invisible(self.viewer)
        self.viewer.add_image(im, name=f"UMAP {self.umapcount}", blending="additive")

        # If selected by user, add an additional stack of scatterplots with vertices colored on a gradient
        # according to each cell marker or morphological parameter.
        if setumapParams.colorbymarkers:
            self.set_invisible(self.viewer)
            pathlist = []
            max = np.percentile(currentimage2[:, 1:-4], 97)
            min = np.min(currentimage2[:, 1:-4])
            adj = np.max(currentimage2[:, 1:-4])
            for i in range(1, 5):
                currentimage2[:, -i] = currentimage2[:, -i] / np.max(currentimage2[:, -i]) * adj
            currentimage2 = currentimage2[:, umapmarkers.markernums]
            for i in range(len(umapmarkers.markernums)):
                plt.figure(figsize=(10, 10))
                col = np.zeros((len(mapper), 3)).astype(np.float)
                for j in range(len(mapper)):
                    col[j, 0] = (currentimage2[j, i] - min) / (max - min)
                    col[j, 2] = 1.0 - (currentimage2[j, i] - min) / (max - min)
                col[col > 1.0] = 1.0
                col[col < 0.0] = 0.0
                col = np.append(col, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=col, marker='.')
                ax = plt.gca()
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title(umapmarkers.objecttrainmarkers[i])
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                plt.savefig(os.path.join(dir, umapmarkers.objecttrainmarkers[i] + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(dir, umapmarkers.objecttrainmarkers[i] + ".png"))
            imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
            self.viewer.add_image(imx, name=f"UMAP {self.umapcount} (Cell Markers)", blending="additive")

        # If given segmented image iteration has been clustered, check if the user elected to use clustering as
        # a basis for vertex coloring.
        if len(self.objecttrainlist[setumapParams.imageindex]) > 0:
            # If the user is coloring according to cluster assignment, prompt to define which clustering
            # iteration is being used.
            if setumapParams.colorbyindivclusters or setumapParams.colorbycombclusters:
                if len(self.objecttrainlist[setumapParams.imageindex]) > 1:
                    iteration = GUIUtils.ObjectTrainIteration(len(self.objecttrainlist[setumapParams.imageindex]))
                    iteration.exec()
                    if not iteration.OK:
                        return
                    startindex = self.objecttrainlist[setumapParams.imageindex][iteration.iteration]
                    GUIUtils.log_actions(self.actionloggerpath,
                                         f"UMAP: Markers ({umapmarkers.objecttrainmarkers}), Segmentation Iteration ({setumapParams.imageindex}), "
                                         f"Min Dist ({setumapParams.min_dist}), Num Neighbours ({setumapParams.n_neighbors}), "
                                         f"Distance ({setumapParams.distance}), Coloring ({setumapParams.colorbymarkers}, "
                                         f"{setumapParams.colorbyindivclusters}, {setumapParams.colorbycombclusters}, "
                                         f"{setumapParams.colorbygroups}), Iteration ({iteration.iteration})")
                else:
                    GUIUtils.log_actions(self.actionloggerpath,
                                         f"UMAP: Markers ({umapmarkers.objecttrainmarkers}), Segmentation Iteration ({setumapParams.imageindex}), "
                                         f"Min Dist ({setumapParams.min_dist}), Num Neighbours ({setumapParams.n_neighbors}), "
                                         f"Distance ({setumapParams.distance}), Coloring ({setumapParams.colorbymarkers}, "
                                         f"{setumapParams.colorbyindivclusters}, {setumapParams.colorbycombclusters}, "
                                         f"{setumapParams.colorbygroups})")
                    startindex = self.objecttrainlist[setumapParams.imageindex][0]
                clusternums = []
                for i in range(self.numimgs):
                    curclusternums = self.objectclusters[startindex * self.numimgs + i]
                    for n in curclusternums:
                        clusternums.append(n - 1)
                numclusters = len(np.unique(self.greyobjects[startindex])) - 1

            # If selected by user, add an additional stack of scatterplots with vertices colored red if
            # corresponding to a cell in the respective cluster, or blue otherwise.
            if setumapParams.colorbyindivclusters:
                self.set_invisible(self.viewer)
                pathlist = []
                for i in range(numclusters):
                    plt.figure(figsize=(10, 10))
                    col = np.zeros((len(mapper), 3)).astype(np.float)
                    for j in range(len(mapper)):
                        if int(clusternums[j]) == i:
                            col[j, 0] = 1.0
                            col[j, 2] = 0.0
                        else:
                            col[j, 0] = 0.0
                            col[j, 2] = 1.0
                    col = np.append(col, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                    plt.scatter(x, y, s=1, c=col, marker='.')
                    ax = plt.gca()
                    plt.xticks([], [])
                    plt.yticks([], [])
                    plt.title(f"Cluster {i + 1}")
                    plt.xlabel("UMAP 1")
                    plt.ylabel("UMAP 2")
                    plt.savefig(os.path.join(dir, f"UMAPCluster{i + 1}.png"), format="PNG", dpi=300)
                    pathlist.append(os.path.join(dir, f"UMAPCluster{i + 1}.png"))
                imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
                self.viewer.add_image(imx, name=f"UMAP {self.umapcount} (Individual Clusters)", blending="additive")

            # If selected by user, add an additional scatterplot colored according to cluster assignment.
            if setumapParams.colorbycombclusters:
                self.set_invisible(self.viewer)
                col_list = generate_colormap(numclusters + 1)
                cols = np.zeros((len(mapper), 3)).astype(np.float)
                for i in range(len(mapper)):
                    cols[i, :] = col_list[int(clusternums[i]), :] / np.array([255.0, 255.0, 255.0])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=cols, marker='.')
                ax = plt.gca()
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title("Clusters")
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                filename = os.path.join(dir, "UMAPClusters.png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename), name=f"UMAP {self.umapcount} (Combined Clusters)",
                                      blending="additive")

        # If selected by user, add an additional scatterplot colored according to group assignment.
        if setumapParams.colorbygroups != []:
            for ind in setumapParams.colorbygroups:
                group = self.groupslist[ind + 1]
                imggroupnames = list(group.values())
                shufflelist = [list(group.keys()).index(name) for name in
                               [os.path.split(fn)[-1] for fn in self.filenames]]
                nameindices = list(set(imggroupnames))
                numgroups = len(nameindices)
                imagegroups = []
                for i in range(self.numimgs):
                    imagegroups.append(nameindices.index(imggroupnames[i]))
                imagegroups = [imagegroups[i] for i in shufflelist]
                self.set_invisible(self.viewer)
                col_list = generate_colormap(numgroups + 1)
                cols = np.zeros((len(mapper), 3)).astype(np.float)
                count = 0
                for i in range(self.numimgs):
                    for j in range(count, count + len(cellsperimage[i])):
                        cols[j, :] = col_list[imagegroups[i], :] / np.array([255.0, 255.0, 255.0])
                    count += len(cellsperimage[i])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=cols, marker='.')
                ax = plt.gca()
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title('UMAP (' + self.groupsnames[ind + 1] + ')')
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                filename = os.path.join(dir, "UMAPGroups_" + self.groupsnames[ind + 1] + ".png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename), name=f"UMAP {self.umapcount} ({self.groupsnames[ind + 1]})",
                                      blending="additive")

        # Keep track of coordinates on UMAP plot, and update variables.
        coordslist = []
        coords = np.hstack((np.expand_dims(x, 1), np.expand_dims(y, 1)))
        count = 0
        for i in range(self.numimgs):
            coordslist.append(coords[count:count + self.Qtab[curimg * self.numimgs + i].shape[0]].astype(np.float))
            count += self.Qtab[curimg * self.numimgs + i].shape[0]
        self.coordinates.append(coordslist)
        self.umapplots.append(True)
        self.segmentationindicesinumap.append(setumapParams.imageindex)
        self.umapcount += 1

    def edit_image(self):
        """
        Open a new popup napari window to allow the user to edit each image and change the raw data.
        """
        # Prompt user to decide whether to edit all images, or to apply edits from one image to all others.
        ### TODO: Should still give option to load edits for single-image.
        if self.numimgs > 1:
            editoptions = GUIUtils.EditOptions()
            editoptions.exec()
            if not editoptions.OK:
                return
            allimgs = editoptions.allimages
            loadedits = editoptions.loadedits
        else:
            allimgs = True
            loadedits = False

        # Load previous edits if selected by the user
        if loadedits:
            path = QFileDialog().getOpenFileName(filter="*editlog.txt")[0]
            if path == "":
                return
            with open(path, 'r') as file:
                for line in file:
                    edit = line[:-1]
                    self.editactions.append(ast.literal_eval(edit))
            print(self.editactions)
            self.apply_edits(self.editactions)
            return

        # Prompt user to select which image will be used, if only using one.
        if not allimgs:
            selectimg = GUIUtils.SelectImgDropdown(self.filenames)
            selectimg.exec()
            if not selectimg.OK:
                return
            imgindex = selectimg.imgindex
        else:
            imgindex = 0

        # Create a new viewer window where images will be added for editing.
        self.edit_viewer = napari.Viewer()
        names = []
        for i in range(len(self.filenames)):
            names.append(self.filenames[i].split("/")[-1])
        self.imagenum = 0
        editdata = np.zeros((len(self.markers), self.numimgs, self.maximageshape[0], self.maximageshape[1]))

        # Keep track of contrast limits for each image and every action taken.
        contrastlimits = []
        editactions = []
        logstrs = ["Edited Image: "]
        cl = []
        for i in range(len(self.markers)):
            cl.append([0, 255])
        for i in range(len(self.filenames)):
            contrastlimits.append(copy.deepcopy(cl))
        print(contrastlimits)

        @magicgui(call_button="Apply Changes")
        def apply_changes_editgui() -> Image:
            # Apply all changes, including any adjusted contrast limits, to the raw images in the main viewer.
            for i in range(len(self.markers)):
                editdata[i, self.imagenum, :, :] = copy.deepcopy(self.edit_viewer.layers[i].data)
                contrastlimits[self.imagenum][i] = [self.edit_viewer.layers[i].contrast_limits[0],
                                                    self.edit_viewer.layers[i].contrast_limits[1]]
                for j in range(self.numimgs):
                    editdata[i, j, :, :] = self.apply_contrast_limits(editdata[i, j, :, :], contrastlimits[j][i])
                self.viewer.layers[i].data = editdata[i, :, :, :]
            self.editactions += editactions
            self.editactions.append(contrastlimits)

            if not self.editedimage:
                self.editimagepath = GUIUtils.create_new_folder("ImageEdits", self.outputfolder)
            with open(os.path.join(self.editimagepath, "editlog.txt"), 'w') as file:
                for item in self.editactions:
                    file.write("%s\n" % item)

            logstrs.append(f"Contrast Limits ({contrastlimits})")
            GUIUtils.log_actions(self.actionloggerpath, "".join(logstrs))
            self.edit_viewer.window.qt_viewer.close()
            self.edit_viewer.window._qt_window.close()

        @magicgui(call_button="Apply Changes")
        def apply_changes_one_editgui() -> Image:
            self.apply_edits(editactions, imgindex)

            # Apply all changes, including any adjusted contrast limits, to the raw images in the main viewer.
            contrastlimits = []
            for i in range(len(self.markers)):
                editdata[i, self.imagenum, :, :] = copy.deepcopy(self.edit_viewer.layers[i].data)
                contrastlimits.append(
                    [self.edit_viewer.layers[i].contrast_limits[0], self.edit_viewer.layers[i].contrast_limits[1]])
                self.viewer.layers[i].data = self.apply_contrast_limits(self.viewer.layers[i].data, contrastlimits[i])
            self.editactions += editactions
            for i in range(self.numimgs - 1):
                contrastlimits.append(contrastlimits[0])
            self.editactions.append(contrastlimits)

            if not self.editedimage:
                self.editimagepath = GUIUtils.create_new_folder("ImageEdits", self.outputfolder)
            with open(os.path.join(self.editimagepath, "editlog.txt"), 'w') as file:
                for item in self.editactions:
                    file.write("%s\n" % item)

            logstrs.append(f"Contrast Limits ({contrastlimits})")
            GUIUtils.log_actions(self.actionloggerpath, f"{self.filenames[imgindex]}: " + "".join(logstrs))
            self.edit_viewer.window.qt_viewer.close()
            self.edit_viewer.window._qt_window.close()

        @magicgui(call_button="Binarize")
        def binarize_image_editgui() -> Image:
            # Apply a denoising algorithm to binarize any or all of the cell markers in the given image.
            markers = GUIUtils.ImageEditingMarkers(self.edit_viewer, self.markers)
            markers.exec()
            if markers.OK:
                for i in markers.markernums:
                    data = denoise_img(self.edit_viewer.layers[i].data)
                    data[data > 0] = 255
                    self.edit_viewer.layers[i].data = data

            # Keep track of which marker had a Median filter applied to them for the current image.
            binarizelog = []
            for i in range(self.nummarkers):
                binarizelog.append([])
            fullbinarizelog = []
            if allimgs:
                for i in range(len(self.filenames)):
                    fullbinarizelog.append(copy.deepcopy(binarizelog))
                for i in range(self.nummarkers):
                    if i in markers.markernums:
                        fullbinarizelog[self.imagenum][i] = "Binarize"
            else:
                for i in range(self.nummarkers):
                    if i in markers.markernums:
                        binarizelog[i] = "Binarize"
                for i in range(len(self.filenames)):
                    fullbinarizelog.append(copy.deepcopy(binarizelog))
            editactions.append(fullbinarizelog)
            print(editactions)

            logstrs.append(f"Binarized Image ({markers.markernums}), ")

        @magicgui(auto_call=True, image={"choices": names, "label": ""})
        def change_image_editgui(image: str):
            # Because only one image is shown at once, allow user to switch between images.
            for i in range(len(self.edit_viewer.layers)):
                editdata[i, self.imagenum, :, :] = copy.deepcopy(self.edit_viewer.layers[i].data)
                contrastlimits[self.imagenum][i] = self.edit_viewer.layers[i].contrast_limits
            self.imagenum = names.index(image)
            for i in range(len(self.edit_viewer.layers)):
                self.edit_viewer.layers[i].contrast_limits = contrastlimits[self.imagenum][i]
                self.edit_viewer.layers[i].data = editdata[i, self.imagenum, :, :]

        @magicgui(call_button="Denoise")
        def denoise_image_editgui() -> Image:
            # Apply a denoising algorithm to any or all of the cell markers in the given image.
            markers = GUIUtils.ImageEditingMarkers(self.edit_viewer, self.markers)
            markers.exec()
            if markers.OK:
                data = np.zeros((self.edit_viewer.layers[0].data.shape[0], self.edit_viewer.layers[0].data.shape[1],
                                 len(markers.markernums)))
                for i in range(len(markers.markernums)):
                    data[:, :, i] = self.edit_viewer.layers[markers.markernums[i]].data
                denoised = denoise_img(data, [j for j in range(len(markers.markernums))])
                for i in range(len(markers.markernums)):
                    self.edit_viewer.layers[markers.markernums[i]].data = denoised[:, :, i]

            # Keep track of which marker had a Median filter applied to them for the current image.
            denoiselog = []
            for i in range(self.nummarkers):
                denoiselog.append([])
            fulldenoiselog = []
            if allimgs:
                for i in range(len(self.filenames)):
                    fulldenoiselog.append(copy.deepcopy(denoiselog))
                for i in range(self.nummarkers):
                    if i in markers.markernums:
                        fulldenoiselog[self.imagenum][i] = "Denoise"
            else:
                for i in range(self.nummarkers):
                    if i in markers.markernums:
                        denoiselog[i] = "Denoise"
                for i in range(len(self.filenames)):
                    fulldenoiselog.append(copy.deepcopy(denoiselog))
            editactions.append(fulldenoiselog)
            print(editactions)

            logstrs.append(f"Denoised Image ({markers.markernums}), ")

        @magicgui(call_button="Gaussian Filter")
        def gaussian_filter_editgui() -> Image:
            # Apply a gaussian filter to any or all of the cell markers in the given image.
            markers = GUIUtils.ImageEditingMarkers(self.edit_viewer, self.markers)
            markers.exec()
            if markers.OK:
                for i in markers.markernums:
                    self.edit_viewer.layers[i].data = ndimage.gaussian_filter(self.edit_viewer.layers[i].data, [1, 1])

                # Keep track of which marker had a Gaussian filter applied to them for the current image.
                gausslog = []
                for i in range(self.nummarkers):
                    gausslog.append([])
                fullgausslog = []
                if allimgs:
                    for i in range(len(self.filenames)):
                        fullgausslog.append(copy.deepcopy(gausslog))
                    for i in range(self.nummarkers):
                        if i in markers.markernums:
                            fullgausslog[self.imagenum][i] = "Gaussian"
                else:
                    for i in range(self.nummarkers):
                        if i in markers.markernums:
                            gausslog[i] = "Gaussian"
                    for i in range(len(self.filenames)):
                        fullgausslog.append(copy.deepcopy(gausslog))
                editactions.append(fullgausslog)
                print(editactions)

                logstrs.append(f"Gaussian Filter ({markers.markernums}), ")

        @magicgui(call_button="Median Filter")
        def median_filter_editgui() -> Image:
            # Apply a median filter to any or all of the cell markers in the given image.
            markers = GUIUtils.ImageEditingMarkers(self.edit_viewer, self.markers)
            markers.exec()
            if markers.OK:
                for i in markers.markernums:
                    self.edit_viewer.layers[i].data = ndimage.median_filter(self.edit_viewer.layers[i].data, [3, 3])

            # Keep track of which marker had a Median filter applied to them for the current image.
            medlog = []
            for i in range(self.nummarkers):
                medlog.append([])
            fullmedlog = []
            if allimgs:
                for i in range(len(self.filenames)):
                    fullmedlog.append(copy.deepcopy(medlog))
                for i in range(self.nummarkers):
                    if i in markers.markernums:
                        fullmedlog[self.imagenum][i] = "Median"
            else:
                for i in range(self.nummarkers):
                    if i in markers.markernums:
                        medlog[i] = "Median"
                for i in range(len(self.filenames)):
                    fullmedlog.append(copy.deepcopy(medlog))
            editactions.append(fullmedlog)
            print(editactions)

            logstrs.append(f"Median Filter ({markers.markernums}), ")

        @magicgui(call_button="Toggle Visibility")
        def toggle_visibility_editgui() -> Image:
            # If any markers are visible, make them invisible. Otherwise, make all markers visible.
            visible = False
            for le in range(len(self.edit_viewer.layers)):
                if self.edit_viewer.layers[le].visible:
                    visible = True
            if visible:
                for i in range(len(self.edit_viewer.layers)):
                    self.edit_viewer.layers[i].visible = False
            else:
                for i in range(len(self.edit_viewer.layers)):
                    self.edit_viewer.layers[i].visible = True

        filterWidget = QWidget()
        filterLayout = QGridLayout()
        filterLayout.setSpacing(0)
        filterLayout.setContentsMargins(0, 0, 0, 0)
        togglevisgui = toggle_visibility_editgui.native
        togglevisgui.setToolTip("Set all layers to visible/invisible")
        filterLayout.addWidget(togglevisgui, 0, 0)
        if self.numimgs > 1 and allimgs:
            changeimagegui = change_image_editgui.native
            changeimagegui.setToolTip("Choose a different image to edit")
            filterLayout.addWidget(changeimagegui, 0, 1)
            reindex = 0
        else:
            reindex = 1
        gaussiangui = gaussian_filter_editgui.native
        gaussiangui.setToolTip("Apply a Gaussian filter to the image")
        filterLayout.addWidget(gaussiangui, 0, 2 - reindex)
        mediangui = median_filter_editgui.native
        mediangui.setToolTip("Apply a Median filter to the image")
        filterLayout.addWidget(mediangui, 0, 3 - reindex)
        denoiseimagegui = denoise_image_editgui.native
        denoiseimagegui.setToolTip("Remove noise from the image")
        filterLayout.addWidget(denoiseimagegui, 0, 4 - reindex)
        binarizeimagegui = binarize_image_editgui.native
        binarizeimagegui.setToolTip("Binarize the image")
        filterLayout.addWidget(binarizeimagegui, 0, 5 - reindex)
        if allimgs:
            applychangesallgui = apply_changes_editgui.native
        else:
            applychangesallgui = apply_changes_one_editgui.native
        applychangesallgui.setToolTip("Apply changes to the raw images")
        filterLayout.addWidget(applychangesallgui, 1, 2 - reindex, 1, 2 + reindex)
        filterWidget.setLayout(filterLayout)
        self.edit_viewer.window.add_dock_widget(filterWidget, name="Filter module", area="bottom")

        # Add first image into the viewer at the start.
        for i in range(len(self.markers)):
            cmap = self.viewer.layers[i].colormap
            self.edit_viewer.add_image(self.viewer.layers[i].data[imgindex, :, :], name=self.markers[i],
                                       rgb=False, colormap=cmap, contrast_limits=[0, 255], blending="additive")
            editdata[i, :, :, :] = self.viewer.layers[i].data

    def filter_table(self):
        """
        Allow user to set a lower or upper bound for any of the parameters currently displayed in the table. This will
        also be applied to all other images included in the same round of analysis.
        """
        # Get all the markers in the currently displayed table, and only use those as options for filtering.
        markers = []
        for i in range(self.tablewidget.columnCount()):
            if self.tablewidget.horizontalHeaderItem(i).text() in self.markers:
                markers.append(self.tablewidget.horizontalHeaderItem(i).text())

        # Prompt user to define which markers, whether to set a lower/upper bound, and the value being used.
        tablefilters = GUIUtils.TableFilters(markers)
        tablefilters.exec()
        if not tablefilters.OK:
            return

        # If resetting the filters, include all the full datasets.
        if tablefilters.reset:
            GUIUtils.log_actions(self.actionloggerpath, "Filtered Table: Reset")
            # If the current table corresponds to segmentation.
            if self.mode == "Segmentation":
                # Reset lower/upper bounds and use the full dataset to display in the table.
                for i in range(self.tablewidget.columnCount()):
                    self.tablewidget.item(0, i).setText(str(round(self.minvalssegment[self.index][i - 1], 3)))
                    self.tablewidget.item(1, i).setText(str(round(self.maxvalssegment[self.index][i - 1], 3)))
                    self.lowerbounds = copy.deepcopy(self.minvalssegment[self.index])
                    self.upperbounds = copy.deepcopy(self.maxvalssegment[self.index])
                    ind = self.cellindices.index(self.listindex)
                    startind = (ind // self.numimgs) * self.numimgs
                    for i in range(self.numimgs):
                        self.lowerboundslist[startind + i] = copy.deepcopy(self.minvalssegment[self.index])
                        self.lowerboundslist[startind + i] = copy.deepcopy(self.maxvalssegment[self.index])
                imind = int(self.index // self.numimgs) * self.numimgs
                for j in range(self.numimgs):
                    self.combcellnums[imind + j] = copy.deepcopy(self.orders[imind + j])
                self.cellnums = self.combcellnums[self.index]
                displaycellnums = [int(self.Qtab[self.index][j, 0]) - 1 for j in self.cellnums]
                self.update_table(self.Qtab[self.index][self.orders[self.index], 1:], self.lowerbounds,
                                  self.upperbounds, self.Qtab[self.index].shape[0], displaycellnums)

            # If the current table corresponds to object-based clustering.
            elif self.mode == "Object":
                # Reset lower/upper bounds and use the full dataset to display in the table.
                for i in range(self.tablewidget.columnCount()):
                    self.tablewidget.item(0, i).setText(str(round(self.minvalsobject[self.index][i], 3)))
                    self.tablewidget.item(1, i).setText(str(round(self.maxvalsobject[self.index][i], 3)))
                    self.lowerbounds = copy.deepcopy(self.minvalsobject[self.index])
                    self.upperbounds = copy.deepcopy(self.maxvalsobject[self.index])
                    self.lowerboundslist[self.listindex] = copy.deepcopy(self.minvalsobject[self.index])
                    self.lowerboundslist[self.listindex] = copy.deepcopy(self.maxvalsobject[self.index])
                self.objectclusternums = copy.deepcopy(self.order)
                self.update_table(self.objectdatalist[self.index][self.order, :], self.lowerbounds,
                                  self.upperbounds, len(self.order), self.objectclusternums)

            # If the current table corresponds to pixel-based clustering.
            else:
                # Reset lower/upper bounds and use the full dataset to display in the table.
                for i in range(self.tablewidget.columnCount()):
                    self.tablewidget.item(0, i).setText(str(round(self.minvalspixel[self.index][i], 3)))
                    self.tablewidget.item(1, i).setText(str(round(self.maxvalspixel[self.index][i], 3)))
                    self.lowerbounds = copy.deepcopy(self.minvalspixel[self.index])
                    self.upperbounds = copy.deepcopy(self.maxvalspixel[self.index])
                    self.lowerboundslist[self.listindex] = copy.deepcopy(self.minvalspixel[self.index])
                    self.lowerboundslist[self.listindex] = copy.deepcopy(self.maxvalspixel[self.index])
                self.pixelclusternums = copy.deepcopy(self.order)
                self.update_table(self.datalist[self.index][self.order, :], self.lowerbounds, self.upperbounds,
                                  self.datalist[self.index].shape[0], self.pixelclusternums)

        # If applying a new filter, add to the existing filters and update the table accordingly.
        else:
            GUIUtils.log_actions(self.actionloggerpath, f"Filtered Table: Bound ({tablefilters.bound}), Marker "
                                                        f"({tablefilters.marker}), Value ({tablefilters.val}")
            # Lower bounds are represented in the first row, while upper bounds are in the second row.
            if tablefilters.bound == "Lower Bound":
                row = 0
            else:
                row = 1

            # Find the column corresponding to the marker being updated.
            for i in range(self.tablewidget.columnCount()):
                if tablefilters.marker == self.tablewidget.horizontalHeaderItem(i).text():
                    column = i

            # Change the filter value in the table.
            self.tablewidget.item(row, column).setText(str(round(tablefilters.val, 3)))

            # Account for the extra column for cell/pixel counts when clustering.
            if self.mode == "Segmentation":
                c = column - 1
            else:
                c = column - 2

            # If user adjusts lower bound, store that for future reference.
            if row == 0 and c >= 0:
                self.lowerbounds[c] = tablefilters.val
                # Lower bound must be smaller than upper bound.
                if self.lowerbounds[c] > self.upperbounds[c]:
                    self.lowerbounds[c] = self.upperbounds[c]
                if self.mode == "Segmentation":
                    ind = self.cellindices.index(self.listindex)
                    startind = (ind // self.numimgs) * self.numimgs
                    for i in range(self.numimgs):
                        self.lowerboundslist[startind + i] = copy.deepcopy(self.lowerbounds)
                else:
                    self.lowerboundslist[self.listindex] = copy.deepcopy(self.lowerbounds)

            # If user adjusts upper bound, store that for future reference.
            elif row == 1 and c >= 0:
                self.upperbounds[c] = tablefilters.val
                # Lower bound must be smaller than upper bound.
                if self.upperbounds[c] < self.lowerbounds[c]:
                    self.upperbounds[c] = self.lowerbounds[c]
                if self.mode == "Segmentation":
                    ind = self.cellindices.index(self.listindex)
                    startind = (ind // self.numimgs) * self.numimgs
                    for i in range(self.numimgs):
                        self.upperboundslist[startind + i] = copy.deepcopy(self.upperbounds)
                else:
                    self.upperboundslist[self.listindex] = copy.deepcopy(self.upperbounds)

            # If filtering a segmentation table.
            if self.mode == "Segmentation":
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(self.lowerbounds)):
                    if self.lowerbounds[i] > self.minvalssegment[self.index][i] or self.upperbounds[i] < \
                            self.maxvalssegment[self.index][i]:
                        filteredmarkers.append(i)

                # Store the segmentation iteration corresponding to the current data table, and the
                # corresponding quantified values.
                imind = int(self.index // self.numimgs) * self.numimgs
                currentdata = self.Qtab[self.index][self.orders[self.index], 1:]
                for i in range(self.numimgs):
                    # Store segmentation data table, and append index values at the end to log sort order.
                    filtereddata = np.append(self.Qtab[imind + i][self.orders[imind + i], 1:],
                                             np.expand_dims(np.arange(self.Qtab[imind + i].shape[0]), 1), 1)

                    # Filter cells one marker at a time according to current lower- and upper-bounds.
                    for marker in filteredmarkers:
                        filtermask = (np.round(filtereddata[:, marker], 3) <= np.round(self.upperbounds[marker], 3))
                        filtereddata = filtereddata[filtermask]
                        filtermask = (np.round(filtereddata[:, marker], 3) >= np.round(self.lowerbounds[marker], 3))
                        filtereddata = filtereddata[filtermask]

                    # Update the list of cell IDs included in the table for each image.
                    self.combcellnums[imind + i] = [self.orders[imind + i][j] for j in
                                                    filtereddata[:, -1].astype(np.int).tolist()]
                    if imind + i == self.index:
                        currentdata = currentdata[filtereddata[:, -1].astype(np.int).tolist(), :]

                # Update the table with quantified values for the included cells.
                self.cellnums = self.combcellnums[self.index]
                displaycellnums = [int(self.Qtab[self.index][i, 0]) - 1 for i in self.cellnums]
                self.update_table(currentdata, self.lowerbounds, self.upperbounds, len(self.Qtab[self.index]),
                                  displaycellnums)

                # If any cells are included, and at least one cell is filtered out, add an image to the
                # viewer containing the included cells.
                self.set_invisible(self.viewer)
                if self.Qtab[self.index].shape[0] > currentdata.shape[0] > 0:
                    for i in range(self.numimgs):
                        mask = np.in1d(self.objectplots[imind + i],
                                       self.Qtab[imind + i][np.asarray(self.combcellnums[imind + i]).astype(np.int), 0])
                        mask = mask.reshape((1, self.maximageshape[0], self.maximageshape[1]))
                        if i == 0:
                            self.viewer.add_image(mask, name="Filter", blending="additive", visible=True)
                        else:
                            self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, mask))

                # Un-check cells that are not included in the filter.
                for i in range(self.Qtab[self.index].shape[0]):
                    if i in self.currentlyselectedcells[self.index] and self.orders[self.index][i] not in \
                            self.combcellnums[self.index]:
                        self.currentlyselectedcells[self.index].remove(i)

            # If filtering an object clustering table.
            elif self.mode == "Object":
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(self.lowerbounds)):
                    if (self.lowerbounds[i] > self.minvalsobject[self.index][i] or self.upperbounds[i] <
                            self.maxvalsobject[self.index][i]):
                        filteredmarkers.append(i)

                # Find object clustering data table, and append index values at the end to log sort order.
                cData = np.append(self.objectdatalist[self.index][self.order, 1:],
                                  np.expand_dims(np.arange(len(self.objectdatalist[self.index])), 1), 1)

                # Find the object clustering iteration corresponding to the current data table.
                if self.numimgs == 1:
                    trainnum = self.index
                else:
                    trainnum = self.index // (self.numimgs + 1)

                # Filter the table one marker at a time according to current lower- and upper-bounds.
                for marker in filteredmarkers:
                    mask = (cData[:, marker] <= self.upperbounds[marker])
                    cData = cData[mask]
                    mask = (cData[:, marker] >= self.lowerbounds[marker])
                    cData = cData[mask]

                # Store cluster IDs that will be included in the table, and in the proper order.
                self.objectclusternums = [self.order[i] for i in cData[:, -1].astype(np.int).tolist()]

                # Update the table with quantified values for the included clusters.
                currentdata = self.objectdatalist[self.index][self.order, :]
                currentdata = currentdata[cData[:, -1].astype(np.int).tolist(), :]
                self.update_table(currentdata, self.lowerbounds, self.upperbounds,
                                  len(self.objectdatalist[self.index]), self.objectclusternums)

                # If any clusters are included, and at least one cluster is filtered out, add an image to the
                # viewer containing the cells in the included clusters.
                if len(self.objectdatalist[self.index]) > len(currentdata) > 0:
                    currentclusters = np.zeros_like(self.greyobjects[trainnum])
                    for index in self.objectclusternums:
                        currentclusters[self.greyobjects[trainnum] == index] = 1
                    self.viewer.add_image(currentclusters.astype(np.float), name="Filter", blending="additive",
                                          visible=True)

                # Un-check clusters that are not included in the filter.
                for i in range(len(currentdata)):
                    if self.order[i] in self.currentlyselectedobjectclusters[trainnum] and self.order[
                        i] not in self.objectclusternums:
                        self.currentlyselectedobjectclusters[trainnum].remove(self.order[i])

            # If filtering a pixel clustering table.
            else:
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(self.lowerbounds)):
                    if (self.lowerbounds[i] > self.minvalspixel[self.index][i] or self.upperbounds[i] <
                            self.maxvalspixel[self.index][i]):
                        filteredmarkers.append(i)

                # Find pixel clustering data table, and append index values at the end to log sort order.
                cData = np.append(self.datalist[self.index][self.order, 1:],
                                  np.expand_dims(np.arange(len(self.datalist[self.index])), 1), 1)

                # Find the pixel clustering iteration corresponding to the current data table.
                if self.numimgs == 1:
                    trainnum = self.index
                else:
                    trainnum = self.index // (self.numimgs + 1)

                # Filter the table one marker at a time according to current lower- and upper-bounds.
                for marker in filteredmarkers:
                    filtermask = (cData[:, marker] <= self.upperbounds[marker])
                    cData = cData[filtermask]
                    filtermask = (cData[:, marker] >= self.lowerbounds[marker])
                    cData = cData[filtermask]

                # Store cluster IDs that will be included in the table, and in the proper order.
                self.pixelclusternums = [self.order[i] for i in cData[:, -1].astype(np.int).tolist()]

                # Update the table with quantified values for the included clusters.
                currentdata = self.datalist[self.index][self.order, :]
                currentdata = currentdata[cData[:, -1].astype(np.int).tolist(), :]
                self.update_table(currentdata, self.lowerbounds, self.upperbounds,
                                  self.datalist[self.index].shape[0], self.pixelclusternums)

                # If any clusters are included, and at least one cluster is filtered out, add an image to the
                # viewer containing the cells in the included clusters.
                if len(self.datalist[self.index]) > len(currentdata) > 0:
                    currentclusters = np.zeros_like(self.greypixels[trainnum])
                    for index in self.pixelclusternums:
                        currentclusters[self.greypixels[trainnum] == index] = 1
                    self.viewer.add_image(currentclusters, name="Filter", blending="additive",
                                          visible=True)

                # Un-check clusters that are not included in the filter.
                for i in range(currentdata.shape[0]):
                    if self.order[i] in self.currentlyselectedpixelclusters[trainnum] and self.order[
                        i] not in self.pixelclusternums:
                        self.currentlyselectedpixelclusters[trainnum].remove(self.order[i])

    def generate_mst(self):
        """
        Generate a minimum spanning tree plot to illustrate phenotypic similarity of clusters for a user-defined round
        of clustering.
        """
        # Random seed for reproducibility.
        np.random.seed(0)

        # Check that the user has performed at least one clustering algorithm.
        if len(self.pixelbasedclusters) == 0:
            GUIUtils.display_error_message("No clustering results found",
                                           "MST can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been performed once, use those results.
        if len(self.pixelbasedclusters) == 1:
            clusteringnum = 0
            ispixelcluster = self.pixelbasedclusters[0]
            name = "Pixel 1" if ispixelcluster else "Object 1"
            GUIUtils.log_actions(self.actionloggerpath, "MST")

        # If multiple rounds of clustering have been performed, prompt the user to select which one to use.
        else:
            selectclusteringround = GUIUtils.SelectClusteringRound(self.pixelbasedclusters)
            selectclusteringround.exec()
            if not selectclusteringround.OK:
                return
            clusteringnum = selectclusteringround.clusteringnum
            ispixelcluster = selectclusteringround.ispixelcluster
            name = selectclusteringround.name
            GUIUtils.log_actions(self.actionloggerpath, f"MST: {clusteringnum}")

        # Retrieve the dataset being used for MST and create the output folder where images will be saved.
        if ispixelcluster:
            if self.numimgs == 1:
                currentdata = np.expand_dims(self.datalist[clusteringnum], axis=0)
            else:
                startindex = clusteringnum * (self.numimgs + 1)
                s = self.datalist[startindex].shape
                currentdata = np.zeros((self.numimgs + 1, s[0], s[1]))
                for i in range(self.numimgs + 1):
                    currentdata[i, :, :] = self.datalist[i + startindex]
            dir = GUIUtils.create_new_folder("PixelMST", self.outputfolder)
        else:
            if self.numimgs == 1:
                currentdata = np.expand_dims(self.objectdatalist[clusteringnum], axis=0)
            else:
                startindex = clusteringnum * (self.numimgs + 1)
                s = self.objectdatalist[startindex].shape
                currentdata = np.zeros((self.numimgs + 1, s[0], s[1]))
                for i in range(self.numimgs + 1):
                    currentdata[i, :, :] = self.objectdatalist[i + startindex]
            dir = GUIUtils.create_new_folder("ObjectMST", self.outputfolder)

        # Generate an MST for each image, plus the combined results if using multiple images.
        pathlist = []
        for i in range(len(currentdata)):
            # Retrieve the clustered data table for the current image.
            tabdata = DataFrame(currentdata[i, :, 1:])

            # Convert data to a distance matrix, and use that to generate the MST.
            distmatrix = np.nan_to_num(distance.cdist(currentdata[i, :, 1:], currentdata[i, :, 1:], 'euclidean'))
            pd.DataFrame(distmatrix).to_csv(os.path.join(self.outputfolder, f"DistMatrix{i + 2}.csv"))
            G = nx.from_numpy_matrix(distmatrix)
            rowname = tabdata.iloc[[i for i in range(tabdata.values.shape[0])]].astype(int).index.tolist()
            rowname = [round(x) + 1 for x in rowname]
            dictionary = dict(zip(G.nodes, rowname))
            G = nx.relabel_nodes(G, dictionary)
            T = nx.minimum_spanning_tree(G)

            # Plot MST on a graph, with nodes colored consistently with their corresponding clusters.
            colorlist = generate_colormap(tabdata.shape[0] + 1)[:, [2, 1, 0]]
            plt.figure(figsize=(10, 10))
            ax = plt.axes()
            ax.set_facecolor("#F8F9F9")
            colormap = []
            for node in T:
                colormap.append(matplotlib.colors.rgb2hex(colorlist[int(node) - 1, :] / 255))
            nx.draw_networkx(T, node_color=colormap, with_labels=True, node_size=100, font_size=5,
                             font_family='sans-serif')
            plt.show(block=False)

            # Define name if using multi-image object-clustering results for combined average data, and save the
            # plot.
            if not ispixelcluster and i == len(currentdata) - 1 and self.numimgs > 1:
                plt.title("Minimum spanning tree (Combined Images) - Object")
                plt.savefig(os.path.join(dir, "MST_Combined.png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(dir, "MST_Combined.png"))
            # Define name if using object-clustering results for single-image data, and save the plot.
            elif not ispixelcluster:
                imgname = self.filenames[i].split("/")[-1]
                imgname = imgname.split(".")[0]
                plt.title("Minimum spanning tree (" + imgname + ") - Object")
                plt.savefig(os.path.join(dir, imgname + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(dir, imgname + ".png"))
            # Define name if using multi-image pixel-clustering results for combined average data, and save the
            # plot.
            elif ispixelcluster and i == len(currentdata) - 1 and self.numimgs > 1:
                plt.title("Minimum spanning tree (Combined Images) - Pixel")
                plt.savefig(os.path.join(dir, "MST_Combined.png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(dir, "MST_Combined.png"))
            # Define name if using pixel-clustering results for single-image data, and save the plot.
            elif ispixelcluster:
                imgname = self.filenames[i].split("/")[-1]
                imgname = imgname.split(".")[0]
                plt.title("Minimum spanning tree (" + imgname + ") - Pixel")
                plt.savefig(os.path.join(dir, imgname + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(dir, imgname + ".png"))

        # Add all MST plots to the viewer as a single stacked image.
        arrays = [imread(fn) for fn in pathlist]
        dask_arrays = [da.from_array(ar) for ar in arrays]
        imx = da.stack(dask_arrays, axis=0)
        self.set_invisible(self.viewer)
        self.viewer.add_image(imx, name='MST (' + name + ")", blending="additive")

    def generate_nn(self):
        """
        Perform a nearest neighbours analysis to find the cells in one cluster that are within a specified radius or
        number of nearest neighbours from any cell in a different cluster, display those cells in the GUI, and quantify
        how the phenotypes of those cells compare to those of the cluster as a whole.
        """
        # Can either use an individual image, or all images combined.
        if len(self.filenames) > 1:
            imgname = GUIUtils.SelectNNImgs(self.filenames)
            imgname.exec()
            if not imgname.OK:
                return
            selectedimgindex = imgname.imgindex
            selimg = imgname.selimg
        else:
            selectedimgindex = 0
            selimg = 'All'

        # Determine which round of segmentation to use.
        imgindex = 0
        if len(self.objectimgnames) > 1:
            segmentedimage = GUIUtils.SelectSegmentedImage(self.objectimgnames)
            segmentedimage.exec()
            if not segmentedimage.OK:
                return
            imgindex = segmentedimage.imageindex

        # Determine which round of clustering to use.
        if len(self.objecttrainlist[imgindex]) > 1:
            iteration = GUIUtils.ObjectTrainIteration(len(self.objecttrainlist[imgindex]))
            iteration.exec()
            if not iteration.OK:
                return
            it = iteration.iteration
        else:
            it = 0

        # Get all the cluster IDs in the selected clustered image, and prompt the user to define source and
        # target clusters.
        clusteringround = self.objecttrainlist[imgindex][it]
        tabdata = self.tabdata[clusteringround]
        numtabs = 1
        if len(self.filenames) > 1:
            numtabs += len(self.filenames)
        clusteringround = clusteringround * numtabs + selectedimgindex
        data = self.objectdatalist[clusteringround]
        clusternums = [i + 1 for i in range(len(data)) if data[i, 0] != 0.0]
        nndis = GUIUtils.NNInRadius(clusternums)
        nndis.exec()
        if not nndis.OK:
            return

        # Show all cells from the target cluster within specified radius and/or number of nearest neighbours
        # from a cell in the source cluster.
        self.set_invisible(self.viewer)
        for i in range(self.numimgs):
            cellind = GUIUtils.get_nn_in_radius(data=tabdata[tabdata['ImgID'] == i], clusterid1=nndis.sourcecluster,
                                                clusterid2=nndis.targetcluster, radius=nndis.radius, nn=nndis.numnn)
            mask = np.in1d(self.objectplots[i], cellind)
            mask = mask.reshape((1, self.maximageshape[0], self.maximageshape[1]))
            if i == 0:
                self.viewer.add_image(mask, name="NN", blending="additive", visible=True)
            else:
                self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, mask))

        # Generate heatmap demonstrating differential marker expression between NN cells and cluster average,
        # and add to the viewer.
        if selimg == "All":
            sbb = GUIUtils.nn_to_heatmap(data=tabdata, clusterid1=nndis.sourcecluster, radius=nndis.radius,
                                         nn=nndis.numnn)
        else:
            for filename in range(len(self.filenames)):
                if str(self.filenames[filename].split("/")[-1].split(".")[0]) == selimg:
                    filenameIDX = filename
            sbb = GUIUtils.nn_to_heatmap(data=tabdata[tabdata['ImgID'] == filenameIDX], clusterid1=nndis.sourcecluster,
                                         radius=nndis.radius, nn=nndis.numnn)
        plt.setp(sbb.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        buf = io.BytesIO()
        sbb.savefig(buf)
        buf.seek(0)
        heatimg = Image.open(buf)
        self.viewer.add_image(np.array(heatimg), name="NN Enrichment", blending="additive", visible=True)
        GUIUtils.log_actions(self.actionloggerpath,
                             f"Nearest Neighbours: Segmentation ({imgindex}), Clustering ({it}), "
                             f"Source ({nndis.sourcecluster}), Target ({nndis.targetcluster}), "
                             f"Radius ({nndis.radius}), #NN ({nndis.numnn})")

    ### TODO: Test this for Windows.
    def generate_RAPID_data(self, markerindices, markernames, normalize, outfolder, PCA, denoise):
        """
        Normalize images before passing them through the RAPID algorithm.

        Args:
            markerindices (list): List of indices of cell markers being used for clustering.
            markernames (list): List of names of cell markers being used for clustering.
            normalize (str): Normalization algorithm to be applied to the image ({"None", "zscore", "log2", "log10", "all"}).
            outfolder (str): Path to folder where results will be saved.
            PCA (bool): True if using PCA normalization, otherwise False.
            denoise (bool): True if denoising the image, otherwise False.
        """

        # Open the zarr file to save files and variables to.
        self.viewer.status = "Preprocessing..."
        fh = zarr.open(outfolder, mode='a')
        fh.create_dataset('imageshapelist', data=self.imageshapelist, dtype='i4')

        # Initialize an array for the unnormalized dataset.
        unnormalized = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], len(markerindices)),
                                dtype=np.uint8)

        # Store the max values for each image for relative normalization of the heatmap in the table.
        self.datanorm = []
        for i in range(self.nummarkers):
            self.datanorm.append(np.amax(self.viewer.layers[i].data))
        # self.datanorm = np.array(self.datanorm)
        fh.create_dataset('minmax', data=self.datanorm, dtype='f8')

        # Copy image data from viewer into one array, and perform denoising/binarizing if necessary.
        for i in range(len(markerindices)):
            tmp = copy.deepcopy(self.viewer.layers[markerindices[i]].data)
            if denoise == "Denoise":
                for j in range(len(tmp)):
                    tmp[j, :, :] = denoise_img(tmp[j, :, :])
            elif denoise == "Binarize":
                for j in range(len(tmp)):
                    tmp[j, :, :] = denoise_img(tmp[j, :, :])
                tmp[tmp > 0] = 255
            unnormalized[:, :, :, i] = tmp

        # Store the total number of pixels in the images being used.
        numpixels = 0
        for shape in self.imageshapelist:
            numpixels += shape[1] * shape[0]
        fhdr = fh.create_dataset('data', shape=(numpixels, len(markerindices)), dtype='uint8')
        fhdn = fh.create_dataset('data_normalized', shape=(numpixels, len(markerindices)), dtype='uint8')
        fhdn.attrs['selmarkernames'] = markernames
        fhdn.attrs['totalpixels'] = numpixels * 1.0
        fhdn.attrs['imageslist'] = self.filenames

        # Determine whether to normalize, and initialize hdf5 file to use for normalization.
        if normalize == "None":
            normalize = None
        if not os.path.exists(os.path.join(self.outputfolder, "hdf5_files")):
            os.mkdir(os.path.join(self.outputfolder, "hdf5_files"))

        # Normalize each individual image according to the normalization type defined by the user.
        pixels = 0
        for i in range(self.numimgs):
            normalizedimg = preprocess(outfolder, medianblur=True, gaussianblur=True, gaussianblurstd=1,
                                       img=da.from_array(
                                           unnormalized[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1],
                                           :], chunks=10000),
                                       normtype=normalize).reshape(-1, unnormalized.shape[3])
            vaex.from_pandas(pd.DataFrame(normalizedimg).astype('float32')).export_hdf5(
                os.path.join(self.outputfolder, 'hdf5_files', (f'analysis_{i:02}.hdf5')))
            fhdn[pixels:pixels + self.imageshapelist[i][0] * self.imageshapelist[i][1], :] = normalizedimg
            fhdr[pixels:pixels + self.imageshapelist[i][0] * self.imageshapelist[i][1], :] = unnormalized[i,
                                                                                             :self.imageshapelist[i][0],
                                                                                             :self.imageshapelist[i][1],
                                                                                             :].reshape(
                (-1, unnormalized.shape[3]))
            pixels += self.imageshapelist[i][0] * self.imageshapelist[i][1]

        df = vaex.open(os.path.join(self.outputfolder, "hdf5_files", "analysis_*.hdf5"))
        percentlist = df.percentile_approx(df.column_names, 99).tolist()
        fhdn.attrs['percentile'] = percentlist

        # If normalizing across all images, apply z-score normalization on the entire image stack.
        if normalize == "all":
            # Apply z-scale normalization.
            df = vaex.open(os.path.join(self.outputfolder, "hdf5_files", "analysis_*.hdf5"))
            scaler = vaex.ml.StandardScaler(features=df.column_names, prefix='scaled_')
            scaler.fit(df)
            normalized = scaler.transform(df)
            scaled_cols = [col for col in normalized.column_names if 'scaled_' in col]
            fhdn[:, :] = np.asarray(normalized[scaled_cols])

            # If specified by user, apply PCA normalization to the z-scale normalized data.
            if PCA:
                npc = len(markerindices)
                if npc > 10:
                    pca = vaex.ml.PCAIncremental(features=scaled_cols, n_components=npc, batch_size=10000000)
                else:
                    pca = vaex.ml.PCA(features=scaled_cols, n_components=npc)
                pca.fit(normalized, progress='widget')
                save_preprocess(pca, self.outputfolder + "/vmodels", zscore=False, pca=True)
                df_trans = pca.transform(normalized)
                PCA_cols = [col for col in df_trans.column_names if 'PCA_' in col]
                for batch in range(0, df_trans.shape[0], 10000000):
                    bs = np.min((df_trans.shape[0] - batch, 10000000))
                    tmpdata = df_trans[PCA_cols][batch:batch + bs, :npc]
                    fhdn[batch:batch + bs, :] = np.asarray(tmpdata)

        try:
            shutil.rmtree(os.path.join(self.outputfolder, "hdf5_files"))
        except:
            if not os.access(os.path.join(self.outputfolder, "hdf5_files"), os.W_OK):
                os.chmod(os.path.join(self.outputfolder, "hdf5_files"), stat.S_IWUSR)
                shutil.rmtree(os.path.join(self.outputfolder, "hdf5_files"))
            else:
                pass
        self.viewer.status = "RAPID data generation complete"

    def load_environment(self):
        """
        Open a directory for the user to load a previous RAPID GUI session to resume it exactly as they left it.
        """
        config = configparser.ConfigParser()
        path = QFileDialog().getOpenFileName(filter="*.ini")[0]
        if path == "":
            return False
        p = "/".join(path.split("/")[:-1])
        imgpaths = glob.glob(p + "/Layer*")
        config.read(path)

        self.datavals = datavals

        self.addedtable = config.getboolean("Variables", 'addedtable')
        self.addwhenchecked = config.getboolean("Variables", 'addwhenchecked')
        self.editedimage = config.getboolean("Variables", 'editedimage')
        self.hasloadedpixel = config.getboolean("Variables", 'hasloadedpixel')
        self.imagehasbeenloaded = config.getboolean("Variables", 'imagehasbeenloaded')

        self.actionloggerpath = config.get("Variables", 'actionloggerpath')
        self.biaxialcount = config.getint("Variables", 'biaxialcount')
        self.displayselectedcount = config.getint("Variables", 'displayselectedcount')
        self.editimagepath = config.getint("Variables", 'editimagepath')
        self.index = config.getint("Variables", 'index')
        self.listindex = config.getint("Variables", 'listindex')
        self.mode = config.get("Variables", 'mode')
        self.numclasses = config.getint("Variables", 'numclasses')
        self.numimgs = config.getint("Variables", 'numimgs')
        self.nummarkers = config.getint("Variables", 'nummarkers')
        self.objecttraincount = config.getint("Variables", 'objecttraincount')
        self.outputfolder = config.get("Variables", 'outputfolder')
        self.pixeltraincount = config.getint("Variables", 'pixeltraincount')
        self.res = config.getfloat("Variables", 'res')
        self.segmentcount = config.getint("Variables", 'segmentcount')
        self.selectedregioncount = config.getint("Variables", 'selectedregioncount')
        self.tableimgcount = config.getint("Variables", 'tableimgcount')
        self.umapcount = config.getint("Variables", 'umapcount')

        self.annotatedclusters = ast.literal_eval(config.get("Variables", 'annotatedclusters'))
        self.cellindices = ast.literal_eval(config.get("Variables", 'cellindices'))
        self.cellnums = ast.literal_eval(config.get("Variables", 'cellnums'))
        columnheaders = ast.literal_eval(config.get("Variables", 'columnheaders'))
        for header in columnheaders:
            self.columnheaders.append(header)
        self.combcellnums = ast.literal_eval(config.get("Variables", 'combcellnums'))
        self.coordinates = []
        coords = ast.literal_eval(config.get("Variables", 'coordinates'))
        for i in range(len(coords)):
            self.coordinates.append([np.array(l) for l in coords[i]])
        self.cortabs = ast.literal_eval(config.get("Variables", 'cortabs'))
        self.curimgs = ast.literal_eval(config.get("Variables", 'curimgs'))
        self.currentlyselectedcells = ast.literal_eval(config.get("Variables", 'currentlyselectedcells'))
        self.currentlyselectedobjectclusters = ast.literal_eval(
            config.get("Variables", 'currentlyselectedobjectclusters'))
        self.currentlyselectedpixelclusters = ast.literal_eval(config.get("Variables", 'curentlyselectedpixelclusters'))
        self.datalist = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'datalist'))]
        self.datanorm = ast.literal_eval(config.get("Variables", 'datanorm'))
        self.datavals = np.array(ast.literal_eval(config.get("Variables", 'datavals')))
        self.editactions = ast.literal_eval(config.get("Variables", 'editactions'))
        self.filenames = ast.literal_eval(config.get("Variables", 'filenames'))
        self.flipimg = pd.DataFrame(ast.literal_eval(config.get("Variables", 'flipimg')))
        self.fulltab = pd.DataFrame(ast.literal_eval(config.get("Variables", 'fulltab')))
        self.greyobjects = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'greyobjects'))]
        self.greypixels = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'greypixels'))]
        self.groupslist = ast.literal_eval(config.get("Variables", 'groupslist'))
        self.groupsnames = ast.literal_eval(config.get("Variables", 'groupsnames'))
        self.imageshapelist = ast.literal_eval(config.get("Variables", 'imageshapelist'))
        self.lowerbounds = ast.literal_eval(config.get("Variables", 'lowerbounds'))
        self.lowerboundslist = ast.literal_eval(config.get("Variables", 'lowerboundslist'))
        self.markers = ast.literal_eval(config.get("Variables", 'markers'))
        self.maximageshape = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'maximageshape'))]
        self.maxvalsobject = ast.literal_eval(config.get("Variables", 'maxvalsobject'))
        self.maxvalspixel = ast.literal_eval(config.get("Variables", 'maxvalspixel'))
        self.maxvalssegment = ast.literal_eval(config.get("Variables", 'maxvalssegment'))
        self.mergedimagespaths = ast.literal_eval(config.get("Variables", 'mergedimagespaths'))
        self.mergememmarkers = ast.literal_eval(config.get("Variables", 'mergememmarkers'))
        self.mergenucmarkers = ast.literal_eval(config.get("Variables", 'mergenuclearmarkers'))
        self.minvalsobject = ast.literal_eval(config.get("Variables", 'minvalsobject'))
        self.minvalspixel = ast.literal_eval(config.get("Variables", 'minvalspixel'))
        self.minvalssegment = ast.literal_eval(config.get("Variables", 'minvalssegment'))
        self.objectclusterdirectories = ast.literal_eval(config.get("Variables", 'objectclusterdirectories'))
        self.objectclusterindices = ast.literal_eval(config.get("Variables", 'objectclusterindices'))
        self.objectclusternums = ast.literal_eval(config.get("Variables", 'objectclusternums'))
        self.objectclusters = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'objectclusters'))]
        self.objectcolor = ast.literal_eval(config.get("Variables", 'objectcolor'))
        self.objectdatalist = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'objectdatalist'))]
        self.objectimgnames = ast.literal_eval(config.get("Variables", 'objectimgnames'))
        self.objectplots = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'objectplots'))]
        self.objecttrainlist = ast.literal_eval(config.get("Variables", 'objecttrainlist'))
        self.order = ast.literal_eval(config.get("Variables", 'order'))
        self.orders = ast.literal_eval(config.get("Variables", 'orders'))
        self.pixelbasedclusters = ast.literal_eval(config.get("Variables", 'pixelbasedclusters'))
        self.pixelclusterdirectories = ast.literal_eval(config.get("Variables", 'pixelclusterdirectories'))
        self.pixelclusterindices = ast.literal_eval(config.get("Variables", 'pixelclusterindices'))
        self.pixelclustermarkers = ast.literal_eval(config.get("Variables", 'pixelclustermarkers'))
        self.pixelclusternums = ast.literal_eval(config.get("Variables", 'pixelclusternums'))
        self.pixelcolor = ast.literal_eval(config.get("Variables", 'pixelcolor'))
        self.Qtab = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'Qtab'))]
        self.sampleshapes = ast.literal_eval(config.get("Variables", 'sampleshapes'))
        self.segmentationindicesinumap = ast.literal_eval(config.get("Variables", 'segmentationindicesinumap'))
        self.segmentcounts = ast.literal_eval(config.get("Variables", 'segmentcounts'))
        self.segmentedimgpaths = ast.literal_eval(config.get("Variables", 'segmentedimgpaths'))
        self.tabdata = [pd.read_json(l) for l in ast.literal_eval(config.get("Variables", 'tabdata'))]
        self.tableimagenames.remove('None')
        tableimagenames = ast.literal_eval(config.get("Variables", 'tableimagenames'))
        for name in tableimagenames:
            self.tableimagenames.append(name)
        self.tableorder = ast.literal_eval(config.get("Variables", 'tableorder'))
        self.umapplots = ast.literal_eval(config.get("Variables", 'umapplots'))
        self.upperbounds = ast.literal_eval(config.get("Variables", 'upperbounds'))
        self.upperboundslist = ast.literal_eval(config.get("Variables", 'upperboundslist'))
        self.verticalheaderlabels = np.array(ast.literal_eval(config.get("Variables", 'verticalheaderlabels')))
        self.xmins = ast.literal_eval(config.get("Variables", 'xmins'))
        self.xmaxs = ast.literal_eval(config.get("Variables", 'xmaxs'))
        self.ymins = ast.literal_eval(config.get("Variables", 'ymins'))
        self.ymaxs = ast.literal_eval(config.get("Variables", 'ymaxs'))

        for i in range(len(imgpaths)):
            fh = zarr.open("/".join(imgpaths[i].split("/")[:-1]))
            file = f"Layer{i + 1}"
            data = np.array(fh[file])
            cmap = Colormap(ColorArray([(0, 0, 0), (
                fh[file].attrs["Colormap0"] / 255., fh[file].attrs["Colormap1"] / 255.,
                fh[file].attrs["Colormap2"] / 255.)]))
            self.viewer.add_image(data, contrast_limits=fh[file].attrs["CLRange"], gamma=fh[file].attrs["Gamma"],
                                  opacity=fh[file].attrs["Opacity"], colormap=cmap, visible=fh[file].attrs["Visible"],
                                  name=fh[file].attrs["Name"], blending="additive")
            self.viewer.layers[fh[file].attrs["Name"]].contrast_limits = fh[file].attrs["CL"]

        if self.addedtable:
            self.addedtable = False
            self.datavals = np.array(ast.literal_eval(config.get("Variables", 'datavals')))
            self.numclasses = config.getint("Variables", 'numclasses')
            self.tableorder = ast.literal_eval(config.get("Variables", 'tableorder'))
            self.update_table(self.datavals, self.lowerbounds, self.upperbounds, self.numclasses, self.tableorder)
            self.loadingenv = True
            self.sorttableimages.marker.choices = self.columnheaders
            self.sorttableimages.data.choices = self.tableimagenames
            self.sorttableimages.marker.value = config.get("Variables", 'tablecurrentmarker')
            self.sorttableimages.data.value = config.get("Variables", 'tablecurrentdata')
            self.sorttableimages.sort.value = config.get("Variables", 'tablecurrentsort')
            self.loadingenv = False
        return path

    def load_object_clusters(self):
        """
        Allow user to select a .csv file that they would like to use to load clusters for a given segmented image.
        """
        # Define path to csv file with clustering results to be loaded, and read into a dataframe.
        loadcsv = GUIUtils.LoadObjectClusters()
        loadcsv.exec()
        if not loadcsv.OK:
            return
        fulltab = pd.read_csv(loadcsv.csvpath)
        fulltab = fulltab.drop(fulltab.columns[0], axis=1)

        # Select segmentation iteration to be used for cluster assignments.
        segmentindex = 0
        if len(self.objectimgnames) > 1:
            segmentedimage = GUIUtils.SelectSegmentedImage(self.objectimgnames)
            segmentedimage.exec()
            if not segmentedimage.OK:
                return
            segmentindex = segmentedimage.imageindex

        # Allow user to decide whether to add the labeled and/or colored image.
        selectimagesadded = GUIUtils.GreyColorImages()
        selectimagesadded.exec()
        if not selectimagesadded.OK:
            return

        # Get the indices of all the columns to use from the segmented table.
        markerinds = [0]
        params = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        markerinds += [params.index(mname) + 1 for mname in fulltab.columns[6:]]
        # [markerinds.append(params.index(mname) + 1) for mname in fulltab.columns[6:]]

        # Retrieve quantified expression of each of the included cell markers for each cell.
        complete_tab = []
        startind = segmentindex * self.numimgs
        for tab_len in range(self.numimgs):
            complete_tab.append(self.Qtab[tab_len + startind][:, markerinds])
        complete_tab = np.vstack(complete_tab)

        # Only can load clusters if there are the same number of cells.
        if fulltab.shape[0] != complete_tab.shape[0]:
            GUIUtils.display_error_message("Incompatible number of cells",
                                           "Please make sure the table you selected corresponds to the segmented image")
            return

        # Store the loaded clustering results and save to the current output folder.
        self.tabdata.append(fulltab)
        dir = GUIUtils.create_new_folder('RAPIDObject_', self.outputfolder)
        fulltab.to_csv(os.path.join(dir, "FullObject_segmentation_dataClusterReclustred.csv"))

        # Save the segmented data table to the current output folder.
        complete_tab_DF = pd.DataFrame(complete_tab)
        complete_tab_DF.columns = fulltab.iloc[:, markerinds].columns
        complete_tab_DF.to_csv(os.path.join(dir, "FullObject_segmentation_data.csv"))

        # Update the segmented data table to include the new cluster IDs for each cell.
        to_values = fulltab['Cluster']
        vals = list(copy.deepcopy(np.unique(to_values)))

        unique = np.unique(to_values)
        for i in range(len(unique)):
            to_values[to_values == unique[i]] = i + 1
        fulltab['Cluster'] = to_values

        # Retrieve relevant columns from relabeled table.
        relabeled_table = fulltab.iloc[:, [i for i in range(4, fulltab.shape[1])]]

        # Initialize data array for clustered image, and generate the colormap.
        relabledgreyimages = np.zeros((self.numimgs, self.objectplots[0].shape[0], self.objectplots[0].shape[1]),
                                      dtype=np.uint8)
        color = generate_colormap(len(np.unique(to_values)) + 1)
        self.objectcolor.append(color)
        np.save(os.path.join(dir, "color.npy"), color)
        fullclusterdata = []
        startindex = 0
        for i in range(self.numimgs):
            # Relabel the segmented result for the current image and save it to the output folder.
            from_values = complete_tab_DF['Label'].values[startindex:startindex + len(self.Qtab[i + startind])]
            tmp_to_values = to_values[startindex:startindex + len(self.Qtab[i + startind])].values
            self.objectclusters.append(copy.deepcopy(tmp_to_values))
            relabeled = self.method_searchsort(from_values, tmp_to_values,
                                               self.objectplots[i + startind].flatten().astype(int))
            relabledgreyimages[i, :, :] = (relabeled.reshape(self.objectplots[i + startind].shape)).astype(np.uint8)
            relabledgreyimages[i, :, :][self.objectplots[i + startind] == 0] = 0
            cv.imwrite(os.path.join(dir, f"RELABELED_Grey{i}.png"),
                       relabledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1)

            # Apply the colormap to the relabeled image and save it to the output folder.
            relabledimages = np.zeros((self.objectplots[0].shape[0], self.objectplots[0].shape[1], 3), dtype=np.uint8)
            for j in range(len(vals)):
                relabledimages[:, :, 0][relabledgreyimages[i, :, :] == j + 1] = color[j][0]
                relabledimages[:, :, 1][relabledgreyimages[i, :, :] == j + 1] = color[j][1]
                relabledimages[:, :, 2][relabledgreyimages[i, :, :] == j + 1] = color[j][2]
            tifffile.imwrite(os.path.join(dir, f"RELABELED_{i}.tif"),
                             relabledimages[:self.imageshapelist[i][0], :self.imageshapelist[i][1], :])

            # Add the relabeled colored and/or greyscale image(s) to the viewer.
            if i == 0:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabledimages.dtype)
                relab[0, :relabledimages.shape[0], :relabledimages.shape[1], :] = relabledimages
                if selectimagesadded.grey:
                    self.viewer.add_image(relabledgreyimages[i, :, :],
                                          name=f"Object Cluster IDs {self.objecttraincount + 1}", blending="additive",
                                          contrast_limits=(0, np.max(relabledgreyimages)))
                if selectimagesadded.color:
                    self.viewer.add_image(relab, name=f"Object Clusters {self.objecttraincount + 1}",
                                          blending="additive")
            else:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabledimages.dtype)
                relab[0, :relabledimages.shape[0], :relabledimages.shape[1], :] = relabledimages
                if selectimagesadded.grey and selectimagesadded.color:
                    self.viewer.layers[-2].data = np.stack((self.viewer.layers[-2].data, relabledgreyimages[i, :, :]),
                                                           0)
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))
                elif selectimagesadded.grey:
                    self.viewer.layers[-1].data = np.stack((self.viewer.layers[-1].data, relabledgreyimages[i, :, :]),
                                                           0)
                elif selectimagesadded.color:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))
            del relabledimages
            gc.collect()

            # Take the quantified values from only the cells in the current image.
            tmp_tab = relabeled_table[startindex:startindex + len(self.Qtab[i])].values
            tmp_tab_df = pd.DataFrame(tmp_tab)
            startindex += len(self.Qtab[i])

            # Find the average marker expression across each cluster represented in the table.
            grouped = tmp_tab_df.groupby(0)
            tabres = grouped.apply(np.mean)

            # Include the image ID and the total number of cells from each cluster in the table.
            tabres.insert(0, "Sample", i)
            _, counts = np.unique(tmp_tab[:, 0], return_counts=True)
            tabres.insert(2, "Cells", counts)

            # Find the min and max values of each cell marker for the clusters in the current image.
            clusteravgs = np.zeros((len(unique), relabeled_table.shape[1] + 2))
            clusteravgs[np.unique(tmp_to_values.astype(np.uint8) - 1), :] = tabres.values
            fullclusterdata.append(clusteravgs.astype(np.float))
            self.objectdatalist.append(clusteravgs[:, 2:].astype(np.float))
            tab = clusteravgs[np.unique(tmp_to_values.astype(np.uint8) - 1), 2:]
            minvals = []
            maxvals = []
            for i in range(tab.shape[1] - 1):
                minvals.append(np.min(tab[:, i + 1]))
                maxvals.append(np.max(tab[:, i + 1]))
            self.minvalsobject.append(copy.deepcopy(minvals))
            self.maxvalsobject.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))

        # Find weighted average data and update lower/upper bounds.
        fullclusterdata = np.nan_to_num((np.vstack(fullclusterdata)))
        if self.numimgs > 1:
            weighted_average = np.zeros((len(np.unique(to_values)), fullclusterdata.shape[1] - 2))
            for i in range(fullclusterdata.shape[0]):
                currcluster = i % weighted_average.shape[0]
                weighted_average[currcluster, 0] += fullclusterdata[i, 2]
            for i in range(fullclusterdata.shape[0]):
                currcluster = i % weighted_average.shape[0]
                weighted_average[currcluster, 1:] += fullclusterdata[i, 3:] * fullclusterdata[i, 2] / weighted_average[
                    currcluster, 0]
            self.objectdatalist.append(weighted_average)
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            self.minvalsobject.append(copy.deepcopy(minvals))
            self.maxvalsobject.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))

        # Relabel the segmented images with cluster IDs.
        for i in range(self.numimgs):
            relabledgreyimages[i, :, :][self.objectplots[i + startind] == 0] = 0
        unique = np.unique(relabledgreyimages)
        for i in range(len(unique)):
            relabledgreyimages[relabledgreyimages == unique[i]] = i
        self.greyobjects.append(relabledgreyimages)
        del relabledgreyimages
        gc.collect()

        # Save the dataset to the output folder as a csv file.
        mergemarkerlist = list(fulltab.columns[5:].values)
        clusterdf = pd.DataFrame(np.nan_to_num(fullclusterdata))
        clusterdf.columns = np.hstack([["Sample", "Cluster", "Pixels"], mergemarkerlist])
        clusterdf.to_csv(os.path.join(dir, "RAPIDObject_cluster_table.csv"))

        # Generate MST plot for the clustered data.
        tabledata, datascaled, DistMatrix, uniqueClusters = \
            prep_for_mst(clustertable=clusterdf, minnumpixels=1, outfolder=dir, includedmarkers=mergemarkerlist)
        generate_mst(distancematrix=DistMatrix, normalizeddf=datascaled[datascaled.columns], colors=color,
                     randomseed=0, outfolder=dir, clusterheatmap=True, displaymarkers=mergemarkerlist,
                     uniqueclusters=uniqueClusters, samplenames=list(np.unique(clusterdf['Sample'])),
                     displaysingle=False)

        # Update the table widget dropdown options.
        for i in range(self.numimgs):
            self.tableimagenames.append(
                f"Object Cluster {self.objecttraincount + 1} - {self.filenames[i].split('/')[-1]}")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
        if self.numimgs > 1:
            self.tableimagenames.append(f"Object Cluster {self.objecttraincount + 1} - Combined Average")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1

        # Update any necessary variables.
        self.objecttrainlist[0].append(self.objecttraincount)
        self.currentlyselectedobjectclusters.append([])
        self.objecttraincount += 1
        self.pixelbasedclusters.append(False)
        self.annotatedclusters.append([])
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Object Cluster {self.objecttraincount} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        GUIUtils.log_actions(self.actionloggerpath, f"Loading Clusters: Path ({loadcsv.csvpath}), Segmentation "
                                                    f"({segmentindex})")

    ### TODO: Decide whether to load all markers, or just the ones used for clustering.
    def load_pixel_results(self):
        """
        Open a directory for the user to select which pixel-based results they would like to load.

        :return: datapath *(str)*: \n
            Path to the results being loaded.
        """
        # User cannot load pixel-based results multiple times due to potential image incompatibility.
        if self.hasloadedpixel:
            GUIUtils.display_error_message("Results already loaded",
                                           "You have already loaded results. Please open another window if you would like to load different data")
            return ""

        # Prompt user to indicate the path to the results being loaded, and ensure the selected path contains compatible
        # RAPID-P results.
        datapath = QFileDialog().getExistingDirectory(None, "Select Folder")
        if datapath == "":
            return ""
        if not datapath.endswith("/RAPID_Data"):
            datapath = os.path.join(datapath, "RAPID_Data")
        try:
            inputzarr = zarr.open(datapath, mode='r')
            color, data, data_normalized, grey, imageshapelist, minmax, prob, tab, filenames, selmarkernames, totalpixels, \
            percentile, columns, arg, flipimg = self.load_pixel_zarr(inputzarr)
        except:
            GUIUtils.display_error_message("No data at indicated path",
                                           "Please select a path with RAPID Data")
            return ""

        # Prompt user to indicate the root folder where new results will be saved.
        GUIUtils.OKButtonPopup("Select Output Folder").exec()
        dialog = QFileDialog()
        outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
        self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
        self.viewer.status = "Loading analysis..."

        # Save image attributes to the output folder.
        dir = GUIUtils.create_new_folder("RAPIDPixel_", self.outputfolder)
        self.pixelclusterdirectories.append(dir)
        outfolder = os.path.join(dir, "RAPID_Data")
        outputzarr = zarr.open(outfolder, 'w')
        outputzarr['color'] = color
        outputzarr['data'] = data
        outputzarr['data_normalized'] = data_normalized
        outputzarr['grey'] = grey
        outputzarr['imageshapelist'] = imageshapelist
        outputzarr['minmax'] = minmax
        outputzarr['prob'] = prob
        outputzarr['tab'] = tab
        outputzarr['data_normalized'].attrs['imageslist'] = filenames
        outputzarr['data_normalized'].attrs['selmarkernames'] = selmarkernames
        outputzarr['data_normalized'].attrs['totalpixels'] = totalpixels
        outputzarr['data_normalized'].attrs['percentile'] = percentile
        outputzarr['tab'].attrs['columns'] = columns
        outputzarr.attrs['arg'] = arg
        outputzarr.attrs['flipimg'] = flipimg
        outputzarr.attrs['markers'] = selmarkernames

        # Prompt user to select which image(s) to load.
        imgnames = []
        for path in filenames:
            name = path.split("/")
            imgnames.append(name[-1])
        imagenums = [0]
        if len(filenames) > 1:
            selectimages = GUIUtils.SelectLoadImages(imgnames)
            selectimages.exec()
            if not selectimages.OK:
                return False
            imagenums = selectimages.images

        # Retrieve data from the results being loaded.
        imageshapelist = inputzarr["imageshapelist"][:]
        self.imageshapelist = [(int(imageshapelist[i][0]), int(imageshapelist[i][1]), int(imageshapelist[i][2])) for i
                               in imagenums]
        greyflattened, tab, c = inputzarr["grey"][:], inputzarr["tab"][:], inputzarr["color"][:]
        self.numimgs = len(imagenums)
        args = runRAPIDzarr.get_parameters()
        args.ncluster = int(len(tab) / len(imgnames))

        # Load cell marker names and store them where applicable.
        self.markers = inputzarr['data_normalized'].attrs['selmarkernames']
        self.pixelclustermarkers.append(self.markers)
        for name in self.markers:
            self.columnheaders.append(name)
        for name in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
            self.columnheaders.append(name)
        self.nummarkers = len(self.markers)

        # Add raw images to the GUI, only for those that have been included by the user.
        colors = generate_colormap(self.nummarkers + 1)
        vdim = max([s[0] for s in imageshapelist])
        hdim = max([s[1] for s in imageshapelist])
        self.maximageshape = np.array([vdim, hdim])
        for i in range(self.nummarkers):
            data = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)
            currentmarkerdata = np.array(inputzarr['data'][:, i])
            currentmarkerdata = img_as_ubyte(currentmarkerdata)
            pixcount = 0
            imgcount = 0
            for j in range(len(imageshapelist)):
                s0 = imageshapelist[j][0]
                s1 = imageshapelist[j][1]
                if j in imagenums:
                    data[imgcount, :s0, :s1] = currentmarkerdata[pixcount:pixcount + s0 * s1].reshape((s0, s1))
                    imgcount += 1
                pixcount += s0 * s1
            cmap = Colormap(ColorArray([(0, 0, 0), (colors[i, 0] / 255., colors[i, 1] / 255., colors[i, 2] / 255.)]))
            self.viewer.add_image(data, contrast_limits=[0, 255], colormap=cmap, name=self.markers[i],
                                  blending="additive")

        # Reshape flattened label values to the proper shape for each image being loaded into the GUI.
        pixcount = 0
        imgcount = 0
        greyimgs = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1])) - 1
        for i in range(len(imageshapelist)):
            s0 = np.array(imageshapelist)[i][0]
            s1 = np.array(imageshapelist)[i][1]
            if i in imagenums:
                temp = greyflattened[pixcount:pixcount + s0 * s1].reshape((s0, s1))
                temp[:, np.array(imageshapelist)[i][1]:] = -1
                temp[np.array(imageshapelist)[i][0]:, :] = -1
                greyimgs[imgcount, :s0, :s1] = temp
                imgcount += 1
            pixcount += s0 * s1

        # By default, initialize sample groupings so that each image is in its own group.
        self.filenames = [filenames[i] for i in imagenums]
        d = {}
        for name in self.filenames:
            n = os.path.split(name)[-1]
            d[n] = n
        self.groupslist.append(d)

        # Exclude table entries for images not being loaded.
        tab = np.vstack(
            [tab[i * args.ncluster:(i + 1) * args.ncluster, :] for i in range(len(imgnames)) if i in imagenums])

        # Account for case when some clusters are no longer present if only appearing in images that have been excluded.
        if not list(np.unique(greyimgs)) == list(np.arange(len(np.unique(greyimgs)))):
            # Find cluster values that are not present.
            excludedclustervals = np.arange(args.ncluster)[~np.isin(np.arange(args.ncluster), np.unique(greyimgs))]
            excludedclustervals = np.sort(excludedclustervals)[::-1]
            # Re-index grey image.
            for cluster in excludedclustervals:
                greyimgs[greyimgs > cluster] -= 1
            # Re-index table.
            excludedrows = []
            for cluster in excludedclustervals:
                excludedrows += [int(i * args.ncluster + cluster) for i in range(len(imagenums))]
            tab = np.delete(tab, np.array(excludedrows, dtype=int), axis=0)
            args.ncluster -= len(excludedclustervals)

        # Update any necessary variables.
        self.flipimg = [inputzarr.attrs['flipimg'][i] for i in imagenums]
        self.datanorm = list(inputzarr['minmax'][:])
        if not max(self.datanorm) > 1.0:
            self.datanorm = [a * 255. for a in self.datanorm]
        self.markernums = [i for i in range(len(self.markers))]
        self.mode = "Pixel"
        self.greypixels.append(greyimgs)
        self.apply_RAPID_pixel(tab, args, c)
        self.viewer.dims.set_current_step(0, 0)
        self.pixeltraincount += 1
        self.annotatedclusters.append([])
        self.currentlyselectedpixelclusters.append([])
        self.sorttableimages.reset_choices()
        self.hasloadedpixel = True

        return datapath

    def load_pixel_zarr(self, zarrpath):
        """
        Load all necessary zarr files when loading pixel-based clustering results.

        Args:
            zarrpath (str): Path to the root directory where zarr files are being loaded from.

        :return: *(tuple)*: \n
            Tuple of zarr attributes that must be loaded when loading pixel-based clustering results.
        """
        return zarrpath['color'], zarrpath['data'], zarrpath['data_normalized'], zarrpath['grey'], \
               zarrpath['imageshapelist'], zarrpath['minmax'], zarrpath['prob'], zarrpath['tab'], \
               zarrpath['data_normalized'].attrs['imageslist'], zarrpath['data_normalized'].attrs['selmarkernames'], \
               zarrpath['data_normalized'].attrs['totalpixels'], zarrpath['data_normalized'].attrs['percentile'], \
               zarrpath['tab'].attrs['columns'], zarrpath.attrs['arg'], zarrpath.attrs['flipimg']

    def load_segmentation_results(self):
        """
        Open a directory for the user to select which segmentation results they would like to load.

        :return: filenames *(list)*: \n
            List of paths to the labeled segmented images being loaded. Return False if no files are selected.
        """
        filenames, _ = QFileDialog.getOpenFileNames(parent=self.viewer.window.qt_viewer, caption='Select Label image', )
        if len(filenames) == 0:
            return False

        # Allow user to decide whether to add the labeled and/or colored image.
        selectimagesadded = GUIUtils.GreyColorImages()
        selectimagesadded.exec()
        if not selectimagesadded.OK:
            return False

        GUIUtils.OKButtonPopup("Select Output Folder").exec()
        dialog = QFileDialog()
        # self.outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
        outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
        self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)

        if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "RawImages")):
            rootfold = os.path.join(os.path.split(filenames[0])[0], "RawImages")
            subfolders = glob.glob(rootfold + "/*")
            subfolders.sort()
            fh = zarr.open(rootfold)
            self.nummarkers = len(subfolders)
            self.imagehasbeenloaded = True
            self.filenames = fh.attrs['filenames']
            self.maximageshape = np.array(fh.attrs['maximageshape'])
            self.imageshapelist = fh.attrs['imageshapelist']
            self.markers = fh.attrs['markers']
            self.markernums = fh.attrs['markernums']
            self.numimgs = fh.attrs['numimgs']
            d = {}
            for name in self.filenames:
                n = os.path.split(name)[-1]
                d[n] = n

            newfilenames = [fn for fn in self.filenames if
                            os.path.split(fn)[-1].split(".")[0] in [os.path.split(fn)[-1].split(".")[0][10:] for fn in
                                                                    filenames]]
            imginds = [self.filenames.index(fn) for fn in newfilenames]
            self.filenames = newfilenames

            self.groupslist.append(d)
            for i in range(self.nummarkers):
                file = os.path.split(subfolders[i])[-1]
                data = np.array(fh[file])
                cmap = Colormap(ColorArray([(0, 0, 0), (
                    fh[file].attrs["Colormap0"] / 255., fh[file].attrs["Colormap1"] / 255.,
                    fh[file].attrs["Colormap2"] / 255.)]))
                self.viewer.add_image(data[imginds, :, :], contrast_limits=fh[file].attrs["CLRange"],
                                      gamma=fh[file].attrs["Gamma"], opacity=fh[file].attrs["Opacity"],
                                      colormap=cmap, visible=fh[file].attrs["Visible"], name=fh[file].attrs["Name"],
                                      blending="additive")
                self.viewer.layers[fh[file].attrs["Name"]].contrast_limits = fh[file].attrs["CL"]
            fh = zarr.open(os.path.join(os.path.split(filenames[0])[0]))
            mergedimg = np.array(fh["MergedImage"])
            print(f"SHAPE: {mergedimg.shape}")
            if len(np.unique(mergedimg[0, imginds, :, :])) == 1:
                self.viewer.add_image(mergedimg[1, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                      blending="additive")
            elif len(np.unique(mergedimg[1, imginds, :, :])) == 1:
                self.viewer.add_image(mergedimg[0, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                      blending="additive")
            else:
                self.viewer.add_image(mergedimg[:, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                      blending="additive")
            self.columnheaders += self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            self.sorttableimages.marker.choices = tuple(self.columnheaders)
            labelimageslist = []
            for path in filenames:
                filename = os.path.join(os.path.abspath(path))
                labelimages = np.zeros((self.maximageshape[0], self.maximageshape[1]), dtype=np.uint32)
                loadedimg = self.parse_img(filename, True)
                labelimages[:loadedimg.shape[0], :loadedimg.shape[1]] = loadedimg
                labelimageslist.append(labelimages)
        else:
            while True:
                compatible = True
                GUIUtils.OKButtonPopup("Open Raw Images").exec()
                openedimgs = self.open_images(filenames)
                if not openedimgs:
                    return False
                elif openedimgs == "False":
                    compatible = False
                else:
                    imgfilenames = [os.path.split(name)[-1].split(".")[0] for name in self.filenames]
                    fnames = copy.deepcopy(imgfilenames)
                    fnames.sort()
                    orders = [fnames.index(name) for name in imgfilenames]
                    origimgnames = [fnames[i] for i in orders]
                    filenames.sort()
                    filenames = [filenames[i] for i in orders]
                    for i in range(len(origimgnames)):
                        filename = os.path.split(filenames[i])[-1].split(".")[0]
                        if not origimgnames[i] in os.path.split(filenames[i])[-1].split(".")[0]:
                            GUIUtils.display_error_message("Mismatching image names",
                                                           "Please ensure the raw images correspond to the segmented "
                                                           "image and are named consistently with the raw images. "
                                                           "Acceptable names are in the format \"[prefix][Raw Image Name]"
                                                           "[Suffix], with the prefix and suffix consistent across all "
                                                           "images\"")
                            compatible = False
                            for j in range(len(self.viewer.layers)):
                                self.viewer.layers.pop(0)
                            self.groupslist = []
                            self.imagehasbeenloaded = False
                            self.imageshapelist = []
                            self.numimgs = 0
                            break
                        if i == 0:
                            prefixsuffix = filename.split(origimgnames[i])
                        else:
                            if filename.split(origimgnames[i]) != prefixsuffix:
                                GUIUtils.display_error_message("Mismatching image names",
                                                               "Please ensure the raw images correspond to the segmented "
                                                               "image and are named consistently with the raw images. "
                                                               "Acceptable names are in the format \"[prefix][Raw Image "
                                                               "Name][Suffix], with the prefix and suffix consistent "
                                                               "across all images\"")
                                compatible = False
                                for j in range(len(self.viewer.layers)):
                                    self.viewer.layers.pop(0)
                                self.groupslist = []
                                self.imagehasbeenloaded = False
                                self.imageshapelist = []
                                self.numimgs = 0
                                break

                if compatible:
                    labelimageslist = []
                    for i in range(len(filenames)):
                        filename = os.path.join(os.path.abspath(filenames[i]))
                        labelimages = np.zeros((self.maximageshape[0], self.maximageshape[1]), dtype=np.uint32)
                        loadedimg = self.parse_img(filename, True)
                        labelimages[:loadedimg.shape[0], :loadedimg.shape[1]] = loadedimg
                        labelimageslist.append(labelimages)
                    break

        cortabs = []
        rgbimages = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
        # all_labelscombined = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint32)
        for path in filenames:
            i = filenames.index(path)
            labelimages = labelimageslist[i]
            minvals = []
            maxvals = []
            # all_labels = labelimages
            # obejctcount = np.max(all_labels)
            # all_labels, obejctcount = measure.label(labelimages, connectivity=1, return_num=True)
            # all_labelscombined[i,:all_labels.shape[0],:all_labels.shape[1]] = all_labels
            proptab = np.zeros((self.nummarkers + 4, len(np.unique(labelimages)) - 1))
            start = time.time()
            for ch in range(self.nummarkers):
                proptab[ch, :] = measure.regionprops_table(labelimages, self.viewer.layers[ch].data[i, :, :],
                                                           properties=['mean_intensity'])['mean_intensity']
            proptab[self.nummarkers, :] = [prop.area for prop in
                                           measure.regionprops(labelimages,
                                                               intensity_image=self.viewer.layers[0].data[i, :, :])]
            proptab[self.nummarkers + 1, :] = [prop.eccentricity for prop in
                                               measure.regionprops(labelimages,
                                                                   intensity_image=self.viewer.layers[0].data[i, :, :])]
            proptab[self.nummarkers + 2, :] = [prop.perimeter for prop in
                                               measure.regionprops(labelimages,
                                                                   intensity_image=self.viewer.layers[0].data[i, :, :])]
            proptab[self.nummarkers + 3, :] = [prop.major_axis_length for prop in
                                               measure.regionprops(labelimages,
                                                                   intensity_image=self.viewer.layers[0].data[i, :, :])]
            end = time.time()
            print((end - start))
            cortab = [prop.centroid for prop in
                      measure.regionprops(labelimages, intensity_image=self.viewer.layers[0].data[i, :, :])]
            labtab = [prop.label for prop in
                      measure.regionprops(labelimages, intensity_image=self.viewer.layers[0].data[i, :, :])]
            IMGMEAN = np.c_[np.asarray(labtab), proptab.T]
            rgbimage = label2rgb(labelimages, image=None, colors=None, alpha=0.3, bg_label=0, bg_color=(0, 0, 0),
                                 image_alpha=1, kind='overlay')
            rgbimage = (rgbimage * 255).astype(np.uint8)
            rgbimages[i, :rgbimage.shape[0], :rgbimage.shape[1], :] = rgbimage

            # Add the segmented image(s) to the main GUI viewer window.
            if i == 0:
                expobj = np.zeros((1, self.maximageshape[0], self.maximageshape[1]), dtype=labelimages.dtype)
                expobj[0, :labelimages.shape[0], :labelimages.shape[1]] = labelimages
                rgbimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=rgbimage.dtype)
                rgbimg[0, :rgbimage.shape[0], :rgbimage.shape[1], :] = rgbimage
                if selectimagesadded.grey:
                    self.viewer.add_image(expobj, name=f"Labels 1", blending="additive", contrast_limits=[0, 1])
                if selectimagesadded.color:
                    self.viewer.add_image(rgbimg, name=f"Segment 1", blending="additive")
            else:
                expobj = np.zeros((1, self.maximageshape[0], self.maximageshape[1]), dtype=labelimages.dtype)
                expobj[0, :labelimages.shape[0], :labelimages.shape[1]] = labelimages
                rgbimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=rgbimage.dtype)
                rgbimg[0, :rgbimage.shape[0], :rgbimage.shape[1], :] = rgbimage
                if selectimagesadded.grey and selectimagesadded.color:
                    self.viewer.layers[-2].data = np.vstack((self.viewer.layers[-2].data, expobj))
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, rgbimg))
                elif selectimagesadded.grey:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, expobj))
                elif selectimagesadded.color:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, rgbimg))

            self.viewer.dims.set_current_step(0, 0)
            cortabs.append(cortab)
            self.set_invisible(self.viewer)
            self.viewer.layers[-1].visible = True
            self.Qtab.append(IMGMEAN)
            for j in range(IMGMEAN.shape[1] - 1):
                minvals.append(np.min(IMGMEAN[:, j + 1]))
                maxvals.append(np.max(IMGMEAN[:, j + 1]))
            self.cellindices.append(len(self.lowerboundslist))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
            self.minvalssegment.append(copy.deepcopy(minvals))
            self.maxvalssegment.append(copy.deepcopy(maxvals))
            self.objectplots.append(labelimages)
            self.tableimagenames.append(f"(Segment [{self.segmentcount}]) - {path.split('/')[-1]}")
            self.tableimgcount += 1
        self.cortabs.append(cortabs)
        if 'None' in self.tableimagenames:
            self.tableimagenames.remove('None')
        self.orders = []
        self.combcellnums = []
        for i in range(len(self.Qtab)):
            order = []
            for j in range(self.Qtab[i].shape[0]):
                order.append(int(self.Qtab[i][j, 0] - 1))
            self.orders.append(order)
            self.combcellnums.append(order)
        self.cellnums = copy.deepcopy(self.orders[self.index])
        self.objecttrainlist.append([])
        for i in range(len(self.Qtab)):
            self.currentlyselectedcells.append([])
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"(Segment [{self.segmentcount}]) - {filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        self.segmentcount += 1
        self.objectimgnames.append(f"Segment {self.segmentcount}")
        self.mode = "Segmentation"
        if not self.addedtable:
            self.lowerbounds = copy.deepcopy(self.minvalssegment[0])
            self.upperbounds = copy.deepcopy(self.maxvalssegment[0])
            self.update_table(self.Qtab[0][:, 1:], self.lowerbounds, self.upperbounds, len(self.Qtab[0]),
                              self.Qtab[0][:, 0].astype(np.uint8).tolist())
        return filenames

    def manual_annotation(self):
        """
        Allow user to draw shapes on a UMAP plot to define clusters, with each shape corresponding to a cluster.
        """
        # There must be at least one UMAP plot to annotate.
        if self.umapcount == 1:
            GUIUtils.display_error_message("No UMAP detected",
                                           "You must first generate a UMAP in order to select cells to be displayed")
            return

        # Ensure there is at least one shape drawn in order to define the region to be quantified.
        ind = -1
        for i in reversed(range(len(self.viewer.layers))):
            if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and self.viewer.layers[i].visible:
                ind = i
                break
        if ind == -1:
            GUIUtils.display_error_message("Please draw a shape first",
                                           "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
            return

        # Prompt user to select which UMAP plot they would like to use.
        umapit = 0
        umapplots = copy.deepcopy(self.umapplots)
        umapplots = [b for b in umapplots if b]
        if len(umapplots) > 1:
            selectplot = GUIUtils.BiaxialUMAPIterations(umapplots)
            selectplot.exec()
            if not selectplot.OK:
                return
            umapit = selectplot.iteration

        # Determine which plot index this corresponds to, factoring in Biaxial plots.
        inds = [i for i, x in enumerate(self.umapplots) if x]
        it = inds[umapit]
        self.viewer.status = "Annotating UMAP"

        # Keep track of segmentation iteration that was used for the specified UMAP plot.
        curimg = self.curimgs[it]

        # Keep track of the bounding box vertices and geometries of each shape.
        verts = [self.viewer.layers[ind].data[i][:, -2:] for i in range(len(self.viewer.layers[ind].data))]
        type = [self.viewer.layers[ind].shape_type[i] for i in range(len(self.viewer.layers[ind].data))]

        # Label each shape and adjust their colors.
        labels = []
        for i in range(len(verts)):
            labels.append(f"Region {i + 1}")
        properties = {'class': labels, }
        s = len(self.viewer.layers[ind].data)
        self.viewer.layers.pop(ind)
        text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
        self.viewer.add_shapes(verts, shape_type=type, edge_width=0, face_color=[np.array([0.2, 0.2, 0.2])],
                               name="Manual Annotation", properties=properties, text=text_properties)

        # Allow user to name the different regions and add them as labels to the shapes.
        regionnamespopup = GUIUtils.ManualAnnotationPopup(len(verts))
        regionnamespopup.exec()
        if regionnamespopup.OK:
            labelnames = list(regionnamespopup.headernames)
            if not labelnames == labels:
                self.viewer.layers.pop(len(self.viewer.layers) - 1)
                properties = {'class': labelnames, }
                text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                self.viewer.add_shapes(verts, shape_type=type, edge_width=0, name="Manual Annotation",
                                       properties=properties,
                                       text=text_properties, face_color=[np.array([0.2, 0.2, 0.2])])
            labelnames += ["Other"]
        else:
            self.viewer.layers.pop(len(self.viewer.layers) - 1)
            return

        # Create a new output folder to save output files to.
        dir = GUIUtils.create_new_folder("RAPIDObject_", self.outputfolder)
        self.objectclusterdirectories.append(dir)

        # Initialize list of arrays of cell IDs for each cluster ID.
        to_values = [np.zeros(len(v)) for v in self.coordinates[it]]

        # Find the cells corresponding to the vertices within each of the shapes to define clusters.
        for shape in range(len(verts)):
            # Scale the vertices from 0-1 to map to coordinates on the plot.
            tupverts = copy.deepcopy(verts[shape])
            tupverts[:, 0] = ((self.xmaxs[it] - tupverts[:, 0]) / (self.xmaxs[it] - self.xmins[it])) * 1.1 - 0.05
            tupverts[:, 1] = ((tupverts[:, 1] - self.ymins[it]) / (self.ymaxs[it] - self.ymins[it])) * 1.1 - 0.05
            tupverts[:, [0, 1]] = tupverts[:, [1, 0]]
            tupverts = [tuple(x) for x in tupverts.tolist()]
            p = self.create_shape_path(tupverts, type[shape])
            for i in range(self.numimgs):
                # Find the vertices on the plot within the shape.
                mask = p.contains_points(self.coordinates[it][i])

                # Find the cells corresponding to those vertices.
                rows = list(self.Qtab[curimg + i][mask, 0].astype(int))
                to_values[i][[x - 1 for x in rows]] = shape + 1

                # Create a masked image containing only the segmented cells corresponding to those vertices.
                arr = copy.deepcopy(self.objectplots[curimg + i])
                arr[np.isin(self.objectplots[curimg + i], rows, invert=True)] = 0
                unique = list(np.unique(arr))
                for j in range(len(unique)):
                    arr[arr == unique[j]] = j
                self.objectplots.append(arr)

        # All remaining cells not within any of the shapes will be in one additional cluster together.
        rows = []
        for i in range(self.numimgs):
            for j in range(len(to_values[i])):
                if to_values[i][j] == 0:
                    rows.append(j + 1)
                    to_values[i][j] = s + 1
            arr = copy.deepcopy(self.objectplots[curimg + i])
            arr[np.isin(self.objectplots[curimg + i], rows, invert=True)] = 0
            unique = list(np.unique(arr))
            for j in range(len(unique)):
                arr[arr == unique[j]] = j
            self.objectplots.append(arr)
        to_values = np.hstack(to_values)

        # Update the table widget dropdown options.
        for i in range(self.numimgs):
            self.tableimagenames.append(
                f"Object Cluster {self.objecttraincount + 1} - {self.filenames[i].split('/')[-1]}")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
        if self.numimgs > 1:
            self.tableimagenames.append(f"Object Cluster {self.objecttraincount + 1} - Combined Average")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1

        # Set random seeds for reproducibility, and initialize to having no clusters selected in the table.
        self.currentlyselectedobjectclusters.append([])
        torch.manual_seed(0)
        np.random.seed(0)
        torch.cuda.manual_seed(0)

        # Combine all cells from each of the images into one dataframe together and save as a csv file.
        fulltab = []
        for tab_len in range(self.numimgs):
            fulltab.append(self.Qtab[tab_len + curimg][:, :len(self.markers) + 1])
        fulltab = np.vstack(fulltab)
        fulltabDF = copy.deepcopy(fulltab)
        fulltabDF = pd.DataFrame(fulltabDF)
        fulltabDF.columns = np.hstack(["Label", self.markers])
        fulltabDF.to_csv(os.path.join(dir, "FullObject_segmentation_data.csv"))

        # Add cluster IDs to the first column of the segmented table.
        fulltab[:, 0] = to_values

        # Initialize array for clustered image and colormap used for the colored cluster image.
        relabeledgreyimages = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)
        color = generate_colormap(len(np.unique(to_values)) + 1)
        self.objectcolor.append(color)
        np.save(os.path.join(dir, "color.npy"), color)
        data = []
        startindex = 0
        self.set_invisible(self.viewer)
        for i in range(self.numimgs):
            # Map cell ID values to corresponding cluster values, relabel each image, and save to output folder.
            from_values = fulltabDF['Label'].values[startindex:startindex + len(self.Qtab[i + curimg])]
            tmp_to_values = to_values[startindex:startindex + len(self.Qtab[i + curimg])]
            self.objectclusters.append(copy.deepcopy(tmp_to_values))
            relabeled = self.method_searchsort(from_values, tmp_to_values, self.objectplots[i + curimg].astype(int))
            relabeledgreyimages[i, :relabeled.shape[0], :relabeled.shape[1]] = relabeled.astype(np.uint8)
            relabeledgreyimages[i, :relabeled.shape[0], :relabeled.shape[1]][self.objectplots[i + curimg] == 0] = 0
            cv.imwrite(os.path.join(dir, f"RELABELED_Grey{i}.png"), relabeledgreyimages[i, :, :] + 1)

            # Apply colormap to each clustered image, add it to the viewer, and save to the output folder.
            relabeledimages = np.zeros((self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
            for j in range(len(np.unique(to_values))):
                relabeledimages[:, :, 0][relabeledgreyimages[i, :, :] == j + 1] = color[j][0]
                relabeledimages[:, :, 1][relabeledgreyimages[i, :, :] == j + 1] = color[j][1]
                relabeledimages[:, :, 2][relabeledgreyimages[i, :, :] == j + 1] = color[j][2]
            if i == 0:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabeledimages.dtype)
                relab[0, :relabeledimages.shape[0], :relabeledimages.shape[1], :] = relabeledimages
                self.viewer.add_image(relab, name=f"Object Clusters {self.objecttraincount + 1}", blending="additive")
                tifffile.imwrite(os.path.join(dir, f"RELABELED_{i}.tif"), relab[0, :, :, :])
            else:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabeledimages.dtype)
                relab[0, :relabeledimages.shape[0], :relabeledimages.shape[1], :] = relabeledimages
                self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))
                tifffile.imwrite(os.path.join(dir, f"RELABELED_{i}.tif"), relab[0, :, :, :])
            del relabeledimages
            gc.collect()

            # Find average cell marker expression for cells from each cluster in the current image.
            currenttab = fulltab[startindex:startindex + len(self.Qtab[i + curimg])]
            currenttabdf = pd.DataFrame(currenttab)
            grouped = currenttabdf.groupby(0)
            tabres = grouped.apply(np.mean)
            _, counts = np.unique(currenttab[:, 0], return_counts=True)
            tabres.insert(0, "Sample", i)
            tabres.insert(2, "Cells", counts)

            # Include clusters without any cells from the current image.
            clustertab = np.zeros((len(np.unique(to_values)), fulltab.shape[1] + 2))
            clustertab[np.unique(tmp_to_values.astype(np.uint8)) - 1, :] = tabres.values

            # Store full cluster data tables to find weighted average.
            data.append(clustertab.astype(np.float))

            # Store cell marker expression cluster data tables to update the table.
            self.objectdatalist.append(clustertab[:, 2:].astype(np.float))

            # Find min and max values for each cluster in the current image.
            minvals = []
            maxvals = []
            clustertab = clustertab[np.unique(tmp_to_values.astype(np.uint8)) - 1, 2:]
            for j in range(clustertab.shape[1] - 1):
                minvals.append(np.min(clustertab[:, j + 1]))
                maxvals.append(np.max(clustertab[:, j + 1]))
            self.minvalsobject.append(copy.deepcopy(minvals))
            self.maxvalsobject.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
            startindex += len(self.Qtab[i + curimg])

        # Re-index label image in case there are any clusters with no cells.
        unique = list(np.unique(relabeledgreyimages))
        for i in range(len(unique)):
            relabeledgreyimages[relabeledgreyimages == unique[i]] = i
        self.greyobjects.append(relabeledgreyimages)
        del relabeledgreyimages
        gc.collect()

        # Find weighted average for each cluster and add as an option to the table.
        data = np.nan_to_num((np.vstack(data)))
        if self.numimgs > 1:
            weighted_average = np.zeros((len(np.unique(to_values)), data.shape[1] - 2))
            for i in range(data.shape[0]):
                currcluster = i % weighted_average.shape[0]
                weighted_average[currcluster, 0] += data[i, 2]
            for i in range(data.shape[0]):
                currcluster = i % weighted_average.shape[0]
                weighted_average[currcluster, 1:] += data[i, 3:] * data[i, 2] / weighted_average[currcluster, 0]
            self.objectdatalist.append(weighted_average)
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            self.minvalsobject.append(copy.deepcopy(minvals))
            self.maxvalsobject.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))

        # Update cluster values for all cluster data and export as csv.
        my_data = pd.DataFrame(np.nan_to_num(data))
        my_data.columns = np.hstack([["Sample", "Cluster", "Pixels"], self.markers])
        my_data['Cluster'] = [int(id) - 1 for id in my_data['Cluster']]
        my_data.to_csv(os.path.join(dir, "RAPIDObject_cluster_table.csv"))

        # Generate MST plot for the clustered data.
        tabledata, my_data_scaled, DistMatrix, uniqueClusters = \
            prep_for_mst(clustertable=my_data, minnumpixels=1, outfolder=dir, includedmarkers=self.markers)
        generate_mst(distancematrix=DistMatrix, normalizeddf=my_data_scaled[my_data_scaled.columns], colors=color,
                     randomseed=0, outfolder=dir, clusterheatmap=True, displaymarkers=self.markers,
                     uniqueclusters=uniqueClusters, samplenames=list(np.unique(my_data['Sample'])), displaysingle=False)

        # Update phenotypes, image IDs, and coordinates for each of the cells in the table and export to csv.
        unique = list(copy.deepcopy(np.unique(to_values)))
        for i in range(len(to_values)):
            to_values[i] = unique.index(to_values[i]) + 1
        fulltabDF.insert(1, "Cluster", [labelnames[int(id) - 1] for id in to_values])
        imgid = [np.repeat(i, self.Qtab[i + self.segmentationindicesinumap[umapit] * self.numimgs].shape[0]) for i in
                 range(self.numimgs)]
        fulltabDF.insert(1, "ImgID", np.hstack(imgid))
        cord = np.vstack(self.cortabs[self.segmentationindicesinumap[umapit]])
        fulltabDF.insert(1, "Y", cord[:, 1])
        fulltabDF.insert(1, "X", cord[:, 0])
        self.tabdata.append(fulltabDF)
        fulltabDF.to_csv(os.path.join(dir, "FullObject_segmentation_dataCluster.csv"))

        # Update any necessary variables.
        self.pixelbasedclusters.append(False)
        self.objecttrainlist[self.segmentationindicesinumap[umapit]].append(self.objecttraincount)
        self.annotatedclusters.append(labelnames)
        self.objecttraincount += 1
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Object Cluster {self.objecttraincount} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        GUIUtils.log_actions(self.actionloggerpath, f"Manual Annotation: Plot ({it}), Shapes ({type}), "
                                                    f"Vertices ({verts})")

    ### TODO: Save all files to output folder, just like in pixel clustering.
    def merge_clusters(self, checked=[]):
        """
        Merge together all clusters that are checked in the currently-displayed table.

        Args:
            checked (list, optional): List of cluster IDs that are currently checked in the table (Default: []).
        """
        # Can't merge cells together, only clusters.
        if self.mode == "Segmentation":
            GUIUtils.display_error_message("Cannot merge cells together",
                                           "Please ensure that the table being displayed represents clusters, not cells.")
            return

        # One table for each image, plus a combined average table if using multiple images.
        if self.numimgs == 1:
            numtabs = 1
        else:
            numtabs = self.numimgs + 1
        n = self.index // numtabs

        # If the uer is merging pixel-based clusters.
        if self.mode == "Pixel":
            # Sort the selected clusters in descending order for easier re-indexing, and ensure multiple
            # clusters are selected.
            if checked == []:
                checked = self.currentlyselectedpixelclusters[n]
            checked.sort(reverse=True)
            if len(checked) <= 1:
                GUIUtils.display_error_message("Fewer than 2 clusters selected",
                                               "Please select at least 2 clusters from the table to be merged together.")
                return
            GUIUtils.log_actions(self.actionloggerpath, f"Merging Clusters: {checked}")

            numclusters = len(self.datalist[self.index]) - len(checked) + 1
            numcols = self.datalist[self.index].shape[1] + 2
            fulltab = np.zeros((self.numimgs * numclusters, numcols))
            # Remove the checked clusters from the table and merge them together as a new entry at the end.
            count = 0
            for i in range(numtabs):
                data = copy.deepcopy(self.datalist[n * numtabs + i])
                table = np.zeros((data.shape[0] + 1, data.shape[1]))
                table[:data.shape[0], :] = data
                table[data.shape[0], 0] = np.sum(data[checked, 0])
                if table[data.shape[0], 0] > 0:
                    table[data.shape[0], 1:] = np.average(data[checked, 1:], axis=0, weights=data[checked, 0])
                else:
                    table[data.shape[0], 1:] = np.zeros_like(table[data.shape[0], 1:])
                notremoved = [j for j in range(len(table)) if j not in checked]
                self.datalist[n * numtabs + i] = table[notremoved, :]
                if i < self.numimgs:
                    fulltab[count:count + len(notremoved), 0] = i + 1
                    fulltab[count:count + len(notremoved), 1] = np.arange(1, len(notremoved) + 1)
                    fulltab[count:count + len(notremoved), 2:] = table[notremoved, :]
                    count += len(notremoved)
            my_data = pd.DataFrame(np.nan_to_num((np.vstack(fulltab))))

            # Save updated table to output folder.
            my_data.columns = np.hstack([["Sample", "Cluster", "Pixels"], self.pixelclustermarkers[n]])
            dir = GUIUtils.create_new_folder(
                os.path.join(os.path.split(self.pixelclusterdirectories[n])[-1], "Merged_"), self.outputfolder)
            my_data.to_csv(os.path.join(dir, "RAPID_cluster_table.csv"))

            # Update the labeled image such that the clusters are merged at the end, removed, and relabeled.
            grey = copy.deepcopy(self.greypixels[n])
            newclusterval = int(np.max(grey) + 1)
            for cluster in checked:
                grey[grey == cluster] = newclusterval
                grey[grey > cluster] = grey[grey > cluster] - 1
                newclusterval -= 1
                self.pixelclusternums.remove(cluster)
                self.pixelclusternums = np.array(self.pixelclusternums)
                self.pixelclusternums[self.pixelclusternums > cluster - 1] -= 1
                self.pixelclusternums = list(self.pixelclusternums)
                index = f"Cluster {cluster + 1} (Pixel [{n}])"
                for i in reversed(range(len(self.viewer.layers))):
                    if self.viewer.layers[i].name == index:
                        self.viewer.layers.pop(i)
                        break
            self.pixelclusternums.append(newclusterval)
            self.greypixels[n] = grey

            # Create a colored image from the newly-labeled image, and add it to the viewer.
            newrgb = np.zeros((grey.shape[0], grey.shape[1], grey.shape[2], 3)).astype(np.uint8)

            color = self.pixelcolor[n]
            newcolor = color[[checked[-1]], :]
            color = np.delete(color, checked, 0)
            color = np.append(color, newcolor, 0)
            self.pixelcolor[n] = color

            for j in range(len(np.unique(grey))):
                newrgb[grey == j] = color[j, :]

            # Allow user to decide whether to add the labeled and/or colored image.
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return

            self.set_invisible(self.viewer)
            if selectimagesadded.grey:
                self.viewer.add_image(grey + 1, name=f"Merged Pixel Cluster IDs {n}", blending="additive")
            if selectimagesadded.color:
                self.viewer.add_image(newrgb, name=f"Merged Pixel Clusters {n}", blending="additive")

            for i in range(self.numimgs):
                imgname = os.path.split(self.filenames[i])[-1].split('.')[0]
                tifffile.imwrite(os.path.join(dir, f"RGB_{imgname}.tif"),
                                 newrgb[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1], :])
                tifffile.imwrite(os.path.join(dir, f"Labels_{imgname}.tif"),
                                 grey[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1)
            self.viewer.layers[-1].visible = True

            self.currentlyselectedpixelclusters[n] = []
            self.order = self.pixelclusternums
            newdisplaydata = self.datalist[self.index][self.pixelclusternums, :]
            self.update_table(newdisplaydata, self.lowerbounds, self.upperbounds, len(self.pixelclusternums),
                              self.pixelclusternums)

        # If the uer is merging object-based clusters.
        elif self.mode == "Object":
            # Sort the selected clusters in descending order for easier re-indexing, and ensure multiple
            # clusters are selected.
            if checked == []:
                checked = self.currentlyselectedobjectclusters[n]
            checked.sort(reverse=True)
            if len(checked) <= 1:
                GUIUtils.display_error_message("Please select more than one cluster to merge",
                                               "In order to merge clusters, run a clustering algorithm and select the clusters from the table that you would like to merge together")
                return
            GUIUtils.log_actions(self.actionloggerpath, f"Merging Clusters: {checked}")

            numclusters = len(self.objectdatalist[self.index]) - len(checked) + 1
            numcols = self.objectdatalist[self.index].shape[1] + 2
            fulltab = np.zeros((self.numimgs * numclusters, numcols))
            # Remove the checked clusters from the table and merge them together as a new entry at the end.
            count = 0
            for i in range(numtabs):
                data = self.objectdatalist[n * numtabs + i]
                table = np.zeros((data.shape[0] + 1, data.shape[1]))
                table[:data.shape[0], :] = data
                table[data.shape[0], 0] = np.sum(data[checked, 0])
                if table[data.shape[0], 0] > 0:
                    table[data.shape[0], 1:] = np.average(data[checked, 1:], axis=0, weights=data[checked, 0])
                else:
                    table[data.shape[0], 1:] = np.zeros_like(table[data.shape[0], 1:])
                notremoved = [j for j in range(len(table)) if j not in checked]
                self.objectdatalist[n * numtabs + i] = table[notremoved, :]
                if i < self.numimgs:
                    fulltab[count:count + len(notremoved), 0] = i + 1
                    fulltab[count:count + len(notremoved), 1] = np.arange(1, len(notremoved) + 1)
                    fulltab[count:count + len(notremoved), 2:] = table[notremoved, :]
                    count += len(notremoved)
            my_data = pd.DataFrame(np.nan_to_num((np.vstack(fulltab))))

            my_data.columns = np.hstack(
                [["Sample", "Cluster", "Cells"], self.markers, ["Area", "Eccentricity", "Perimeter", "Major Axis"]])
            dir = GUIUtils.create_new_folder(
                os.path.join(os.path.split(self.objectclusterdirectories[n])[-1], "Merged_"), self.outputfolder)
            my_data.to_csv(os.path.join(dir, "RAPID_cluster_table.csv"))

            grey = copy.deepcopy(self.greyobjects[n])

            # Update the labeled image such that the clusters are merged at the end, removed, and relabeled.
            tabdata = self.tabdata[n]
            clusterids = np.array(tabdata["Cluster"]) - 1
            newclusterval = int(np.max(grey) + 1)
            for cluster in checked:
                clusterids[clusterids == cluster] = newclusterval - 1
                clusterids[clusterids > cluster] = clusterids[clusterids > cluster] - 1
                cluster += 1
                grey[grey == cluster] = newclusterval
                grey[grey > cluster] = grey[grey > cluster] - 1
                newclusterval -= 1
                self.objectclusternums.remove(cluster - 1)
                self.objectclusternums = np.array(self.objectclusternums)
                self.objectclusternums[self.objectclusternums > cluster - 1] -= 1
                self.objectclusternums = list(self.objectclusternums)
                for i in range(self.numimgs):
                    self.objectclusters[n * self.numimgs + i][
                        self.objectclusters[n * self.numimgs + i] == cluster] = newclusterval + 1
                    self.objectclusters[n * self.numimgs + i][self.objectclusters[n * self.numimgs + i] > cluster] -= 1
                index = f"Cluster {cluster} (Object [{n}])"
                for i in reversed(range(len(self.viewer.layers))):
                    if self.viewer.layers[i].name == index:
                        self.viewer.layers.pop(i)
                        break
            clusterids = clusterids + 1
            self.tabdata[n]['Cluster'] = list(clusterids.astype(np.uint8))
            self.tabdata[n].to_csv(
                os.path.join(self.objectclusterdirectories[n], "FullObject_segmentation_dataCluster.csv"))
            self.greyobjects[n] = grey

            # Create a colored image from the newly-labeled image, and add it to the viewer.
            newrgb = np.zeros((grey.shape[0], grey.shape[1], grey.shape[2], 3)).astype(np.uint8)

            color = self.objectcolor[n]
            newcolor = color[[checked[-1]], :]
            color = np.delete(color, checked, 0)
            color = np.append(color, newcolor, 0)
            self.objectcolor[n] = color

            for j in range(1, len(np.unique(grey))):
                newrgb[grey == j] = color[j - 1, :]

            # Allow user to decide whether to add the labeled and/or colored image.
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return

            self.set_invisible(self.viewer)
            if selectimagesadded.grey:
                self.viewer.add_image(grey, name=f"Merged Object Cluster IDs {n}", blending="additive")
            if selectimagesadded.color:
                self.viewer.add_image(newrgb, name=f"Merged Object Clusters {n}", blending="additive")
            self.viewer.layers[-1].visible = True

            for i in range(self.numimgs):
                imgname = os.path.split(self.filenames[i])[-1].split('.')[0]
                tifffile.imwrite(os.path.join(dir, f"RGB_{imgname}.tif"),
                                 newrgb[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1], :])
                tifffile.imwrite(os.path.join(dir, f"Labels_{imgname}.tif"),
                                 grey[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1)

            self.objectclusternums.append(newclusterval - 1)
            self.order = self.objectclusternums
            self.currentlyselectedobjectclusters[n] = []
            newdisplaydata = self.objectdatalist[self.index][self.objectclusternums, :]
            self.update_table(newdisplaydata, self.lowerbounds, self.upperbounds, newclusterval, self.objectclusternums)

    ### TODO: Test additional arguments from Jupyter.
    def merge_markers(self, nucmarkernums=None, nucalg=None, memmarkernums=None, memalg=None):
        """
        Merge together all nuclear and/or membrane markers, as defined by the user, to prepare for segmentation.

        Args:
            nucmarkernums (list, optional): List of indices of each nuclear cell marker being combined.
            nucalg (str, optional): Algorithm being used to combine the nuclear cell markers.
            memmarkernums (list, optional): List of indices of each membrane cell marker being combined.
            memalg (str, optional): Algorithm being used to combine the membrane cell markers.
        """
        # At least one image must be loaded in order to merge markers.
        if len(self.markers) == 0:
            GUIUtils.display_error_message("Please open an image first",
                                           "Begin by opening the image(s) that you would like to train RAPID on")
            return

        # Notify user that contrast limits are accounted for when merging markers.
        if len(self.mergememmarkers) == 0:
            GUIUtils.display_error_message("Double-check contrast limits before proceeding",
                                           "Current contrast limits for each of the markers being merged together will be "
                                           "accounted for when segmenting. If you would like to use the raw data values "
                                           "for this, exit out of the next popup window and reset the contrast limits "
                                           "either manually or by clicking the \"Reset Metadata\" button in the \"Image "
                                           "Visualization\" module")

        if nucmarkernums is None or nucalg is None:
            # Define which nuclear markers to use for segmentation
            nucmarkers = GUIUtils.MergeMarkers(self.viewer, self.markers, False, nucmarkernums, nucalg)
            nucmarkers.exec()
            if not nucmarkers.OK:
                return
            nucmarkernums = nucmarkers.markernums
            nucalg = nucmarkers.alg

        if memmarkernums is None or memalg is None:
            # Define which membrane markers to use for segmentation
            memmarkers = GUIUtils.MergeMarkers(self.viewer, self.markers, True, memmarkernums, memalg)
            memmarkers.exec()
            if not memmarkers.OK:
                return
            memmarkernums = memmarkers.markernums
            memalg = memmarkers.alg

        mergednucmarkers = [self.markers[i] for i in nucmarkernums]
        mergedmemmarkers = [self.markers[i] for i in memmarkernums]

        # Check that the user defined at least one cell marker to use.
        if len(memmarkernums) == 0 and len(nucmarkernums) == 0:
            GUIUtils.display_error_message("No cell markers selected",
                                           "Please select at least one nuclear and/or membrane marker to use for segmentation.")
            return

        # Open zarr file where data will be saved.
        path = GUIUtils.create_new_folder("MergedImage", self.outputfolder)
        self.mergedimagespaths.append(path)
        fh = zarr.open(path, mode='a')
        self.segmentcounts.append([-1, -1])

        # Merge nuclear markers together if any nuclear markers were selected.
        self.viewer.status = "Merging nuclear markers..."
        nucdata = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)
        nuccls = []
        if len(nucmarkernums) > 0:
            if nucalg == "avg":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nuccls.append(self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nucdata += (image / len(nucmarkernums)).astype(np.uint8)
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
            if nucalg == "sum":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nuccls.append(self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nucdata += np.minimum(255 - nucdata, image)
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
            if nucalg == "max":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nuccls.append(self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nucdata = np.maximum(nucdata, image)
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
            if nucalg == "median":
                img = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], len(nucmarkernums)),
                               dtype=np.uint8)
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    nuccls.append(self.viewer.layers[nucmarkernums[i]].contrast_limits)
                    img[:, :, :, i] = image
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
                nucdata = np.median(img, axis=3)
        fh.create_dataset("Nucleus", data=nucdata, dtype=np.uint8)
        self.mergenucmarkers.append(len(nucmarkernums) > 0)
        gc.collect()

        # Merge membrane markers together if any membrane markers were selected.
        self.viewer.status = "Merging membrane markers..."
        memdata = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)
        memcls = []
        if len(memmarkernums) > 0:
            if memalg == "avg":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memcls.append(self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memdata += (image / len(memmarkernums)).astype(np.uint8)
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
            if memalg == "sum":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memcls.append(self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memdata += np.minimum(255 - memdata, image)
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
            if memalg == "max":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memcls.append(self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memdata = np.maximum(memdata, image)
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
            if memalg == "median":
                img = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], len(memmarkernums)),
                               dtype=np.uint8)
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       self.viewer.layers[memmarkernums[i]].contrast_limits)
                    memcls.append(self.viewer.layers[memmarkernums[i]].contrast_limits)
                    img[:, :, :, i] = image
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
                memdata = np.median(img, axis=3)
        fh.create_dataset("Membrane", data=memdata, dtype=np.uint8)
        self.set_invisible(self.viewer)
        self.mergememmarkers.append(len(memmarkernums) > 0)
        gc.collect()

        # Add merged image to the viewer
        if mergednucmarkers and mergedmemmarkers:
            self.viewer.add_image(np.stack([memdata, nucdata], axis=0), name=f'Merged Image {len(self.segmentcounts)}',
                                  blending="additive", contrast_limits=[0, 255])
        elif mergednucmarkers:
            self.viewer.add_image(nucdata, name=f'Merged Image {len(self.segmentcounts)}', blending="additive",
                                  contrast_limits=[0, 255])
        else:
            self.viewer.add_image(memdata, name=f'Merged Image {len(self.segmentcounts)}', blending="additive",
                                  contrast_limits=[0, 255])

        GUIUtils.log_actions(self.actionloggerpath,
                             f"Merged Markers: Membrane Markers ({mergedmemmarkers}, {memalg}, "
                             f"{nuccls}), Nuclear Markers ({mergednucmarkers}, {nucalg}, {memcls})")
        self.viewer.status = "Finished merging markers"

    def method_searchsort(self, from_values, to_values, array):
        """
        Relabels an array.

        Args:
            from_values (numpy.ndarray): Original values from the array.
            to_values (numpy.ndarray): Final values defining the transformation.
            array (numpy.ndarray): Input array whose values will be updated.

        :return: out *(numpy.ndarray)*: \n
            Relabeled array.
        """

        sort_idx = np.argsort(from_values)
        idx = np.searchsorted(from_values, array, sorter=sort_idx)
        out = to_values[sort_idx][idx]
        return out

    def object_clustering(self):
        """
        Perform object-based clustering on a segmented image using the algorithm selected by the user.
        """
        # Can only perform clustering if segmentation has been done
        if self.segmentcount == 0:
            GUIUtils.display_error_message("You must segment before running object-based clustering",
                                           "Object-based clustering cannot be done until the image has been segmented")
            return

        # Define which markers will be used for clustering
        trainmarkers = GUIUtils.RAPIDObjectParams(self.markers)
        trainmarkers.exec()
        if not trainmarkers.OK:
            return
        objectmarkernums = trainmarkers.markernums

        # Define which algorithm will be used for clustering
        alg = GUIUtils.ClusteringAlgorithm(self.objectimgnames)
        alg.exec()
        if not alg.OK:
            return
        imagenum = alg.imageindex * self.numimgs

        # Allow user to decide whether to add the labeled and/or colored image.
        selectimagesadded = GUIUtils.GreyColorImages()
        selectimagesadded.exec()
        if not selectimagesadded.OK:
            return
        colored = selectimagesadded.color
        grey = selectimagesadded.grey

        # Load model, indicate whether to continue training or use for prediction, and define parameters for
        # whichever algorithm was selected by the user
        continuetraining = True
        if alg.alg == "Pretrained":
            try:
                hf = zarr.open("/".join(alg.dirpath[:-1]), 'r')
                # self.objectmodelloaded = hf.attrs['RAPIDObject']
                # self.pixelmodelloaded = False
                loadedargs = hf.attrs['arg']
            except:
                return
            loadoptions = GUIUtils.LoadModelOptions()
            loadoptions.exec()
            if not loadoptions.OK:
                return
            continuetraining = not loadoptions.prediction
            args = Namespace(**loadedargs)
            norm = GUIUtils.LoadModelNormalize(False)
            norm.exec()
            if not norm.OK:
                return
            args.normalize = norm.normalize
            pca = norm.pca
            if continuetraining:
                setParams = GUIUtils.RAPIDObjectTrainLoadedParameters(args)
                setParams.exec()
                if not setParams.OK:
                    return
                args.nit = int(setParams.nit)
                args.bs = int(setParams.bs)
                args.lr = float(setParams.lr)
                args.phenograph = 'False'
                args.distance = 'YES'
                args.blankpercent = float(setParams.blankpercent)
                args.epoch = 1
                args.GUI = True
                GUIUtils.log_actions(self.actionloggerpath,
                                     f"Object Clustering: Markers ({trainmarkers.objecttrainmarkers}), Alg ({alg.alg}), "
                                     f"Image Index ({alg.imageindex}), Path ({alg.dirpath}), Continue Training ({continuetraining}), "
                                     f"Params ({norm.normalize}, {pca}, {setParams.nit}, {setParams.bs}, {setParams.lr}, "
                                     f"{setParams.blankpercent})")
            else:
                GUIUtils.log_actions(self.actionloggerpath,
                                     f"Object Clustering: Markers ({trainmarkers.objecttrainmarkers}), Alg ({alg.alg}), "
                                     f"Image Index ({alg.imageindex}), Path ({alg.dirpath}), "
                                     f"Continue Training ({continuetraining}), Params ({norm.normalize}, {pca})")

        elif alg.alg == "RAPID":
            setParams = GUIUtils.RAPIDObjectParameters(len(trainmarkers.markernums))
            setParams.exec()
            if not setParams.OK:
                return
            args = runRAPIDzarr.get_parameters()
            args.ncluster = int(setParams.nc)
            args.nit = int(setParams.nit)
            args.bs = int(setParams.bs)
            if setParams.mse == "True":
                args.mse = True
            args.normalize = setParams.normalize
            args.lr = float(setParams.lr)
            args.phenograph = 'False'
            args.RAPID = 'True'
            args.distance = 'YES'
            args.blankpercent = float(setParams.blankpercent)
            args.epoch = 1
            args.GUI = True
            pca = setParams.pca
            GUIUtils.log_actions(self.actionloggerpath,
                                 f"Object Clustering: Markers ({trainmarkers.objecttrainmarkers}), Alg ({alg.alg}), "
                                 f"Image Index ({alg.imageindex}), Continue Training ({continuetraining}), "
                                 f"Params ({setParams.nc}, {setParams.nit}, {setParams.bs}, {setParams.mse}, "
                                 f"{setParams.normalize}, {setParams.lr}, {setParams.blankpercent}, {pca})")

        elif alg.alg == "SciPy":
            setParams = GUIUtils.SciPyParameters()
            setParams.exec()
            if not setParams.OK:
                return
            args = runRAPIDzarr.get_parameters()
            args.phenograph = 'False'
            args.RAPID = 'False'
            args.PGdis = "euclidean"
            args.PGnn = 70
            args.PGres = 0.5
            args.normalize = setParams.normalize
            args.scipyalgo = setParams.scipyalgo
            args.scipyargs = setParams.scipyargs
            args.scipykwarg = setParams.scipykwarg
            args.GUI = True
            pca = setParams.pca
            GUIUtils.log_actions(self.actionloggerpath,
                                 f"Object Clustering: Markers ({trainmarkers.objecttrainmarkers}), Alg ({alg.alg}), "
                                 f"Image Index ({alg.imageindex}), Continue Training ({continuetraining}), "
                                 f"Params ({setParams.normalize}, {setParams.scipyalgo}, {setParams.scipyargs}, "
                                 f"{setParams.scipykwarg}, {pca})")

        else:
            setParams = GUIUtils.PhenographParameters()
            setParams.exec()
            if not setParams.OK:
                return
            args = runRAPIDzarr.get_parameters()
            args.phenograph = 'True'
            args.RAPID = 'False'
            args.PGdis = str(setParams.PGdis)
            args.PGnn = int(setParams.PGnn)
            args.PGres = float(setParams.PGres)
            args.normalize = setParams.normalize
            args.graphalgo = setParams.graphalgo
            args.GUI = True
            pca = setParams.pca
            GUIUtils.log_actions(self.actionloggerpath,
                                 f"Object Clustering: Markers ({trainmarkers.objecttrainmarkers}), Alg ({alg.alg}), "
                                 f"Image Index ({alg.imageindex}), Continue Training ({continuetraining}), "
                                 f"Params ({setParams.PGdis}, {setParams.PGnn}, {setParams.PGres}, {setParams.normalize}, "
                                 f"{setParams.graphalgo}, {pca})")

        # Count total number of cells for segmented image used for clustering
        numcells = 0
        for i in range(self.numimgs):
            ind = i + imagenum
            numcells += self.Qtab[ind].shape[0]

        # Store normalized cell marker expression
        expressionavgs = np.zeros((numcells, len(objectmarkernums)))
        if args.normalize == "zscale":
            scaler = StandardScaler()
            count = 0
            for i in range(self.numimgs):
                img = copy.deepcopy(self.Qtab[ind][:, objectmarkernums])
                scaler.fit(img)
                expressionavgs[count:count + self.Qtab[ind].shape[0], :] = scaler.transform(img)
                count += self.Qtab[ind].shape[0]
        else:
            count = 0
            for i in range(self.numimgs):
                ind = i + imagenum
                expressionavgs[count:count + self.Qtab[ind].shape[0], :] = self.Qtab[ind][:, objectmarkernums]
                count += self.Qtab[ind].shape[0]

            if args.normalize == "all":
                scaler = StandardScaler()
                scaler.fit(expressionavgs)
                expressionavgs = scaler.transform(expressionavgs)
                if pca:
                    expressionavgs = run_pca(data=expressionavgs, numcomponents=0.999)
            elif args.normalize == "log10":
                expressionavgs = np.nan_to_num(np.log10(expressionavgs), nan=0, posinf=0, neginf=0)
            elif args.normalize == "log2":
                expressionavgs = np.nan_to_num(np.log2(expressionavgs), nan=0, posinf=0, neginf=0)

        # Train algorithm if necessary, and then apply to segmented image.
        self.viewer.status = "RAPID clustering..."
        self.set_invisible(self.viewer)
        dir = GUIUtils.create_new_folder("RAPIDObject_", self.outputfolder)
        self.objectclusterdirectories.append(dir)
        if not continuetraining:
            model = RAPIDMixNet(dimension=len(objectmarkernums), nummodules=5, mse=args.mse,
                                numclusters=int(args.ncluster))
            optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                    weight_decay=0.01, amsgrad=False)
            model.apply(weight_init)
            model = load_checkpoint("/".join(alg.dirpath), model, optimizer)
            self.test_object(model, expressionavgs, args, [i + 1 for i in range(len(self.markers) + 4)], colored, grey,
                             imagenum, optimizer=optimizer, outputpath=dir, predict=True)
        else:
            if args.phenograph == 'True':
                model = 0
                self.test_object(model, expressionavgs, args, [i + 1 for i in range(len(self.markers) + 4)], colored, grey,
                                 imagenum, outputpath=dir)
                pass
            elif args.phenograph == 'False' and args.RAPID == 'False':
                model = 0
                self.test_object(model, expressionavgs, args, [i + 1 for i in range(len(self.markers) + 4)], colored, grey,
                                 imagenum, outputpath=dir)
                pass
            else:
                hf = zarr.open(dir, 'a')
                hf.attrs['arg'] = vars(args)
                hf.attrs['RAPIDObject'] = True
                torch.manual_seed(args.seed)
                np.random.seed(args.seed)
                torch.cuda.manual_seed(args.seed)
                # if not alg.objectmodelloaded:
                if not alg.alg == "Pretrained":
                    model = RAPIDMixNet(dimension=len(objectmarkernums), nummodules=5, mse=args.mse,
                                        numclusters=int(args.ncluster))
                    model.apply(weight_init)
                    optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                            weight_decay=0.01, amsgrad=False)
                else:
                    model = RAPIDMixNet(dimension=len(objectmarkernums), nummodules=5, mse=args.mse,
                                        numclusters=int(args.ncluster))
                    optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                            weight_decay=0.01, amsgrad=False)
                    model.apply(weight_init)
                    model = load_checkpoint("/".join(alg.dirpath), model, optimizer)
                print(model)
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                model.to(device)
                self.train_object(model, expressionavgs, optimizer, args)
                self.test_object(model, expressionavgs, args, [i + 1 for i in range(len(self.markers) + 4)], colored, grey,
                                 imagenum, optimizer=optimizer, outputpath=dir)
        self.viewer.status = "RAPID clustering done."

        # Update table sort module and other variables.
        for i in range(self.numimgs):
            self.tableimagenames.append(
                f"Object Cluster {self.objecttraincount + 1} - {self.filenames[i].split('/')[-1]}")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
        if self.numimgs > 1:
            self.tableimagenames.append(f"Object Cluster {self.objecttraincount + 1} - Combined Average")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
        self.objecttrainlist[alg.imageindex].append(self.objecttraincount)
        self.objecttraincount += 1
        self.pixelbasedclusters.append(False)
        self.annotatedclusters.append([])
        self.currentlyselectedobjectclusters.append([])
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Object Cluster {self.objecttraincount} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()

    def open_docs(self):
        """
        Open the RAPID documentation in a web browser.
        """
        import gdown
        import shutil
        rootfold = os.path.dirname(os.path.abspath(__file__))
        if (os.path.exists(rootfold+"/../DocFiles")):
            pass
        else:
            pass
            #gdown.download("https://drive.google.com/uc?id=1JhoHXYTQzy_ffSF_pbm-o33vhgFpGzjP",rootfold+"/../DocFiles.zip")
            #shutil.unpack_archive(rootfold+"/../DocFiles.zip", rootfold+"/../")
        if (os.path.exists(rootfold+"/../docs")):
            pass
        else:
            gdown.download("https://drive.google.com/uc?id=1JhpIjMd_Rq-i1_laivxzavwZDJPOa4b1",rootfold+"/../docs.zip")
            shutil.unpack_archive(rootfold+"/../docs.zip", rootfold+"/../")
        webbrowser.open(f"file://{rootfold}/../docs/_build/html/index.html", new=2)
    ### TODO: double-check that this works for loading a matrix.
    ### TODO: Delayed function? Pyramid/multiscale?
    def open_images(self, segmentedimgpaths=[]):
        """
        Open a directory for the user to select which images they would like to use, and load them into the viewer.

        Args:
            segmentedimgpaths (list, optional): List of paths to segmented images if loading segmentation results (Default: []).

        :return: *(bool)*: \n
            True if user has loaded images, False if none are selected.
        """

        # Only open images at the start, not after performing downstream analysis.
        if len(self.viewer.layers) > len(self.markers):
            GUIUtils.display_error_message("Cannot open additional images",
                                           "If you have done downstream analysis, please open images in a new session")
            return

        # Prompt user to select paths to images to load.
        filenames, _ = QFileDialog.getOpenFileNames(
            parent=self.viewer.window.qt_viewer,
            caption='Select images...',
            filter='*.afm *.nef *.lif *.nhdr *.ps *.bmp *.frm *.pr3 *.tif *.aim *.dat *.fits *.pcoraw *.qptiff *.acff '
                   '*.xys *.mrw *.xml *.svs *.arf *.dm4 *.ome.xml *.v *.pds *.zvi *.apl *.mrcs *.i2i *.mdb *.ipl *.oir '
                   '*.ali *.fff *.vms *.jpg *.inr *.pcx *.vws *.html *.al3d *.ims *.bif *.labels *.dicom *.par *.map '
                   '*.ome.tf2 *.htd *.tnb *.mrc *.obf *.xdce *.png *.jpx *.fli *.psd *.pgm *.obsep *.jpk *.ome.tif '
                   '*.rcpnl *.pbm *.grey *.raw *.zfr *.klb *.spc *.sdt *.2fl *.ndpis *.ipm *.pict *.st *.seq *.nii *.lsm '
                   '*.epsi *.cr2 *.zfp *.wat *.lim *.1sc *.ffr *.liff *.mea *.nd2 *.tf8 *.naf *.ch5 *.afi *.ipw *.img '
                   '*.ids *.mnc *.crw *.mtb *.cxd *.gel *.dv *.jpf *.tga *.vff *.ome.tiff *.ome *.bin *.cfg *.dti '
                   '*.ndpi *.c01 *.avi *.sif *.flex *.spe *.ics *.jp2 *.xv *.spi *.lms *.sld *.vsi *.lei *.sm3 '
                   '*.hx *.czi *.nrrd *.ppm *.exp *.mov *.xqd *.dm3 *.im3 *.pic *.his *.j2k *.rec *.top *.pnl *.tf2 '
                   '*.oif *.l2d *.stk *.fdf *.mng *.ome.btf *.tfr *.res *.dm2 *.eps *.hdr *.am *.stp *.sxm *.ome.tf8 '
                   '*.dib *.mvd2 *.wlz *.nd *.h5 *.cif *.mod *.nii.gz *.bip *.oib *.amiramesh *.scn *.gif *.sm2 '
                   '*.tiff *.hdf *.hed *.r3d *.wpi *.dcm *.btf *.msr *.xqf'
        )
        print(filenames)

        # If loading segmentation, make sure the images being loaded correspond to the segmented images.
        if segmentedimgpaths and len(filenames) != len(segmentedimgpaths):
            GUIUtils.display_error_message("Mismatching number of images",
                                           "Please ensure the raw images correspond to the segmented image and are in the correct order")
            return "False"

        # User must load at least one image.
        if len(filenames) == 0:
            return False

        # If this is the first time loading images.
        if not self.imagehasbeenloaded:
            # Initialize lists of image paths and image arrays, and keep track of number of cell markers being loaded.
            imagelist = []
            self.filenames = []
            nummarkers = 0
            incompatiblenummarkers = False

            # Loop through each image path.
            for path in filenames:
                # Read the image into a numpy array.
                filename = os.path.join(os.path.abspath(path))
                img = self.parse_img(filename)

                # If this image has a different number of markers than previous images, prompt user to load matrix of
                # markers instead of one singular set of markers.
                if len(img) != nummarkers and path != filenames[0]:
                    incompatiblenummarkers = True

                # If loading a single z-slice, load the image as is.
                if len(img.shape) == 3:
                    imagelist.append(img)
                    self.filenames.append(path)
                    nummarkers = max(nummarkers, img.shape[0])

                # If loading multiple z-slices, load as separate images for each z-slice.
                elif len(img.shape) == 4:
                    name_ext = path.split(".")

                    channelorder = GUIUtils.ChannelOrder4D()
                    channelorder.exec()
                    if not channelorder.OK:
                        return

                    if channelorder.cfirst:
                        for i in range(img.shape[1]):
                            currentz = copy.deepcopy(img[:, i, :, :])
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            self.filenames.append('.'.join(currentname))
                        nummarkers = max(nummarkers, img.shape[0])

                    else:
                        for i in range(img.shape[0]):
                            currentz = copy.deepcopy(img[i, :, :, :])
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            self.filenames.append('.'.join(currentname))
                        nummarkers = max(nummarkers, img.shape[1])

            print(self.filenames)

            # Keep track of the maximum x- and y- dimensions to use for the shape of the image in the viewer.
            self.maximageshape = np.array([np.max(self.sampleshapes, 0)[0], np.max(self.sampleshapes, 0)[1]])

            # Prompt user to load a matrix of markers to account for different marker sets between different images, or
            # if they have the same shape, choose between loading a matrix or loading a single common marker order.
            if incompatiblenummarkers:
                markernames = GUIUtils.LoadMatrix(self.outputfolder)
            else:
                markernames = GUIUtils.MarkerNames(len(imagelist) > 1, self.outputfolder)
            markernames.exec()
            if not markernames.OK:
                self.maximageshape = np.array([])
                self.sampleshapes = []
                return
            inputmarkernames = markernames.markers.replace(" ", "").split(",")
            GUIUtils.log_actions(self.actionloggerpath, f"Opened Images: Paths ({filenames}), ")

            # If loading a matrix of markers.
            if markernames.matrix:
                # Keep only the images that are included in the matrix.
                filenames = [os.path.split(path)[-1].split(".")[0] for path in self.filenames]
                imgindices = []
                for name in filenames:
                    if name in markernames.imagenames:
                        imgindices.append(markernames.imagenames.index(name))
                imgindices.sort()
                markernames.imagenames = [name for name in filenames if name in markernames.imagenames]
                imageindices = [markernames.imagenames.index(name) for name in filenames]

                # Remove extra markers from matrix in case there are more markers than channels in the images.
                numchansmin = min([len(img) for img in imagelist])
                markerindiceslist = []
                for indices in markernames.indiceslist:
                    inds = []
                    for j in range(len(indices)):
                        if indices[j] < numchansmin:
                            inds.append(j)
                    markerindiceslist.append([indices[i] for i in inds])

                imagelist = [imagelist[imageindices[i]][markerindiceslist[imgindices[i]], :, :] for i in
                             range(len(imageindices))]
                self.nummarkers = len(markerindiceslist[0])
                self.numimgs += len(imageindices)

            # If loading one common list of cell marker names.
            else:
                self.nummarkers = nummarkers
                self.numimgs += len(self.filenames)

            # Store the names of the cell markers that are being included.
            markers = []
            for i in range(self.nummarkers):
                markers.append(f"Marker {i}")
            if not (len(inputmarkernames) == 1 and inputmarkernames[0] == ""):
                if len(inputmarkernames) > len(markers):
                    markers = [inputmarkernames[i] for i in range(len(markers))]
                elif len(inputmarkernames) == len(markers):
                    markers = inputmarkernames
                else:
                    for i in range(len(inputmarkernames)):
                        markers[i] = inputmarkernames[i]

            # Allow user to remove any markers that they do not want to include.
            removemarkernames = GUIUtils.RemoveMarkerNames(markers)
            removemarkernames.exec()
            if not removemarkernames.OK:
                self.maximageshape = np.array([])
                self.sampleshapes = []
                self.numimgs = 0
                self.nummarkers = 0
                return
            self.markers = [markers[ind] for ind in removemarkernames.markernums]
            self.markernums = copy.deepcopy(removemarkernames.markernums)
            self.nummarkers = len(self.markers)

            # Store the shapes of each of the images being loaded.
            for i in range(len(imagelist)):
                imagelist[i] = imagelist[i][self.markernums, :, :]
                dim2 = imagelist[i].shape[1]
                dim3 = imagelist[i].shape[2]
                self.imageshapelist.append((dim2, dim3, len(self.markernums)))

            # Add each image to the viewer.
            colforinput = generate_colormap(self.nummarkers + 1)
            for ch in range(self.nummarkers):
                addarr = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]),
                                  dtype=imagelist[0].dtype)
                for i in range(self.numimgs):
                    addarr[i, :imagelist[i].shape[1], :imagelist[i].shape[2]] = imagelist[i][0, :, :]
                    imagelist[i] = imagelist[i][1:, :, :]
                cmap = Colormap(ColorArray(
                    [(0, 0, 0), (colforinput[ch, 0] / 255, colforinput[ch, 1] / 255, colforinput[ch, 2] / 255)]))
                self.viewer.add_image(addarr, name=self.markers[ch], rgb=False, colormap=cmap, contrast_limits=[0, 255],
                                      blending="additive", visible=False)
            self.imagehasbeenloaded = True

            # By default, initialize sample groupings so that each image is in its own group.
            d = {}
            for name in filenames:
                n = os.path.split(name)[-1]
                d[n] = n
            self.groupslist.append(d)

            # Update the dropdown options for the sort table widget.
            self.columnheaders += self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            self.sorttableimages.marker.choices = tuple(self.columnheaders)
            self.sorttableimages.reset_choices()
            self.viewer.dims.set_current_step(0, 0)

        # If at least one image has already been loaded.
        else:
            imagelist = []
            for path in filenames:
                # Read the image into a numpy array.
                filename = os.path.join(os.path.abspath(path))
                img = self.parse_img(filename)

                # If loading a single z-slice, load the image as is.
                if len(img.shape) == 3:
                    imagelist.append(img[self.markernums, :, :])
                    self.filenames.append(path)

                # If loading multiple z-slices, load as separate images for each z-slice.
                elif len(img.shape) == 4:
                    name_ext = path.split(".")
                    for i in range(img.shape[1]):
                        currentz = copy.deepcopy(img[:, i, :, :])
                        imagelist.append(currentz[self.markernums, :, :])
                        currentname = copy.deepcopy(name_ext)
                        currentname[-2] += f"_z{i + 1}"
                        self.filenames.append('.'.join(currentname))

            # Store the shapes of each of the images being loaded.
            for i in range(len(imagelist)):
                dim0 = imagelist[i].shape[0]
                dim2 = imagelist[i].shape[1]
                dim3 = imagelist[i].shape[2]
                self.imageshapelist.append((dim2, dim3, dim0))

            # Add each of the new images to the default grouping.
            for name in filenames:
                n = os.path.split(name)[-1]
                self.groupslist[0][n] = n
            self.numimgs += len(filenames)

            # Update the maximum x- and y- dimensions to use for the shape of the image in the viewer.
            self.maximageshape = np.array([np.max(self.sampleshapes, 0)[0], np.max(self.sampleshapes, 0)[1]])
            for ch in range(self.nummarkers):
                newarr = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]),
                                  dtype=imagelist[0].dtype)
                prevarr = self.viewer.layers[ch].data
                newarr[:prevarr.shape[0], :prevarr.shape[1], :prevarr.shape[2]] = prevarr
                for i in range(len(filenames)):
                    newarr[i + prevarr.shape[0], :imagelist[i].shape[1], :imagelist[i].shape[2]] = imagelist[i][0, :, :]
                    imagelist[i] = imagelist[i][1:, :, :]
                self.viewer.layers[ch].data = newarr

        GUIUtils.log_actions(self.actionloggerpath, f"Opened Images: Paths ({filenames})")
        return True

    def on_cell_changed(self, row, column):
        """
        Add actions for the case when a checkbox is toggled. When a box is checked, the corresponding cell/cluster
        should be made visible in the viewer, and if a box is unchecked then the corresponding cell/cluster should
        be made invisible.

        Args:
            row (int): Row of the checkbox being toggled.
            column (int): Column of the checkbox being toggled.
        """
        if self.addwhenchecked and ((column == 0 and row > 2) or row == 2):
            item = self.tablewidget.item(row, column)
            currentState = item.checkState()
            col = column - 1
            r = row - 3
            if currentState == QtCore.Qt.Checked:
                if column > 0:
                    if self.mode == "Segmentation":
                        self.viewer.layers[self.markers[col]].visible = True
                    elif column > 1:
                        self.viewer.layers[self.markers[col - 1]].visible = True
                else:
                    if self.mode == "Segmentation":
                        r = int(self.combcellnums[self.index][r])
                        mask = np.in1d(self.objectplots[self.index], self.Qtab[self.index][r, 0])
                        mask = mask.reshape((self.maximageshape[0], self.maximageshape[1]))
                        outputimg = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]),
                                             dtype=np.bool)
                        outputimg[self.index % self.numimgs, :, :] = mask
                        self.viewer.add_image(outputimg, name=f"Cell {r + 1}", blending="additive", visible=True)
                        self.currentlyselectedcells[self.index].append(r)
                    elif self.mode == "Object":
                        r = int(self.objectclusternums[r])
                        currentcluster = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1])).astype(
                            np.bool)
                        ind = self.index
                        if self.numimgs > 1:
                            ind = int(self.index / (self.numimgs + 1))
                        color = self.objectcolor[ind][r, :] / 255

                        if self.numimgs == 1:
                            trainnum = self.index
                        else:
                            trainnum = self.index // (self.numimgs + 1)
                        currentcluster[self.greyobjects[trainnum] == r + 1] = 1
                        cmap = Colormap(ColorArray([(0, 0, 0), (color[0], color[1], color[2])]))
                        self.viewer.add_image(currentcluster, name=f"Cluster {r + 1} (Object [{trainnum}])",
                                              blending="additive", colormap=cmap, visible=True)
                        self.currentlyselectedobjectclusters[trainnum].append(r)
                    else:
                        r = self.pixelclusternums[r]
                        currentcluster = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1])).astype(
                            np.bool)
                        ind = self.index
                        if self.numimgs > 1:
                            ind = int(self.index / (self.numimgs + 1))

                        color = self.pixelcolor[ind][r, :] / 255

                        if self.numimgs == 1:
                            trainnum = self.index
                        else:
                            trainnum = self.index // (self.numimgs + 1)
                        currentcluster[self.greypixels[trainnum] == r] = 1
                        cmap = Colormap(ColorArray([(0, 0, 0), (color[0], color[1], color[2])]))
                        self.viewer.add_image(currentcluster, name=f"Cluster {r + 1} (Pixel [{trainnum}])",
                                              rgb=False, colormap=cmap, blending="additive", visible=True)
                        self.currentlyselectedpixelclusters[trainnum].append(r)
            else:
                if column > 0:
                    if self.mode == "Segmentation" and col < len(self.markers):
                        self.viewer.layers[self.markers[col]].visible = False
                    # elif self.mode == "Object":
                    #    self.viewer.layers[self.markers[col-1]].visible = False
                    elif column > 1:
                        self.viewer.layers[self.markers[col - 1]].visible = False
                else:
                    if self.mode == "Segmentation":
                        r = int(self.cellnums[r])
                        self.currentlyselectedcells[self.index].remove(r)
                        index = f"Cell {r + 1}"
                    elif self.mode == "Object":
                        r = self.objectclusternums[r]
                        if self.numimgs == 1:
                            trainnum = self.index
                        else:
                            trainnum = self.index // (self.numimgs + 1)
                        self.currentlyselectedobjectclusters[trainnum].remove(r)
                        index = f"Cluster {r + 1} (Object [{trainnum}])"
                    else:
                        r = self.pixelclusternums[r]
                        if self.numimgs == 1:
                            trainnum = self.index
                        else:
                            trainnum = self.index // (self.numimgs + 1)
                        self.currentlyselectedpixelclusters[trainnum].remove(r)
                        index = f"Cluster {r + 1} (Pixel [{trainnum}])"
                    for i in range(len(self.viewer.layers)):
                        if self.viewer.layers[i].name == index:
                            self.viewer.layers.pop(i)
                            break

    ### TODO: Terminate anytime this returns False.
    def parse_img(self, imgpath, islabel=False):
        """
        Read an input image into a numpy array to be loaded in the viewer.

        Args:
            imgpath (str): Path to the image being loaded.
            islabel (bool, optional): True if loading segmentation results. Otherwise, False (Default: False).

        :return: img *(numpy.ndarray)*: \n
            The image in numpy array format.
        """

        try:
            try:
                img = tifffile.imread(imgpath)
                print("tiff")
            except:
                reader_function = napari_get_reader(imgpath)
                img = reader_function(imgpath)[0][0]
                print("Not tiff")
        except:
            msg = QMessageBox()
            msg.setWindowTitle("RAPID Alert")
            msg.setText("Please convert your file to .tiff format")
            msg.setDetailedText("Because your Java path is not set, your file must be in .tiff format")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return False

        if not islabel:
            # img = img_as_ubyte(exposure.rescale_intensity(img))
            img = img_as_ubyte(img)

        self.flipimg.append(False)
        if img.shape[-2] > img.shape[-1]:
            img = np.moveaxis(img, -1, -2)
            self.flipimg[-1] = True

        self.sampleshapes.append([img.shape[-2], img.shape[-1]])
        return img

    def pixel_clustering(self):
        """
        Perform RAPID pixel-based clustering, by either training a new model or loading a previously-trained model and
        applying it to each of the images loaded into the GUI.
        """
        logstr = ["Pixel Clustering: "]
        # Can't use RAPID before opening an image.
        if len(self.markers) == 0:
            GUIUtils.display_error_message("Please open an image first",
                                           "Begin by opening the image(s) that you would like to train RAPID on")
            return

        # Allow user to either load a model and define the path to the model, or train a new model.
        loadmodel = GUIUtils.LoadModel()
        loadmodel.exec()
        if not loadmodel.OK:
            return
        logstr.append(f"Model Loaded ({loadmodel.load}), ")

        # If loading a model, allow user to either continue training or predict. Otherwise, default to training.
        predict = False
        if loadmodel.load:
            logstr.append(f"Model Path ({loadmodel.dirpath}), ")
            loadmodeloptions = GUIUtils.LoadModelOptions()
            loadmodeloptions.exec()
            if not loadmodeloptions.OK:
                return
            predict = loadmodeloptions.prediction
            logstr.append(f"Predict ({predict}), ")
            hf = zarr.open("/".join(loadmodel.dirpath[:-1]) + "/RAPID_Data", 'r')
            trainmarkernames = hf['data_normalized'].attrs['selmarkernames']
            numtrainmarkers = len(trainmarkernames)

            # Define which normalization mode to use, if any.
            normalization = GUIUtils.LoadModelNormalize(True)
            normalization.exec()
            if not normalization.OK:
                return
            normalize = normalization.normalize

        # If training, allow user to define specific patches to train on, otherwise default to random patches.
        randompatchgeneration = True
        if not predict:
            definepatches = GUIUtils.DefinePatches()
            definepatches.exec()
            if not definepatches.OK:
                return
            randompatchgeneration = definepatches.randompatchgeneration
        logstr.append(f"Random Patches ({randompatchgeneration}), ")

        # Define which markers to use for pixel clustering.
        trainmarkers = GUIUtils.PixelTrainMarkers(self.viewer, self.markers)
        trainmarkers.exec()
        if not trainmarkers.OK:
            return
        # Must use at least 3 cell markers.
        if len(trainmarkers.markernums) < 3:
            GUIUtils.display_error_message("Not enough markers selected",
                                           "Please select at least three markers for clustering")
            return
        # If loading a model, must use the same number of markers as were used when the model was trained.
        if loadmodel.load:
            if len(trainmarkers.markernums) != numtrainmarkers:
                GUIUtils.display_error_message("Incompatible number of markers",
                                               "Please ensure you use the same number of markers as the model you loaded")
                return
        logstr.append(f"Markers ({trainmarkers.markernums}), ")
        self.pixelclustermarkers.append(trainmarkers.pixeltrainmarkers)

        # Save image attributes to the output folder.
        dir = GUIUtils.create_new_folder("RAPIDPixel_", self.outputfolder)
        self.pixelclusterdirectories.append(dir)
        outfolder = os.path.join(dir, "RAPID_Data")
        hf = zarr.open(outfolder, 'w')
        hf.attrs['markers'] = self.markers
        hf.attrs['flipimg'] = self.flipimg

        # Add a separate popup window for the user to define patches to use for training.
        if not randompatchgeneration:
            # Keep track of where the patches are located for each image.
            self.currentimage = 0
            patchesstart = []
            shapesdata = []
            for i in range(self.numimgs):
                patchesstart.append([])
                shapesdata.append([])

            names = []
            for i in range(len(self.filenames)):
                names.append(self.filenames[i].split("/")[-1])

            contrastlimits = []
            cl = []
            for i in range(len(trainmarkers.markernums)):
                cl.append([0, 255])
            for i in range(len(self.filenames)):
                contrastlimits.append(copy.deepcopy(cl))

            self.define_patches_viewer = napari.Viewer()

            @magicgui(auto_call=True, image={"choices": names, "label": ""})
            def change_image_pixelgui(image: str):
                for i in range(len(self.define_patches_viewer.layers)):
                    # Loop through each shape within each shapes layer.
                    if isinstance(self.define_patches_viewer.layers[i], napari.layers.shapes.shapes.Shapes) and \
                            self.define_patches_viewer.layers[i].visible:
                        for shape in range(len(self.define_patches_viewer.layers[i].data)):
                            # Split each shape into 64x64 patches, adding padding as necessary.
                            # Information will be stored as the top-right corner x- and y- values of each
                            # of these patches.
                            verts = copy.deepcopy(self.define_patches_viewer.layers[i].data[shape])
                            xmin = min(verts[0][1], verts[2][1])
                            xmax = max(verts[0][1], verts[2][1])
                            ymin = min(verts[0][0], verts[2][0])
                            ymax = max(verts[0][0], verts[2][0])
                            xdiff = 64 - ((xmax - xmin) % 64)
                            ydiff = 64 - ((ymax - ymin) % 64)
                            xmin = int(round(xmin - xdiff / 2))
                            xmax = int(round(xmax + xdiff / 2))
                            ymin = int(round(ymin - ydiff / 2))
                            ymax = int(round(ymax + ydiff / 2))
                            if ymin < 0:
                                ymax -= ymin
                                ymin = 0
                            if xmin < 0:
                                xmax -= xmin
                                xmin = 0
                            if ymax > self.imageshapelist[self.currentimage][0]:
                                diff = ymax - self.imageshapelist[self.currentimage][0] + 1
                                ymin -= diff
                                ymax = self.imageshapelist[self.currentimage][0]
                            if xmax > self.imageshapelist[self.currentimage][1]:
                                diff = xmax - self.imageshapelist[self.currentimage][1] + 1
                                xmin -= diff
                                xmax = self.imageshapelist[self.currentimage][1]
                            numxpatches = int((xmax - xmin) / 64)
                            numypatches = int((ymax - ymin) / 64)
                            for j in range(numxpatches):
                                for k in range(numypatches):
                                    cornerx = int(xmin + 64 * j)
                                    cornery = int(ymin + 64 * k)
                                    patchesstart[self.currentimage].append([cornery, cornerx])
                    else:
                        contrastlimits[self.currentimage][i] = self.define_patches_viewer.layers[i].contrast_limits

                # Go to the selected image.
                self.currentimage = names.index(image)

                # Change the images in the viewer to display the next image data.
                for i in range(len(trainmarkers.markernums)):
                    self.define_patches_viewer.layers[i].data = self.viewer.layers[trainmarkers.markernums[i]].data[
                                                                self.currentimage, :, :]
                    self.define_patches_viewer.layers[i].contrast_limits = contrastlimits[self.currentimage][i]

                # Store the shapes for the previous image so they can be added again if necessary.
                for i in range(len(self.define_patches_viewer.layers) - len(trainmarkers.markernums)):
                    if len(self.define_patches_viewer.layers[len(trainmarkers.markernums)].data) > 0:
                        shapesdata[self.currentimage - 1].append(
                            self.define_patches_viewer.layers[len(trainmarkers.markernums)].data)
                    self.define_patches_viewer.layers.pop(len(trainmarkers.markernums))

                # Add any shapes that had been previously added for this image.
                for i in range(len(shapesdata[self.currentimage])):
                    self.define_patches_viewer.add_shapes(shapesdata[self.currentimage][i])
                shapesdata[self.currentimage] = []
                patchesstart[self.currentimage] = []

            @magicgui(call_button="Finish")
            def finish_pixelgui() -> Image:
                for i in range(len(self.define_patches_viewer.layers)):
                    # Loop through each shape within each shapes layer.
                    if isinstance(self.define_patches_viewer.layers[i], napari.layers.shapes.shapes.Shapes) and \
                            self.define_patches_viewer.layers[i].visible:
                        for shape in range(len(self.define_patches_viewer.layers[i].data)):
                            # Split each shape into 64x64 patches, adding padding as necessary.
                            # Information will be stored as the top-right corner x- and y- values of each of
                            # these patches.
                            verts = copy.deepcopy(self.define_patches_viewer.layers[i].data[shape])
                            xmin = min(verts[0][1], verts[2][1])
                            xmax = max(verts[0][1], verts[2][1])
                            ymin = min(verts[0][0], verts[2][0])
                            ymax = max(verts[0][0], verts[2][0])
                            xdiff = 64 - ((xmax - xmin) % 64)
                            ydiff = 64 - ((ymax - ymin) % 64)
                            xmin = int(round(xmin - xdiff / 2))
                            xmax = int(round(xmax + xdiff / 2))
                            ymin = int(round(ymin - ydiff / 2))
                            ymax = int(round(ymax + ydiff / 2))
                            if ymin < 0:
                                ymax -= ymin
                                ymin = 0
                            if xmin < 0:
                                xmax -= xmin
                                xmin = 0
                            if ymax > self.imageshapelist[self.currentimage][0]:
                                diff = ymax - self.imageshapelist[self.currentimage][0]
                                ymin -= diff
                                ymax = self.imageshapelist[self.currentimage][0]
                            if xmax > self.imageshapelist[self.currentimage][1]:
                                diff = xmax - self.imageshapelist[self.currentimage][1]
                                xmin -= diff
                                xmax = self.imageshapelist[self.currentimage][1]
                            numxpatches = int((xmax - xmin) / 64)
                            numypatches = int((ymax - ymin) / 64)
                            for j in range(numxpatches):
                                for k in range(numypatches):
                                    cornerx = int(xmin + 64 * j)
                                    cornery = int(ymin + 64 * k)
                                    patchesstart[self.currentimage].append([cornery, cornerx])

                # Find the number of patches across all the images.
                numpatches = 0
                for img in patchesstart:
                    numpatches += len(img)

                # Prompt user to define parameters.
                args = runRAPIDzarr.get_parameters()
                args.predict = False
                if loadmodel.load:
                    params = GUIUtils.RAPIDTrainLoadedParams(args, randompatches=False)
                    args.rfold = "/".join(loadmodel.dirpath[:-1])
                    copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(dir, "checkpoint.pth"))
                    args.loadmodel = True
                else:
                    maximgshape = np.insert(self.maximageshape, 0, self.nummarkers)
                    params = GUIUtils.RAPIDPixelParameters(len(trainmarkers.markernums), maximgshape,
                                                           randompatches=False)
                    args.rfold = self.outputfolder
                    args.loadmodel = False
                params.exec()
                if not params.OK:
                    return

                # Normalize data for RAPID input.
                self.viewer.status = "Generating RAPID data..."
                self.generate_RAPID_data(trainmarkers.markernums, trainmarkers.pixeltrainmarkers,
                                         params.normalize, outfolder, params.pca, params.denoise)

                # Update parameters and save them to the output folder.
                logstr.append(f"Parameters ({params.nc}, {params.nit}, {params.bs}, {params.mse}, "
                              f"{params.RCN}, {params.lr}, {params.SCAN}, {params.normalize}, {params.pca}, "
                              f"{params.denoise}), ")
                args.ncluster = int(params.nc)
                args.nit = int(params.nit)
                args.bs = int(params.bs)
                args.patchsize = 64
                args.npatches = numpatches
                if params.mse == "True":
                    args.mse = True
                else:
                    args.mse = False
                if params.RC == "True":
                    args.rescale = True
                else:
                    args.rescale = False
                args.rescalefactor = float(params.RCN)
                args.rescale = True
                args.distance = True
                args.lr = float(params.lr)
                args.epoch = 1
                args.GUI = True
                hf = zarr.open(dir, 'a')
                hf.attrs['arg'] = vars(args)
                hf = zarr.open(os.path.join(dir, "RAPID_Data"), mode='r')
                args.nchannels = hf["data_normalized"].shape[1]
                args.SCANloss = params.SCAN
                args.testbs = 20000
                if not self.addedtable:
                    self.mode = "Pixel"
                if not os.path.exists(args.rfold):
                    os.mkdir(args.rfold)
                    args.rfold = args.rfold + "/"
                else:
                    args.rfold = args.rfold + "/"

                # Train RAPID algorithm.
                self.viewer.status = "Training RAPID..."
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                self.viewer.window._status_bar._toggle_activity_dock(True)
                grey, prob, tab, colors, _ = runRAPIDzarr.train_rapid(args, device, os.path.join(dir, "RAPID_Data"),
                                                                      dir, patchesstart)
                self.viewer.window._status_bar._toggle_activity_dock(False)

                # Reshape results into multi-channel image array.
                greypixels = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]))
                count = 0
                for i in range(self.numimgs):
                    xdim = hf["imageshapelist"][i, 0]
                    ydim = hf["imageshapelist"][i, 1]
                    greypixels[i, :xdim, :ydim] = grey[count: count + xdim * ydim].reshape(xdim, ydim)
                    count += xdim * ydim

                # Save colors to the output folder.
                if loadmodel.load:
                    colors = np.load("/".join(loadmodel.dirpath[:-1]) + "/color.npy")
                np.save(os.path.join(dir, "color.npy"), colors)

                # Pad the images and add arranged cluster IDs at the end for sampling.
                greypixels[:, -args.ncluster:, -1] = np.unique(args.ncluster)
                for i in range(self.numimgs):
                    greypixels[i, :, self.imageshapelist[i][1]:] = -1
                    greypixels[i, self.imageshapelist[i][0]:, :] = -1

                # Update any relevant variables and close the window.
                self.greypixels.append(greypixels)
                self.currentlyselectedpixelclusters.append([])
                self.apply_RAPID_pixel(tab.values, args, colors, dir)
                self.pixeltraincount += 1
                logstr.append(f"Patches ({patchesstart}), ")
                self.define_patches_viewer.window.qt_viewer.close()
                self.define_patches_viewer.window._qt_window.close()

            @magicgui(call_button="Toggle Visibility")
            def toggle_visibility_pixelgui() -> Image:
                # If any markers are visible, make them invisible. Otherwise, make all markers visible.
                visible = False
                for le in range(len(self.define_patches_viewer.layers)):
                    if self.define_patches_viewer.layers[le].visible:
                        visible = True
                if visible:
                    for i in range(len(self.define_patches_viewer.layers)):
                        self.define_patches_viewer.layers[i].visible = False
                else:
                    for i in range(len(self.define_patches_viewer.layers)):
                        self.define_patches_viewer.layers[i].visible = True

            # Add widgets to the bottom of the patches window.
            definepatcheswidget = QWidget()
            filterLayout = QGridLayout()
            filterLayout.setSpacing(0)
            filterLayout.setContentsMargins(0, 0, 0, 0)
            togglevisgui = toggle_visibility_pixelgui.native
            togglevisgui.setToolTip("Set all layers to visible/invisible")
            filterLayout.addWidget(togglevisgui, 0, 0)

            # Allow user to toggle between images if there are multiple images.
            if self.numimgs > 1:
                changeimagegui = change_image_pixelgui.native
                changeimagegui.setToolTip("Toggle images")
                filterLayout.addWidget(changeimagegui, 0, 1)
                finishgui = finish_pixelgui.native
                finishgui.setToolTip("Perform Clustering")
                filterLayout.addWidget(finishgui, 0, 2)

            else:
                finishgui = finish_pixelgui.native
                finishgui.setToolTip("Perform Clustering")
                filterLayout.addWidget(finishgui, 0, 1)
            definepatcheswidget.setLayout(filterLayout)
            self.define_patches_viewer.window.add_dock_widget(definepatcheswidget, area="bottom")

            # Add the first image to the patches window.
            for i in trainmarkers.markernums:
                cmap = self.viewer.layers[i].colormap
                self.define_patches_viewer.add_image(self.viewer.layers[i].data[0, :, :], name=self.markers[i],
                                                     rgb=False, colormap=cmap, contrast_limits=[0, 255],
                                                     visible=True, blending="additive")

        # If randomly generating patches.
        else:
            # If not predicting without any further training.
            if loadmodel.load and predict:
                # Normalize data for RAPID input.
                self.viewer.status = "Generating RAPID data..."
                pca = False
                if normalize == "all (PCA)":
                    normalize = "all"
                    pca = True
                elif normalize == "all (no PCA)":
                    normalize = "all"
                self.generate_RAPID_data(trainmarkers.markernums, trainmarkers.pixeltrainmarkers, normalize,
                                         outfolder, pca, normalization.denoise)
                self.viewer.status = "Applying loaded model..."

                # Update parameters and save them to the output folder.
                hf = zarr.open("/".join(loadmodel.dirpath[:-1]) + "/RAPID_Data", 'r')
                args = Namespace(**hf.attrs['arg'])
                args.nchannels = hf["data_normalized"].shape[1]
                args.GUI = True
                args.rfold = "/".join(loadmodel.dirpath[:-1])
                copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(dir, "checkpoint.pth"))
                args.train = False
                args.predict = True
                print(args)
                logstr.append(f"Normalize ({normalize})")

            # If training a model.
            else:
                # If training a pretrained model.
                if loadmodel.load:
                    # Update parameters and save them to the output folder.
                    hf = zarr.open("/".join(loadmodel.dirpath[:-1]) + "/RAPID_Data", 'r')
                    args = Namespace(**hf.attrs['arg'])
                    args.predict = False
                    params = GUIUtils.RAPIDTrainLoadedParams(args)
                    args.rfold = "/".join(loadmodel.dirpath[:-1])
                    copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(dir, "checkpoint.pth"))
                    args.loadmodel = True

                # If training a new model.
                else:
                    # Update parameters and save them to the output folder.
                    args = runRAPIDzarr.get_parameters()
                    args.predict = False
                    maximgshape = np.insert(self.maximageshape, 0, self.nummarkers)
                    params = GUIUtils.RAPIDPixelParameters(len(trainmarkers.markernums), maximgshape)
                    args.rfold = self.outputfolder
                    args.loadmodel = False
                params.exec()
                if not params.OK:
                    return
                logstr.append(f"Parameters ({params.nc}, {params.nit}, {params.bs}, {params.ps}, {params.nop}, "
                              f"{params.mse},, {params.RC} {params.RCN}, {params.lr}, {params.SCAN}, "
                              f"{params.normalize}, {params.pca}, {params.denoise})")
                self.viewer.status = "Generating RAPID data..."
                self.generate_RAPID_data(trainmarkers.markernums, trainmarkers.pixeltrainmarkers,
                                         params.normalize, outfolder, params.pca, params.denoise)
                self.viewer.status = "Training RAPID..."
                args.ncluster = int(params.nc)
                args.nit = int(params.nit)
                args.bs = int(params.bs)
                args.patchsize = int(params.ps)
                args.npatches = int(params.nop)
                args.mse = (params.mse == "True")
                args.rescale = (params.RC == "True")
                args.rescalefactor = float(params.RCN)
                args.rescale = True
                args.distance = True
                args.lr = float(params.lr)
                args.epoch = 1
                args.SCANloss = params.SCAN
                args.testbs = 20000
                args.GUI = True
                hf = zarr.open(os.path.join(dir, "RAPID_Data"), 'a')
                hf.attrs['arg'] = vars(args)
                hf = zarr.open(os.path.join(dir, "RAPID_Data"), mode='r')
                args.nchannels = hf["data_normalized"].shape[1]
            args.testbs = 20000

            # Train RAPID algorithm.
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.viewer.window._status_bar._toggle_activity_dock(True)
            grey, prob, tab, colors, _ = runRAPIDzarr.train_rapid(args, device, os.path.join(dir, "RAPID_Data"), dir)
            self.viewer.window._status_bar._toggle_activity_dock(False)
            if not self.addedtable:
                self.mode = "Pixel"
            if not os.path.exists(args.rfold):
                os.mkdir(args.rfold)

            # Reshape results into multi-channel image array.
            greypixels = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]))
            count = 0
            for i in range(self.numimgs):
                xdim = hf["imageshapelist"][i, 0]
                ydim = hf["imageshapelist"][i, 1]
                greypixels[i, :xdim, :ydim] = grey[count:count + xdim * ydim].reshape(xdim, ydim)
                count += xdim * ydim
            greypixels[:, -args.ncluster:, -1] = np.arange(args.ncluster)
            for i in range(self.numimgs):
                greypixels[i, :, self.imageshapelist[i][1]:] = -1
                greypixels[i, self.imageshapelist[i][0]:, :] = -1

            # Save colors to the output folder.
            if loadmodel.load:
                colors = np.load("/".join(loadmodel.dirpath[:-1]) + "/color.npy")
            np.save(os.path.join(dir, "color.npy"), colors)

            # Update any relevant variables and close the window.
            self.greypixels.append(greypixels)
            self.currentlyselectedpixelclusters.append([])
            self.apply_RAPID_pixel(tab.values, args, colors, dir)
            self.pixeltraincount += 1
            GUIUtils.log_actions(self.actionloggerpath, "".join(logstr))

    def quantify_object_cluster_region(self, imgindex, shapelayerindex, shapetypes, clusteriteration):
        """
        Find number of cells from each object-based cluster in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapelayerindex (int): Layer index corresponding to the shapes drawn by the user.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
            clusteriteration (int): Index for the round of object clustering being used for analysis.
        """
        for i in range(len(self.objecttrainlist)):
            if clusteriteration in self.objecttrainlist[i]:
                segmentimgindex = i * self.numimgs

        greysegment = self.objectplots[segmentimgindex + imgindex]
        qtab = self.Qtab[segmentimgindex * self.numimgs + imgindex]
        currentimg = np.zeros((greysegment.shape[0], greysegment.shape[1], 3))
        currentimg[:, :, 0] = greysegment
        for i in range(currentimg.shape[0]):
            currentimg[i, :, 1] = i
        for i in range(currentimg.shape[1]):
            currentimg[:, i, 2] = i
        dim1 = currentimg.shape[0]
        dim2 = currentimg.shape[1]
        currentimg = np.reshape(currentimg, (dim1 * dim2, currentimg.shape[2]))

        avgs = []
        numcells = []
        celldata = []
        for shape in range(len(self.viewer.layers[shapelayerindex].data)):
            cells = 0
            tupVerts = copy.deepcopy(self.viewer.layers[shapelayerindex].data[shape])[:, -2:]
            p = self.create_shape_path(tupVerts, shapetypes[shape])
            mask = p.contains_points(currentimg[:, 1:])
            cellindices = currentimg[:, 0][mask]
            cellindices = np.unique(cellindices)
            clustervals = copy.deepcopy(cellindices[cellindices > 0])
            tabdata = pd.DataFrame(qtab[[int(i - 1) for i in clustervals], :])
            tabdata.columns = ["Cell ID"] + self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            celldata.append(tabdata)

            clusternums = self.objectclusters[clusteriteration * self.numimgs + imgindex]
            for i in range(len(clustervals)):
                clustervals[i] = clusternums[int(clustervals[i]) - 1]
            currentimgavgs = []
            for i in range(int(np.max(self.greyobjects[clusteriteration]))):
                currentimgavgs.append(np.count_nonzero(clustervals == i + 1))
                cells += np.count_nonzero(clustervals == i + 1)
            avgs.append(currentimgavgs)
            numcells.append(cells)
        return avgs, int(np.max(self.greyobjects[clusteriteration])), numcells, celldata

    def quantify_pixel_cluster_region(self, imgindex, shapelayerindex, shapetype, clusteriteration):
        """
        Find number of pixels from each pixel-based cluster in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapelayerindex (int): Additional user-defined parameters used for training.
            shapetype (list): List of strings representing shapes for the connected series of vertices.
            clusteriteration (int): Index for the round of pixel clustering being used for analysis.
        """
        numpixels = []
        grey = self.greypixels[clusteriteration]
        currentimg = np.zeros((grey.shape[1], grey.shape[2], 3))
        currentimg[:, :, 0] = grey[imgindex, :, :]
        for i in range(currentimg.shape[0]):
            currentimg[i, :, 1] = i
        for i in range(currentimg.shape[1]):
            currentimg[:, i, 2] = i
        dim1 = currentimg.shape[0]
        dim2 = currentimg.shape[1]
        currentimg = np.reshape(currentimg, (dim1 * dim2, currentimg.shape[2]))
        avgs = []
        for shape in range(len(self.viewer.layers[shapelayerindex].data)):
            tupVerts = copy.deepcopy(self.viewer.layers[shapelayerindex].data[shape])[:, -2:]
            p = self.create_shape_path(tupVerts, shapetype[shape])
            mask = p.contains_points(currentimg[:, 1:])
            numpixels.append(np.count_nonzero(mask))
            currentimgavgs = []
            clustervals = currentimg[:, 0][mask]
            for i in range(0, int(np.max(grey)) + 1):
                currentimgavgs.append(np.count_nonzero(clustervals == i))
            avgs.append(currentimgavgs)
        return avgs, int(np.max(grey)) + 1, numpixels

    def quantify_raw_img_region(self, imgindex, shapelayerindex, shapetype, verts):
        """
        Find average expression values for each cell marker in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapelayerindex (int): Additional user-defined parameters used for training.
            shapetype (list): List of strings representing shapes for the connected series of vertices.
            verts (list): List of coordinates for vertices being connected to form the shape(s).
        """
        currentimg = np.zeros((self.nummarkers, self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint32)
        for i in range(self.nummarkers):
            currentimg[i, :, :, 0] = self.viewer.layers[i].data[imgindex, :, :]
        for i in range(currentimg.shape[1]):
            currentimg[:, i, :, 1] = i
        for i in range(currentimg.shape[2]):
            currentimg[:, :, i, 2] = i
        dim1 = currentimg.shape[1]
        dim2 = currentimg.shape[2]
        currentimg = np.reshape(currentimg, (currentimg.shape[0], dim1 * dim2, currentimg.shape[3]))
        avgs = []
        numpixels = []
        for i in range(len(self.viewer.layers[shapelayerindex].data)):
            p = self.create_shape_path(verts[i][:, 1:], shapetype[i])
            mask = p.contains_points(currentimg[0, :, 1:])
            numpixels.append(np.count_nonzero(mask))
            currentimgavgs = []
            for j in range(len(currentimg)):
                img = currentimg[j, :, 0]
                avg = np.mean(img[mask])
                currentimgavgs.append(round(avg, 2))
            avgs.append(currentimgavgs)
        return avgs, numpixels

    def quantify_region(self):
        """
        Provide quantitative readouts for the phenotypes of pixels or cells in each shape drawn by the user, either for
        the raw image or for a clustered image.
        """
        # Ensure there is at least one shape drawn in order to define the region to be quantified.
        ind = -1
        for i in reversed(range(len(self.viewer.layers))):
            if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and self.viewer.layers[i].visible:
                ind = i
                break
        if ind == -1:
            GUIUtils.display_error_message("Please draw a shape first",
                                           "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
            return

        # Find the bounding vertices and the geometries for each of the shapes drawn.
        verts = [self.viewer.layers[ind].data[i] for i in range(len(self.viewer.layers[ind].data))]
        shapetype = [self.viewer.layers[ind].shape_type[i] for i in range(len(self.viewer.layers[ind].data))]

        # Can only do this if an image has been loaded or if the current image ID is greater than the number of
        # images (ie, more UMAP plots than there are images).
        imgnum = self.viewer.dims.current_step[0]
        if imgnum > self.numimgs:
            GUIUtils.display_error_message("No image in the viewer",
                                           "Please make sure that there is a valid image being displayed in the viewer")
            return

        # Prompt user to define whether to quantify average marker expression from raw image, or cluster number
        # of objects from cluster assignments.
        if len(self.pixelbasedclusters) > 0:
            selectdatapopup = GUIUtils.SelectData()
            selectdatapopup.exec()
            if not selectdatapopup.OK:
                return
            rawimg = selectdatapopup.rawimg
        else:
            rawimg = True

        # If using raw image, find average expression of each marker in each shape.
        if rawimg:
            # Find averages and number of pixels in each shape.
            avgs, numpixels = self.quantify_raw_img_region(imgnum, ind, shapetype, verts)

            # Re-color and label each of the shapes.
            self.viewer.layers.pop(ind)
            labels = []
            for i in range(len(avgs)):
                labels.append(f"Region {i + 1}")
            properties = {'class': labels, }
            text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
            self.viewer.add_shapes(verts, shape_type=shapetype, edge_width=0, properties=properties,
                                   name=f"Quantified Regions {self.selectedregioncount}", text=text_properties,
                                   face_color=[np.array([0.2, 0.2, 0.2])])

            # Add labels for each of the regions for the saved csv file and to add to the shapes.
            dir = GUIUtils.create_new_folder("QuantifiedRawRegion_", self.outputfolder)
            quantifypopup = GUIUtils.QuantifyRegionPopup(avgs, "raw", len(self.markers), self.markers, numpixels,
                                                         dir, self.selectedregioncount)
            quantifypopup.exec()
            if quantifypopup.saved:
                labelnames = list(quantifypopup.headernames)[1:]
                if not labelnames == labels:
                    self.viewer.layers.pop(len(self.viewer.layers) - 1)
                    properties = {'class': labelnames, }
                    text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    self.viewer.add_shapes(verts, shape_type=shapetype, edge_width=0,
                                           name=f"Quantified Regions {self.selectedregioncount}",
                                           properties=properties, text=text_properties,
                                           face_color=[np.array([0.2, 0.2, 0.2])])
                self.selectedregioncount += 1
            GUIUtils.log_actions(self.actionloggerpath, f"Quantified Region: Vertices ({verts}), Shapes: ({shapetype}),"
                                                        f" Raw Image, Saved ({quantifypopup.saved})")

        # If using clustered results, find number of pixels/cells from each cluster within each shape.
        else:
            # If clustering has only been done once, use that by default.
            if len(self.pixelbasedclusters) == 1:
                clusteringnum = 0
                ispixelcluster = self.pixelbasedclusters[0]
            # If clustering has been done more than once, prompt the user to choose which one to use.
            else:
                selectclusteringround = GUIUtils.SelectClusteringRound(self.pixelbasedclusters)
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                clusteringnum = selectclusteringround.clusteringnum
                ispixelcluster = selectclusteringround.ispixelcluster

            # If the user selected pixel-based clustering results.
            if ispixelcluster:
                # Find number of pixels from each cluster in each shape.
                avgs, numrows, numpixels = self.quantify_pixel_cluster_region(imgnum, ind, shapetype, clusteringnum)

                # Re-color and label each of the shapes.
                self.viewer.layers.pop(ind)
                labels = []
                for i in range(len(avgs)):
                    labels.append(f"Region {i + 1}")
                properties = {'class': labels, }
                textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                self.viewer.add_shapes(verts, shape_type=shapetype, edge_width=0,
                                       name=f"Quantified Regions {self.selectedregioncount}",
                                       properties=properties, text=textproperties,
                                       face_color=[np.array([0.2, 0.2, 0.2])])

                # Add labels for each of the regions for the saved csv file and to add to the shapes.
                dir = GUIUtils.create_new_folder("QuantifiedPixelRegion_", self.outputfolder)
                quantifypopup = GUIUtils.QuantifyRegionPopup(avgs, "pixel", numrows, self.markers, numpixels, dir,
                                                             self.selectedregioncount)
                quantifypopup.exec()
                if quantifypopup.saved:
                    labelnames = list(quantifypopup.headernames)[1:]
                    if not labelnames == labels:
                        self.viewer.layers.pop(len(self.viewer.layers) - 1)
                        properties = {'class': labelnames, }
                        textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                        self.viewer.add_shapes(verts, shape_type=shapetype, edge_width=0,
                                               name=f"Quantified Regions {self.selectedregioncount}",
                                               properties=properties, text=textproperties,
                                               face_color=[np.array([0.2, 0.2, 0.2])])
                    self.selectedregioncount += 1
                GUIUtils.log_actions(self.actionloggerpath, f"Quantified Region: Vertices ({verts}), Shapes: "
                                                            f"({shapetype}), Pixel Clustering ({clusteringnum}), "
                                                            f"Saved ({quantifypopup.saved})")
            else:
                # Find averages and number of pixels in each shape.
                avgs, numrows, numcells, celldata = self.quantify_object_cluster_region(imgnum, ind, shapetype,
                                                                                        clusteringnum)

                # Re-color and label each of the shapes.
                self.viewer.layers.pop(ind)
                labels = []
                for i in range(len(avgs)):
                    labels.append(f"Region {i + 1}")
                properties = {'class': labels, }
                textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                self.viewer.add_shapes(verts, shape_type=shapetype, edge_width=0,
                                       name=f"Quantified Regions {self.selectedregioncount}",
                                       properties=properties, text=textproperties,
                                       face_color=[np.array([0.2, 0.2, 0.2])])
                filenames = [os.path.split(name)[-1].split(".")[0] for name in self.filenames]

                # Add labels for each of the regions for the saved csv file and to add to the shapes.
                dir = GUIUtils.create_new_folder("QuantifiedObjectRegion_", self.outputfolder)
                quantifypopup = GUIUtils.QuantifyRegionPopup(avgs, "object", numrows, self.markers, numcells, dir,
                                                             self.selectedregioncount, celldata)
                quantifypopup.exec()
                if quantifypopup.saved:
                    labelnames = list(quantifypopup.headernames)[1:]
                    if not labelnames == labels:
                        self.viewer.layers.pop(len(self.viewer.layers) - 1)
                        properties = {'class': labelnames, }
                        textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                        self.viewer.add_shapes(verts, shape_type=shapetype, edge_width=0,
                                               name=f"Quantified Regions {self.selectedregioncount}",
                                               properties=properties, text=textproperties,
                                               face_color=[np.array([0.2, 0.2, 0.2])])
                    self.selectedregioncount += 1
                GUIUtils.log_actions(self.actionloggerpath, f"Quantified Region: Vertices ({verts}), Shapes: "
                                                            f"({shapetype}), Object Clustering ({clusteringnum}), "
                                                            f"Saved ({quantifypopup.saved})")

    ### TODO: Redo Example in doctest
    def remove_large_objects(self, array, maxsize=64, connectivity=1, in_place=False):
        """
        Remove connected components from an image array that are smaller than the specified size.
        (Taken from sklearn)

        Args:
            array (numpy.ndarray): The image array containing the connected components of interest. If the array type is int, it is assumed that it contains already-labeled objects. The values must be non-negative.
            maxsize (int, optional): The smallest allowable connected component size (Default: 64).
            connectivity (int, {1, 2, ..., ar.ndim}, optional): The connectivity defining the neighborhood of a pixel (Default: 1).
            in_place (bool, optional): If True, remove the connected components in the input array itself. Otherwise, make a copy (Default: False).

        Raises:
            TypeError: If the input array is of an invalid type, such as float or string.
            ValueError: If the input array contains negative values.

        :return: out *(numpy.ndarray)*: \n
            The input array with small connected components removed.

        :Examples:

        >>> a = np.array([[0, 0, 0, 1, 0],
        ...               [1, 1, 1, 0, 0],
        ...               [1, 1, 1, 0, 1]], bool)
        >>> b = morphology.remove_small_objects(a, 6)
        >>> b
        array([[False, False, False, False, False],
               [ True,  True,  True, False, False],
               [ True,  True,  True, False, False]], dtype=bool)
        >>> c = morphology.remove_small_objects(a, 7, connectivity=2)
        >>> c
        array([[False, False, False,  True, False],
               [ True,  True,  True, False, False],
               [ True,  True,  True, False, False]], dtype=bool)
        >>> d = morphology.remove_small_objects(a, 6, in_place=True)
        >>> d is a
        True
        """

        if in_place:
            out = array
        else:
            out = array.copy()

        if maxsize == 0:  # shortcut for efficiency
            return out

        if out.dtype == bool:
            selem = ndi.generate_binary_structure(array.ndim, connectivity)
            ccs = np.zeros_like(array, dtype=np.int32)
            ndi.label(array, selem, output=ccs)
        else:
            ccs = out

        try:
            component_sizes = np.bincount(ccs.ravel())
        except ValueError:
            raise ValueError("Negative value labels are not supported. Try "
                             "relabeling the input with `scipy.ndimage.label` or "
                             "`skimage.morphology.label`.")

        too_large = component_sizes > maxsize
        too_large_mask = too_large[ccs]
        out[too_large_mask] = 0

        return out

    def reset_metadata(self):
        """
        Reset the contrast limits, gamma, and opacity values to their original values.
        """
        for i in range(len(self.viewer.layers)):
            try:
                self.viewer.layers[i].contrast_limits = self.viewer.layers[i].contrast_limits_range
            except:
                pass
            try:
                self.viewer.layers[i].gamma = 1.0
            except:
                pass
            try:
                self.viewer.layers[i].opacity = 1.0
            except:
                pass
        GUIUtils.log_actions(self.actionloggerpath, "Reset Metadata")

    ### TODO: Think of which analyses the cluster names should be used for, as well as with saved files.
    def rename_clusters(self):
        """
        Prompt the user to select a round of clustering and assign a name to each cluster.
        """
        # Check that the user has performed at least one clustering algorithm.
        if len(self.pixelbasedclusters) == 0:
            GUIUtils.display_error_message("No clustering results found",
                                           "Spatial analysis can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been executed once, use that by default.
        if len(self.pixelbasedclusters) == 1:
            clusteringnum = 0

        # If clustering has been executed multiple times, allow user to select which one.
        else:
            selectclusteringround = GUIUtils.SelectClusteringRound(self.pixelbasedclusters)
            selectclusteringround.exec()
            if not selectclusteringround.OK:
                return
            clusteringnum = selectclusteringround.clusteringnum

        # Find current names of clusters.
        currentnames = self.annotatedclusters[clusteringnum]

        # If list is empty, find number of clusters and use those for the names.
        if len(currentnames) == 0:
            if self.pixelbasedclusters[clusteringnum]:
                ind = self.pixelbasedclusters[:clusteringnum].count(True)
                numclusters = len(np.unique(self.greypixels[ind]))
            else:
                ind = self.pixelbasedclusters[:clusteringnum].count(False)
                numclusters = len(np.unique(self.greyobjects[ind])) - 1
            currentnames = [f"Cluster {i + 1}" for i in range(numclusters)]

        # Prompt user to rename clusters.
        renameclusters = GUIUtils.RenameClusters(currentnames)
        renameclusters.exec()
        if not renameclusters.OK:
            return

        # Store new names in list.
        self.annotatedclusters[clusteringnum] = renameclusters.newclusternames

        # If table is currently visible, update the names accordingly.
        self.verticalheaderlabels[3:] = renameclusters.newclusternames
        self.tablewidget.setVerticalHeaderLabels(np.asarray(self.verticalheaderlabels))

        GUIUtils.log_actions(self.actionloggerpath,
                             f"Renamed Clusters: Clustering Round ({clusteringnum}), Names ({renameclusters.newclusternames})")

    def sample_group(self):
        """
        Open a popup window for the user to assign each image to different groups.
        """
        # No necessity to assign groups if fewer than 3 images are loaded.
        if self.numimgs < 3:
            GUIUtils.display_error_message("More images required",
                                           "At least 3 images needed to create groups")
            return

        # Prompt user to define the number of groups
        self.ng = GUIUtils.NumGroups(self.numimgs)
        self.ng.exec()
        if not self.ng.OK:
            return

        # Retrieve the names of all loaded images.
        imgnames = []
        for fname in self.filenames:
            name = fname.split("/")
            imgnames.append(name[-1])

        # Prompt user to assign each image to a group.
        gawidget = GUIUtils.GroupAssign(self.ng.ngroups, imgnames, self.viewer, self.groupsnames)
        gawidget.exec()
        self.groupslist.append(gawidget.namelist)
        self.groupsnames.append(gawidget.name)
        GUIUtils.log_actions(self.outputfolder,
                             f"Assigned groups: Name ({gawidget.name}), Groupings ({gawidget.namelist})")

    def save_data(self):
        """
        Open a popup for the user to save data. Options include "Save Visible Window" (to save exactly what is currently
        visible in the viewer window), "Save Screenshot of GUI" (to save a screenshot of the entire RAPID GUI window),
        "Save Clusters" (to save each individual cluster from a selected round of clustering), "Save Table" (to export
        the exact data table currently being displayed as a csv file), and "Save Full Visible Images" (to save each
        user-selected raw image individually, including contrast limits and colormaps).
        """
        self.viewer.status = "Saving..."
        GUIUtils.SaveData(self.viewer, self.outputfolder, self.fulltab, self.pixelbasedclusters, self.greypixels,
                          self.greyobjects, self.imageshapelist, self.filenames, self.flipimg).exec()

    ### TODO: Do this continuously while using GUI. Store/load all global variables from there.
    def save_environment(self):
        """
        Save a RAPID GUI session so the user may resume it exactly as they are leaving it.
        """
        self.viewer.status = "Saving environment..."
        GUIUtils.log_actions(self.outputfolder, "Saved Environment")

        # Store variables.
        config = configparser.ConfigParser()
        config.add_section("Variables")
        config.set("Variables", 'addedtable', unicode(self.addedtable))
        config.set("Variables", 'addwhenchecked', unicode(self.addwhenchecked))
        config.set("Variables", 'editedimage', unicode(self.editedimage))
        config.set("Variables", 'hasloadedpixel', unicode(self.hasloadedpixel))
        config.set("Variables", 'imagehasbeenloaded', unicode(self.imagehasbeenloaded))

        config.set("Variables", 'actionloggerpath', unicode(self.actionloggerpath))
        config.set("Variables", 'biaxialcount', unicode(self.biaxialcount))
        config.set("Variables", 'displayselectedcount', unicode(self.displayselectedcount))
        config.set("Variables", 'editimagepath', unicode(self.editimagepath))
        config.set("Variables", 'index', unicode(self.index))
        config.set("Variables", 'listindex', unicode(self.listindex))
        config.set("Variables", 'mode', unicode(self.mode))
        config.set("Variables", 'numclasses', unicode(self.numclasses))
        config.set("Variables", 'numimgs', unicode(self.numimgs))
        config.set("Variables", 'nummarkers', unicode(self.nummarkers))
        config.set("Variables", 'objecttraincount', unicode(self.objecttraincount))
        config.set("Variables", 'outputfolder', unicode(self.outputfolder))
        config.set("Variables", 'pixeltraincount', unicode(self.pixeltraincount))
        config.set("Variables", 'res', unicode(self.res))
        config.set("Variables", 'segmentcount', unicode(self.segmentcount))
        config.set("Variables", 'selectedregioncount', unicode(self.selectedregioncount))
        config.set("Variables", 'tableimgcount', unicode(self.tableimgcount))
        config.set("Variables", 'umapcount', unicode(self.umapcount))

        config.set("Variables", 'annotatedclusters', unicode(self.annotatedclusters))
        config.set("Variables", 'cellindices', unicode(self.cellindices))
        config.set("Variables", 'cellnums', unicode(self.cellnums))
        config.set("Variables", 'columnheaders', unicode(self.columnheaders))
        config.set("Variables", 'combcellnums', unicode(self.combcellnums))
        coords = []
        for i in range(len(self.coordinates)):
            coords.append([arr.tolist() for arr in self.coordinates[i]])
        config.set("Variables", 'coordinates', unicode(coords))
        config.set("Variables", 'cortabs', unicode(self.cortabs))
        config.set("Variables", 'curimgs', unicode(self.curimgs))
        config.set("Variables", 'currentlyselectedcells', unicode(self.currentlyselectedcells))
        config.set("Variables", 'currentlyselectedobjectclusters', unicode(self.currentlyselectedobjectclusters))
        config.set("Variables", 'curentlyselectedpixelclusters', unicode(self.currentlyselectedpixelclusters))
        config.set("Variables", 'datalist', unicode([arr.tolist() for arr in self.datalist]))
        config.set("Variables", 'datanorm', unicode(self.datanorm))
        config.set("Variables", 'datavals', unicode(self.datavals.tolist()))
        config.set("Variables", 'editactions', unicode(self.editactions))
        config.set("Variables", 'filenames', unicode(self.filenames))
        config.set("Variables", 'flipimg', unicode(self.flipimg))
        config.set("Variables", 'fulltab', unicode(self.fulltab.to_json()))
        config.set("Variables", 'greyobjects', unicode([arr.tolist() for arr in self.greyobjects]))
        config.set("Variables", 'greypixels', unicode([arr.tolist() for arr in self.greypixels]))
        config.set("Variables", 'groupslist', unicode(self.groupslist))
        config.set("Variables", 'groupsnames', unicode(self.groupsnames))
        config.set("Variables", 'imageshapelist', unicode(self.imageshapelist))
        config.set("Variables", 'lowerbounds', unicode(self.lowerbounds))
        config.set("Variables", 'lowerboundslist', unicode(self.lowerboundslist))
        config.set("Variables", 'markers', unicode(self.markers))
        config.set("Variables", 'maximageshape', unicode([arr.tolist() for arr in self.maximageshape]))
        config.set("Variables", 'maxvalsobject', unicode(self.maxvalsobject))
        config.set("Variables", 'maxvalspixel', unicode(self.maxvalspixel))
        config.set("Variables", 'maxvalssegment', unicode(self.maxvalssegment))
        config.set("Variables", 'mergedimagespaths', unicode(self.mergedimagespaths))
        config.set("Variables", 'mergememmarkers', unicode(self.mergememmarkers))
        config.set("Variables", 'mergenuclearmarkers', unicode(self.mergenucmarkers))
        config.set("Variables", 'minvalsobject', unicode(self.minvalsobject))
        config.set("Variables", 'minvalspixel', unicode(self.minvalspixel))
        config.set("Variables", 'minvalssegment', unicode(self.minvalssegment))
        config.set("Variables", 'objectclusterdirectories', unicode(self.objectclusterdirectories))
        config.set("Variables", 'objectclusterindices', unicode(self.objectclusterindices))
        config.set("Variables", 'objectclusternums', unicode(self.objectclusternums))
        config.set("Variables", 'objectclusters', unicode([arr.tolist() for arr in self.objectclusters]))
        config.set("Variables", 'objectcolor', unicode(self.objectcolor))
        config.set("Variables", 'objectdatalist', unicode([arr.tolist() for arr in self.objectdatalist]))
        config.set("Variables", 'objectimgnames', unicode(self.objectimgnames))
        config.set("Variables", 'objectplots', unicode([arr.tolist() for arr in self.objectplots]))
        config.set("Variables", 'objecttrainlist', unicode(self.objecttrainlist))
        config.set("Variables", 'order', unicode(self.order))
        config.set("Variables", 'orders', unicode(self.orders))
        config.set("Variables", 'pixelbasedclusters', unicode(self.pixelbasedclusters))
        config.set("Variables", 'pixelclusterdirectories', unicode(self.pixelclusterdirectories))
        config.set("Variables", 'pixelclusterindices', unicode(self.pixelclusterindices))
        config.set("Variables", 'pixelclustermarkers', unicode(self.pixelclustermarkers))
        config.set("Variables", 'pixelclusternums', unicode(self.pixelclusternums))
        config.set("Variables", 'pixelcolor', unicode(self.pixelcolor))
        config.set("Variables", 'Qtab', unicode([arr.tolist() for arr in self.Qtab]))
        config.set("Variables", 'sampleshapes', unicode(self.sampleshapes))
        config.set("Variables", 'segmentationindicesinumap', unicode(self.segmentationindicesinumap))
        config.set("Variables", 'segmentcounts', unicode(self.segmentcounts))
        config.set("Variables", 'segmentedimgpaths', unicode(self.segmentedimgpaths))
        config.set("Variables", 'tabdata', unicode([d.to_json() for d in self.tabdata]))
        config.set("Variables", 'tableimagenames', unicode(self.tableimagenames))
        config.set("Variables", 'tableorder', unicode(self.tableorder))
        config.set("Variables", 'umapplots', unicode(self.umapplots))
        config.set("Variables", 'upperbounds', unicode(self.upperbounds))
        config.set("Variables", 'upperboundslist', unicode(self.upperboundslist))
        config.set("Variables", 'verticalheaderlabels', unicode(self.verticalheaderlabels.tolist()))
        config.set("Variables", 'xmins', unicode(self.xmins))
        config.set("Variables", 'xmaxs', unicode(self.xmaxs))
        config.set("Variables", 'ymins', unicode(self.ymins))
        config.set("Variables", 'ymaxs', unicode(self.ymaxs))
        if self.addedtable:
            config.set("Variables", 'datavals', unicode(self.datavals.tolist()))
            config.set("Variables", 'numclasses', unicode(self.numclasses))
            config.set("Variables", 'tableorder', unicode(self.tableorder))
            config.set("Variables", 'tablecurrentmarker', unicode(self.sorttableimages.marker.value))
            config.set("Variables", 'tablecurrentdata', unicode(self.sorttableimages.data.value))
            config.set("Variables", 'tablecurrentsort', unicode(self.sorttableimages.sort.value))

        # Save variables to a config file.
        dir = GUIUtils.create_new_folder("SavedEnvironment", self.outputfolder)
        cfgfile = open(os.path.join(dir, "savedenvironment.ini"), "w")
        config.write(cfgfile)
        cfgfile.close()

        # Store metadata for all layers in the GUI.
        fh = zarr.open(dir, mode='a')
        for i in range(len(self.viewer.layers)):
            try:
                data = fh.create_dataset(f"Layer{i + 1}", data=self.viewer.layers[i].data)
                data.attrs["CL"] = [float(j) for j in self.viewer.layers[i].contrast_limits]
                data.attrs["CLRange"] = [float(j) for j in self.viewer.layers[i].contrast_limits_range]
                data.attrs["Gamma"] = self.viewer.layers[i].gamma
                data.attrs["Opacity"] = self.viewer.layers[i].opacity
                data.attrs["Colormap0"] = int(self.viewer.layers[i].colormap.colors[-1][0] * 255)
                data.attrs["Colormap1"] = int(self.viewer.layers[i].colormap.colors[-1][1] * 255)
                data.attrs["Colormap2"] = int(self.viewer.layers[i].colormap.colors[-1][2] * 255)
                data.attrs["Visible"] = self.viewer.layers[i].visible
                data.attrs["Name"] = self.viewer.layers[i].name
            except:
                print(f"Did not save for layer {i + 1}")
        self.viewer.status = "Completed saving environment"

    def segment(self):
        """
        Use the RAPID segmentation algorithm on the images loaded into the RAPID GUI.
        """
        # Can only segment if markers have been merged.
        import gdown
        if len(self.segmentcounts) == 0:
            GUIUtils.display_error_message("Please merge markers first",
                                           "Begin by opening the image(s) that you would like to segment, then merge the markers to be used for segmentation.")
            return

        # Indicate whether to use RAPID or RAPID+ segmentation model.
        segmentationmodel = GUIUtils.SegmentationModel()
        segmentationmodel.exec()
        if not segmentationmodel.OK:
            return
        rootfolder = os.path.dirname(os.path.abspath(__file__))

        modelpath = rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6.pth"
        if (os.path.exists(modelpath)):
            pass
        else:
            gdown.download("https://drive.google.com/uc?id=1JiYrohWce5-uLjI_-yovDUUxroorwE5W",
                           rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6.pth")
            gdown.download("https://drive.google.com/uc?id=1MQjnmpmflQ-BvWgRbsQXwyeQjjfod4mw",
                           rootfolder + "/../models/RAPID-O_RDSB_DC_Fin__MemMix_UnetPlus_Model__resnet50_nclass_2_nchannels_2_gpu_4_seed_100_DCBD38_theta_0.6.pth")
        # shutil.unpack_archive(rootfold+"/../../DocFiles.zip", rootfold+"/../../")

        # shutil.unpack_archive(rootfold+"/../../docs.zip", rootfold+"/../../")
        if segmentationmodel.modelindex == 1:
            modelpath = rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6_Plus.pth"
            if (os.path.exists(modelpath)):
                pass
            else:
                gdown.download("https://drive.google.com/uc?id=1Ji6XmIITbcKR05wt86USEWuous_K5SWl",
                               rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6_Plus.pth")
        # Prompt user to indicate the resolution of the images.
        if self.segmentcount == 0:
            res = GUIUtils.ImageRes()
            res.exec()
            if not res.OK:
                return
            self.res = res.imageres

        # If user has merged markers multiple times, prompt to indicate which one to use.
        iteration = 0
        if len(self.segmentcounts) > 1:
            mergememiteration = GUIUtils.MergeMarkerIteration(len(self.segmentcounts))
            mergememiteration.exec()
            if not mergememiteration.OK:
                return
            iteration = mergememiteration.iteration
        print(iteration)

        # Save images to zarr so they can be easily added when loading segmentation results in the future.
        dir = GUIUtils.create_new_folder("Segmentation", self.outputfolder)
        os.mkdir(os.path.join(dir, "RawImages"))
        fh = zarr.open(os.path.join(dir, "RawImages"), mode='a')
        for i in range(self.nummarkers):
            data = fh.create_dataset(str(i + 1) + "_" + self.viewer.layers[i].name, data=self.viewer.layers[i].data)
            data.attrs["CL"] = [float(j) for j in self.viewer.layers[i].contrast_limits]
            data.attrs["CLRange"] = [float(j) for j in self.viewer.layers[i].contrast_limits_range]
            data.attrs["Gamma"] = self.viewer.layers[i].gamma
            data.attrs["Opacity"] = self.viewer.layers[i].opacity
            data.attrs["Colormap0"] = int(self.viewer.layers[i].colormap.colors[-1][0] * 255)
            data.attrs["Colormap1"] = int(self.viewer.layers[i].colormap.colors[-1][1] * 255)
            data.attrs["Colormap2"] = int(self.viewer.layers[i].colormap.colors[-1][2] * 255)
            data.attrs["Visible"] = self.viewer.layers[i].visible
            data.attrs["Name"] = self.viewer.layers[i].name
        fh.attrs['filenames'] = self.filenames
        fh.attrs['maximageshape'] = self.maximageshape.tolist()
        fh.attrs['markers'] = self.markers
        fh.attrs['markernums'] = self.markernums
        fh.attrs['imageshapelist'] = self.imageshapelist
        fh.attrs['numimgs'] = self.numimgs
        hf = zarr.open(self.mergedimagespaths[iteration], mode='r')
        memimg = hf['Membrane']
        nucimg = hf['Nucleus']
        fh = zarr.open(dir, mode='a')
        fh.create_dataset("MergedImage", data=np.stack([memimg, nucimg], axis=0))

        if not self.addedtable:
            self.mode = "Segmentation"

        # Check if the user has already segmented on the selected merged image.
        alreadysegmented = True
        if self.segmentcounts[iteration][segmentationmodel.modelindex] == -1:
            alreadysegmented = False
            self.segmentcounts[iteration][segmentationmodel.modelindex] = np.max(np.array(self.segmentcounts) + 1)

        # No need to segment again on a merged image that has already been passed through the algorithm.
        if not alreadysegmented:
            self.viewer.status = "Segmenting..."
            self.segmentedimgpaths.append(dir)
            self.viewer.window._status_bar._toggle_activity_dock(True)
            with progress(self.filenames, desc='Image', total=0 if len(self.filenames) == 1 else None, ) as pbr:
                for name in pbr:
                    i = self.filenames.index(name)
                    memimage = memimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]]
                    nucimage = nucimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]]
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    feature = objectmodels.unet_featurize(memimg=memimage, nucimg=nucimage,
                                                          containsmem=self.mergememmarkers[iteration],
                                                          containsnuc=self.mergenucmarkers[iteration], device=device,
                                                          segmodelpath=modelpath)
                    fh.create_dataset(f"Features{i}", data=feature, dtype=np.float)
            self.viewer.window._status_bar._toggle_activity_dock(False)

        # Initialize thresholds to use for segmentation preview popup window.
        self.probthreshold = 1.0
        self.currentimagenum = 0
        self.minsize = round(10 * 0.284 / self.res)
        self.maxsize = round(2000 * 0.284 / self.res)

        # Populate the segmentation preview popup window.
        fh = zarr.open(self.segmentedimgpaths[self.segmentcounts[iteration][segmentationmodel.modelindex]], mode='r')
        binarized = np.array(fh["Features0"]) >= self.probthreshold
        blobs = measure.label(binarized, connectivity=1)
        blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
        blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
        binarized[blobs == 0] = 0
        self.segmentviewer = napari.Viewer()
        self.segmentviewer.add_image(binarized, name="Segmentation", blending="additive", colormap="red",
                                     contrast_limits=[0, 1])
        del binarized
        gc.collect()
        if self.mergenucmarkers[iteration]:
            self.segmentviewer.add_image(nucimg[0, :, :], name="Merged Nuclear Markers", blending="additive")
        if self.mergememmarkers[iteration]:
            self.segmentviewer.add_image(memimg[0, :, :], name="Merged Membrane Markers", blending="additive")

        # Find names of images to populate dropdown.
        names = []
        for i in range(len(self.filenames)):
            names.append(self.filenames[i].split("/")[-1])

        # Allow user to toggle between images.
        @magicgui(auto_call=True, image={"choices": names, "label": ""})
        def change_image_segmentgui(image: str):
            self.currentimagenum = names.index(image)
            segmented = np.array(fh[f"Features{self.currentimagenum}"]) >= self.probthreshold
            blobs = measure.label(segmented, connectivity=1)
            blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
            blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
            segmented[blobs == 0] = 0
            self.segmentviewer.layers["Segmentation"].data = segmented
            if self.mergenucmarkers[iteration]:
                self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
            if self.mergememmarkers[iteration]:
                self.segmentviewer.layers["Merged Membrane Markers"].data = memimg[self.currentimagenum, :, :]

        # Apply filters for final segmented results.
        @magicgui(call_button="Finish")
        def finish_segmentgui() -> Image:
            self.viewer.status = "Segmentation Completed"
            numCellsList = []
            cortabs = []

            # Allow user to decide whether to add the labeled and/or colored image.
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return

            # Allow user to define wither to quantify using mean expression, or root-mean-square.
            quantmode = GUIUtils.QuantificationMode()
            quantmode.exec()
            if not quantmode.OK:
                return

            for i in range(self.numimgs):
                # FInd cells within threshold values set by the user.
                xcrop = self.maximageshape[0]
                ycrop = self.maximageshape[1]
                blobs = np.array(fh[f"Features{i}"]) >= self.probthreshold
                blobs = measure.label(blobs[:xcrop, :ycrop], connectivity=1)
                blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
                blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
                expandobject = objectmodels.expand_objects(objectimg=blobs, numiterations=round(0.284 / self.res))
                expandobject = morphology.remove_small_objects(expandobject.astype(bool), min_size=int(self.minsize),
                                                               in_place=True)

                # Label the segmented images and save to output folder.
                s = self.imageshapelist[i]
                expandobject, objectcount = measure.label(expandobject, connectivity=1, return_num=True)
                expandobject = expandobject.astype(np.uint32)
                outfilename = "Segmented_" + os.path.split(self.filenames[i])[-1].split(".")[0] + ".tif"
                tifffile.imwrite(os.path.join(dir, outfilename), expandobject[:s[0], :s[1]])
                self.objectplots.append(expandobject)

                # Store quantified expression values for each cell in an array.
                proptab = np.zeros((self.nummarkers + 4, objectcount))
                for ch in range(self.nummarkers):
                    data = self.viewer.layers[ch].data[i, :expandobject.shape[0], :expandobject.shape[1]]
                    if not quantmode.avg:
                        data = data.astype(np.uint16)
                        data = data * data
                    proptab[ch, :] = measure.regionprops_table(expandobject, data, properties=['mean_intensity'])[
                        'mean_intensity']
                    if not quantmode.avg:
                        proptab[ch, :] = np.sqrt(proptab[ch, :])

                # Store quantified morphological values for each cell in the same array.
                intensityimg = copy.deepcopy(
                    self.viewer.layers[0].data[i, :expandobject.shape[0], :expandobject.shape[1]])
                proptab[self.nummarkers, :] = [prop.area for prop in
                                               measure.regionprops(expandobject, intensity_image=intensityimg)]
                proptab[self.nummarkers + 1, :] = [prop.eccentricity for prop in
                                                   measure.regionprops(expandobject, intensity_image=intensityimg)]
                proptab[self.nummarkers + 2, :] = [prop.perimeter for prop in
                                                   measure.regionprops(expandobject, intensity_image=intensityimg)]
                proptab[self.nummarkers + 3, :] = [prop.major_axis_length for prop in
                                                   measure.regionprops(expandobject, intensity_image=intensityimg)]

                # Store centroid coordinates and cell labels, and store full quantified tables in memory.
                cortab = [prop.centroid for prop in measure.regionprops(expandobject, intensity_image=intensityimg)]
                cortabs.append(cortab)
                labtab = [prop.label for prop in measure.regionprops(expandobject, intensity_image=intensityimg)]
                IMGMEAN = np.c_[np.asarray(labtab), proptab.T]
                numCellsList.append(IMGMEAN.shape[0])
                self.Qtab.append(IMGMEAN)

                # Create RGB-colored image for segmentation and save it to the output folder.
                rgbimage = (label2rgb(expandobject, image=None, colors=None, alpha=0.3, bg_label=0, bg_color=(0, 0, 0),
                                      image_alpha=1, kind='overlay') * 255).astype(np.uint8)
                cv.imwrite(os.path.join(dir, f"RGB_{i}.tif"), rgbimage[:, :, [2, 1, 0]])

                # Store min and max values for each of the cell markers and morphological parameters.
                minvals = []
                maxvals = []
                for j in range(IMGMEAN.shape[1] - 1):
                    minvals.append(np.min(IMGMEAN[:, j + 1]))
                    maxvals.append(np.max(IMGMEAN[:, j + 1]))
                self.cellindices.append(len(self.lowerboundslist))
                self.lowerboundslist.append(copy.deepcopy(minvals))
                self.upperboundslist.append(copy.deepcopy(maxvals))
                self.minvalssegment.append(copy.deepcopy(minvals))
                self.maxvalssegment.append(copy.deepcopy(maxvals))

                # Update dropdown menu for table widget.
                self.tableimagenames.append(f"(Segment [{self.segmentcount}]) - {self.filenames[i].split('/')[-1]}")
                self.tableimgcount += 1

                # Add the segmented image(s) to the main GUI viewer window.
                if i == 0:
                    expobj = np.zeros((1, self.maximageshape[0], self.maximageshape[1]), dtype=expandobject.dtype)
                    expobj[0, :expandobject.shape[0], :expandobject.shape[1]] = expandobject
                    rgbimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=rgbimage.dtype)
                    rgbimg[0, :rgbimage.shape[0], :rgbimage.shape[1], :] = rgbimage
                    if selectimagesadded.grey:
                        self.viewer.add_image(expobj, name=f"Labels {self.segmentcount + 1}", blending="additive",
                                              contrast_limits=[0, 1])
                    if selectimagesadded.color:
                        self.viewer.add_image(rgbimg, name=f"Segment {self.segmentcount + 1}", blending="additive")
                else:
                    expobj = np.zeros((1, self.maximageshape[0], self.maximageshape[1]), dtype=expandobject.dtype)
                    expobj[0, :expandobject.shape[0], :expandobject.shape[1]] = expandobject
                    rgbimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=rgbimage.dtype)
                    rgbimg[0, :rgbimage.shape[0], :rgbimage.shape[1], :] = rgbimage
                    if selectimagesadded.grey and selectimagesadded.color:
                        self.viewer.layers[-2].data = np.vstack((self.viewer.layers[-2].data, expobj))
                        self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, rgbimg))
                    elif selectimagesadded.grey:
                        self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, expobj))
                    elif selectimagesadded.color:
                        self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, rgbimg))

            # Set only the most recently-added image to visible.
            self.set_invisible(self.viewer)
            self.viewer.layers[-1].visible = True

            # Store cell coordinates.
            self.cortabs.append(cortabs)
            if 'None' in self.tableimagenames:
                self.tableimagenames.remove('None')

            # Keep track of the current order of cell IDs in the table. Default to increasing order.
            self.orders = []
            self.combcellnums = []
            for i in range(len(self.Qtab)):
                order = []
                for j in range(self.Qtab[i].shape[0]):
                    order.append(int(self.Qtab[i][j, 0] - 1))
                self.orders.append(order)
                self.combcellnums.append(order)

            # Save table to the output folder as a csv file.
            startindex = len(self.Qtab) - self.numimgs
            for i in range(self.numimgs):
                segmentedtable = pd.DataFrame(np.hstack([np.vstack(self.Qtab[i + startindex]), cortabs[i]]))
                segmentedtable.columns = np.hstack(
                    ["Label", self.markers, "Area", "Eccentricity", "Perimeter", "Major Axis", "y", "x"])
                segmentedtable.to_csv(os.path.join(dir, f"Segmentation_Table_{i + 1}.csv"))

            # Update any pertinent variables.
            self.objecttrainlist.append([])
            for i in range(len(self.Qtab)):
                self.currentlyselectedcells.append([])
            self.sorttableimages.data.choices = tuple(self.tableimagenames)
            self.sorttableimages.data.value = f"(Segment [{self.segmentcount}]) - {self.filenames[0].split('/')[-1]}"
            self.sorttableimages.reset_choices()
            self.segmentcount += 1
            self.objectimgnames.append(f"Segment {self.segmentcount}")

            # If this is the first table being generated, set upper and lower bounds consistent with first
            # segmented image.
            if not self.addedtable:
                self.lowerbounds = copy.deepcopy(self.minvalssegment[0])
                self.upperbounds = copy.deepcopy(self.maxvalssegment[0])
                self.update_table(self.Qtab[0][:, 1:], self.lowerbounds, self.upperbounds, len(self.Qtab[0]),
                                  self.Qtab[0][:, 0].astype(np.uint8).tolist())

            GUIUtils.log_actions(self.actionloggerpath,
                                 f"Segmented: RAPID+ ({segmentationmodel.modelindex}), Iteration ({iteration}), "
                                 f"Resolution ({self.res}), Prob ({self.probthreshold}), Min ({self.minsize}), "
                                 f"Max ({self.maxsize}), Avg ({quantmode.avg})")

            self.segmentviewer.window.qt_viewer.close()
            self.segmentviewer.window._qt_window.close()

        # Allow user to select maximum size for cells. Any cells above this are filtered out.
        @magicgui(auto_call=True,
                  threshold={"widget_type": "FloatSlider", "max": self.maxsize * 4, "label": "Maximum Size:"}, )
        def max_size_threshold_segmentgui(threshold: int = self.maxsize) -> Image:
            self.maxsize = round(threshold)
            segmented = np.array(fh[f"Features{self.currentimagenum}"]) >= self.probthreshold
            blobs = measure.label(segmented, connectivity=1)
            blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
            blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
            segmented[blobs == 0] = 0
            self.segmentviewer.layers["Segmentation"].data = segmented
            if self.mergenucmarkers[iteration]:
                self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
            if self.mergememmarkers[iteration]:
                self.segmentviewer.layers["Merged Membrane Markers"].data = memimg[self.currentimagenum, :, :]

        # Allow user to select minimum size for cells. Any cells below this are filtered out.
        @magicgui(auto_call=True,
                  threshold={"widget_type": "FloatSlider", "max": self.minsize * 10, "label": "Minimum Size:"}, )
        def min_size_threshold_segmentgui(threshold: int = self.minsize) -> Image:
            self.minsize = round(threshold)
            segmented = np.array(fh[f"Features{self.currentimagenum}"]) >= self.probthreshold
            blobs = measure.label(segmented, connectivity=1)
            blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
            blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
            segmented[blobs == 0] = 0
            self.segmentviewer.layers["Segmentation"].data = segmented
            if self.mergenucmarkers[iteration]:
                self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
            if self.mergememmarkers[iteration]:
                self.segmentviewer.layers["Merged Membrane Markers"].data = memimg[self.currentimagenum, :, :]

        # Allow user to set a minimum confidence value for segmentation.
        @magicgui(auto_call=True,
                  threshold={"widget_type": "FloatSlider", "max": 1, "label": "Probability Threshold:"}, )
        def prob_threshold_segmentgui(threshold: float = self.probthreshold) -> Image:
            self.probthreshold = round(threshold, 2)
            segmented = np.array(fh[f"Features{self.currentimagenum}"]) >= self.probthreshold
            blobs = measure.label(segmented, connectivity=1)
            blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
            blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
            segmented[blobs == 0] = 0
            self.segmentviewer.layers["Segmentation"].data = segmented
            if self.mergenucmarkers[iteration]:
                self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
            if self.mergememmarkers[iteration]:
                self.segmentviewer.layers["Merged Membrane Markers"].data = memimg[self.currentimagenum, :, :]

        # Add widgets to the segmentation popup window.
        segmentwidget = QWidget()
        segmentlayout = QGridLayout()
        segmentlayout.setSpacing(0)
        segmentlayout.setContentsMargins(0, 0, 0, 0)
        if self.numimgs > 1:
            changeimagegui = change_image_segmentgui.native
            changeimagegui.setToolTip("Choose a different image to edit")
            segmentlayout.addWidget(changeimagegui, 0, 0)
            reindex = 0
        else:
            reindex = 1
        probfiltergui = prob_threshold_segmentgui.native
        probfiltergui.setToolTip("Set probability threshold")
        segmentlayout.addWidget(probfiltergui, 0, 1 - reindex)
        minsizegui = min_size_threshold_segmentgui.native
        minsizegui.setToolTip("Set minimum size")
        segmentlayout.addWidget(minsizegui, 0, 2 - reindex)
        maxsizegui = max_size_threshold_segmentgui.native
        maxsizegui.setToolTip("Set maximum size")
        segmentlayout.addWidget(maxsizegui, 0, 3 - reindex)
        finishgui = finish_segmentgui.native
        finishgui.setToolTip("Finish")
        segmentlayout.addWidget(finishgui, 1, 1, 1, 2 - reindex)
        segmentwidget.setLayout(segmentlayout)
        self.segmentviewer.window.add_dock_widget(segmentwidget, area="bottom")

    def set_invisible(self, viewer):
        """
        Set all layers within a viewer window to become invisible.

        Args:
            viewer (napari.Viewer): Viewer window whose layers are to be set to invisible.
        """
        for le in range(len(viewer.layers)):
            if viewer.layers[le].visible:
                viewer.layers[le].visible = False

    def sort_table_image(self):
        """
        Populate the table according to the currently selected image and round of analysis, the parameter that it is
        sorted according to, and whether the user indicated for it to sort in ascending or descending order.
        """
        data = self.sorttableimages.data.value
        marker = self.sorttableimages.marker.value
        sort = self.sorttableimages.sort.value

        # Make sure analysis has been done and that there is a table to be displayed.
        if (self.segmentcount > 0 or self.pixeltraincount > 0) and not self.loadingenv:
            # Get the index of the round of analysis being displayed in the table.
            index = self.tableimagenames.index(data)

            # Keep track of the current round of analysis being displayed in the table.
            self.listindex = copy.deepcopy(index)

            # Retrieve current lower and upper bounds.
            self.lowerbounds = self.lowerboundslist[index]
            self.upperbounds = self.upperboundslist[index]

            # If displaying segmentation results.
            if index in self.cellindices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                self.mode = "Segmentation"
                self.index = self.cellindices.index(index)
                currentData = copy.deepcopy(self.Qtab[self.index])

                # Get the column being used to sort the table and sort the clusters according to user selection.
                m = self.columnheaders.index(marker)
                for i in range(len(self.Qtab)):
                    # Find the order by which to sort the cells in the table.
                    order = np.argsort(self.Qtab[i][:, m]).astype(np.int).tolist()
                    if sort == "▼":
                        order.reverse()
                    self.orders[i] = order

                    # Filter out cells that don't fall within the user-defined lower/upper bounds.
                    filtereddata = np.append(self.Qtab[i][order, 1:],
                                             np.expand_dims(np.arange(self.Qtab[i].shape[0]), 1), 1)
                    for chan in range(len(self.lowerbounds)):
                        filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(self.upperbounds[chan], 3))
                        filtereddata = filtereddata[filtermask]
                        filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(self.lowerbounds[chan], 3))
                        filtereddata = filtereddata[filtermask]
                    self.combcellnums[i] = [order[j] for j in filtereddata[:, -1].astype(np.int).tolist()]

                    # Get the cell indices to be used as the vertical header labels.
                    if i == self.index:
                        cellnumlabels = [int(self.Qtab[i][order[j], 0]) for j in
                                         filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the cells according to user selection and update the table accordingly.
                self.cellnums = self.combcellnums[self.index]
                displayData = currentData[self.cellnums, 1:]
                self.update_table(displayData, self.lowerbounds, self.upperbounds, currentData.shape[0],
                                  cellnumlabels)

            # If displaying object-based clustering results.
            elif index in self.objectclusterindices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                self.mode = "Object"
                self.index = self.objectclusterindices.index(index)
                currentdata = copy.deepcopy(self.objectdatalist[self.index])

                # Find any clusters for the current round of analysis that have at least one cell.
                clusters = []
                for i in range(len(currentdata)):
                    if currentdata[i, 0] != 0.0:
                        clusters.append(i)

                # One table for every image, plus an extra for the combined average if using more than one image.
                if self.numimgs == 1:
                    numtabs = 1
                else:
                    numtabs = self.numimgs + 1

                # Get the column being used to sort the table and sort the clusters according to user selection.
                m = self.columnheaders.index(marker)
                if m == 0:
                    self.order = np.arange(len(currentdata)).tolist()
                else:
                    self.order = np.argsort(currentdata[:, m]).astype(np.int).tolist()
                if sort == "▼":
                    self.order.reverse()

                # Filter out clusters that don't fall within the user-defined lower/upper bounds.
                filtereddata = currentdata[self.order, 1:]
                filtereddata = np.append(filtereddata, np.expand_dims(np.arange(len(self.order)), 1), 1)
                for chan in range(len(self.lowerbounds)):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(self.upperbounds[chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(self.lowerbounds[chan], 3))
                    filtereddata = filtereddata[filtermask]
                self.objectclusternums = [self.order[i] for i in filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the clusters according to user selection and update the table accordingly.
                displaydata = currentdata[self.objectclusternums, :]

                # Find names for the clusters for the round of clustering being displayed in the table.
                print(i)
                print(self.pixelbasedclusters)
                annotationindex = [j for j, n in enumerate(self.pixelbasedclusters) if not n][0]
                print(annotationindex)
                annotationindex = [i for i, n in enumerate(self.pixelbasedclusters) if not n][0]

                # Update the display table in the GUI.
                self.update_table(displaydata, self.lowerbounds, self.upperbounds, len(clusters),
                                  self.objectclusternums, headernames=self.annotatedclusters[annotationindex])

            # If displaying pixel-based clustering results.
            elif index in self.pixelclusterindices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                self.mode = "Pixel"
                self.index = self.pixelclusterindices.index(index)
                currentdata = copy.deepcopy(self.datalist[self.index])

                # Sort the clusters according to user selection.
                if marker in self.markers:
                    m = self.markers.index(marker) + 1
                    self.order = np.argsort(currentdata[:, m]).astype(np.int).tolist()
                else:
                    self.order = np.arange(len(currentdata)).tolist()
                if sort == "▼":
                    self.order.reverse()

                # Filter out clusters that don't fall within the user-defined lower/upper bounds.
                filtereddata = currentdata[self.order, 1:]
                filtereddata = np.append(filtereddata, np.expand_dims(np.arange(filtereddata.shape[0]), 1), 1)
                for chan in range(len(self.lowerbounds)):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(self.upperbounds[chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(self.lowerbounds[chan], 3))
                    filtereddata = filtereddata[filtermask]
                self.pixelclusternums = [self.order[i] for i in filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the clusters according to user selection and update the table accordingly.
                displaydata = currentdata[self.pixelclusternums, :]

                # Find names for the clusters for the round of clustering being displayed in the table.
                annotationindex = [i for i, n in enumerate(self.pixelbasedclusters) if n][0]

                # Update the display table in the GUI.
                self.update_table(displaydata, self.lowerbounds, self.upperbounds, currentdata.shape[0],
                                  self.pixelclusternums, headernames=self.annotatedclusters[annotationindex])

            GUIUtils.log_actions(self.actionloggerpath,
                                 f"Sorted Table: Data ({data}), Marker ({marker}), Sort ({sort})")

    def spatial_analysis(self):
        """
        Perform spatial codistribution analysis on a user-defined clustered image.
        """
        # Check that the user has performed at least one clustering algorithm.
        if len(self.pixelbasedclusters) == 0:
            GUIUtils.display_error_message("No clustering results found",
                                           "Spatial analysis can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been executed once, use that by default.
        if len(self.pixelbasedclusters) == 1:
            clusteringnum = 0
            ispixelcluster = self.pixelbasedclusters[0]

        # If clustering has been executed multiple times, allow user to select which one.
        else:
            selectclusteringround = GUIUtils.SelectClusteringRound(self.pixelbasedclusters)
            selectclusteringround.exec()
            if not selectclusteringround.OK:
                return
            clusteringnum = selectclusteringround.clusteringnum
            ispixelcluster = selectclusteringround.ispixelcluster

        # Retrieve the labeled cluster images for the selected round of clustering.
        if not ispixelcluster:
            grey = self.greyobjects[clusteringnum]
        else:
            grey = self.greypixels[clusteringnum]

        for i in range(len(grey)):
            if i == 0:
                rclusters = grey[i, :, :]
            else:
                rclusters = KNN.concat_images(rclusters, grey[i, :, :])

        ### TODO: Make default parameters intelligent.
        spatialparams = GUIUtils.SpatialParameters()
        spatialparams.exec()
        if not spatialparams.OK:
            return
        pval, tab = KNN.random_kdtree_single(rclusters, spatialparams.npix, spatialparams.nsim)
        for i in range(len(tab)):
            val = copy.deepcopy(tab[i, i])
            tab[i:, i] = tab[i:, i] - val
            tab[i, :i] = tab[i, :i] - val
        pd.DataFrame(tab).to_csv(self.outputfolder + "/FC.csv")

        tab += tab.transpose()
        tab = np.max(tab) - tab
        DataTab = pd.DataFrame(tab)

        tab2 = copy.deepcopy(tab)
        lowerrange = np.median(tab2) - np.min(tab2)
        upperrange = np.max(tab2) - np.median(tab2)
        ratio = lowerrange / upperrange
        tab2[tab2 > np.median(tab2)] = (tab2[tab2 > np.median(tab2)] - np.median(tab)) * ratio + np.median(tab)

        plt.figure(figsize=(40, 40))
        ClusterDend = sns.clustermap(DataTab, row_cluster=True, col_cluster=True, linewidth=0.05, center=np.median(tab),
                                     vmax=np.max(tab), vmin=0, yticklabels=DataTab.columns + 1,
                                     xticklabels=DataTab.columns + 1, cmap="RdBu_r")
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.show(block=False)
        plt.title("Spatial Analysis")
        plt.savefig(os.path.join(self.outputfolder, "Codistribution.png"), format="PNG", dpi=300)
        heatmap = imread(os.path.join(self.outputfolder, "Codistribution.png"))
        self.set_invisible(self.viewer)
        self.viewer.add_image(da.from_array(heatmap), name='Codistribution', blending="additive")

        DataTab = pd.DataFrame(tab2)
        plt.figure(figsize=(40, 40))
        ClusterDend = sns.clustermap(DataTab, row_cluster=True, col_cluster=True, linewidth=0.05,
                                     center=np.median(tab2),
                                     vmax=np.max(tab2), vmin=0, yticklabels=DataTab.columns + 1,
                                     xticklabels=DataTab.columns + 1, cmap="RdBu_r")
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.show(block=False)
        plt.title("Spatial Analysis")
        plt.savefig(os.path.join(self.outputfolder, "Codistribution.png"), format="PNG", dpi=300)
        heatmap = imread(os.path.join(self.outputfolder, "Codistribution.png"))
        self.set_invisible(self.viewer)
        self.viewer.add_image(da.from_array(heatmap), name='Codistribution', blending="additive")

        df = pd.DataFrame(pval)
        df.to_csv(self.outputfolder + "/Pval.csv")
        pval[pval < 0.00000001] = 255
        pval[pval < 0.000001] = 150
        pval[pval < 0.0001] = 75
        pval[pval < 0.05] = 25
        pval[pval < 25] = 0
        df_pval = pd.DataFrame(pval)
        df_pval.index.astype(str).str.replace(r"^", "RP-")
        df_pval.index = (["RP-" + str(i + 1) for i in df_pval.index])
        df_pval.columns = (["RP-" + str(i + 1) for i in df_pval.columns.values])
        df_pval.to_csv(self.outputfolder + "/PvalNorm.csv")
        GUIUtils.log_actions(self.actionloggerpath, f"Spatial Analysis: Cluster ({clusteringnum})")

    def subcluster(self):
        """
        Allow user to select an object-based cluster and clustering algorithm to further subdivide the chosen cluster.
        """
        # Determine which round of segmentation to use.
        imgindex = 0
        if len(self.objectimgnames) > 1:
            segmentedimage = GUIUtils.SelectSegmentedImage(self.objectimgnames)
            segmentedimage.exec()
            if not segmentedimage.OK:
                return
            imgindex = segmentedimage.imageindex

        # Determine which round of clustering to use.
        if len(self.objecttrainlist[imgindex]) > 1:
            iteration = GUIUtils.ObjectTrainIteration(len(self.objecttrainlist[imgindex]))
            iteration.exec()
            if not iteration.OK:
                return
            it = iteration.iteration
        elif len(self.objecttrainlist[imgindex]) == 1:
            it = 0
        else:
            GUIUtils.display_error_message("Must run clustering first",
                                           "Please run a clustering algorithm (\"Object Clustering\" or \"UMAP Annotation\") first")
            return

        # Select which cluster to sub-divide.
        it = self.objecttrainlist[imgindex][it]
        startindex = it * self.numimgs
        currentgreyimg = self.greyobjects[it]
        clusternums = [i + 1 for i in range(len(np.unique(currentgreyimg)) - 1)]
        selectcluster = GUIUtils.SubCluster(clusternums)
        selectcluster.exec()
        if not selectcluster.OK:
            return
        clusternum = selectcluster.cluster

        # Define which markers to use to train the sub-clustering algorithm.
        trainmarkers = GUIUtils.RAPIDObjectParams(self.markers)
        trainmarkers.exec()
        if not trainmarkers.OK:
            return

        # Retrieve the full segmented data table for the defined cluster and the number of cells from that
        # cluster in each image.
        numcellsperimage = []
        currentimage = []
        for i in range(self.numimgs):
            count = 0
            for j in range(len(self.Qtab[i + imgindex * self.numimgs])):
                if int(self.objectclusters[startindex + i][j]) == int(clusternum):
                    currentimage.append(self.Qtab[i + imgindex * self.numimgs][j, :])
                    count += 1
            numcellsperimage.append(copy.deepcopy(count))
        currentimage = np.vstack(currentimage)

        # Define the algorithm to be used to sub-divide the cluster.
        alg = GUIUtils.ClusteringAlgorithm(self.objectimgnames, subclustering=True)
        alg.exec()
        if not alg.OK:
            return

        # If using the RAPID algorithm for sub-clustering.
        if alg.alg == "RAPID":
            # Define the parameters used to train the model.
            setParams = GUIUtils.RAPIDObjectParameters(len(trainmarkers.markernums))
            setParams.exec()
            if not setParams.OK:
                return
            args = runRAPIDzarr.get_parameters()
            args.ncluster = int(setParams.nc)
            args.nit = int(setParams.nit)
            args.bs = int(setParams.bs)
            if setParams.mse == "True":
                args.mse = True
            else:
                args.mse = False
            args.lr = float(setParams.lr)
            args.phenograph = 'False'
            args.distance = 'YES'
            args.blankpercent = float(setParams.blankpercent)
            args.epoch = 1
            args.GUI = True

            # Initialize the model and train the algorithm.
            self.viewer.status = "Training RAPID..."
            torch.manual_seed(args.seed)
            np.random.seed(args.seed)
            torch.cuda.manual_seed(args.seed)
            model = RAPIDMixNet(dimension=len(trainmarkers.markernums), nummodules=5, mse=args.mse,
                                numclusters=args.ncluster)
            model.apply(weight_init)
            print(model)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                    weight_decay=0.01,
                                    amsgrad=False)
            self.train_object(model, currentimage[:, trainmarkers.markernums], optimizer, args)
            GUIUtils.log_actions(self.actionloggerpath, f"Sub-Clustering: Segmentation ({imgindex}), Clustering ({it}),"
                                                        f" Cluster ({clusternum}), Markers ({trainmarkers.markernums}),"
                                                        f" Algorithm ({alg.alg}), Args ({setParams.nc}, {setParams.nit},"
                                                        f" {setParams.bs}, {args.mse}, {setParams.lr}, "
                                                        f"{setParams.blankpercent})")

        elif alg.alg == "Phenograph":
            # Define the parameters used for phenograph clustering.
            model = 0
            setParams = GUIUtils.PhenographParameters()
            setParams.exec()
            if not setParams.OK:
                return
            args = runRAPIDzarr.get_parameters()
            args.phenograph = 'True'
            args.PGdis = str(setParams.PGdis)
            args.PGnn = int(setParams.PGnn)
            args.PGres = float(setParams.PGres)
            args.GUI = True
            GUIUtils.log_actions(self.actionloggerpath, f"Sub-Clustering: Segmentation ({imgindex}), Clustering ({it}),"
                                                        f" Cluster ({clusternum}), Markers ({trainmarkers.markernums}),"
                                                        f" Algorithm ({alg.alg}), Args ({setParams.PGdis}, "
                                                        f"{setParams.PGnn}, {setParams.PGres})")

        elif alg.alg == "SciPy":
            model = 0
            setParams = GUIUtils.SciPyParameters()
            setParams.exec()
            if not setParams.OK:
                return
            args = runRAPIDzarr.get_parameters()
            args.phenograph = 'False'
            args.RAPID = 'False'
            args.normalize = setParams.normalize
            args.scipyalgo = setParams.scipyalgo
            args.scipyargs = setParams.scipyargs
            args.scipykwarg = setParams.scipykwarg
            args.GUI = True
            pca = setParams.pca
            GUIUtils.log_actions(self.actionloggerpath, f"Sub-Clustering: Segmentation ({imgindex}), Clustering ({it}),"
                                                        f" Cluster ({clusternum}), Markers ({trainmarkers.markernums}),"
                                                        f" Algorithm ({alg.alg}), Args ({setParams.normalize}, "
                                                        f"{setParams.scipyalgo}, {setParams.scipyargs}, "
                                                        f"{setParams.scipykwarg}, {pca})")

        else:
            model = 0
            try:
                hf = zarr.open("/".join(alg.dirpath[:-1]), 'r')
                # self.objectmodelloaded = hf.attrs['RAPIDObject']
                # self.pixelmodelloaded = False
                loadedargs = hf.attrs['arg']
            except:
                return
            loadoptions = GUIUtils.LoadModelOptions()
            loadoptions.exec()
            if not loadoptions.OK:
                return
            continuetraining = not loadoptions.prediction
            args = Namespace(**loadedargs)
            norm = GUIUtils.LoadModelNormalize(False)
            norm.exec()
            if not norm.OK:
                return
            args.normalize = norm.normalize
            pca = norm.pca
            if continuetraining:
                setParams = GUIUtils.RAPIDObjectTrainLoadedParameters(args)
                setParams.exec()
                if not setParams.OK:
                    return
                args.nit = int(setParams.nit)
                args.bs = int(setParams.bs)
                args.lr = float(setParams.lr)
                args.phenograph = 'False'
                args.distance = 'YES'
                args.blankpercent = float(setParams.blankpercent)
                args.epoch = 1
                args.GUI = True
                GUIUtils.log_actions(self.actionloggerpath,
                                     f"Sub-Clustering: Segmentation ({imgindex}), Clustering ({it}),"
                                     f" Cluster ({clusternum}), Continue Training ({continuetraining}),"
                                     f" Markers ({trainmarkers.markernums}), Algorithm ({alg.alg}),"
                                     f" Args ({norm.normalize}, {pca}, {setParams.nit},"
                                     f" {setParams.bs}, {setParams.lr}, {setParams.blankpercent})")
            else:
                GUIUtils.log_actions(self.actionloggerpath,
                                     f"Sub-Clustering: Segmentation ({imgindex}), Clustering ({it}),"
                                     f" Cluster ({clusternum}), Continue Training ({continuetraining}),"
                                     f" Markers ({trainmarkers.markernums}), Algorithm ({alg.alg}),"
                                     f" Args ({norm.normalize}, {pca})")

        pd.DataFrame(currentimage).to_csv(os.path.join(self.outputfolder, "Dataframe.csv"))
        self.viewer.status = "Performing clustering..."
        self.set_invisible(self.viewer)
        print("Current Image Shape:", currentimage.shape)
        self.test_object_subcluster(model, currentimage, args, [i + 1 for i in range(len(self.markers) + 4)],
                                    numcellsperimage, it, clusternum, imgindex * self.numimgs, startindex,
                                    trainmarkers.markernums)
        self.viewer.status = "RAPID subclustering complete"

    def test_object(self, model, quantifiedvals, args, markerindices, createcolorimg, creategreyimg, startind=0,
                    optimizer="", outputpath="", predict=False):
        """
        Apply a clustering algorithm to segmented results.

        Args:
            model (RAPID.network.f): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            args (Namespace): Additional user-defined parameters used for training.
            markerindices (list): List of ints corresponding to the indices of the markers being used for clustering.
            createcolorimg (bool): True if generating an RGB-colored image, otherwise False.
            creategreyimg (bool): True if generating a grey labeled image, otherwise False.
            startind (int, optional): Index value of the table for the first image being clustered on.
            optimizer (torch.optim.AdamW, optional): Initialized optimizer to be used for training (Default: "").
            outputpath (str, optional): Path to the folder where the model will be saved (Default: "").
            predict (bool, optional): True if the model is only being used to predict and no further training, otherwise False (Default: False).
        """

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.manual_seed(args.seed)
        np.random.seed(args.seed)
        torch.cuda.manual_seed(args.seed)
        if device == "cuda":
            torch.set_deterministic(True)
            torch.backends.cudnn.deterministic = True
        mergemarkerlist = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        complete_tab = []
        qtabindices = [0]
        for ind in markerindices:
            qtabindices.append(ind)
        for tab_len in range(self.numimgs):
            complete_tab.append(self.Qtab[tab_len + startind][:, qtabindices])
        complete_tab = np.vstack(complete_tab)
        complete_tab_DF = pd.DataFrame(complete_tab)
        complete_tab_DF.columns = np.hstack(["Label", mergemarkerlist])
        complete_tab_DF.to_csv(os.path.join(outputpath, "FullObject_segmentation_data.csv"))
        fulltab = copy.deepcopy(complete_tab_DF)
        imgid = []
        for i in range(self.numimgs):
            imgid.append(np.repeat(i, self.Qtab[i + startind].shape[0]))
        if args.phenograph == 'True':
            os.chdir(self.outputfolder)
            if args.normalize:
                numcells = 0
                for i in range(self.numimgs):
                    numcells += self.Qtab[i + startind].shape[0]
                currentImage = np.zeros((numcells, len(markerindices)))
                count = 0
                for i in range(self.numimgs):
                    currentImage[count:count + self.Qtab[i + startind].shape[0], :] = self.Qtab[i + startind][:,
                                                                                      markerindices]
                    count += self.Qtab[i + startind].shape[0]
                afternorm = np.zeros_like(complete_tab_DF.values[:, 1:])
                scaler = MinMaxScaler()

                scaler.fit(complete_tab_DF.values[:, 1:])
                afternorm[:, :] = scaler.transform(complete_tab_DF.values[:, 1:])
                phenopgraphin = afternorm
                print("Normalizing again, please check this param")
            else:
                phenopgraphin = complete_tab_DF.values[:, 1:]
            to_values, graph, Q = phenograph.cluster(phenopgraphin, n_jobs=1, clustering_algo=str(args.graphalgo),
                                                     resolution_parameter=float(args.PGres), k=int(args.PGnn),
                                                     primary_metric=str(args.PGdis))

        elif args.phenograph == 'False' and args.RAPID == 'False':
            import sklearn.cluster as cluster
            print(args.scipyalgo)
            import json
            if args.scipyalgo == "KMeans":
                algo = cluster.KMeans
            if args.scipyalgo == "AffinityPropagation":
                algo = cluster.AffinityPropagation
            if args.scipyalgo == "SpectralClustering":
                algo = cluster.SpectralClustering
            if args.scipyalgo == "AgglomerativeClustering":
                algo = cluster.AgglomerativeClustering
            if args.scipyalgo == "DBSCAN":
                algo = cluster.DBSCAN
            if args.scipyalgo == "HDBSCAN":
                import hdbscan
                algo = hdbscan.HDBSCAN
            print(json.loads(str(args.scipykwarg)))
            to_values = algo(**json.loads(args.scipykwarg)).fit_predict(complete_tab_DF.values[:, 1:])

        else:
            model.eval()
            with torch.no_grad():
                testdata = copy.deepcopy(quantifiedvals)
                TESTPATCHPRED = testdata.reshape((-1, testdata.shape[1]))
                to_values = np.zeros((TESTPATCHPRED.shape[0]))
                for BSTART in range(0, TESTPATCHPRED.shape[0], 50000):
                    x = torch.from_numpy(TESTPATCHPRED[BSTART:BSTART + (50000), :]).float().to(device)
                    outputs, AA = model(torch.unsqueeze(x, 1))
                    to_values[BSTART:BSTART + (50000)] = outputs[0].argmax(dim=1).cpu()
            if not predict:
                checkpoint = {'model': RAPIDMixNet(dimension=len(markerindices), nummodules=5, mse=args.mse,
                                                   numclusters=int(args.ncluster)),
                              'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict()}
                torch.save(checkpoint, os.path.join(outputpath, 'checkpoint.pth'))

        vals = list(copy.deepcopy(np.unique(to_values)))
        for i in range(len(to_values)):
            to_values[i] = vals.index(to_values[i]) + 1
        relabeled_table = copy.deepcopy(complete_tab)
        relabeled_table[:, 0] = to_values
        fulltab.insert(1, "Cluster", to_values)
        cord = np.vstack(self.cortabs[int(startind / self.numimgs)])
        fulltab.insert(1, "ImgID", np.hstack(imgid))
        fulltab.insert(1, "Y", cord[:, 1])
        fulltab.insert(1, "X", cord[:, 0])
        self.tabdata.append(fulltab)
        fulltab.to_csv(os.path.join(outputpath, "FullObject_segmentation_dataCluster.csv"))
        # relabledimages = np.zeros((self.numimgs, self.objectplots[0].shape[0], self.objectplots[0].shape[1], 3), dtype=np.uint8)
        relabledgreyimages = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)
        color = generate_colormap(len(np.unique(to_values)) + 1)
        self.objectcolor.append(color)
        np.save(os.path.join(outputpath, "color.npy"), color)
        data = []
        startindex = 0
        for i in range(self.numimgs):
            emptytab = np.zeros((len(np.unique(to_values)), relabeled_table.shape[1] + 2))
            from_values = complete_tab_DF['Label'].values[startindex:startindex + len(self.Qtab[i + startind])]
            tmp_to_values = to_values[startindex:startindex + len(self.Qtab[i + startind])]
            self.objectclusters.append(copy.deepcopy(tmp_to_values))
            relabeled = self.method_searchsort(from_values, tmp_to_values,
                                               self.objectplots[i + startind].flatten().astype(int))
            relabledgreyimages[i, :self.objectplots[i + startind].shape[0],
            :self.objectplots[i + startind].shape[1]] = (
                relabeled.reshape(self.objectplots[i + startind].shape)).astype(np.uint8)
            relabledgreyimages[i, :self.objectplots[i + startind].shape[0], :self.objectplots[i + startind].shape[1]][
                self.objectplots[i + startind] == 0] = 0
            cv.imwrite(os.path.join(outputpath, f"RELABELED_Grey{i}.png"),
                       relabledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1)
            relabledimages = np.zeros((self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
            for j in range(len(vals)):
                relabledimages[:, :, 0][relabledgreyimages[i, :, :] == j + 1] = color[j][0]
                relabledimages[:, :, 1][relabledgreyimages[i, :, :] == j + 1] = color[j][1]
                relabledimages[:, :, 2][relabledgreyimages[i, :, :] == j + 1] = color[j][2]
            tifffile.imwrite(os.path.join(outputpath, f"RELABELED_{i}.tif"),
                             relabledimages[:self.imageshapelist[i][0], :self.imageshapelist[i][1], :])

            if i == 0:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabledimages.dtype)
                relab[0, :relabledimages.shape[0], :relabledimages.shape[1], :] = relabledimages
                if creategreyimg:
                    self.viewer.add_image(relabledgreyimages[i, :, :],
                                          name=f"Object Cluster IDs {self.objecttraincount + 1}", blending="additive",
                                          contrast_limits=(0, np.max(relabledgreyimages)))
                if createcolorimg:
                    self.viewer.add_image(relab, name=f"Object Clusters {self.objecttraincount + 1}",
                                          blending="additive")
            else:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabledimages.dtype)
                relab[0, :relabledimages.shape[0], :relabledimages.shape[1], :] = relabledimages
                if creategreyimg and createcolorimg:
                    self.viewer.layers[-2].data = np.stack((self.viewer.layers[-2].data, relabledgreyimages[i, :, :]),
                                                           0)
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))
                elif creategreyimg:
                    self.viewer.layers[-1].data = np.stack((self.viewer.layers[-1].data, relabledgreyimages[i, :, :]),
                                                           0)
                elif createcolorimg:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))

            del relabledimages
            gc.collect()
            tmp_tab = relabeled_table[startindex:startindex + len(self.Qtab[i + startind])]
            tmp_tab_df = pd.DataFrame(tmp_tab)
            startindex += len(self.Qtab[i + startind])
            grouped = tmp_tab_df.groupby(0)
            tabres = grouped.apply(np.mean)
            tabres.insert(0, "Sample", i)
            _, counts = np.unique(tmp_tab[:, 0], return_counts=True)
            tabres.insert(2, "Cells", counts)
            StandardScaler().fit_transform(tabres.values[:, 3:])
            scaler = MinMaxScaler()
            scaler.fit(StandardScaler().fit_transform(tabres.values[:, 3:]))
            min_max_normdata = scaler.transform(StandardScaler().fit_transform(tabres.values[:, 3:]))
            # Cutoff the overflowing (>1) of values
            min_max_normdata[min_max_normdata > 1] = 1
            emptytab[np.unique(tmp_to_values.astype(np.uint8) - 1), :] = tabres.values
            data.append(emptytab.astype(np.float))
            self.objectdatalist.append(emptytab[:, 2:].astype(np.float))
            minvals = []
            maxvals = []
            tab = emptytab[np.unique(tmp_to_values.astype(np.uint8) - 1), 2:]
            for j in range(tab.shape[1] - 1):
                minvals.append(np.min(tab[:, j + 1]))
                maxvals.append(np.max(tab[:, j + 1]))
            self.minvalsobject.append(copy.deepcopy(minvals))
            self.maxvalsobject.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
        data = np.nan_to_num((np.vstack(data)))
        my_data = pd.DataFrame(np.nan_to_num(data))
        ''' Find weighted average data '''
        if self.numimgs > 1:
            weighted_average = np.zeros((len(np.unique(to_values)), data.shape[1] - 2))
            for i in range(data.shape[0]):
                currcluster = i % weighted_average.shape[0]
                weighted_average[currcluster, 0] += data[i, 2]
            for i in range(data.shape[0]):
                currcluster = i % weighted_average.shape[0]
                weighted_average[currcluster, 1:] += data[i, 3:] * data[i, 2] / weighted_average[currcluster, 0]
            self.objectdatalist.append(weighted_average)
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            self.minvalsobject.append(copy.deepcopy(minvals))
            self.maxvalsobject.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
        unique = list(np.unique(relabledgreyimages))
        for i in range(len(unique)):
            relabledgreyimages[relabledgreyimages == unique[i]] = i
        self.greyobjects.append(relabledgreyimages)
        del relabledgreyimages
        gc.collect()
        my_data.columns = np.hstack([["Sample", "Cluster", "Pixels"], mergemarkerlist])
        my_data.to_csv(os.path.join(outputpath, "RAPIDObject_cluster_table.csv"))
        tabledata, my_data_scaled, DistMatrix, uniqueClusters = \
            prep_for_mst(clustertable=my_data, minnumpixels=1, outfolder=outputpath, includedmarkers=mergemarkerlist)
        generate_mst(distancematrix=DistMatrix, normalizeddf=my_data_scaled[my_data_scaled.columns], colors=color,
                     randomseed=0, outfolder=outputpath, displaymarkers=mergemarkerlist, uniqueclusters=uniqueClusters,
                     samplenames=list(np.unique(my_data['Sample'])), displaysingle=False)

    ### TODO: Do we need markernames variable?
    def test_object_subcluster(self, model, quantifiedvals, args, markernames, numcellsperimage, iteration, clusternum,
                               startind, objectclustersstartindex, markerindices):
        """
        Apply a clustering algorithm to a specified cluster from an image that has already been passed through an object
        clustering algorithm.

        Args:
            model (RAPID.network.RAPIDMixNet): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            args (Namespace): Additional user-defined parameters used for training.
            markernames (list): List of names of markers that are being used for clustering.
            numcellsperimage (list): List of the number of cells that are in each image.
            iteration (int): Index for the round of clustering being subclustered.
            clusternum (int): Index for the cluster that is being subclustered.
            startind (int, optional): Index value of the table for the first image being clustered on.
            objectclustersstartindex (int): Index for the table corresponding to the first object clustering round being subclustered.
            markerindices (list): List of indices of each of the cell markers included in the table.
        """

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.manual_seed(args.seed)
        np.random.seed(args.seed)
        torch.cuda.manual_seed(args.seed)
        clusterimg = quantifiedvals[:, markerindices]
        cellslist = quantifiedvals[:, 0]
        quantifiedvals = quantifiedvals[:, 1:]
        if args.phenograph == 'True':
            os.chdir(self.outputfolder)
            if args.normalize:
                for ch in range(clusterimg.shape[1]):
                    tmpData = clusterimg[:, ch]
                    lowpercentile = np.percentile(clusterimg[clusterimg[:, ch] > 0], 1)
                    toppercentile = np.percentile(clusterimg[clusterimg[:, ch] > 0], 99)
                    tmpData[tmpData <= lowpercentile] = lowpercentile
                    tmpData[tmpData >= toppercentile] = toppercentile
                    tmpData = (tmpData - lowpercentile) / (toppercentile - lowpercentile)
                    clusterimg[:, ch] = tmpData
            to_values, graph, Q = phenograph.cluster(clusterimg, n_jobs=1,
                                                     resolution_parameter=float(args.PGres), k=int(args.PGnn),
                                                     primary_metric=str(args.PGdis))

        elif args.phenograph == 'False' and args.RAPID == 'False':
            import sklearn.cluster as cluster
            print(args.scipyalgo)
            import json
            if args.scipyalgo == "KMeans":
                algo = cluster.KMeans
            if args.scipyalgo == "AffinityPropagation":
                algo = cluster.AffinityPropagation
            if args.scipyalgo == "SpectralClustering":
                algo = cluster.SpectralClustering
            if args.scipyalgo == "AgglomerativeClustering":
                algo = cluster.AgglomerativeClustering
            if args.scipyalgo == "DBSCAN":
                algo = cluster.DBSCAN
            if args.scipyalgo == "HDBSCAN":
                import hdbscan
                algo = hdbscan.HDBSCAN
            print(json.loads(str(args.scipykwarg)))
            to_values = algo(**json.loads(args.scipykwarg)).fit_predict(clusterimg)

        else:
            model.eval()
            with torch.no_grad():
                TESTPATCHPRED = clusterimg.reshape((-1, clusterimg.shape[1]))
                to_values = np.zeros((TESTPATCHPRED.shape[0]))
                for BSTART in range(0, TESTPATCHPRED.shape[0], 50000):
                    x = torch.from_numpy(TESTPATCHPRED[BSTART:BSTART + (50000), :]).float().to(device)
                    outputs, AA = model(torch.unsqueeze(x, 1))
                    to_values[BSTART:BSTART + (50000)] = outputs[0].argmax(dim=1).cpu()

        relabeled_table = np.hstack((to_values.reshape((len(to_values), 1)), quantifiedvals))

        startindex = 0
        images = []
        for i in range(len(numcellsperimage)):
            if numcellsperimage[i] != 0:
                images.append(i)
        data = np.zeros((len(images), len(np.unique(to_values)), len(markernames) + 1))
        c = np.zeros((len(images), len(np.unique(to_values))))
        for i in range(len(images)):
            tmp_tab = relabeled_table[startindex:startindex + numcellsperimage[images[i]]]
            startindex += numcellsperimage[images[i]]
            tmp_tab_df = pd.DataFrame(tmp_tab)
            grouped = tmp_tab_df.groupby(0)
            tabres = grouped.apply(np.mean)
            unique, counts = np.unique(tmp_tab[:, 0], return_counts=True)
            count = 0
            for j in range(len(np.unique(to_values))):
                if j in unique:
                    c[i, j] = counts[count]
                    count += 1
                else:
                    c[i, j] = 0
            data[i, [int(j) for j in unique], :] = tabres.values
        numtabs = 1
        if self.numimgs > 1:
            numtabs += self.numimgs
        it = iteration * numtabs
        for i in range(numtabs):
            indices = [j for j in range(len(self.objectdatalist[it + i]))]
            indices.remove(clusternum - 1)
            ''' Find weighted average data '''
            weighted_average = np.zeros((len(np.unique(to_values)), len(markernames) + 1))
            for j in range(len(np.unique(to_values))):
                weighted_average[j, 0] = np.sum(np.array(c[:, j]))
                weighted_average[j, 1:] = np.average(data[:, j, 1:], axis=0, weights=c[:, j])
            newtable = np.zeros(
                (len(self.objectdatalist[it + i]) - 1 + len(np.unique(to_values)), len(markernames) + 1))
            newtable[:len(self.objectdatalist[it + i]) - 1, :] = copy.deepcopy(self.objectdatalist[it + i])[indices, :]
            newtable[len(self.objectdatalist[it + i]) - 1:, :] = weighted_average
            self.objectdatalist[it + i] = newtable
            minvals = []
            maxvals = []
            for j in range(newtable.shape[1] - 1):
                minvals.append(np.min(newtable[:, j + 1]))
                maxvals.append(np.max(newtable[:, j + 1]))
            self.minvalsobject[it + i] = copy.deepcopy(minvals)
            self.maxvalsobject[it + i] = copy.deepcopy(maxvals)
            self.lowerboundslist[self.objectclusterindices[iteration]] = copy.deepcopy(minvals)
            self.upperboundslist[self.objectclusterindices[iteration]] = copy.deepcopy(maxvals)
            # self.objecttrainmarkers[it+i] = markerlist
            if self.mode == "Object" and self.index == it + i:
                self.update_table(newtable, minvals, maxvals, len(newtable))
                self.objectclusternums = [j for j in range(len(newtable))]
        self.currentlyselectedobjectclusters[iteration] = []
        self.greyobjects[iteration] = copy.deepcopy(self.greyobjects[iteration])
        self.greyobjects[iteration][self.greyobjects[iteration] == clusternum] = 0
        self.greyobjects[iteration][self.greyobjects[iteration] > clusternum] = self.greyobjects[iteration][
                                                                                    self.greyobjects[
                                                                                        iteration] > clusternum] - 1
        newstart = copy.deepcopy(np.max(self.greyobjects[iteration])) + 1
        count = 0
        counter = 0
        tabdata = self.tabdata[iteration]
        for i in range(self.numimgs):
            updated_to_values = np.array(self.objectclusters[objectclustersstartindex + i])
            updated_to_values[updated_to_values == clusternum] = -1
            updated_to_values[updated_to_values > clusternum] = updated_to_values[updated_to_values > clusternum] - 1
            segmentedimg = self.objectplots[i + startind]
            currentgreyimg = self.greyobjects[iteration][i, :, :]
            for j in range(numcellsperimage[i]):
                currentcell = int(cellslist[count])
                currentgreyimg[segmentedimg == currentcell] = int(to_values[count] + newstart)
                updated_to_values[currentcell - 1] = int(to_values[count] + newstart)
                count += 1
            self.objectclusters[objectclustersstartindex + i] = list(updated_to_values)
            self.greyobjects[iteration][i, :, :] = currentgreyimg
            tabdata['Cluster'][counter:counter + len(list(updated_to_values))] = list(updated_to_values)
            counter += len(list(updated_to_values))
        self.tabdata[iteration] = tabdata
        # self.greyobjects[iteration] = grey
        # self.viewer.add_image(self.greyobjects[iteration], name='Re-Clustered nums', blending="additive", contrast_limits=(0, np.max(grey)))
        colorimg = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)

        colors = self.objectcolor[iteration]
        colors = np.append(colors, colors[[clusternum - 1], :], 0)
        colors = np.delete(colors, clusternum - 1, 0)
        newcolors = generate_colormap(len(np.unique(self.greyobjects[iteration])))
        while len(colors) < len(np.unique(self.greyobjects[iteration])):
            if not newcolors[0, :].tolist() in colors.tolist():
                colors = np.append(colors, newcolors[[0], :], 0)
            newcolors = newcolors[1:, :]
        self.objectcolor[iteration] = colors

        for i in range(len(np.unique(self.greyobjects[iteration]))):
            colorimg[:, :, :, 0][self.greyobjects[iteration] == i + 1] = colors[i][0]
            colorimg[:, :, :, 1][self.greyobjects[iteration] == i + 1] = colors[i][1]
            colorimg[:, :, :, 2][self.greyobjects[iteration] == i + 1] = colors[i][2]
        self.viewer.add_image(colorimg, name='Re-Clustered', blending="additive", contrast_limits=(0, 255))

    def toggle_visibility(self):
        """
        If any layers are currently visible, set all layers invisible. Otherwise, set all layers to be visible.
        """
        if self.count_visible_layers() > 0:
            for i in range(len(self.viewer.layers)):
                self.viewer.layers[i].visible = False
        else:
            for i in range(len(self.viewer.layers)):
                self.viewer.layers[i].visible = True
        GUIUtils.log_actions(self.actionloggerpath, "Toggled Visibility")

    def train_object(self, model, quantifiedvals, optimizer, args):
        """
        Train the RAPID-O clustering model.

        Args:
            model (RAPID.network.RAPIDMixNet): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            optimizer (torch.optim.AdamW): Initialized optimizer to be used for training.
            args (Namespace): Additional user-defined parameters used for training.
        """

        bs = args.bs
        numiterations = args.nit
        model.train()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        lossAvg = 0
        loss_fn = nn.MSELoss()
        for batch_idx in range(0, numiterations):
            dataTrain = quantifiedvals
            RANDINDEX = np.random.randint(0, len(quantifiedvals), size=bs)
            data = np.squeeze(dataTrain[RANDINDEX, :])
            NZ = np.ones_like(data.reshape(-1))
            NZ[0:int(len(NZ) * args.blankpercent)] = 0
            np.random.shuffle(NZ)
            NZ = NZ.reshape(data.shape)
            optimizer.zero_grad()
            HOWMANY = 1
            for REP in range(HOWMANY):
                RAWData = dataTrain[RANDINDEX, :]
                RAWData = RAWData * NZ
                RAWData = torch.from_numpy(RAWData).float().to(device)
                output, AA = model(torch.unsqueeze(RAWData, 1))
                NOISE = np.random.normal(loc=0, scale=1, size=dataTrain[RANDINDEX, :].shape).astype(np.float32)
                NOISEADD = dataTrain[RANDINDEX, :] / 80
                NOISE = NOISE * NOISEADD
                newdata = dataTrain[RANDINDEX, :] + NOISE
                newdata = newdata * NZ
                data_perturb = torch.from_numpy(newdata).float().to(device)
                output_alt, BB = model(torch.unsqueeze(data_perturb, 1))
                CLUS = output[0].argmax(dim=1).detach().cpu().numpy()
                if args.distance is not None:
                    COR = runRAPIDzarr.clustercosinedistancetorch(dataTrain[RANDINDEX, :], CLUS)
                if REP == 0:
                    loss1 = torch.sum(torch.stack([IID_loss.IID_loss(o, o_perturb) for o, o_perturb in
                                                   zip(output, output_alt)])).mean()
                else:
                    TMP = loss1.clone()
                    loss1 = TMP + torch.sum(torch.stack(
                        [IID_loss.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                         zip(output, output_alt, AA, AA)])).mean()
                if args.mse:
                    MSE = loss_fn(torch.unsqueeze(RAWData, 1), AA)
                    loss1 += MSE + COR
                else:
                    loss1 += COR
            loss1.backward()
            optimizer.step()
            lossAvg = lossAvg + loss1.item()
            if batch_idx % 1 == 0:
                print(
                    'Train Epoch {} -iteration {}/{} - LR {:.6f} -\ttotal loss: {:.6f} -\t IIC loss: {:.3f}-\t MSE:{:.3f}'.format(
                        0, batch_idx, numiterations, 10, (lossAvg / 10), loss1, COR))
                lossAvg = 0

    def update_table(self, datavals, lowerbounds, upperbounds, numclasses, order=[], headernames=[]):
        """
        Apply both lower- and upper-bound thresholds to an image array.

        Args:
            datavals (numpy.ndarray): Array containing the data values being represented in the table.
            lowerbounds (list): List of lower bounds for the values in each column in the table.
            upperbounds (list): List of upper bounds for the values in each column in the table.
            numclasses (int): Total number of cells/clusters for the image corresponding to the table.
            order (list, optional): List containing the indices corresponding to the cells/clusters that are included in the table, and in the correct order (Default: []).
            headernames (list, optional): List containing the annotated cluster names, if applicable (Default: []).
        """

        numrows = datavals.shape[0]
        numcols = datavals.shape[1]
        vals = []
        for i in range(numrows + 3):
            vals.append(None)
        data = {'': vals}
        params = ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        for i in range(numcols):
            if self.mode == "Segmentation":
                if i < numcols - 4:
                    key = str(self.viewer.layers[self.markers[i]])
                else:
                    key = params[i + 4 - numcols]
            elif self.mode == "Object":
                if i == 0:
                    key = "# Cells"
                else:
                    # key = self.objecttrainmarkers[self.index][i-1]
                    keys = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
                    key = keys[i - 1]
            elif self.mode == "Pixel":
                if i == 0:
                    key = "# Pixels"
                else:
                    # key = str(self.pixelmarkers[self.index][i-1])
                    # key = str(self.markers[i-1])
                    numtabs = 1
                    if self.numimgs > 1:
                        numtabs += self.numimgs
                    ind = self.index // numtabs
                    key = str(self.pixelclustermarkers[ind][i - 1])
            values = [None, None, None]
            rvals = datavals[:, i]
            for j in rvals:
                values.append(j)
            data[key] = values
        df = pd.DataFrame(data=data)
        df.replace(to_replace=[None], value=np.nan, inplace=True)
        df.fillna(0)
        df.columns = data.keys()
        data = df.to_dict()
        count = 0
        for key in data.keys():
            if key != '' and key != '# Cells' and key != '# Pixels' and key != 'Cluster #':
                print(key)
                data[key][0] = lowerbounds[count]
                data[key][1] = upperbounds[count]
                count += 1
        try:
            self.tablewidget.hide()
        except:
            print("")
        self.create_table(data)
        if self.mode == "Segmentation":
            if len(order) > 0:
                self.verticalheaderlabels = np.asarray(
                    [f"{numrows}/{numclasses}"] + [""] + [""] + [f"Cell {int(i)}" for i in order]).astype(np.str)
            else:
                self.verticalheaderlabels = np.asarray(np.asarray(
                    [f"{numrows}/{numclasses}"] + [""] + [""] + [f"Cell {int(i) + 1}" for i in range(numrows)]).astype(
                    np.str))
        else:
            if headernames != []:
                labels = [headernames[i] for i in order]
                self.verticalheaderlabels = np.asarray([f"{numrows}/{numclasses}"] + [""] + [""] + labels).astype(
                    np.str)
            elif len(order) > 0:
                self.verticalheaderlabels = np.asarray(np.asarray(
                    [f"{numrows}/{numclasses}"] + [""] + [""] + [f"Cluster {int(i) + 1}" for i in order]).astype(
                    np.str))
            else:
                self.verticalheaderlabels = np.asarray(np.asarray(
                    [f"{numrows}/{numclasses}"] + [""] + [""] + [f"Cluster {int(i) + 1}" for i in
                                                                 range(numrows)]).astype(np.str))
                self.order = []
                for i in range(numrows):
                    self.order.append(i)
        self.tablewidget.setVerticalHeaderLabels(self.verticalheaderlabels)

        self.addwhenchecked = False
        if len(order) > 0:
            order = [int(i) for i in order]
            counter = 3
            for a in order:
                if self.mode == "Segmentation":
                    if a in self.currentlyselectedcells[self.index]:
                        self.tablewidget.item(counter, 0).setCheckState(QtCore.Qt.Checked)
                else:
                    if self.numimgs == 1:
                        trainnum = self.index
                    else:
                        trainnum = self.index // (self.numimgs + 1)
                    if self.mode == "Object":
                        selclusters = self.currentlyselectedobjectclusters[trainnum]
                    elif self.mode == "Pixel":
                        selclusters = self.currentlyselectedpixelclusters[trainnum]
                    if a in selclusters:
                        self.tablewidget.item(counter, 0).setCheckState(QtCore.Qt.Checked)
                    else:
                        self.tablewidget.item(counter, 0).setCheckState(QtCore.Qt.Unchecked)
                counter += 1
        self.addwhenchecked = True
        self.tablewidget.verticalHeader().setFont(QFont("Helvetica", pointSize=12))
        self.tablewidget.horizontalHeader().setFont(QFont("Helvetica", pointSize=12))
        vstrings = [self.tablewidget.verticalHeaderItem(i).text() for i in range(self.tablewidget.rowCount())]
        vwidth = GUIUtils.font_width("Helvetica", 12, vstrings)
        self.tablewidget.verticalHeader().setMinimumWidth(vwidth + 15)
        hstrings = [self.tablewidget.horizontalHeaderItem(i).text() for i in range(self.tablewidget.columnCount())]
        hwidth = GUIUtils.font_width("Helvetica", 12, hstrings)
        self.tablewidget.horizontalHeader().setMinimumWidth(hwidth + 15)
        self.tablewidget.horizontalHeader().setMinimumHeight(self.tablewidget.rowHeight(0))
        if self.addedtable:
            self.viewer.window.remove_dock_widget(self.viewer.window._qt_window.findChildren(QDockWidget)[-1])
        self.viewer.window.add_dock_widget(self.tablewidget, area="top", name="Table")
        self.addedtable = True
        self.fulltab = pd.DataFrame(data).fillna(0)
        self.fulltab.insert(0, "Labels", vstrings)

        self.datavals = datavals
        self.numclasses = numclasses
        self.tableorder = order

    def testGUI(self):
        """
        Function containing magicgui elements, where the napari window gets populated with RAPID-specific widgets.
        """
        with napari.gui_qt():
            self.viewer = napari.Viewer()
            self.viewer.window.file_menu.clear()
            self.viewer.layers.move_selected = lambda a, b: print()

            @magicgui(call_button="Biaxial gating")
            def biaxial_gate_gui() -> Image:
                self.biaxial_gate()

            @magicgui(call_button="Display Selected")
            def display_selected_cells_gui() -> Image:
                self.display_selected_cells()

            @magicgui(call_button="UMAP")
            def display_umap_gui() -> Image:
                self.display_umap()

            ### TODO: Loading previous edits assumes the same number of images and markers
            @magicgui(call_button="Edit Image")
            def edit_image_gui() -> Image:
                self.edit_image()

            @magicgui(call_button="Filter Table")
            def filter_table_gui() -> Image:
                self.filter_table()

            @magicgui(call_button="MST")
            def generate_mst_gui():
                self.generate_mst()

            @magicgui(call_button="Nearest Neighbours")
            def generate_nn_gui() -> Image:
                self.generate_nn()

            @magicgui(call_button="Load Clusters")
            def load_object_clusters_gui() -> Image:
                self.load_object_clusters()

            @magicgui(call_button="UMAP Annotation")
            def manual_annotation_gui() -> Image:
                self.manual_annotation()

            ### TODO: Automate the metaclustering?
            @magicgui(call_button="Merge Clusters")
            def merge_clusters_gui() -> Image:
                self.merge_clusters()

            @magicgui(call_button="Merge Markers")
            def merge_mem_gui() -> Image:
                self.merge_markers()

            @magicgui(call_button="Object Clustering")
            def object_clustering_gui():
                self.object_clustering()

            @magicgui(call_button="Quantify Region")
            def quantify_region_gui():
                self.quantify_region()

            @magicgui(call_button="Reset Metadata")
            def reset_metadata_gui() -> Image:
                self.reset_metadata()

            @magicgui(call_button="Segment")
            def segment_gui() -> Image:
                self.segment()

            @magicgui(auto_call=True,
                      data={"choices": self.tableimagenames, "label": "Display data:  "},
                      marker={"choices": self.columnheaders, "label": "Parameter:        "},
                      sort={"choices": ["▲", "▼"], "label": "Order:         "})
            def sort_table_image_gui(data: str, marker: str, sort: str) -> Image:
                self.sort_table_image()

            @magicgui(call_button="Sub-Cluster")
            def subcluster_gui() -> Image:
                self.subcluster()

            @magicgui(call_button="Spatial Analysis")
            def spatial_analysis_gui():
                self.spatial_analysis()

            @magicgui(call_button="Pixel Clustering")
            def pixel_clustering_gui():
                self.pixel_clustering()

            @magicgui(call_button="Toggle Visibility")
            def toggle_visibility_gui() -> Image:
                self.toggle_visibility()

            layerswidget = QWidget()
            layerswidgetlayout = QGridLayout()
            layerswidgetlayout.setSpacing(0)
            layerswidgetlayout.setContentsMargins(0, 0, 0, 0)
            layerswidgetlabel = QLabel("Image visualization")
            layerswidgetlabel.setAlignment(Qt.AlignCenter)
            layerswidgetlayout.addWidget(layerswidgetlabel, 0, 0)
            editimagewidget = edit_image_gui.native
            editimagewidget.setToolTip("Apply edits to the raw image")
            layerswidgetlayout.addWidget(editimagewidget, 1, 0)
            togglevisibilitywidget = toggle_visibility_gui.native
            togglevisibilitywidget.setToolTip("Toggle visibility of all layers")
            layerswidgetlayout.addWidget(togglevisibilitywidget, 2, 0)
            resetmetadatawidget = reset_metadata_gui.native
            resetmetadatawidget.setToolTip("Reset the metadata for all of the layers")
            layerswidgetlayout.addWidget(resetmetadatawidget, 3, 0)
            layerswidget.setLayout(layerswidgetlayout)
            layerswidget.setToolTip("This module includes functions that manipulate the layers")
            self.viewer.window.add_dock_widget(layerswidget, name="Data visibility", area="bottom")

            clusteringwidget = QWidget()
            clusteringlayout = QGridLayout()
            clusteringlayout.setSpacing(0)
            clusteringlayout.setContentsMargins(0, 0, 0, 0)
            clusteringlabelwidget = QLabel("Pixel-based analysis")
            clusteringlabelwidget.setAlignment(Qt.AlignCenter)
            clusteringlayout.addWidget(clusteringlabelwidget, 0, 0)
            trainrapidwidget = pixel_clustering_gui.native
            trainrapidwidget.setToolTip("Classify each pixel in the image into different clusters")
            clusteringlayout.addWidget(trainrapidwidget, 1, 0)
            emptylabelwidget = QLabel("")
            emptylabelwidget.setAlignment(Qt.AlignCenter)
            clusteringlayout.addWidget(emptylabelwidget, 2, 0, 2, 1)
            clusteringwidget.setLayout(clusteringlayout)
            clusteringwidget.setToolTip("This module includes functions that are specific to pixel-based analysis")
            self.viewer.window.add_dock_widget(clusteringwidget, name="Pixel-based pipeline", area="bottom")

            objectBasedWidget = QWidget()
            objectBasedLayout = QGridLayout()
            objectBasedLayout.setSpacing(0)
            objectBasedLayout.setContentsMargins(0, 0, 0, 0)
            objectlabelwidget = QLabel("Object-based pipeline")
            objectlabelwidget.setAlignment(Qt.AlignCenter)
            objectBasedLayout.addWidget(objectlabelwidget, 0, 0, 1, 3)
            mergememwidget = merge_mem_gui.native
            mergememwidget.setToolTip("Select the cell markers that you would like to define the membranes")
            objectBasedLayout.addWidget(mergememwidget, 1, 0)
            segmentwidget = segment_gui.native
            segmentwidget.setToolTip(
                "Segment the cells according to the membranes defined in the \"Merged Membranes\" layer")
            objectBasedLayout.addWidget(segmentwidget, 1, 1)
            trainobjectwidget = object_clustering_gui.native
            trainobjectwidget.setToolTip("Classify the segmented cells into different clusters")
            objectBasedLayout.addWidget(trainobjectwidget, 1, 2)
            biaxialwidget = biaxial_gate_gui.native
            biaxialwidget.setToolTip("Generate a biaxial plot from the segmented cells")
            objectBasedLayout.addWidget(biaxialwidget, 2, 0)
            umapwidget = display_umap_gui.native
            umapwidget.setToolTip("Generate a UMAP from the segmented cells")
            objectBasedLayout.addWidget(umapwidget, 2, 1)
            displayselectedwidget = display_selected_cells_gui.native
            displayselectedwidget.setToolTip(
                "Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(displayselectedwidget, 2, 2)
            nngui = generate_nn_gui.native
            nngui.setToolTip("Run a nearest neighbor analysis based on spatial distributions of cells in clusters")
            objectBasedLayout.addWidget(nngui, 3, 0)
            manualannotationwidget = manual_annotation_gui.native
            manualannotationwidget.setToolTip(
                "Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(manualannotationwidget, 3, 1)
            loadclusterswidget = load_object_clusters_gui.native
            loadclusterswidget.setToolTip("Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(loadclusterswidget, 3, 2)
            objectBasedWidget.setLayout(objectBasedLayout)
            objectBasedWidget.setToolTip("This module includes functions that are specific to object-based analysis")
            self.viewer.window.add_dock_widget(objectBasedWidget, name="Object-based pipeline", area="bottom")

            analysisWidget = QWidget()
            analysisLayout = QGridLayout()
            analysisLayout.setSpacing(0)
            analysisLayout.setContentsMargins(0, 0, 0, 0)
            analysislabelwidget = QLabel("Downstream analysis")
            analysislabelwidget.setAlignment(Qt.AlignCenter)
            analysisLayout.addWidget(analysislabelwidget, 0, 0, 1, 2)
            spatialgui = spatial_analysis_gui.native
            spatialgui.setToolTip(
                "Generate a heatmap according to the relative spatial codistribution of each pair of clusters")
            analysisLayout.addWidget(spatialgui, 1, 0)
            mstgui = generate_mst_gui.native
            mstgui.setToolTip(
                "Generate a minimum spanning tree based on relative expression profiles of the clusters in the current table")
            analysisLayout.addWidget(mstgui, 1, 1)
            mergeclusterswidget = merge_clusters_gui.native
            mergeclusterswidget.setToolTip("Merge together all clusters that are selected in the table")
            analysisLayout.addWidget(mergeclusterswidget, 2, 0)
            quantifyregionwidget = quantify_region_gui.native
            quantifyregionwidget.setToolTip(
                "Acquire average cell marker expression information for given regions of the image")
            analysisLayout.addWidget(quantifyregionwidget, 2, 1)
            subclusterwidget = subcluster_gui.native
            subclusterwidget.setToolTip("Divide a given cluster into subclusters")
            analysisLayout.addWidget(subclusterwidget, 3, 0)
            filtertablegui = filter_table_gui.native
            filtertablegui.setToolTip("Set filters for markers in the table")
            analysisLayout.addWidget(filtertablegui, 3, 1)
            analysisWidget.setLayout(analysisLayout)
            analysisWidget.setToolTip(
                "This module includes functions that can be used for either pixel- or object-bnased analysis")
            self.viewer.window.add_dock_widget(analysisWidget, name="Downstream analysis", area="bottom")

            self.tablesortwidget = QWidget()
            tablelayout = QGridLayout()
            tablelayout.setSpacing(0)
            tablelayout.setContentsMargins(0, 0, 0, 0)
            analysislabelwidget = QLabel("Table sort")
            analysislabelwidget.setAlignment(Qt.AlignCenter)
            tablelayout.addWidget(analysislabelwidget, 0, 0)
            self.sorttableimages = sort_table_image_gui
            self.sorttableimages.native.setToolTip("Sort the visible elements in the table")
            tablelayout.addWidget(self.sorttableimages.native, 1, 0)
            self.tablesortwidget.setLayout(tablelayout)
            self.tablesortwidget.setToolTip(
                "This module includes functions that can dictate the displayed data in the table")
            self.viewer.window.add_dock_widget(self.tablesortwidget, name="Table sort", area="bottom")

            while True:
                outputfolder = GUIUtils.OutFolder()
                outputfolder.exec()
                if outputfolder.OK:
                    if outputfolder.loadseg:
                        segmentationpath = self.load_segmentation_results()
                        if segmentationpath:
                            self.actionloggerpath = GUIUtils.create_new_folder("ActionLogs", self.outputfolder)
                            GUIUtils.log_actions(self.actionloggerpath, f"Loaded segmentation: {segmentationpath}")
                            break
                    elif outputfolder.loadenv:
                        envpath = self.load_environment()
                        if envpath:
                            self.actionloggerpath = GUIUtils.create_new_folder("ActionLogs", self.outputfolder)
                            GUIUtils.log_actions(self.actionloggerpath, f"Loaded environment: {envpath}")
                            break
                    elif outputfolder.loadpixel:
                        pixelpath = self.load_pixel_results()
                        if not pixelpath == "":
                            self.actionloggerpath = GUIUtils.create_new_folder("ActionLogs", self.outputfolder)
                            GUIUtils.log_actions(self.actionloggerpath, f"Loaded pixel results: {pixelpath}")
                            break
                    else:
                        dialog = QFileDialog()
                        outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
                        if outputfolder != "":
                            self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
                            self.actionloggerpath = GUIUtils.create_new_folder("ActionLogs", self.outputfolder)
                            GUIUtils.log_actions(self.actionloggerpath, "Opened")
                            break
                else:
                    self.viewer.window.close()
                    self.viewer.close()
                    return

            openimgs = QAction('Open File(s)', self.viewer.window._qt_window)
            openimgs.setShortcut('Ctrl+O')
            openimgs.setStatusTip('Open file(s)')
            openimgs.triggered.connect(self.open_images)

            savedata = QAction('Save Data', self.viewer.window._qt_window)
            savedata.setShortcut('Ctrl+S')
            savedata.setStatusTip('Save Data')
            savedata.triggered.connect(self.save_data)

            ### TODO: Add other functionalities for this (new table entries for combined average within groups?).
            group = QAction('Sample grouping', self.viewer.window._qt_window)
            group.setShortcut('Ctrl+G')
            group.setStatusTip('Sample grouping')
            group.triggered.connect(self.sample_group)

            saveenv = QAction('Save Environment', self.viewer.window._qt_window)
            saveenv.setShortcut('Ctrl+Shift+S')
            saveenv.setStatusTip('Save Environment')
            saveenv.triggered.connect(self.save_environment)

            cmgroup = QAction('Set colormap', self.viewer.window._qt_window)
            cmgroup.setShortcut('Ctrl+Shift+C')
            cmgroup.setStatusTip('Set colormap for clusters')
            cmgroup.triggered.connect(self.colormap_group)

            rename = QAction('Rename clusters', self.viewer.window._qt_window)
            rename.setShortcut('Ctrl+R')
            rename.setStatusTip('Change names of clusters')
            rename.triggered.connect(self.rename_clusters)

            opendocs = QAction('Open documentation', self.viewer.window._qt_window)
            opendocs.setShortcut('Ctrl+D')
            opendocs.setStatusTip('Open documentation')
            opendocs.triggered.connect(self.open_docs)

            changefolder = QAction('Change output folder', self.viewer.window._qt_window)
            changefolder.setStatusTip('Change output folder')
            changefolder.triggered.connect(self.change_folder)

            self.viewer.window.file_menu.addAction(openimgs)
            self.viewer.window.file_menu.addAction(savedata)
            self.viewer.window.file_menu.addAction(group)
            self.viewer.window.file_menu.addAction(saveenv)
            self.viewer.window.file_menu.addAction(cmgroup)
            self.viewer.window.file_menu.addAction(rename)
            self.viewer.window.file_menu.addAction(changefolder)
            self.viewer.window.help_menu.addAction(opendocs)


def run_rapid_gui():
    gui = RAPIDGUI()
    gui.testGUI()


if __name__ == '__main__':
    try:
        run_rapid_gui()
    except Exception as ex:
        print(ex)
