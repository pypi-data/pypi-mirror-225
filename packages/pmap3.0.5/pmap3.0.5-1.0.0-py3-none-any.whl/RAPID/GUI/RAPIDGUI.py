from argparse import Namespace
import ast
import configparser
import copy
from dask import array as da
import gc
import gdown
import glob
from imageio.v2 import imread
import io
from magicgui import magicgui
import matplotlib
from matplotlib import patches, pyplot as plt
from matplotlib.path import Path

matplotlib.use("Agg")
import napari
from napari_bioformats import napari_get_reader
from napari.layers import Image
from napari.utils.progress import progress
import networkx as nx
import numpy as np
from numpy import math, unicode
import os
import pandas as pd
from pandas import DataFrame
from PIL import Image
import phenograph
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import RAPID.GUI.GUIUtils as GUIUtils
from RAPID.Impressionist import runRAPIDzarr
from RAPID.network import objectmodels, IID_loss
from RAPID.network.model import load_checkpoint, weight_init, RAPIDMixNet
from RAPID.spatialanalysis import KNN
from RAPID.util.utils import generate_colormap, denoise_img, preprocess, save_preprocess, run_pca
from RAPID.util.mst import prep_for_mst, generate_mst
import re
from scipy import ndimage as ndi, ndimage
from scipy.spatial import distance
import seaborn as sns
import shutil
from shutil import copyfile
from skimage import img_as_ubyte, measure, morphology
from skimage.color import label2rgb
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import stat
import tifffile
import torch
from torch import optim
import torch.nn as nn
import umap
import vaex
import vaex.ml
from vispy.color import ColorArray, Colormap
import webbrowser
import zarr

path = os.path.dirname(os.path.abspath(__file__)) + "/../models/ModelDenoise_UnetPlus40.pt"
if not os.path.exists(path):
    gdown.download("https://drive.google.com/uc?id=1aYBi0oKbJq-bjYBPc6DxhRl8cjMU8O4d", path, verify=False)
gc.enable()


### TODO: Add to documentation.
### TODO: Segmented images save as binary and re-label later?
### TODO: Add error messages on Jupyter.

class RAPIDGUI():
    """
    Class containing all functions available in the RAPID GUI, as well as core functions/attributes.
    """

    def __init__(self):
        self.addwhenchecked = True
        self.hasaddedtable = False
        self.haseditedimage = False
        self.hasloadedpixel = False
        self.hasloadedimage = False
        self.isloadingenv = False
        self.updatelogfile = False

        self.actionloggerpath = ""
        self.analysisindex = 0
        self.analysismode = ""
        self.biaxialcount = 1
        self.displayselectedcount = 1
        self.editimagepath = ""
        self.numimgs = 0
        self.nummarkers = 0
        self.objectclustercount = 0
        self.pixelclustercount = 0
        self.resolution = 0
        self.segmentcount = 0
        self.selectedregioncount = 1
        self.tableimgcount = 0
        self.tableindex = 0
        self.totalnumrows = 0
        self.umapcount = 1

        self.analysislog = []
        self.cellclustervals = []
        self.cellcoordinates = []
        self.clusternames = []
        self.clustersarepixelbased = []
        self.currentlyselected = []
        self.currenttableordersfiltered = []
        self.currenttableorderfull = []
        self.currenttabdata = np.array([])
        self.currentverticalheaderlabels = np.array([])
        self.datalist = []
        self.editactions = []
        self.filenames = []
        self.fulltab = pd.DataFrame()
        self.groupslist = []
        self.groupsnames = ['Individual']
        self.histogramcounts = []
        self.imageisflipped = []
        self.imageshapelist = []
        self.labeledimgs = []
        self.lowerboundslist = []
        self.markers = []
        self.maximageshape = np.array([])
        self.maxpixelclustervals = []
        self.maxvals = []
        self.mergedimagespaths = []
        self.mergememmarkers = []
        self.mergenucmarkers = []
        self.minvals = []
        self.objectclustercolors = []
        self.objectclusterdfs = []
        self.objectclusterdirectories = []
        self.objectclusterindices = []
        self.objectimgnames = []
        self.pixelclustercolors = []
        self.pixelclusterdirectories = []
        self.pixelclusterindices = []
        self.pixelclustermarkers = []
        self.plotcoordinates = []
        self.plotisumap = []
        self.plotsegmentationindices = []
        self.plotxmins = []
        self.plotxmaxs = []
        self.plotymins = []
        self.plotymaxs = []
        self.segmentationclusteringrounds = []
        self.segmentationindices = []
        self.segmentationzarrpaths = []
        self.segmentcounts = []
        self.tableimagenames = ['None']
        self.tableorder = []
        self.tableparams = ['ID']
        self.totalnumcells = []
        self.upperboundslist = []

    def apply_clusters_defined_patches(self,
                                       patchesstart,
                                       isloadingmodel,
                                       outfolder,
                                       modelparams,
                                       markerindices,
                                       markernames,
                                       modelpath,
                                       addgreyimg,
                                       addcolorimg,
                                       ):
        """
        Perform pixel-based clustering on user-defined patches.

        Args:
            patchesstart (list): List of vertices defining top-left corner for each 64x64 patch, for each image.
            isloadingmodel (bool): If True, load pre-trained model weights. Otherwise, use random weight initialization.
            outfolder (str): Path to the folder where results will be saved.
            modelparams (iterable): List of parameters for the desired clustering algorithm.
            markerindices (list): List of indices of cell markers to be considered for clustering.
            markernames (list): List of names of cell markers to be considered for clustering.
            modelpath (str): Path to pretrained model, if loading a model.
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """

        # Prompt user to define parameters.
        args = runRAPIDzarr.get_parameters()

        # Find the number of patches across all the images.
        args.npatches = 0
        for img in patchesstart:
            args.npatches += len(img)

        if isloadingmodel:
            params = GUIUtils.RAPIDTrainLoadedParams(args, israndompatches=False)
            args.rfold = "/".join(modelpath[:-1])
            copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(outfolder, "checkpoint.pth"))
            args.loadmodel = True
        else:
            maximgshape = np.insert(self.maximageshape, 0, self.nummarkers)
            params = GUIUtils.RAPIDPixelParameters(len(markerindices), maximgshape, israndompatches=False)
            args.rfold = self.outputfolder
            args.loadmodel = False

        if modelparams == []:
            params.exec()
            if not params.OK:
                return
            args.ncluster = int(params.nc)
            args.nit = int(params.nit)
            args.bs = int(params.bs)
            args.mse = params.mse == "True"
            args.rescalefactor = float(params.RCN)
            args.lr = float(params.lr)
            args.SCANloss = params.SCAN
            args.rescale = params.RC == "True"
            denoise = params.denoise
            normalize = params.normalize
            modelparams = [args.ncluster, args.nit, args.bs, args.mse, args.rescalefactor, args.lr, args.SCANloss,
                           args.rescale, denoise, normalize]
        else:
            args.ncluster, args.nit, args.bs, args.mse, args.rescalefactor, \
            args.lr, args.SCANloss, args.rescale, denoise, normalize = modelparams
        args.normalize, args.normalizeall, args.normtype, args.pca = GUIUtils.pixel_normtype(normalize)

        # Normalize data for RAPID input.
        self.viewer.status = "Generating RAPID data..."
        self.generate_RAPID_data(markerindices,
                                 markernames,
                                 os.path.join(outfolder, "RAPID_Data"),
                                 denoise,
                                 args.normalize,
                                 args.normalizeall,
                                 args.normtype,
                                 args.pca,
                                 )

        # Update parameters and save them to the output folder.
        hf = zarr.open(os.path.join(outfolder, "RAPID_Data"), mode='r+')
        args.nchannels = hf["data"].shape[1]
        args.distance = True
        args.predict = False
        args.patchsize = 64
        args.epoch = 1
        args.GUI = True
        args.testbs = 20000
        if not self.hasaddedtable:
            self.analysismode = "Pixel"
        if not os.path.exists(args.rfold):
            os.mkdir(args.rfold)
            args.rfold = args.rfold + "/"
        else:
            args.rfold = args.rfold + "/"
        hf.attrs['arg'] = vars(args)

        # Train RAPID algorithm.
        self.viewer.status = "Training RAPID..."
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.viewer.window._status_bar._toggle_activity_dock(True)
        grey, prob, tab, colors, _ = runRAPIDzarr.train_rapid(args,
                                                              device,
                                                              os.path.join(outfolder, "RAPID_Data"),
                                                              outfolder,
                                                              patchesstart,
                                                              )
        self.viewer.window._status_bar._toggle_activity_dock(False)

        # Reshape results into multi-channel image array.
        count = 0
        for i in range(self.numimgs):
            vdim = self.imageshapelist[i][0]
            hdim = self.imageshapelist[i][1]
            self.labeledimgs.append(GUIUtils.convert_dtype(grey[count: count + vdim * hdim].reshape(vdim, hdim)))
            count += vdim * hdim

        # Save colors to the output folder.
        if isloadingmodel:
            colors = np.load("/".join(modelpath[:-1]) + "/color.npy")
        np.save(os.path.join(outfolder, "color.npy"), colors)

        # Update any relevant variables and close the window.
        self.apply_pixel_clustering(tab.values, args, colors, addgreyimg, addcolorimg, outfolder)
        self.pixelclustercount += 1
        self.analysislog.append("P")
        return modelparams

    def apply_contrast_limits(self,
                              img,
                              contrast_limits,
                              ):
        """
        Apply both lower- and upper-bound thresholds to an image array.

        Args:
            img (numpy.ndarray): Array for image data having contrast limits applied to it.
            contrast_limits (iterable): List containing the lower and upper bound values for the contrast limits being applied.
        """
        lower = contrast_limits[0]
        upper = contrast_limits[1]
        img[img < lower] = lower
        img[img > upper] = upper
        img = (img - lower) / (upper - lower) * 255
        img[img < 0] = 0
        img[img > 255] = 255
        return img.astype(np.uint8)

    def apply_edits(self,
                    editactions,
                    imgindex=-1,
                    ):
        """
        Apply any changes made in the Edit Image popup window.

        Args:
            editactions (list): Sequence of edits to be made for each image.
            imgindex (int, optional): Index of image to apply edits to. If -1, apply across all images (Default: -1).
        """
        imgnums = [i for i in range(self.numimgs) if not i == imgindex]
        for i in range(self.nummarkers):
            for edits in editactions:
                for j in imgnums:
                    if edits[j][i] == "Gaussian":
                        self.viewer.layers[i].data[j, :, :] = ndimage.gaussian_filter(
                            self.viewer.layers[i].data[j, :, :], [1, 1])
                    elif edits[j][i] == "Median":
                        self.viewer.layers[i].data[j, :, :] = ndimage.median_filter(self.viewer.layers[i].data[j, :, :],
                                                                                    [1, 1])
                    elif len(edits[j][i]) == 2:
                        self.viewer.layers[i].data[j, :, :] = self.apply_contrast_limits(
                            self.viewer.layers[i].data[j, :, :], edits[j][i])
                if any([edits[j][i] == "Denoise" or edits[j][i] == "Binarize" for j in imgnums]):
                    denoiseimgnums = [j for j in imgnums if edits[j][i] == "Denoise" or edits[j][i] == "Binarize"]
                    self.viewer.layers[i].data[denoiseimgnums, :, :] = np.moveaxis(
                        denoise_img(np.moveaxis(self.viewer.layers[i].data[denoiseimgnums, :, :], 0, -1).astype(float)),
                        -1, 0)
                if any([edits[j][i] == "Binarize" for j in imgnums]):
                    binarizeimgnums = [j for j in imgnums if edits[j][i] == "Binarize"]
                    self.viewer.layers[i].data[binarizeimgnums, :, :][
                        self.viewer.layers[i].data[binarizeimgnums, :, :] > 0] = 255
            if not imgindex == -1:
                self.viewer.layers[i].data[imgindex, :, :] = self.edit_viewer.layers[i].data

    def apply_object_clustering(self,
                                clusterids,
                                tabindex,
                                segmentedtab,
                                outputpath,
                                addcolorimg,
                                addgreyimg,
                                labelnames,
                                ):
        """
        Apply object cluster labels to segmented images, add relabeled images to the viewer, and save relabeled images
        and data tables to output folder.

        Args:
            clusterids (numpy.ndarray): Array of cluster IDs for each cell across all images.
            tabindex (int): Index of first table for the selected round of segmentation being used for clustering.
            segmentedtab (numpy.ndarray): Array of average expression values for each cell across all images.
            outputpath (str): Path to folder where results will be saved.
            addcolorimg (bool): True if adding RGB-color images to the viewer, otherwise False.
            addgreyimg (bool): True if adding greyscale labeled images to the viewer, otherwise False.
            labelnames (list): List of names for each of the clusters if applicable.
        """

        paramslist = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        numclusters = len(np.unique(clusterids))

        vals = list(np.unique(clusterids))
        for i in range(len(clusterids)):
            clusterids[i] = vals.index(clusterids[i]) + 1

        # Save data table for segmented results with cluster assignments as well as image ID and (x,y)-coordinates.
        cord = np.vstack(self.cellcoordinates[int(tabindex / self.numimgs)])
        imgid = []
        for i in range(self.numimgs):
            imgid.append(np.repeat(i, len(self.datalist[self.segmentationindices[i + tabindex]])))
        segmentedtab_DF = pd.DataFrame(segmentedtab)
        segmentedtab_DF.columns = np.array(paramslist)
        segmentedtab_DF.insert(0, "Cluster", [str(val) for val in clusterids])
        segmentedtab_DF.insert(0, "ImgID", np.hstack(imgid))
        segmentedtab_DF.insert(0, "Y", cord[:, 1])
        segmentedtab_DF.insert(0, "X", cord[:, 0])
        segmentedtab_DF.to_csv(os.path.join(outputpath, "SegmentationClusterIDs.csv"))
        self.objectclusterdfs.append(segmentedtab_DF)

        # Insert cluster IDs to segmentation data table
        segmentedtab = np.insert(segmentedtab, 0, clusterids, axis=1)

        # Initialize image array to store cluster IDs for each pixel
        labelimg = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)

        # Initialize list of arrays containing mean cluster expression levels, sample and cluster IDs, and cell counts.
        data = []

        # Generate colors to map to each cluster ID
        color = generate_colormap(numclusters + 1)[:-1, :]
        self.objectclustercolors.append(color)
        np.save(os.path.join(outputpath, "color.npy"), color)

        # Retrieve segmentation results being used for clustering.
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][tabindex // self.numimgs] * self.numimgs
        for i in range(self.numimgs):
            # Get name of current image
            imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]

            # Number of cells in the current image.
            numcells = len(self.datalist[self.segmentationindices[i + tabindex]])

            # Cluster IDs for each of the cells in the current image.
            to_values = clusterids[:numcells]
            self.cellclustervals.append(to_values)

            # Save image with labeled cluster IDs.
            imgshape = (self.imageshapelist[i][0], self.imageshapelist[i][1])
            relabeled = self.method_searchsort(np.arange(1, 1 + numcells), to_values,
                                               self.labeledimgs[i + analysisnum].flatten().astype(int))
            labelimg[i, :imgshape[0], :imgshape[1]] = relabeled.reshape((imgshape[0], imgshape[1])).astype(np.uint8)
            labelimg[i, :imgshape[0], :imgshape[1]][self.labeledimgs[i + analysisnum] == 0] = 0
            GUIUtils.save_img(os.path.join(outputpath, f"ObjectClusterLabels_{imgname}.tif"),
                              labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1,
                              self.imageisflipped[i])

            # Save colored clustered image.
            rgbimg = np.zeros((self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
            for j in range(len(vals)):
                rgbimg[:, :, 0][labelimg[i, :, :] == j + 1] = color[j][0]
                rgbimg[:, :, 1][labelimg[i, :, :] == j + 1] = color[j][1]
                rgbimg[:, :, 2][labelimg[i, :, :] == j + 1] = color[j][2]
            GUIUtils.save_img(os.path.join(outputpath, f"ObjectClusters_{imgname}.tif"),
                              rgbimg[:self.imageshapelist[i][0], :self.imageshapelist[i][1], :],
                              self.imageisflipped[i])

            # Add images to the viewer.
            if addcolorimg:
                paddedrgbimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
                paddedrgbimg[0, :self.maximageshape[0], :self.maximageshape[1], :] = rgbimg

            if i == 0:
                if addgreyimg:
                    self.viewer.add_image(labelimg[[i], :, :],
                                          name=f"Object Cluster IDs {self.objectclustercount + 1}", blending="additive",
                                          contrast_limits=(0, np.max(labelimg)))
                if addcolorimg:
                    self.viewer.add_image(paddedrgbimg, name=f"Object Clusters {self.objectclustercount + 1}",
                                          blending="additive")
            else:
                if addgreyimg and addcolorimg:
                    self.viewer.layers[-2].data = np.vstack((self.viewer.layers[-2].data, labelimg[[i], :, :]))
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, paddedrgbimg))
                elif addgreyimg:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, labelimg[[i], :, :]))
                elif addcolorimg:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, paddedrgbimg))

            # Group cells with the same cluster ID and find mean expression values for each cluster.
            tabres = pd.DataFrame(segmentedtab[:numcells])
            tabres = tabres.groupby(0)
            tabres = tabres.apply(np.mean)
            tabres.insert(0, "Sample", i)
            _, counts = np.unique(to_values, return_counts=True)
            tabres.insert(2, "Cells", counts)
            datatab = np.zeros((numclusters, tabres.values.shape[1]))
            datatab[np.unique(to_values.astype(np.uint8) - 1), :] = tabres.values
            data.append(datatab)
            datatab = datatab[:, 2:]
            self.datalist.append(datatab)

            # Update variables.
            self.currenttableordersfiltered.append(list(range(len(np.unique(to_values)))))
            minvals = []
            maxvals = []
            uniqueclusters = np.unique(to_values.astype(np.uint8) - 1)
            for j in range(1, datatab.shape[1]):
                minvals.append(np.min(datatab[uniqueclusters, j]))
                maxvals.append(np.max(datatab[uniqueclusters, j]))
            self.minvals.append(copy.deepcopy(minvals))
            self.maxvals.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
            clusterids = clusterids[numcells:]
            segmentedtab = segmentedtab[numcells:]
        data = np.nan_to_num((np.vstack(data)))
        self.labeledimgs += [GUIUtils.convert_dtype(labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]])
                             for i in range(len(labelimg))]

        # Find weighted average data across all images and store min and max expression averages for each parameter.
        if self.numimgs > 1:
            weighted_average = np.zeros((numclusters, data.shape[1] - 2))
            for i in range(numclusters):
                clusterids = [i + j * numclusters for j in range(int(len(data) / numclusters))]
                weighted_average[i, 0] = np.sum(data[clusterids, 2])
                weighted_average[i, 1:] = np.average(data[clusterids, 3:], axis=0, weights=data[clusterids, 2])
            self.datalist.append(weighted_average)
            self.currenttableordersfiltered.append(list(range(len(weighted_average))))
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            self.minvals.append(copy.deepcopy(minvals))
            self.maxvals.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))

        # Save full clustered data table.
        data = pd.DataFrame(data)
        data.columns = np.hstack([["Sample", "Cluster", "# Cells"], paramslist])
        data.to_csv(os.path.join(outputpath, "ObjectClusterAvgExpressionVals.csv"))
        tabledata, my_data_scaled, distmatrix, uniqueclusters = prep_for_mst(clustertable=data,
                                                                             minclustersize=1,
                                                                             clustersizes=data["# Cells"],
                                                                             includedmarkers=paramslist,
                                                                             )
        generate_mst(distancematrix=distmatrix,
                     normalizeddf=my_data_scaled,
                     colors=color,
                     randomseed=0,
                     clusterheatmap=True,
                     outfolder=outputpath,
                     displaymarkers=paramslist,
                     uniqueclusters=uniqueclusters,
                     samplenames=list(np.unique(data['Sample'])),
                     displaysingle=False,
                     values="# Cells",
                     )

        self.viewer.add_image(imread(os.path.join(outputpath, "MeanExpressionHeatmap.png")),
                              name=f"Object Clusters {self.objectclustercount + 1} Heatmap",
                              blending="additive",
                              visible=False,
                              )

        # Update table sort module and other necessary variables.
        for i in range(self.numimgs):
            self.tableimagenames.append(
                f"Object Cluster {self.objectclustercount + 1} - {self.filenames[i].split('/')[-1]}")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
            self.currentlyselected.append([])
        if self.numimgs > 1:
            self.tableimagenames.append(f"Object Cluster {self.objectclustercount + 1} - Combined Average")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
            self.currentlyselected.append([])
        self.segmentationclusteringrounds[int(tabindex / self.numimgs)].append(self.objectclustercount)
        self.objectclustercount += 1
        self.analysislog.append("O")
        self.clustersarepixelbased.append(False)
        self.clusternames.append(labelnames)
        self.updatelogfile = False
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Object Cluster {self.objectclustercount} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        self.updatelogfile = True

    def apply_pixel_clustering(self,
                               tab,
                               args,
                               colors,
                               addgreyimg,
                               addcolorimg,
                               outfolder,
                               ):
        """
        Populate the viewer and the table with results from RAPID-P clustering.

        Args:
            tab (numpy.ndarray): Data being used to populate the table.
            args (Namespace): Additional user-defined parameters used for training.
            colors (numpy.ndarray): Array (#clusters x 3) of RGB values for each cluster.
            addgreyimg (bool): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't.
            addcolorimg (bool): If True, add RGB-colored segmented image to the viewer. Otherwise, don't.
            outfolder (str): Path to the folder where results will be saved.
        """
        if self.numimgs > 1:
            data = np.zeros((self.numimgs + 1, args.ncluster, tab.shape[1] - 2))
        else:
            data = np.zeros((self.numimgs, args.ncluster, tab.shape[1] - 2))
        for i in range(self.numimgs):
            data[i, :, :] = tab[args.ncluster * i:args.ncluster * (i + 1), 2:]
            self.tableimagenames.append(
                f"Pixel Cluster {self.pixelclustercount + 1} - {self.filenames[i].split('/')[-1]}")
            self.pixelclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
        if 'None' in self.tableimagenames:
            self.tableimagenames.remove('None')
        if self.numimgs > 1:
            self.tableimagenames.append(f"Pixel Cluster {self.pixelclustercount + 1} - Combined Average")
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
                self.minvals.append(copy.deepcopy(minvals))
                self.maxvals.append(copy.deepcopy(maxvals))
                self.lowerboundslist.append(copy.deepcopy(minvals))
                self.upperboundslist.append(copy.deepcopy(maxvals))
                self.currentlyselected.append([])
        elif self.numimgs == 1:
            minvals = []
            maxvals = []
            for j in range(data.shape[2] - 1):
                minvals.append(np.min(data[0, :, j + 1]))
                maxvals.append(np.max(data[0, :, j + 1]))
            self.minvals.append(copy.deepcopy(minvals))
            self.maxvals.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
            self.currentlyselected.append([])

        if not self.hasaddedtable:
            self.update_table(data[0, :, :],
                              self.lowerboundslist[self.tableindex],
                              self.upperboundslist[self.tableindex],
                              data.shape[1])

        self.currenttableorderfull = []
        for i in range(data.shape[1]):
            self.currenttableorderfull.append(i)
        for i in range(len(data)):
            self.datalist.append(data[i, :, :])
            self.currenttableordersfiltered.append(list(range(data.shape[1])))

        # Add the clustered image(s) to the main GUI viewer window.
        for i in range(self.numimgs):
            labelimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1]),
                                dtype=self.labeledimgs[i - self.numimgs].dtype) - 1
            colorimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
            labelimg[0, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = self.labeledimgs[i - self.numimgs]
            labelimg += 1
            for j in range(args.ncluster):
                colorimg[labelimg == j + 1] = colors[j, :]

            if i == 0:
                if addgreyimg:
                    self.viewer.add_image(labelimg,
                                          name=f"Pixel Cluster IDs {self.pixelclustercount + 1}",
                                          blending="additive",
                                          contrast_limits=(0, args.ncluster))
                if addcolorimg:
                    self.viewer.add_image(colorimg,
                                          name=f"Pixel Clusters {self.pixelclustercount + 1}",
                                          blending="additive")
            else:
                if addgreyimg and addcolorimg:
                    self.viewer.layers[-2].data = np.vstack((self.viewer.layers[-2].data, labelimg))
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, colorimg))
                elif addgreyimg:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, labelimg))
                elif addcolorimg:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, colorimg))
        self.set_invisible(self.viewer)
        self.viewer.layers[-1].visible = True

        self.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                              name=f"Pixel Clusters {self.pixelclustercount + 1} Heatmap",
                              blending="additive",
                              visible=False,
                              )

        # Update any necessary variables.
        self.viewer.status = "RAPID clustering done"
        self.clustersarepixelbased.append(True)
        self.pixelclustercolors.append(colors)
        self.clusternames.append([])
        self.updatelogfile = False
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Pixel Cluster {self.pixelclustercount + 1} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        self.updatelogfile = True

    def apply_segmentation(self,
                           addgreyimg,
                           addcolorimg,
                           quant_avg,
                           outfolder,
                           zarrpath="",
                           probthreshold=None,
                           minsize=None,
                           maxsize=None,
                           loadedresultspaths=[],
                           ):
        """
        Convert outputs from segmentation algorithm to an image with labeled cells, and quantify average marker
        expression and morphological information.

        Args:
            addgreyimg (bool): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't.
            addcolorimg (bool): If True, add RGB-colored segmented image to the viewer. Otherwise, don't.
            quant_avg (bool): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values.
            outfolder (str): Path to the folder where results will be saved.
            zarrpath (str, optional): Path to zarr file where results and image properties will be stored (Default: "").
            probthreshold (float, optional): Value in the range [0,1] defining model prediction probability threshold for cells to include (Default: None).
            minsize (int, optional): Minimum pixel area of cells to include in segmentation (Default: None).
            maxsize (int, optional): Maximum pixel area of cells to include in segmentation (Default: None).
            loadedresultspaths (list, optional): List of paths for the segmented images being loaded (Default: []).
        """

        self.viewer.status = "Calculating cell phenotypes"
        cortabs = []
        numcells = 0
        for img_index, path in enumerate(self.filenames):
            # Get name of current image
            imgname = os.path.splitext(os.path.split(path)[-1])[0]

            if loadedresultspaths == []:
                # Find cells within threshold values set by the user.
                xcrop = self.maximageshape[0]
                ycrop = self.maximageshape[1]
                fh = zarr.open(zarrpath, mode='r')
                blobs = np.array(fh[f"Features{img_index}"]) >= probthreshold
                blobs = measure.label(blobs[:xcrop, :ycrop], connectivity=1)
                blobs = morphology.remove_small_objects(blobs, min_size=int(minsize))
                blobs = self.remove_large_objects(blobs, maxsize=int(maxsize))
                label_image = objectmodels.expand_objects(objectimg=blobs, numiterations=round(0.284 / self.resolution))
                label_image = morphology.remove_small_objects(label_image.astype(bool), min_size=int(minsize),
                                                              in_place=True)

                # Label the segmented images and save to output folder.
                label_image, _ = measure.label(label_image, connectivity=1, return_num=True)
                label_image = label_image[:self.imageshapelist[img_index][0], :self.imageshapelist[img_index][1]]
                label_image = label_image.astype(np.uint32)
            else:
                # Store labeled segmented image files.
                filename = os.path.join(os.path.abspath(loadedresultspaths[img_index]))
                label_image, flipimg = self.parse_img(filename, True)
                self.imageisflipped.append(flipimg)

            object_count = len(np.unique(label_image)) - 1
            GUIUtils.save_img(os.path.join(outfolder, f"SegmentedLabels_{imgname}.tif"),
                              label_image,
                              self.imageisflipped[img_index],
                              )
            self.labeledimgs.append(GUIUtils.convert_dtype(label_image))

            quant_tab = GUIUtils.quantify_segmented_img(object_count,
                                                        self.nummarkers,
                                                        quant_avg,
                                                        label_image,
                                                        img_index,
                                                        self.viewer.layers,
                                                        )

            # Create RGB-colored image for segmentation and save it to the output folder.
            rgb_image = (label2rgb(label_image,
                                   image=None,
                                   colors=None,
                                   alpha=0.3,
                                   bg_label=0,
                                   bg_color=(0, 0, 0),
                                   image_alpha=1,
                                   kind='overlay',
                                   ) * 255).astype(np.uint8)

            # Save RGB-colored segmented image to the output folder
            GUIUtils.save_img(os.path.join(outfolder, f"Segmented_{imgname}.tif"),
                              rgb_image[:self.imageshapelist[img_index][0], :self.imageshapelist[img_index][1], :],
                              self.imageisflipped[img_index],
                              )

            # Add the segmented image(s) to the main GUI viewer window.
            GUIUtils.add_results_to_viewer(img_index,
                                           self.maximageshape,
                                           addgreyimg,
                                           addcolorimg,
                                           rgb_image,
                                           label_image,
                                           self.viewer,
                                           [0, 1],
                                           f"Labels {self.segmentcount + 1}",
                                           f"Segment {self.segmentcount + 1}",
                                           )

            # Store centroid coordinates and cell labels, and store full quantified tables in memory.
            cortabs.append([prop.centroid for prop in measure.regionprops(label_image)])
            self.datalist.append(quant_tab)
            self.currentlyselected.append([])
            self.currenttableordersfiltered.append(list(range(len(quant_tab))))
            numcells += len(quant_tab)

            # Store min and max values for each of the cell markers and morphological parameters.
            minvals = []
            maxvals = []
            for j in range(quant_tab.shape[1]):
                minvals.append(np.min(quant_tab[:, j]))
                maxvals.append(np.max(quant_tab[:, j]))
            self.segmentationindices.append(len(self.lowerboundslist))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))
            self.minvals.append(copy.deepcopy(minvals))
            self.maxvals.append(copy.deepcopy(maxvals))

            # Update dropdown menu for table widget.
            self.tableimagenames.append(f"(Segment [{self.segmentcount}]) - {path.split('/')[-1]}")
            self.tableimgcount += 1

        self.totalnumcells.append(numcells)

        # Set only the most recently-added image to visible.
        self.set_invisible(self.viewer)
        self.viewer.layers[-1].visible = True

        # Store cell coordinates.
        self.cellcoordinates.append(cortabs)
        if 'None' in self.tableimagenames:
            self.tableimagenames.remove('None')

        # Save table to the output folder as a csv file, and keep track of the current order of cell IDs in the table.
        startindex = len(self.datalist) - self.numimgs
        self.currenttableorderfull = list(range(len(self.datalist[startindex])))
        for i in range(self.numimgs):
            imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]
            segmentedtable = pd.DataFrame(np.hstack([np.vstack(self.datalist[i + startindex]), cortabs[i]]))
            segmentedtable.columns = np.hstack(
                [self.markers, "Area", "Eccentricity", "Perimeter", "Major Axis", "y", "x"])
            segmentedtable.to_csv(os.path.join(outfolder, f"Segmentation_Table_{imgname}.csv"))
            self.currenttableordersfiltered.append(list(range(len(self.datalist[i + startindex]))))

        # Update any pertinent variables.
        self.segmentationclusteringrounds.append([])
        self.updatelogfile = False
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"(Segment [{self.segmentcount}]) - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        self.updatelogfile = True
        self.segmentcount += 1
        self.analysislog.append("S")
        self.objectimgnames.append(f"Segment {self.segmentcount}")
        self.analysismode = "Segmentation"

        # If this is the first table being generated, set upper and lower bounds consistent with first segmented image.
        if not self.hasaddedtable:
            self.lowerboundslist[self.tableindex] = copy.deepcopy(self.minvals[0])
            self.upperboundslist[self.tableindex] = copy.deepcopy(self.maxvals[0])
            self.update_table(self.datalist[startindex],
                              self.lowerboundslist[self.tableindex],
                              self.upperboundslist[self.tableindex],
                              len(self.datalist[startindex]),
                              list(range(1, 1 + len(self.datalist[startindex]))))

        self.viewer.status = "Segmentation complete"

    def biaxial_gate(self,
                     segindex=None,
                     chan1="",
                     chan2="",
                     colorparam="",
                     norm="",
                     colorbygroups=[],
                     colorbyindivclusters=None,
                     colorbycombclusters=None,
                     clusteringindex=None,
                     ):
        """
        Generate a biaxial plot according to cell markers and normalization algorithm defined by the user.

        Args:
            segindex (int, optional): Index of segmentation round to be used for biaxial gating (Default: None).
            chan1 (str, optional): Name of parameter to define the horizontal axis (Default: "").
            chan2 (str, optional): Name of parameter to define the vertical axis (Default: "").
            colorparam (str, optional): Name of parameter to define the color gradient (Default: "").
            norm (str, optional): Normalization algorithm to be used for data preprocessing (Default: "").
            colorbygroups (list, optional): List of group assignment indices to use for coloring biaxial plot(s) (Default: []).
            colorbyindivclusters (bool, optional): If True, generate a plots for each cluster, with vertex colors representing membership of the respective cluster. Otherwise, do nothing (Default: None).
            colorbycombclusters (bool, optional): If True, generate a plot with vertices colored according to cluster assignment. Otherwise, do nothing (Default: None).
            clusteringindex (int, optional): Index of the round of clustering to be used for color assignment, if applicable (Default: None).
        """
        params = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        # User must first run object-based segmentation in order to generate a Biaxial Plot.
        if self.segmentcount == 0:
            GUIUtils.display_error_message("You must segment before running biaxial gating",
                                           "Biaxial gating cannot be done until the image has been segmented")
            return

        # Prompt user to select which cell markers to use as parameters for the plot and vertex coloring.
        if any(param is None for param in (segindex, colorbyindivclusters, colorbycombclusters)) or any(
                param == "" for param in (norm, chan1, chan2, colorparam)):
            biaxial = GUIUtils.BiaxialGate(self.markers, self.objectimgnames, self.objectclustercount > 0,
                                           self.groupsnames[1:])
            biaxial.exec()
            if not biaxial.OK:
                return
            segindex = biaxial.segmentationindex
            chan1 = biaxial.chan1
            chan2 = biaxial.chan2
            colorparam = biaxial.color
            norm = biaxial.norm
            colorbygroups = biaxial.colorbygroups
            if len(self.segmentationclusteringrounds[segindex]) > 0:
                colorbyindivclusters = biaxial.colorbyindivclusters
                colorbycombclusters = biaxial.colorbycombclusters

        self.plotsegmentationindices.append(segindex * self.numimgs)

        # Compile quantified cells from each individual image into one combined data array.
        numcells = 0
        for i in range(self.numimgs):
            numcells += len(self.datalist[self.segmentationindices[segindex * self.numimgs + i]])
        fullquantified = np.zeros((numcells, self.datalist[self.segmentationindices[segindex * self.numimgs]].shape[1]))
        count = 0
        cellsperimage = []
        for i in range(self.numimgs):
            cellsincurrimg = []
            index1 = params.index(chan1) + 1
            index2 = params.index(chan2) + 1
            currentimage = self.datalist[self.segmentationindices[segindex * self.numimgs + i]]
            for j in range(count, count + len(currentimage)):
                cellsincurrimg.append(j)
            fullquantified[count:count + len(currentimage), :] = currentimage
            count += len(currentimage)
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
        if colorparam != '---(Optional)---':
            colorindex = params.index(colorparam) + 1
            max = np.percentile(fullquantified[:, colorindex], 97)
            min = np.min(fullquantified[:, colorindex])
            for i in range(len(fullquantified)):
                cols[i, 0] = (fullquantified[i, colorindex] - min) / (max - min)
                cols[i, 2] = 1.0 - (fullquantified[i, colorindex] - min) / (max - min)
            cols[cols > 1.0] = 1.0
            cols[cols < 0.0] = 0.0
            name = f" ({colorparam})"
        cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)

        # Perform any necessary normalization and define vertices that will be plotted on the biaxial scatterplot
        x = fullquantified[:, index1]
        y = fullquantified[:, index2]
        if norm == "Log10":
            x = np.log10(x * 9.0 + 1.0)
            y = np.log10(y * 9.0 + 1.0)
        elif norm == "Log2":
            x = np.log2(x + 1.0)
            y = np.log2(y + 1.0)
        x = np.append(x, [-0.05 * np.max(x), 1.05 * np.max(x)])
        y = np.append(y, [-0.05 * np.max(y), 1.05 * np.max(y)])

        # Use resulting points to generate a scatterplot and add it to the viewer.
        plt.figure(figsize=(10, 10))
        plt.scatter(x, y, s=1, c=cols)
        plt.show(block=False)
        plt.title(f"Biaxial Gate{name}")
        plt.xlabel(str(chan1))
        plt.ylabel(str(chan2))
        outfolder = GUIUtils.create_new_folder("Biaxial_", self.outputfolder)
        plt.savefig(os.path.join(outfolder, "Biaxial.png"), format="PNG", dpi=300)
        im = imread(os.path.join(outfolder, "Biaxial.png"))
        im = np.asarray(im)
        im[:, :, [0, 2]] = im[:, :, [2, 0]]
        locs = np.where((im[:, :, 0] == 242) & (im[:, :, 1] == 255) & (im[:, :, 2] == 242))
        self.plotxmins.append(np.min(locs[0]))
        self.plotxmaxs.append(np.max(locs[0]))
        self.plotymins.append(np.min(locs[1]))
        self.plotymaxs.append(np.max(locs[1]))
        self.set_invisible(self.viewer)
        self.viewer.add_image(im, name=f"Biaxial {self.biaxialcount} ({chan1} vs. {chan2})",
                              blending="additive")

        # If given segmented image iteration has been clustered, check if the user elected to use clustering as
        # a basis for vertex coloring.
        if len(self.segmentationclusteringrounds[segindex]) > 0:
            # If the user is coloring according to cluster assignment, prompt to define which clustering
            # iteration is being used.
            if colorbyindivclusters or colorbycombclusters:
                if len(self.segmentationclusteringrounds[segindex]) > 1:
                    if clusteringindex is None:
                        iteration = GUIUtils.ObjectClusterIteration(self.segmentationclusteringrounds[segindex])
                        iteration.exec()
                        if not iteration.OK:
                            return
                        clusteringindex = iteration.iteration

                    startindex = self.segmentationclusteringrounds[segindex][clusteringindex]
                else:
                    startindex = self.segmentationclusteringrounds[segindex][0]
                clusternums = []
                for i in range(self.numimgs):
                    curclusternums = self.cellclustervals[startindex * self.numimgs + i]
                    for n in curclusternums:
                        clusternums.append(n - 1)
                analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][startindex] * self.numimgs
                labelimg = self.concat_label_imgs(
                    [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)])
                numclusters = len(np.unique(labelimg)) - 1

            # If selected by user, add an additional stack of scatterplots with vertices colored red if
            # corresponding to a cell in the respective cluster, or blue otherwise.
            if colorbyindivclusters:
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
                    plt.xlabel(chan1)
                    plt.ylabel(chan2)
                    plt.savefig(os.path.join(outfolder, f"Biaxial_Cluster{i + 1}.png"), format="PNG", dpi=300)
                    pathlist.append(os.path.join(outfolder, f"Biaxial_Cluster{i + 1}.png"))
                imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
                self.viewer.add_image(imx,
                                      name=f"Biaxial {self.biaxialcount} ({chan1} vs. {chan2}) (Individual Clusters)",
                                      blending="additive")

            # If selected by user, add an additional scatterplot colored according to cluster assignment.
            if colorbycombclusters:
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
                plt.xlabel(chan1)
                plt.ylabel(chan2)
                filename = os.path.join(outfolder, "BiaxialClusters.png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename, pilmode='RGB'),
                                      name=f"Biaxial {self.biaxialcount} ({chan1} vs. {chan2}) (Combined Clusters)",
                                      blending="additive")

        # If selected by user, add an additional scatterplot colored according to group assignment.
        if colorbygroups != []:
            for ind in colorbygroups:
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
                plt.title(f"{chan1} vs. {chan2} ({self.groupsnames[ind + 1]})")
                plt.xlabel(chan1)
                plt.ylabel(chan2)
                filename = os.path.join(outfolder, f"BiaxialGroups_{self.groupsnames[ind + 1]}.png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename, pilmode='RGB'),
                                      name=f"Biaxial {self.biaxialcount} ({chan1} vs. {chan2}) ({self.groupsnames[ind + 1]})",
                                      blending="additive")

        # Keep track of coordinates on Biaxial plot, and update variables.
        coordslist = []
        coords = np.hstack((np.expand_dims(x / np.max(x), 1), np.expand_dims(y / np.max(y), 1)))
        count = 0
        for i in range(self.numimgs):
            numcells = len(self.datalist[self.segmentationindices[segindex * self.numimgs + i]])
            coordslist.append(coords[count:count + numcells].astype(np.float))
            count += numcells
        self.plotcoordinates.append(coordslist)
        self.plotisumap.append(False)
        self.biaxialcount += 1
        GUIUtils.log_actions(self.actionloggerpath, f"gui.biaxial_gate(segindex={segindex}, chan1=\"{chan1}\", "
                                                    f"chan2=\"{chan2}\", colorparam=\"{colorparam}\", norm=\"{norm}\", "
                                                    f"colorbygroups={colorbygroups}, "
                                                    f"colorbyindivclusters={colorbyindivclusters}, "
                                                    f"colorbycombclusters={colorbycombclusters}, "
                                                    f"clusteringindex={clusteringindex})")

    def calculate_table_cell_color(self,
                                   analysismode,
                                   ):
        color = QColor(0, 0, 0)
        if analysismode == "Segment":
            return
        elif analysismode == "Pixel":
            return
        elif analysismode == "Object":
            return
        return color

    def change_folder_gui(self):
        self.change_folder()

    def change_folder(self,
                      outputfolder="",
                      ):
        """
        Change the root directory path where results from the GUI will be saved.
        """
        if outputfolder == "":
            dialog = QFileDialog()
            outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")

        if outputfolder != "":
            GUIUtils.log_actions(self.actionloggerpath, f"gui.change_folder(outputfolder=\"{outputfolder}\")")
            outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
            os.rename(self.outputfolder, outputfolder)
            self.actionloggerpath = self.actionloggerpath.replace(self.outputfolder, outputfolder)
            self.editimagepath = self.editimagepath.replace(self.outputfolder, outputfolder)
            self.mergedimagespaths = [path.replace(self.outputfolder, outputfolder) for path in self.mergedimagespaths]
            self.objectclusterdirectories = [path.replace(self.outputfolder, outputfolder) for path in
                                             self.objectclusterdirectories]
            self.pixelclusterdirectories = [path.replace(self.outputfolder, outputfolder) for path in
                                            self.pixelclusterdirectories]
            self.segmentationzarrpaths = [path.replace(self.outputfolder, outputfolder) for path in
                                          self.segmentationzarrpaths]
            self.outputfolder = outputfolder
        return

    def colormap_group_gui(self):
        self.colormap_group()

    def colormap_group(self,
                       newcolorlist=[],
                       ):
        """
        Load preset colormap options from a csv file to allow the user to assign custom colors to each cluster.

        Args:
            newcolorlist (optional, list): List of colors for each cluster in the current table (Default: []).
        """
        if self.analysismode == "Segmentation":
            GUIUtils.display_error_message("Must be displaying clustered image",
                                           "Please ensure that the currently selected table corresponds to clustering results.")

        ind = self.analysisindex
        if self.numimgs > 1:
            ind = int(self.analysisindex / (self.numimgs + 1))
        if self.analysismode == "Pixel":
            analysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][ind] * self.numimgs
            labelimg = self.concat_label_imgs(
                [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)], pixelbased=True)
            nc = len(np.unique(labelimg))
        elif self.analysismode == "Object":
            analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][ind] * self.numimgs
            labelimg = self.concat_label_imgs(
                [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)])
            nc = len(np.unique(labelimg)) - 1

        if newcolorlist == []:
            if nc < 57:
                colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color56.csv"
            elif 56 < nc < 142:
                colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color141.csv"
            else:
                colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color282.csv"
            colordf = pd.read_csv(colorcsvpath, index_col=0)

            cmapwidget = GUIUtils.ColorAssign(nc, colordf, self.viewer)
            cmapwidget.exec()
            if not cmapwidget.OK:
                return
            newcolorlist = cmapwidget.newcolorlist.tolist()

        if self.analysismode == "Pixel":
            self.pixelclustercolors[ind] = np.array(newcolorlist)
            data = self.datalist[self.tableindex]
            index = [f"RP-{i + 1}" for i in range(nc)]
            cols = self.fulltab.columns[3:]
        else:
            self.objectclustercolors[ind] = np.array(newcolorlist)
            data = self.datalist[self.tableindex][:, 1:-4]
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
                                              int(max(minwidth, len(my_data_scaled) * 0.4))),
                                     linecolor='#799579')
        ClusterDend.ax_row_dendrogram.set_visible(False)
        ClusterDend.ax_col_dendrogram.set_visible(False)
        ClusterDend.cax.set_visible(False)
        for tick_label in ClusterDend.ax_heatmap.axes.get_xticklabels():
            if self.analysismode == "Pixel":
                tick_text = tick_label.get_text().replace(r"RP-", "")
                tick_label.set_color(self.pixelclustercolors[ind][int(tick_text) - 1, :] / 255)
                if self.pixelclustercolors[ind][int(tick_text) - 1, 0] == 255 and self.pixelclustercolors[ind][
                    int(tick_text) - 1, 1] == 255 and self.pixelclustercolors[ind][int(tick_text) - 1, 2] == 255:
                    tick_label.set_color("black")
            else:
                tick_text = tick_label.get_text().replace(r"RO-", "")
                tick_label.set_color(self.objectclustercolors[ind][int(tick_text) - 1, :] / 255)
                if self.objectclustercolors[ind][int(tick_text) - 1, 0] == 255 and self.objectclustercolors[ind][
                    int(tick_text) - 1, 1] == 255 and self.objectclustercolors[ind][int(tick_text) - 1, 2] == 255:
                    tick_label.set_color("black")

        if self.analysismode == "Pixel":
            plt.savefig(os.path.join(self.pixelclusterdirectories[ind], "ClusterHeatmap.png"), dpi=300)
            np.save(os.path.join(self.pixelclusterdirectories[ind], "COLOR.npy"), self.pixelclustercolors[ind])
        else:
            plt.savefig(os.path.join(self.objectclusterdirectories[ind], "ClusterHeatmap.png"), dpi=300)
            np.save(os.path.join(self.objectclusterdirectories[ind], "COLOR.npy"), self.objectclustercolors[ind])

        GUIUtils.log_actions(self.actionloggerpath, f"gui.colormap_group(newcolorlist={newcolorlist})")

    def concat_label_imgs(self,
                          imgs,
                          pixelbased=False,
                          ):
        dtype = np.uint32
        while True:
            for img in imgs:
                if img.dtype == dtype:
                    break
            dtype = np.uint16
            for img in imgs:
                if img.dtype == dtype:
                    break
            dtype = np.uint8
            break
        concatimg = np.zeros((len(imgs), self.maximageshape[0], self.maximageshape[1]), dtype=dtype)
        if pixelbased:
            concatimg -= 1
        for i, img in enumerate(imgs):
            concatimg[i, :img.shape[0], :img.shape[1]] = img
        if pixelbased:
            concatimg += 1
        return concatimg

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

    def create_shape_path(self,
                          verts,
                          shapetype,
                          ):
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

    def create_table(self,
                     data,
                     ):
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
                if data[headerList[j]][i] is not None and j == 1 and i >= 3 and not self.analysismode == "Segmentation":
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
                elif i == 2 and j == 1 and not (self.analysismode == "Segmentation"):
                    newitem = QTableWidgetItem("")
                    newitem.setBackground(QColor(0, 0, 0))
                elif i == 2 or j == 0:
                    newitem = QTableWidgetItem("")
                    if key not in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
                        newitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        newitem.setCheckState(QtCore.Qt.Unchecked)
                elif j == 1 and not (self.analysismode == "Segmentation"):
                    newitem.setBackground(QColor(0, 0, 0))
                else:
                    if self.analysismode == "Object" and numrows > 4:
                        minv = self.minvals[self.tableindex][j - 2]
                        maxv = self.maxvals[self.tableindex][j - 2]
                        clusterindex, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                        tabnum = self.analysisindex % numtabs
                        for k in range(len(self.segmentationclusteringrounds)):
                            l = self.segmentationclusteringrounds[k]
                            if clusterindex in l:
                                segmentindex = k * self.numimgs
                        if tabnum == self.numimgs:
                            maxsegment = []
                            for k in range(self.numimgs):
                                maxsegment.append(np.array(self.maxvals[self.segmentationindices[segmentindex + k]]))
                            maxsegment = np.vstack(maxsegment)
                            maxsegment = list(np.amax(maxsegment, axis=0))
                        else:
                            maxsegment = self.maxvals[self.segmentationindices[segmentindex + tabnum]]
                        adj = (data[key][i] - minv) / (maxv - minv) * maxsegment[j - 2] / np.max(
                            np.asarray(maxsegment[:-4]))
                    elif self.analysismode == "Segmentation" and numrows > 4:
                        minv = self.minvals[self.tableindex][j - 1]
                        maxv = self.maxvals[self.tableindex][j - 1]
                        adj = (data[key][i] - minv) / (maxv - minv)
                    elif self.analysismode == "Pixel":
                        minv = self.minvals[self.tableindex][j - 2]
                        maxv = self.maxvals[self.tableindex][j - 2]
                        clusterindex, _ = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                        adj = ((data[key][i] - minv) / (maxv - minv) * self.maxpixelclustervals[clusterindex][
                            j - 2]) / 255
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
        self.tablewidget.setMaximumHeight(self.tablewidget.rowHeight(3) * 14)

    def display_selected_cells(self,
                               plotindex=None,
                               shapetypes=[],
                               vertslist=[],
                               ):
        """
        Mask the image according to the cells within user-defined shapes overlaid on a Biaxial or UMAP plot.

        Args:
            plotindex (int, optional): Index of the plot of vertices being selected from (Default: None).
            shapetypes (list, optional): List of geometries for each shape drawn by the user (Default: []).
            vertslist (list, optional): List of vertices for each shape drawn by the user (Default: []).
        """
        # https://stackoverflow.com/questions/21339448/how-to-get-list-of-points-inside-a-polygon-in-python
        # Can only use display selected for UMAP or Biaxial gating.
        if self.biaxialcount == 1 and self.umapcount == 1:
            GUIUtils.display_error_message("No UMAP or biaxial gate output detected",
                                           "You must first generate a UMAP or biaxial-gate plot in order to select cells to be displayed")
            return

        # Select which plot is being used.
        if plotindex is None:
            plotindex = 0
            if len(self.plotisumap) > 1:
                selectplot = GUIUtils.BiaxialUMAPIterations(self.plotisumap)
                selectplot.exec()
                if not selectplot.OK:
                    return
                plotindex = selectplot.iteration
        numcells = self.totalnumcells[int(self.plotsegmentationindices[plotindex] / self.numimgs)]
        self.viewer.status = "Displaying selected cells"

        if shapetypes == [] or vertslist == []:
            # Find the most recent shapes layer to define which vertices to use to define the shapes.
            ind = -1
            for i in reversed(range(len(self.viewer.layers))):
                if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and self.viewer.layers[
                    i].visible:
                    ind = i
                    break
            # If no shapes have been drawn, prompt user to first draw a shape.
            if ind == -1:
                GUIUtils.display_error_message("Please draw a shape in the viewer first",
                                               "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
                return

            shapetypes = [self.viewer.layers[ind].shape_type[i] for i in range(len(self.viewer.layers[ind].data))]
            vertslist = [self.viewer.layers[ind].data[i] for i in range(len(self.viewer.layers[ind].data))]
            self.viewer.layers.pop(ind)
        else:
            vertslist = [np.array(verts) for verts in vertslist]

        # Define the colors of each of the shapes, which will be coordinated with the selected cells.
        if len(shapetypes) == 1:
            cols = [np.array([1, 0, 0])]
        elif len(shapetypes) == 2:
            cols = [np.array([1, 0, 0]), np.array([0, 1, 1])]
        elif len(shapetypes) == 3:
            cols = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
        else:
            cols = generate_colormap(len(shapetypes) + 1) / 255.0
            cols = [cols[i] for i in range(len(cols) - 1)]

        # Update the shapes layer with shapes colored consistently with the displayed images.
        self.viewer.add_shapes(vertslist, shape_type=shapetypes, edge_width=0, edge_color=cols, face_color=cols,
                               name="Selected Regions")
        self.set_invisible(self.viewer)

        shapeverts = []
        for verts in vertslist:
            # Find the vertices of the shapes relative to the scale of the plot, and the vertices within each shape.
            verts = copy.deepcopy(verts[:, -2:])
            verts[:, 0] = ((self.plotxmaxs[plotindex] - verts[:, 0]) / (
                    self.plotxmaxs[plotindex] - self.plotxmins[plotindex])) * 1.1 - 0.05
            verts[:, 1] = ((verts[:, 1] - self.plotymins[plotindex]) / (
                    self.plotymaxs[plotindex] - self.plotymins[plotindex])) * 1.1 - 0.05
            verts[:, [0, 1]] = verts[:, [1, 0]]
            shapeverts.append([tuple(x) for x in verts.tolist()])

        # Keep track of masked images and percentages of cells that are selected in each shape.
        masklist = []
        percents = []
        segindex = self.plotsegmentationindices[plotindex]
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][segindex // self.numimgs]
        for shape in range(len(shapeverts)):
            p = self.create_shape_path(shapeverts[shape], shapetypes[shape])

            # Keep track of quantified cell marker expression for each selected cell.
            inclrows = []

            # Mask each image to filter out cells that aren't selected.
            masks = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]))

            # Keep track of the total number of cells and number of selected cells to calculate percentages.
            selectedcells = 0
            for i in range(self.numimgs):
                # Add the number of total and selected cells in the image.
                rows = list(p.contains_points(self.plotcoordinates[plotindex][i]))
                rows = [j for j, b in enumerate(rows) if b]
                inclrows.append(rows)
                selectedcells += len(rows)

                # Mask the image for the selected cells.
                labelimg = copy.deepcopy(self.labeledimgs[analysisnum * self.numimgs + i])
                labelimg[np.isin(labelimg, [r + 1 for r in rows], invert=True)] = 0
                labelimg = self.method_searchsort(np.unique(labelimg),
                                                  np.array([j for j in range(len(np.unique(labelimg)))]), labelimg)
                self.labeledimgs.append(GUIUtils.convert_dtype(labelimg))
                masks[i, :len(labelimg), :labelimg.shape[1]][labelimg > 0] = 1

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
                self.currenttableorderfull = inclrows[0]
                for i in range(self.numimgs):
                    # Re-index the selected cells and create a new table entry.
                    newentry = self.datalist[self.segmentationindices[segindex + i]][inclrows[i], :]
                    self.datalist.append(newentry)
                    self.currenttableordersfiltered.append(list(range(len(newentry))))

                    # Find the coordinates of only the selected cells.
                    cortabs.append([self.cellcoordinates[int(segindex / self.numimgs)][i][j] for j in inclrows[i]])

                    # Find the min/max vals for each marker for the table for the current image.
                    minvals = []
                    maxvals = []
                    for j in range(self.datalist[self.segmentationindices[segindex + i]].shape[1]):
                        try:
                            minvals.append(
                                np.min(self.datalist[self.segmentationindices[segindex + i]][inclrows[i], j]))
                            maxvals.append(
                                np.max(self.datalist[self.segmentationindices[segindex + i]][inclrows[i], j]))
                        except:
                            minvals.append(0)
                            maxvals.append(0)
                    mins.append(copy.deepcopy(minvals))
                    maxs.append(copy.deepcopy(maxvals))

                    # Keep track of the orders of the cells and default to no cells being selected in the table.
                    self.currentlyselected.append([])

                # Keep track of the coordinates for each selected cell and the min/max values for each marker
                # for each cell in each image.
                self.cellcoordinates.append(cortabs)
                minvals = []
                maxvals = []
                for i in range(len(mins[0])):
                    minvals.append(min([l[i] for l in mins]))
                    maxvals.append(max([l[i] for l in maxs]))
                for i in range(self.numimgs):
                    self.minvals.append(copy.deepcopy(minvals))
                    self.maxvals.append(copy.deepcopy(maxvals))
                    self.lowerboundslist.append(copy.deepcopy(minvals))
                    self.upperboundslist.append(copy.deepcopy(maxvals))

                # Keep track of the percentages of cells selected for each image.
                percent = round(float(selectedcells * 100 / numcells), 2)
                percents.append(copy.deepcopy(percent))

                # Update the dropdown options for the sort table widget.
                for i in range(len(inclrows)):
                    imgname = f"Selected{self.displayselectedcount}-{i + 1} ({percent}%)"
                    self.tableimagenames.append(f"{imgname} - {self.tableimagenames[self.segmentationindices[i]]}")
                    self.segmentationindices.append(self.tableimgcount)
                    self.tableimgcount += 1
                self.analysislog.append("S")
                self.totalnumcells.append(numcells)

        # Add the selected cells from each image to the viewer.
        for i in range(len(masklist)):
            cmap = Colormap(ColorArray([(0, 0, 0), cols[i]]))
            imgname = f"Selected{self.displayselectedcount}-{i + 1} ({percents[i]}%)"
            self.viewer.add_image(masklist[i], name=imgname, blending="additive", colormap=cmap)
            self.objectimgnames.append(imgname)
            self.segmentationclusteringrounds.append([])
        self.updatelogfile = False
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Selected{self.displayselectedcount}-1 ({percents[0]}%) - {self.tableimagenames[self.segmentationindices[0]]}"
        self.displayselectedcount += 1
        self.sorttableimages.reset_choices()
        self.updatelogfile = True
        GUIUtils.log_actions(self.actionloggerpath, f"gui.display_selected_cells(plotindex={plotindex}, "
                                                    f"shapetypes={shapetypes}, vertslist={[verts.tolist() for verts in vertslist]})")

    def draw_shapes(self,
                    data,
                    shape_type,
                    properties,
                    name,
                    text,
                    face_color,
                    ):
        properties = {'class': np.array(properties), }
        text_properties = {'text': '{class}', 'anchor': 'center', 'size': text[0], 'color': np.array(text[1]), }
        self.viewer.add_shapes(data=np.array(data), shape_type=shape_type, edge_width=0, properties=properties,
                               name=name, text=text_properties, face_color=np.array(face_color))

    def edit_image(self,
                   editactions=[],
                   ):
        """
        Open a new popup napari window to allow the user to edit each image and change the raw data.

        Args:
            editactions (list, optional):  (Default: [])
        """
        # Prompt user to decide whether to edit all images, or to apply edits from one image to all others.
        if editactions != []:
            self.apply_edits(editactions)
            self.editactions += editactions
            GUIUtils.log_actions(self.actionloggerpath, f"gui.edit_image(editactions={editactions})")
            return

        editoptions = GUIUtils.EditOptions(self.numimgs)
        editoptions.exec()
        if not editoptions.OK:
            return
        allimgs = editoptions.allimages
        loadedits = editoptions.loadedits

        # Load previous edits if selected by the user
        if loadedits:
            editactions = []
            path = QFileDialog().getOpenFileName(filter="*editlog.txt")[0]
            if path == "":
                return
            with open(path, 'r') as file:
                for line in file:
                    edit = line[:-1]
                    editactions.append(ast.literal_eval(edit))
            if not len(editactions[0]) == self.numimgs:
                if len(editactions[0]) == 1:
                    editactions = [action * self.numimgs for action in editactions]
                else:
                    GUIUtils.display_error_message("Incompatible number of images",
                                                   "Please ensure you are using the same number of images that you used for the edits being loaded")
                    return
            if not len(editactions[0][0]) == self.nummarkers:
                GUIUtils.display_error_message("Incompatible number of cell markers",
                                               "Please ensure you are using the same number of cell markers that you used for the edits being loaded")
                return
            self.apply_edits(editactions)
            self.editactions += editactions
            GUIUtils.log_actions(self.actionloggerpath, f"gui.edit_image(editactions={editactions})")
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
        cl = []
        for i in range(len(self.markers)):
            cl.append([0, 255])
        for i in range(len(self.filenames)):
            contrastlimits.append(copy.deepcopy(cl))

        @magicgui(call_button="Apply Changes")
        def apply_changes_editgui() -> Image:
            # Apply all changes, including any adjusted contrast limits, to the raw images in the main viewer.
            for i in range(len(self.markers)):
                editdata[i, self.imagenum, :, :] = copy.deepcopy(self.edit_viewer.layers[i].data)
                contrastlimits[self.imagenum][i] = [self.edit_viewer.layers[i].contrast_limits[0],
                                                    self.edit_viewer.layers[i].contrast_limits[1]]
                for j in range(self.numimgs):
                    if contrastlimits[j][i] != [0, 255]:
                        editdata[i, j, :, :] = self.apply_contrast_limits(editdata[i, j, :, :], contrastlimits[j][i])
                self.viewer.layers[i].data = editdata[i, :, :, :]
            self.editactions += editactions
            self.editactions.append(contrastlimits)

            if not self.haseditedimage:
                self.editimagepath = GUIUtils.create_new_folder("ImageEdits", self.outputfolder)
            with open(os.path.join(self.editimagepath, "editlog.txt"), 'w') as file:
                for item in self.editactions:
                    file.write("%s\n" % item)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.edit_image(editactions={editactions})")
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

            if not self.haseditedimage:
                self.editimagepath = GUIUtils.create_new_folder("ImageEdits", self.outputfolder)
            with open(os.path.join(self.editimagepath, "editlog.txt"), 'w') as file:
                for item in self.editactions:
                    file.write("%s\n" % item)

            GUIUtils.log_actions(self.actionloggerpath, f"gui.edit_image(editactions={editactions})")
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
                data = np.zeros((len(self.edit_viewer.layers[0].data), self.edit_viewer.layers[0].data.shape[1],
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
            self.edit_viewer.add_image(self.viewer.layers[i].data[imgindex, :, :], name=self.markers[i],
                                       rgb=False, colormap=self.viewer.layers[i].colormap, contrast_limits=[0, 255],
                                       blending="additive")
            editdata[i, :, :, :] = self.viewer.layers[i].data

    def filter_table(self,
                     reset=None,
                     bound="",
                     marker="",
                     val=None,
                     ):
        """
        Allow user to set a lower or upper bound for any of the parameters currently displayed in the table. This will
        also be applied to all other images included in the same round of analysis.

        Args:
            reset (bool, optional): If True, reset all filters in the table. Otherwise, set specified filter (Default: None).
            bound (str, optional): "Lower Bound" if defining a lower bound, "Upper Bound" if defining an upper bound (Default: None).
            marker (str, optional): Name of the cell marker being filtered on (Default: None).
            val (float, optional): Value of the bound being set (Default: None).
        """
        # Get all the markers in the currently displayed table, and only use those as options for filtering.
        markers = []
        for i in range(self.tablewidget.columnCount()):
            if self.tablewidget.horizontalHeaderItem(i).text() in self.markers:
                markers.append(self.tablewidget.horizontalHeaderItem(i).text())

        # Prompt user to define which markers, whether to set a lower/upper bound, and the value being used.
        if any(param is None for param in (reset, val)) or any(param == "" for param in (bound, marker)):
            tablefilters = GUIUtils.TableFilters(markers)
            tablefilters.exec()
            if not tablefilters.OK:
                return
            reset = tablefilters.reset
            bound = tablefilters.bound
            marker = tablefilters.marker
            val = tablefilters.val

        # If resetting the filters, include all the full datasets.
        if reset:
            self.currenttableordersfiltered[self.tableindex] = copy.deepcopy(self.currenttableorderfull)
            # If the current table corresponds to segmentation.

            if self.analysismode == "Segmentation":
                # Reset lower/upper bounds and use the full dataset to display in the table.
                self.lowerboundslist[self.tableindex] = copy.deepcopy(self.minvals[self.tableindex])
                self.upperboundslist[self.tableindex] = copy.deepcopy(self.maxvals[self.tableindex])
                self.update_table(self.datalist[self.tableindex][self.currenttableorderfull, :],
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(self.datalist[self.tableindex]),
                                  [id + 1 for id in self.currenttableordersfiltered[self.tableindex]])

            # If the current table corresponds to object-based clustering.
            elif self.analysismode == "Object":
                # Reset lower/upper bounds and use the full dataset to display in the table.
                self.lowerboundslist[self.tableindex] = copy.deepcopy(self.minvals[self.tableindex])
                self.upperboundslist[self.tableindex] = copy.deepcopy(self.maxvals[self.tableindex])
                analysisnum, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                ind = [i for i, m in enumerate(self.clustersarepixelbased) if not m][analysisnum]
                self.update_table(self.datalist[self.tableindex][self.currenttableorderfull, :],
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(self.currenttableorderfull),
                                  self.currenttableorderfull,
                                  headernames=self.clusternames[ind])

            # If the current table corresponds to pixel-based clustering.
            else:
                # Reset lower/upper bounds and use the full dataset to display in the table.
                self.lowerboundslist[self.tableindex] = copy.deepcopy(self.minvals[self.tableindex])
                self.upperboundslist[self.tableindex] = copy.deepcopy(self.maxvals[self.tableindex])
                analysisnum, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                ind = [i for i, m in enumerate(self.clustersarepixelbased) if m][analysisnum]
                self.update_table(self.datalist[self.tableindex][self.currenttableorderfull, :],
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(self.datalist[self.tableindex]),
                                  self.currenttableorderfull,
                                  headernames=self.clusternames[ind])

        # If applying a new filter, add to the existing filters and update the table accordingly.
        else:
            # Lower bounds are represented in the first row, while upper bounds are in the second row.
            if bound == "Lower Bound":
                row = 0
            else:
                row = 1

            # Find the column corresponding to the marker being updated.
            for i in range(self.tablewidget.columnCount()):
                if marker == self.tablewidget.horizontalHeaderItem(i).text():
                    column = i

            # Change the filter value in the table.
            self.tablewidget.item(row, column).setText(str(round(val, 3)))

            # Account for the extra column for cell/pixel counts when clustering.
            if self.analysismode == "Segmentation":
                c = column - 1
            else:
                c = column - 2

            # If user adjusts lower bound, store that for future reference.
            if row == 0 and c >= 0:
                # Lower bound must be smaller than upper bound.
                self.lowerboundslist[self.tableindex][c] = val
                if self.lowerboundslist[self.tableindex][c] > self.upperboundslist[self.tableindex][c]:
                    self.lowerboundslist[self.tableindex][c] = self.upperboundslist[self.tableindex][c]

            # If user adjusts upper bound, store that for future reference.
            elif row == 1 and c >= 0:
                # Lower bound must be smaller than upper bound.
                self.upperboundslist[self.tableindex][c] = val
                if self.upperboundslist[self.tableindex][c] < self.lowerboundslist[self.tableindex][c]:
                    self.upperboundslist[self.tableindex][c] = self.lowerboundslist[self.tableindex][c]

            # If filtering a segmentation table.
            if self.analysismode == "Segmentation":
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(self.lowerboundslist[self.tableindex])):
                    if self.lowerboundslist[self.tableindex][i] > self.minvals[self.tableindex][i] or \
                            self.upperboundslist[self.tableindex][i] < self.maxvals[self.tableindex][i]:
                        filteredmarkers.append(i)

                # Store the segmentation iteration corresponding to the current data table, and the
                # corresponding quantified values.
                currentdata = self.datalist[self.tableindex][self.currenttableorderfull, :]

                # Store segmentation data table, and append index values at the end to log sort order.
                filtereddata = np.append(self.datalist[self.tableindex][self.currenttableorderfull, :],
                                         np.expand_dims(np.arange(len(self.datalist[self.tableindex])), 1), 1)

                # Filter cells one marker at a time according to current lower- and upper-bounds.
                for markerid in filteredmarkers:
                    filtermask = (np.round(filtereddata[:, markerid], 3) <= np.round(
                        self.upperboundslist[self.tableindex][markerid], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, markerid], 3) >= np.round(
                        self.lowerboundslist[self.tableindex][markerid], 3))
                    filtereddata = filtereddata[filtermask]

                # Update the list of cell IDs included in the table for each image.
                self.currenttableordersfiltered[self.tableindex] = [self.currenttableorderfull[j] for j in
                                                                    filtereddata[:, -1].astype(np.int).tolist()]
                currentdata = currentdata[filtereddata[:, -1].astype(np.int).tolist(), :]

                # Update the table with quantified values for the included cells.
                self.update_table(currentdata,
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(self.datalist[self.tableindex]),
                                  [ind + 1 for ind in self.currenttableordersfiltered[self.tableindex]])

                # If any cells are included, and at least one cell is filtered out, add an image to the
                # viewer containing the included cells.
                self.set_invisible(self.viewer)
                if len(self.datalist[self.tableindex]) > len(currentdata) > 0:
                    for i in range(self.numimgs):
                        if i == self.analysisindex % self.numimgs:
                            analysisnum = [j for j, n in enumerate(self.analysislog) if n == "S"][
                                self.analysisindex // self.numimgs]
                            labelimg = self.labeledimgs[analysisnum * self.numimgs + i]
                            filtered = np.in1d(labelimg,
                                               np.asarray(self.currenttableordersfiltered[self.tableindex]) + 1)
                            filtered = filtered.reshape((1, self.imageshapelist[i][0], self.imageshapelist[i][1]))
                        else:
                            filtered = np.zeros((1, self.imageshapelist[self.analysisindex % self.numimgs][0],
                                                 self.imageshapelist[self.analysisindex % self.numimgs][1]),
                                                dtype=np.bool)
                        if i == 0:
                            self.viewer.add_image(filtered, name="Filter", blending="additive", visible=True)
                        else:
                            self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, filtered))

                # Un-check cells that are not included in the filter.
                for i in range(len(self.datalist[self.tableindex])):
                    if i in self.currentlyselected[self.tableindex] and self.currenttableorderfull[i] not in \
                            self.currenttableordersfiltered[self.tableindex]:
                        self.currentlyselected[self.analysisindex].remove(i)

            # If filtering an object clustering table.
            elif self.analysismode == "Object":
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(self.lowerboundslist[self.tableindex])):
                    if self.lowerboundslist[self.tableindex][i] > self.minvals[self.tableindex][i] or \
                            self.upperboundslist[self.tableindex][i] < self.maxvals[self.tableindex][i]:
                        filteredmarkers.append(i)

                # Find object clustering data table, and append index values at the end to log sort order.
                cData = np.append(self.datalist[self.tableindex][self.currenttableorderfull, 1:],
                                  np.expand_dims(np.arange(len(self.datalist[self.tableindex])), 1), 1)

                # Filter the table one marker at a time according to current lower- and upper-bounds.
                for markerid in filteredmarkers:
                    mask = (cData[:, markerid] <= self.upperboundslist[self.tableindex][markerid])
                    cData = cData[mask]
                    mask = (cData[:, markerid] >= self.lowerboundslist[self.tableindex][markerid])
                    cData = cData[mask]

                # Store cluster IDs that will be included in the table, and in the proper order.
                self.currenttableordersfiltered[self.tableindex] = [self.currenttableorderfull[i] for i in
                                                                    cData[:, -1].astype(np.int).tolist()]

                # Update the table with quantified values for the included clusters.
                currentdata = self.datalist[self.tableindex][self.currenttableorderfull, :]
                currentdata = currentdata[cData[:, -1].astype(np.int).tolist(), :]
                analysisnum, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                ind = [i for i, m in enumerate(self.clustersarepixelbased) if not m][analysisnum]
                self.update_table(currentdata,
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(self.datalist[self.tableindex]),
                                  self.currenttableordersfiltered[self.tableindex],
                                  headernames=self.clusternames[ind])

                # If any clusters are included, and at least one cluster is filtered out, add an image to the
                # viewer containing the cells in the included clusters.
                analysisnum, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                imganalysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][self.analysisindex // numtabs]
                if len(self.datalist[self.tableindex]) > len(currentdata) > 0:
                    currentclusters = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]),
                                               dtype=np.bool)
                    labelimg = self.concat_label_imgs([self.labeledimgs[ind] for ind in
                                                       range(imganalysisnum * self.numimgs,
                                                             imganalysisnum * self.numimgs + self.numimgs)])
                    for index in self.currenttableordersfiltered[self.tableindex]:
                        currentclusters[labelimg == index + 1] = 1
                    self.viewer.add_image(currentclusters, name="Filter", blending="additive", visible=True)

                # Un-check clusters that are not included in the filter.
                objectclusterindex = self.objectclusterindices.index(self.tableindex)
                ind = self.tableindex - objectclusterindex % numtabs
                for i in range(len(currentdata)):
                    for j in range(ind, ind + numtabs):
                        if self.currenttableorderfull[i] in self.currentlyselected[j] and self.currenttableorderfull[
                            i] not in self.currenttableordersfiltered[self.tableindex]:
                            self.currentlyselected[j].remove(self.currenttableorderfull[i])

            # If filtering a pixel clustering table.
            else:
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(self.lowerboundslist[self.tableindex])):
                    if self.lowerboundslist[self.tableindex][i] > self.minvals[self.tableindex][i] or \
                            self.upperboundslist[self.tableindex][i] < self.maxvals[self.tableindex][i]:
                        filteredmarkers.append(i)

                # Find pixel clustering data table, and append index values at the end to log sort order.
                cData = np.append(self.datalist[self.tableindex][self.currenttableorderfull, 1:],
                                  np.expand_dims(np.arange(len(self.datalist[self.tableindex])), 1), 1)

                # Filter the table one marker at a time according to current lower- and upper-bounds.
                for markerid in filteredmarkers:
                    filtermask = (cData[:, markerid] <= self.upperboundslist[self.tableindex][markerid])
                    cData = cData[filtermask]
                    filtermask = (cData[:, markerid] >= self.lowerboundslist[self.tableindex][markerid])
                    cData = cData[filtermask]

                # Store cluster IDs that will be included in the table, and in the proper order.
                self.currenttableordersfiltered[self.tableindex] = [self.currenttableorderfull[i] for i in
                                                                    cData[:, -1].astype(np.int).tolist()]

                # Update the table with quantified values for the included clusters.
                currentdata = self.datalist[self.tableindex][self.currenttableorderfull, :]
                currentdata = currentdata[cData[:, -1].astype(np.int).tolist(), :]
                analysisnum, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                ind = [i for i, m in enumerate(self.clustersarepixelbased) if m][analysisnum]
                self.update_table(currentdata,
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(self.datalist[self.tableindex]),
                                  self.currenttableordersfiltered[self.tableindex],
                                  headernames=self.clusternames[ind])

                # If any clusters are included, and at least one cluster is filtered out, add an image to the
                # viewer containing the cells in the included clusters.
                imganalysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][self.analysisindex // numtabs]
                if len(self.datalist[self.tableindex]) > len(currentdata) > 0:
                    currentclusters = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]),
                                               dtype=np.bool)
                    labelimg = self.concat_label_imgs([self.labeledimgs[ind] for ind in
                                                       range(imganalysisnum * self.numimgs,
                                                             imganalysisnum * self.numimgs + self.numimgs)],
                                                      pixelbased=True)
                    for index in self.currenttableordersfiltered[self.tableindex]:
                        currentclusters[labelimg == index + 1] = 1
                    self.viewer.add_image(currentclusters, name="Filter", blending="additive", visible=True)

                # Un-check clusters that are not included in the filter.
                pixelclusterindex = self.pixelclusterindices.index(self.tableindex)
                ind = self.tableindex - pixelclusterindex % numtabs
                for i in range(len(currentdata)):
                    for j in range(ind, ind + numtabs):
                        if self.currenttableorderfull[i] in self.currentlyselected[j] and self.currenttableorderfull[
                            i] not in self.currenttableordersfiltered[self.tableindex]:
                            self.currentlyselected[j].remove(self.currenttableorderfull[i])

        GUIUtils.log_actions(self.actionloggerpath, f"gui.filter_table(reset={reset}, bound=\"{bound}\", "
                                                    f"marker=\"{marker}\", val={val})")

    def generate_RAPID_data(self,
                            markerindices,
                            markernames,
                            outfolder,
                            denoise,
                            normalizeeach,
                            normalizeall,
                            normtype,
                            pca,
                            ):
        """
        Normalize images before passing them through the RAPID algorithm.

        Args:
            markerindices (list): List of indices of cell markers being used for clustering.
            markernames (list): List of names of cell markers being used for clustering.
            outfolder (str): Path to folder where results will be saved.
            denoise (bool): If True, apply denoising on the image, otherwise do nothing.
            normalizeeach (bool): If True, apply specified normalization algorithm to each image individually. Otherwise, do nothing.
            normalizeall (bool): If True, apply z-scale normalization on all images together. Otherwise, do nothing.
            normtype (str): Normalization algorithm to be used on the image ({"None", "zscore", "log2", "log10", "all"}).
            pca (bool): If True, apply PCA reduction before normalization. Otherwise, do nothing.
        """

        # Open the zarr file to save files and variables to.
        self.viewer.status = "Preprocessing..."
        fh = zarr.open(outfolder, mode='a')
        fh.create_dataset('imageshapelist', data=self.imageshapelist, dtype='i4')

        # Initialize an array for the unnormalized dataset.
        unnormalized = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], len(markerindices)),
                                dtype=np.uint8)

        # Store the max values for each image for relative normalization of the heatmap in the table.
        maxpixelclustervals = []
        for i in range(self.nummarkers):
            maxpixelclustervals.append(np.amax(self.viewer.layers[i].data))
        fh.create_dataset('minmax', data=maxpixelclustervals, dtype='f8')
        self.maxpixelclustervals.append(maxpixelclustervals)

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
        fhdn = fh.create_dataset('data_normalized', shape=(numpixels, len(markerindices)), dtype='f8')
        fh.attrs['selmarkernames'] = markernames
        fh.attrs['totalpixels'] = numpixels * 1.0
        fh.attrs['imageslist'] = self.filenames

        # Determine whether to normalize, and initialize hdf5 file to use for normalization.
        if not (normalizeeach or normalizeall):
            normtype = None
        if not os.path.exists(os.path.join(self.outputfolder, "hdf5_files")):
            os.mkdir(os.path.join(self.outputfolder, "hdf5_files"))

        # Normalize each individual image according to the normalization type defined by the user.
        pixels = 0
        for i in range(self.numimgs):
            vdim = self.imageshapelist[i][0]
            hdim = self.imageshapelist[i][1]
            img = unnormalized[i, :vdim, :hdim, :]
            if normalizeeach:
                img = preprocess(outfolder, medianblur=True, gaussianblur=True, gaussianblurstd=1,
                                 img=da.from_array(img, chunks=10000), normtype=normtype).reshape(-1, img.shape[-1])
            img = img.reshape(-1, img.shape[-1])

            vaex.from_pandas(pd.DataFrame(img).astype('float32')).export_hdf5(
                os.path.join(self.outputfolder, 'hdf5_files', (f'analysis_{i:02}.hdf5')))
            fhdn[pixels:pixels + vdim * hdim, :] = img
            fhdr[pixels:pixels + vdim * hdim, :] = unnormalized[i, :vdim, :hdim, :].reshape((-1, img.shape[-1]))
            pixels += vdim * hdim

        df = vaex.open(os.path.join(self.outputfolder, "hdf5_files", "analysis_*.hdf5"))
        arr = df.to_arrays(array_type='list')
        percentlist = [np.percentile(a, 99) for a in arr]
        fh.attrs['percentile'] = percentlist

        # If normalizing across all images, apply z-score normalization on the entire image stack.
        if normalizeall:
            # Apply z-scale normalization.
            df = vaex.open(os.path.join(self.outputfolder, "hdf5_files", "analysis_*.hdf5"))
            scaler = vaex.ml.StandardScaler(features=df.column_names, prefix='scaled_')
            scaler.fit(df)
            normalized = scaler.transform(df)
            scaled_cols = [col for col in normalized.column_names if 'scaled_' in col]
            fhdn[:, :] = np.asarray(normalized[scaled_cols])

            # If specified by user, apply PCA normalization to the z-scale normalized data.
            if pca:
                npc = len(markerindices)
                if npc > 10:
                    pcanorm = vaex.ml.PCAIncremental(features=scaled_cols, n_components=npc, batch_size=10000000)
                else:
                    pcanorm = vaex.ml.PCA(features=scaled_cols, n_components=npc)
                pcanorm.fit(normalized, progress='widget')
                save_preprocess(pcanorm, self.outputfolder + "/vmodels", zscore=False, pca=True)
                df_trans = pcanorm.transform(normalized)
                PCA_cols = [col for col in df_trans.column_names if 'PCA_' in col]
                for batch in range(0, len(df_trans), 10000000):
                    bs = np.min((len(df_trans) - batch, 10000000))
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

    def load_environment(self,
                         envpath="",
                         ):
        """
        Open a directory for the user to load a previous RAPID GUI session to resume it exactly as they left it.

        envpath (str, optional): Path to the saved environment file being loaded (Default: "").

        :return: envpath *(str)*: \n
            Path to the saved environment file being loaded.
        """
        config = configparser.ConfigParser()

        if envpath == "":
            envpath = QFileDialog().getOpenFileName(filter="*.ini")[0]
            if envpath == "":
                return envpath

        p = "/".join(envpath.split("/")[:-1])
        imgpaths = glob.glob(p + "/*Layer*")
        order = [int(os.path.split(path)[-1].split("_")[-1]) for path in imgpaths]
        sorted = np.argsort(np.array(order))
        imgpaths = [imgpaths[i] for i in sorted]
        config.read(envpath)

        import time
        self.hasaddedtable = config.getboolean("Variables", 'hasaddedtable')
        self.haseditedimage = config.getboolean("Variables", 'haseditedimage')
        self.hasloadedpixel = config.getboolean("Variables", 'hasloadedpixel')
        self.hasloadedimage = config.getboolean("Variables", 'hasloadedimage')

        self.actionloggerpath = config.get("Variables", 'actionloggerpath')
        self.analysisindex = config.getint("Variables", 'analysisindex')
        self.analysismode = config.get("Variables", 'analysismode')
        self.biaxialcount = config.getint("Variables", 'biaxialcount')
        self.displayselectedcount = config.getint("Variables", 'displayselectedcount')
        self.editimagepath = config.get("Variables", 'editimagepath')
        self.numimgs = config.getint("Variables", 'numimgs')
        self.nummarkers = config.getint("Variables", 'nummarkers')
        self.objectclustercount = config.getint("Variables", 'objectclustercount')
        self.outputfolder = os.path.abspath(os.path.join(envpath, "../.."))
        self.pixelclustercount = config.getint("Variables", 'pixelclustercount')
        self.resolution = config.getfloat("Variables", 'resolution')
        self.segmentcount = config.getint("Variables", 'segmentcount')
        self.selectedregioncount = config.getint("Variables", 'selectedregioncount')
        self.tableimgcount = config.getint("Variables", 'tableimgcount')
        self.tableindex = config.getint("Variables", 'tableindex')
        self.umapcount = config.getint("Variables", 'umapcount')

        self.analysislog = ast.literal_eval(config.get("Variables", 'analysislog'))
        self.cellclustervals = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'cellclustervals'))]
        self.cellcoordinates = ast.literal_eval(config.get("Variables", 'cellcoordinates'))
        self.clusternames = ast.literal_eval(config.get("Variables", 'clusternames'))
        self.clustersarepixelbased = ast.literal_eval(config.get("Variables", 'clustersarepixelbased'))
        self.currenttableordersfiltered = ast.literal_eval(config.get("Variables", 'currenttableordersfiltered'))
        self.currenttableorderfull = ast.literal_eval(config.get("Variables", 'currenttableorderfull'))
        self.currentlyselected = ast.literal_eval(config.get("Variables", 'currentlyselected'))
        for i, step in enumerate(ast.literal_eval(config.get("Variables", 'currentstep'))):
            self.viewer.dims.set_current_step(i, step)

        self.currentverticalheaderlabels = np.array(
            ast.literal_eval(config.get("Variables", 'currentverticalheaderlabels')))
        ###
        self.datalist = ast.literal_eval(config.get("Variables", 'datalist'))
        self.editactions = ast.literal_eval(config.get("Variables", 'editactions'))
        self.filenames = ast.literal_eval(config.get("Variables", 'filenames'))
        self.imageisflipped = ast.literal_eval(config.get("Variables", 'imageisflipped'))
        ###
        self.fulltab = ast.literal_eval(config.get("Variables", 'fulltab'))
        self.groupslist = ast.literal_eval(config.get("Variables", 'groupslist'))
        self.groupsnames = ast.literal_eval(config.get("Variables", 'groupsnames'))
        self.histogramcounts = ast.literal_eval(config.get("Variables", 'histogramcounts'))
        self.imageshapelist = ast.literal_eval(config.get("Variables", 'imageshapelist'))
        ###
        self.labeledimgs = ast.literal_eval(config.get("Variables", 'labeledimgs'))
        self.fulltab = pd.DataFrame(self.fulltab)
        self.datalist = [np.array(d) for d in self.datalist]
        self.labeledimgs = [np.array(l) for l in self.labeledimgs]
        self.lowerboundslist = ast.literal_eval(config.get("Variables", 'lowerboundslist'))
        self.markers = ast.literal_eval(config.get("Variables", 'markers'))
        self.maximageshape = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'maximageshape'))]
        self.maxpixelclustervals = ast.literal_eval(config.get("Variables", 'maxpixelclustervals'))
        self.maxvals = ast.literal_eval(config.get("Variables", 'maxvals'))
        self.mergedimagespaths = ast.literal_eval(config.get("Variables", 'mergedimagespaths'))
        self.mergememmarkers = ast.literal_eval(config.get("Variables", 'mergememmarkers'))
        self.mergenucmarkers = ast.literal_eval(config.get("Variables", 'mergenucmarkers'))
        self.minvals = ast.literal_eval(config.get("Variables", 'minvals'))
        self.objectclustercolors = [np.array(l) for l in
                                    ast.literal_eval(config.get("Variables", 'objectclustercolors'))]
        self.objectclusterdfs = [pd.read_json(l) for l in ast.literal_eval(config.get("Variables", 'objectclusterdfs'))]
        for i in range(len(self.objectclusterdfs)):
            self.objectclusterdfs[i]["Cluster"] = [str(id) for id in self.objectclusterdfs[i]["Cluster"]]
        self.objectclusterdirectories = ast.literal_eval(config.get("Variables", 'objectclusterdirectories'))
        self.objectclusterindices = ast.literal_eval(config.get("Variables", 'objectclusterindices'))
        self.objectimgnames = ast.literal_eval(config.get("Variables", 'objectimgnames'))
        self.pixelclustercolors = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'pixelclustercolors'))]
        self.pixelclusterdirectories = ast.literal_eval(config.get("Variables", 'pixelclusterdirectories'))
        self.pixelclusterindices = ast.literal_eval(config.get("Variables", 'pixelclusterindices'))
        self.pixelclustermarkers = ast.literal_eval(config.get("Variables", 'pixelclustermarkers'))
        self.plotcoordinates = []
        coords = ast.literal_eval(config.get("Variables", 'plotcoordinates'))
        for i in range(len(coords)):
            self.plotcoordinates.append([np.array(l) for l in coords[i]])
        self.plotisumap = ast.literal_eval(config.get("Variables", 'plotisumap'))
        self.plotsegmentationindices = ast.literal_eval(config.get("Variables", 'plotsegmentationindices'))
        self.plotxmins = ast.literal_eval(config.get("Variables", 'plotxmins'))
        self.plotxmaxs = ast.literal_eval(config.get("Variables", 'plotxmaxs'))
        self.plotymins = ast.literal_eval(config.get("Variables", 'plotymins'))
        self.plotymaxs = ast.literal_eval(config.get("Variables", 'plotymaxs'))
        self.segmentationclusteringrounds = ast.literal_eval(config.get("Variables", 'segmentationclusteringrounds'))
        self.segmentationindices = ast.literal_eval(config.get("Variables", 'segmentationindices'))
        self.segmentationzarrpaths = ast.literal_eval(config.get("Variables", 'segmentationzarrpaths'))
        self.segmentcounts = ast.literal_eval(config.get("Variables", 'segmentcounts'))
        self.tableimagenames.remove('None')
        tableimagenames = ast.literal_eval(config.get("Variables", 'tableimagenames'))
        for name in tableimagenames:
            self.tableimagenames.append(name)
        self.totalnumcells = ast.literal_eval(config.get("Variables", 'totalnumcells'))
        self.upperboundslist = ast.literal_eval(config.get("Variables", 'upperboundslist'))

        for i in range(len(imgpaths)):
            fh = zarr.open("/".join(imgpaths[i].split("/")[:-1]))
            file = imgpaths[i].split("/")[-1]
            if file.startswith("Image"):
                data = np.array(fh[file])
                try:
                    cmap = Colormap(ColorArray([(0, 0, 0), (
                        fh[file].attrs["Colormap0"] / 255., fh[file].attrs["Colormap1"] / 255.,
                        fh[file].attrs["Colormap2"] / 255.)]))
                    self.viewer.add_image(data, contrast_limits=fh[file].attrs["CLRange"],
                                          gamma=fh[file].attrs["Gamma"],
                                          opacity=fh[file].attrs["Opacity"], colormap=cmap,
                                          visible=fh[file].attrs["Visible"],
                                          name=fh[file].attrs["Name"], blending="additive")
                    self.viewer.layers[fh[file].attrs["Name"]].contrast_limits = fh[file].attrs["CL"]
                except:
                    self.viewer.add_image(data, visible=fh[file].attrs["Visible"], name=fh[file].attrs["Name"],
                                          blending="additive")
            else:
                self.draw_shapes(fh[file].attrs["Data"],
                                 fh[file].attrs["ShapeType"],
                                 fh[file].attrs["Properties"],
                                 fh[file].attrs["Name"],
                                 fh[file].attrs["Text"],
                                 fh[file].attrs["FaceColor"])

        if self.hasaddedtable:
            self.hasaddedtable = False
            self.currenttabdata = np.array(ast.literal_eval(config.get("Variables", 'currenttabdata')))
            self.totalnumrows = config.getint("Variables", 'totalnumrows')
            self.tableorder = ast.literal_eval(config.get("Variables", 'tableorder'))
            header_names = []
            if not self.analysismode == "Segmentation":
                clusterindex, _ = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                annotationindex = [j for j, n in enumerate(self.clustersarepixelbased) if n == (self.analysismode == "Pixel")][clusterindex]
                header_names = self.clusternames[annotationindex]
            self.update_table(self.currenttabdata,
                              self.lowerboundslist[self.tableindex],
                              self.upperboundslist[self.tableindex],
                              self.totalnumrows,
                              self.tableorder,
                              headernames=header_names,
                              )
            self.isloadingenv = True
            self.tableparams += self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            self.sorttableimages.marker.choices = tuple(self.tableparams)
            self.sorttableimages.data.choices = self.tableimagenames
            self.sorttableimages.marker.value = config.get("Variables", 'tablecurrentmarker')
            self.sorttableimages.data.value = config.get("Variables", 'tablecurrentdata')
            self.sorttableimages.sort.value = config.get("Variables", 'tablecurrentsort')
            self.isloadingenv = False

        GUIUtils.log_actions(self.actionloggerpath, f"gui.load_environment(envpath=\"{envpath}\")")
        return envpath

    def load_object_clusters(self,
                             csvpath="",
                             segindex=None,
                             addgreyimg=None,
                             addcolorimg=None,
                             ):
        """
        Allow user to select a .csv file that they would like to use to load clusters for a given segmented image.

        Args:
            csvpath (str, optional): Path to the csv file containing cluster assignments for each cell (Default: None).
            segindex (int, optional): Index of segmentation round to be used for biaxial gating (Default: None).
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """

        # Define path to csv file with clustering results to be loaded, and read into a dataframe.
        if csvpath == "":
            loadcsv = GUIUtils.LoadObjectClusters()
            loadcsv.exec()
            if not loadcsv.OK:
                return
            csvpath = loadcsv.csvpath
        fulltab = pd.read_csv(csvpath)
        fulltab = fulltab.drop(fulltab.columns[0], axis=1)

        # Select segmentation iteration to be used for cluster assignments.
        if segindex is None:
            segindex = 0
            if len(self.objectimgnames) > 1:
                segmentedimage = GUIUtils.SelectSegmentedImage(self.objectimgnames)
                segmentedimage.exec()
                if not segmentedimage.OK:
                    return
                segindex = segmentedimage.imageindex
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][segindex] * self.numimgs

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        # Get the indices of all the columns to use from the segmented table.
        params = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        markerinds = [params.index(mname) for mname in fulltab.columns[5:]]
        # [markerinds.append(params.index(mname) + 1) for mname in fulltab.columns[6:]]

        # Retrieve quantified expression of each of the included cell markers for each cell.
        complete_tab = []
        startind = segindex * self.numimgs
        for tab_len in range(self.numimgs):
            complete_tab.append(self.datalist[self.segmentationindices[tab_len + startind]][:, markerinds])
        complete_tab = np.vstack(complete_tab)

        # Only can load clusters if there are the same number of cells.
        if len(fulltab) != len(complete_tab):
            GUIUtils.display_error_message("Incompatible number of cells",
                                           "Please make sure the table you selected corresponds to the segmented image")
            return

        # Store the loaded clustering results and save to the current output folder.
        self.objectclusterdfs.append(fulltab)
        outfolder = GUIUtils.create_new_folder('RAPIDObject_', self.outputfolder)
        fulltab.to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))

        # Update the segmented data table to include the new cluster IDs for each cell.
        to_values = fulltab['Cluster']
        vals = list(copy.deepcopy(np.unique(to_values)))

        unique = np.unique(to_values)
        for i in range(len(unique)):
            to_values[to_values == unique[i]] = i + 1
        fulltab['Cluster'] = to_values

        # Retrieve relevant columns from relabeled table.
        relabeled_table = fulltab.iloc[:, [i for i in range(3, fulltab.shape[1])]]

        # Initialize data array for clustered image, and generate the colormap.
        relabeledgreyimages = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)
        color = generate_colormap(len(np.unique(to_values)) + 1)
        self.objectclustercolors.append(color[:-1, :])
        np.save(os.path.join(outfolder, "color.npy"), color)
        fullclusterdata = []
        startindex = 0
        for i in range(self.numimgs):
            # Get name of current image
            imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]

            # Relabel the segmented result for the current image and save it to the output folder.
            numcells = len(self.datalist[self.segmentationindices[i + startind]])
            from_values = np.arange(1, 1 + numcells)
            tmp_to_values = to_values[startindex:startindex + numcells].values
            self.cellclustervals.append(copy.deepcopy(tmp_to_values))
            relabeled = self.method_searchsort(from_values, tmp_to_values,
                                               self.labeledimgs[analysisnum + i].flatten().astype(int))
            relabeledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = relabeled.reshape(
                (self.imageshapelist[i][0], self.imageshapelist[i][1])).astype(np.uint8)
            relabeledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]][
                self.labeledimgs[analysisnum + i] == 0] = 0
            GUIUtils.save_img(os.path.join(outfolder, f"ObjectClusterLabels_{imgname}.tif"),
                              relabeledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1,
                              self.imageisflipped[i])

            # Apply the colormap to the relabeled image and save it to the output folder.
            relabeledimages = np.zeros((self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)
            for j in range(len(vals)):
                relabeledimages[:, :, 0][relabeledgreyimages[i, :, :] == j + 1] = color[j][0]
                relabeledimages[:, :, 1][relabeledgreyimages[i, :, :] == j + 1] = color[j][1]
                relabeledimages[:, :, 2][relabeledgreyimages[i, :, :] == j + 1] = color[j][2]

            GUIUtils.save_img(os.path.join(outfolder, f"ObjectClusters_{imgname}.tif"),
                              relabeledimages[:self.imageshapelist[i][0], :self.imageshapelist[i][1], :],
                              self.imageisflipped[i])

            # Add the relabeled colored and/or greyscale image(s) to the viewer.
            if i == 0:
                self.set_invisible(self.viewer)
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabeledimages.dtype)
                relab[0, :len(relabeledimages), :relabeledimages.shape[1], :] = relabeledimages
                if addgreyimg:
                    self.viewer.add_image(relabeledgreyimages[[i], :, :],
                                          name=f"Object Cluster IDs {self.objectclustercount + 1}", blending="additive",
                                          contrast_limits=(0, np.max(relabeledgreyimages)))
                if addcolorimg:
                    self.viewer.add_image(relab, name=f"Object Clusters {self.objectclustercount + 1}",
                                          blending="additive")
            else:
                relab = np.zeros((1, self.maximageshape[0], self.maximageshape[1], 3), dtype=relabeledimages.dtype)
                relab[0, :len(relabeledimages), :relabeledimages.shape[1], :] = relabeledimages
                if addgreyimg and addcolorimg:
                    self.viewer.layers[-2].data = np.vstack(
                        (self.viewer.layers[-2].data, relabeledgreyimages[[i], :, :]))
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))
                elif addgreyimg:
                    self.viewer.layers[-1].data = np.vstack(
                        (self.viewer.layers[-1].data, relabeledgreyimages[[i], :, :]))
                elif addcolorimg:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, relab))

            # Take the quantified values from only the cells in the current image.
            tmp_tab = relabeled_table[startindex:startindex + len(self.datalist[self.segmentationindices[i]])].values
            tmp_tab_df = pd.DataFrame(tmp_tab)
            startindex += len(self.datalist[self.segmentationindices[i]])

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

            self.datalist.append(clusteravgs[:, 2:].astype(np.float))

            self.currenttableordersfiltered.append(list(range(len(clusteravgs))))
            tab = clusteravgs[np.unique(tmp_to_values.astype(np.uint8) - 1), 2:]
            minvals = []
            maxvals = []
            for i in range(tab.shape[1] - 1):
                minvals.append(np.min(tab[:, i + 1]))
                maxvals.append(np.max(tab[:, i + 1]))
            self.minvals.append(copy.deepcopy(minvals))
            self.maxvals.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))

        # Find weighted average data and update lower/upper bounds.
        fullclusterdata = np.nan_to_num((np.vstack(fullclusterdata)))
        if self.numimgs > 1:
            weighted_average = np.zeros((len(np.unique(to_values)), fullclusterdata.shape[1] - 2))
            for i in range(len(fullclusterdata)):
                currcluster = i % len(weighted_average)
                weighted_average[currcluster, 0] += fullclusterdata[i, 2]
            for i in range(len(fullclusterdata)):
                currcluster = i % len(weighted_average)
                weighted_average[currcluster, 1:] += fullclusterdata[i, 3:] * fullclusterdata[i, 2] / weighted_average[
                    currcluster, 0]
            self.datalist.append(weighted_average)
            self.currenttableordersfiltered.append(list(range(len(weighted_average))))
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            self.minvals.append(copy.deepcopy(minvals))
            self.maxvals.append(copy.deepcopy(maxvals))
            self.lowerboundslist.append(copy.deepcopy(minvals))
            self.upperboundslist.append(copy.deepcopy(maxvals))

        # Relabel the segmented images with cluster IDs.
        for i in range(self.numimgs):
            relabeledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]][
                self.labeledimgs[analysisnum + i] == 0] = 0
        unique = np.unique(relabeledgreyimages)
        for i in range(len(unique)):
            relabeledgreyimages[relabeledgreyimages == unique[i]] = i
        self.labeledimgs += [
            GUIUtils.convert_dtype(relabeledgreyimages[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]]) for i
            in range(len(relabeledgreyimages))]

        # Save the dataset to the output folder as a csv file.
        mergemarkerlist = list(fulltab.columns[4:].values)
        clusterdf = pd.DataFrame(np.nan_to_num(fullclusterdata))
        clusterdf.columns = np.hstack([["Sample", "Cluster", "# Cells"], mergemarkerlist])
        clusterdf.to_csv(os.path.join(outfolder, "ObjectClusterAvgExpressionVals.csv"))

        # Generate MST plot for the clustered data.
        tabledata, datascaled, DistMatrix, uniqueClusters = \
            prep_for_mst(clustertable=clusterdf,
                         minclustersize=1,
                         clustersizes=clusterdf["# Cells"],
                         includedmarkers=mergemarkerlist,
                         )
        generate_mst(distancematrix=DistMatrix,
                     normalizeddf=datascaled[datascaled.columns],
                     colors=color,
                     randomseed=0,
                     outfolder=outfolder,
                     clusterheatmap=True,
                     displaymarkers=mergemarkerlist,
                     uniqueclusters=uniqueClusters,
                     samplenames=list(np.unique(clusterdf['Sample'])),
                     displaysingle=False,
                     values="# Cells",
                     )
        self.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                              name=f"Object Clusters {self.objectclustercount + 1} Heatmap",
                              blending="additive",
                              visible=False,
                              )

        # Update the table widget dropdown options.
        for i in range(self.numimgs):
            self.tableimagenames.append(
                f"Object Cluster {self.objectclustercount + 1} - {self.filenames[i].split('/')[-1]}")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
            self.currentlyselected.append([])
        if self.numimgs > 1:
            self.tableimagenames.append(f"Object Cluster {self.objectclustercount + 1} - Combined Average")
            self.objectclusterindices.append(self.tableimgcount)
            self.tableimgcount += 1
            self.currentlyselected.append([])

        # Update any necessary variables.
        self.segmentationclusteringrounds[0].append(self.objectclustercount)
        self.objectclustercount += 1
        self.analysislog.append("O")
        self.clustersarepixelbased.append(False)
        self.clusternames.append([])
        self.updatelogfile = False
        self.sorttableimages.data.choices = tuple(self.tableimagenames)
        self.sorttableimages.data.value = f"Object Cluster {self.objectclustercount} - {self.filenames[0].split('/')[-1]}"
        self.sorttableimages.reset_choices()
        self.updatelogfile = True
        GUIUtils.log_actions(self.actionloggerpath, f"gui.load_object_clusters(csvpath=\"{csvpath}\", "
                                                    f"segindex={segindex}, addgreyimg={addgreyimg}, "
                                                    f"addcolorimg={addcolorimg})")

    def load_pixel_results(self,
                           datapath="",
                           outputfolder="",
                           addgreyimg=None,
                           addcolorimg=None,
                           ):
        """
        Open a directory for the user to select which pixel-based results they would like to load.

        Args:
            datapath (str, optional): Path to data folder with RAPID results being loaded (Default: "").
            outputfolder (str, optional): Path to output folder where results will be saved (Default: "").
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).

        :return: datapath *(str)*: \n
            Path to data folder with RAPID results being loaded.
        """
        # User cannot load pixel-based results multiple times due to potential image incompatibility.
        if self.hasloadedpixel:
            GUIUtils.display_error_message("Results already loaded",
                                           "You have already loaded results. Please open another window if you would like to load different data")
            return ""

        # Prompt user to indicate the path to the results being loaded, and ensure the selected path contains compatible
        # RAPID-P results.
        if datapath == "":
            datapath = QFileDialog().getExistingDirectory(None, "Select Folder")
            if datapath == "":
                return ""
            if not datapath.endswith("/RAPID_Data"):
                datapath = os.path.join(datapath, "RAPID_Data")

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        inputzarr = zarr.open(datapath, mode='r')
        color, data, grey, imageshapelist, minmax, prob, tab, filenames, selmarkernames, totalpixels, \
        percentile, columns, arg, flipimg = self.load_pixel_zarr(inputzarr)

        # Prompt user to indicate the root folder where new results will be saved.
        if outputfolder == "":
            GUIUtils.OKButtonPopup("Select Output Folder").exec()
            dialog = QFileDialog()
            outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
        self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
        self.actionloggerpath = GUIUtils.initialize_logger(self.outputfolder,
                                                           pixel_results_path=datapath,
                                                           add_color_img=addcolorimg,
                                                           add_grey_img=addgreyimg,
                                                           )
        self.viewer.status = "Loading analysis..."

        # Save image attributes to the output folder.
        outfolder = GUIUtils.create_new_folder("RAPIDPixel_", self.outputfolder)
        self.pixelclusterdirectories.append(outfolder)

        paths = glob.glob(os.path.join(os.path.split(datapath)[0], "*"))
        paths.remove(os.path.join(datapath))
        for path in paths:
            shutil.copy(path, os.path.join(outfolder, os.path.split(path)[-1]))

        datafolder = os.path.join(outfolder, "RAPID_Data")
        outputzarr = zarr.open(datafolder, 'w')
        outputzarr['color'] = color
        outputzarr['data'] = data
        outputzarr['grey'] = grey
        outputzarr['imageshapelist'] = imageshapelist
        outputzarr['minmax'] = minmax
        outputzarr['prob'] = prob
        outputzarr['tab'] = tab
        outputzarr['tab'].attrs['columns'] = columns
        outputzarr.attrs['imageslist'] = filenames
        outputzarr.attrs['selmarkernames'] = selmarkernames
        outputzarr.attrs['totalpixels'] = totalpixels
        outputzarr.attrs['percentile'] = percentile
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
        greyflattened, tab, col_list = inputzarr["grey"][:], inputzarr["tab"][:], inputzarr["color"][:]
        self.numimgs = len(imagenums)
        args = runRAPIDzarr.get_parameters()
        args.ncluster = int(len(tab) / len(imgnames))

        # Load cell marker names and store them where applicable.
        self.markers = inputzarr.attrs['selmarkernames']
        self.pixelclustermarkers.append(self.markers)
        self.nummarkers = len(self.markers)
        for name in self.markers:
            self.tableparams.append(name)
        for name in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
            self.tableparams.append(name)

        # Add raw images to the GUI, only for those that have been included by the user.
        vdim = max([s[0] for s in imageshapelist])
        hdim = max([s[1] for s in imageshapelist])
        self.maximageshape = np.array([vdim, hdim])
        colors = generate_colormap(self.nummarkers + 1)
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
        self.imageisflipped = [inputzarr.attrs['flipimg'][i] for i in imagenums]
        self.maxpixelclustervals.append(list(inputzarr['minmax'][:]))
        if not max(self.maxpixelclustervals[0]) > 1.0:
            self.maxpixelclustervals[0] = [a * 255. for a in self.maxpixelclustervals[0]]
        self.markernums = [i for i in range(len(self.markers))]
        self.analysismode = "Pixel"
        self.labeledimgs += [GUIUtils.convert_dtype(greyimgs[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]])
                             for i in range(len(greyimgs))]
        self.analysislog.append("P")

        self.apply_pixel_clustering(tab, args, col_list, selectimagesadded.grey, selectimagesadded.color, outfolder)
        self.viewer.dims.set_current_step(0, 0)
        self.pixelclustercount += 1
        self.clusternames.append([])
        self.updatelogfile = False
        self.sorttableimages.reset_choices()
        self.updatelogfile = True
        self.hasloadedpixel = True

        return datapath

    def load_pixel_zarr(self,
                        zarrpath,
                        ):
        """
        Load all necessary zarr files when loading pixel-based clustering results.

        Args:
            zarrpath (str): Path to the root directory where zarr files are being loaded from.

        :return: *(tuple)*: \n
            Tuple of zarr attributes that must be loaded when loading pixel-based clustering results.
        """
        return zarrpath['color'], zarrpath['data'], zarrpath['grey'], zarrpath['imageshapelist'], zarrpath['minmax'], \
               zarrpath['prob'], zarrpath['tab'], zarrpath.attrs['imageslist'], zarrpath.attrs['selmarkernames'], \
               zarrpath.attrs['totalpixels'], zarrpath.attrs['percentile'], zarrpath['tab'].attrs['columns'], \
               zarrpath.attrs['arg'], zarrpath.attrs['flipimg']

    def load_segmentation_results(self,
                                  filenames=[],
                                  outputfolder="",
                                  quant_avg=None,
                                  addgreyimg=None,
                                  addcolorimg=None,
                                  ):
        """
        Open a directory for the user to select which segmentation results they would like to load.

        Args:
            filenames (list, optional): List of paths to segmentation label images being loaded (Default: []).
            outputfolder (str, optional): Path to folder where results will be saved (Default: "").
            quant_avg (bool): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values.
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).

        :return: filenames *(list)*: \n
            List of paths to the labeled segmented images being loaded. Return False if no files are selected.
        """

        # Prompt user to select labeled image to load.
        if filenames == []:
            filenames, _ = QFileDialog.getOpenFileNames(parent=self.viewer.window.qt_viewer,
                                                        caption='Select Label image', )
            if len(filenames) == 0:
                return False

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        # Allow user to define wither to quantify using mean expression, or root-mean-square.
        if quant_avg is None:
            quantmode = GUIUtils.QuantificationMode()
            quantmode.exec()
            if not quantmode.OK:
                return
            quant_avg = quantmode.avg

        # Prompt user to choose path to output folder where data will be saved.
        if outputfolder == "":
            GUIUtils.OKButtonPopup("Select Output Folder").exec()
            dialog = QFileDialog()
            outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
        self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
        outfolder = GUIUtils.create_new_folder("Segmentation", self.outputfolder)
        self.actionloggerpath = GUIUtils.initialize_logger(self.outputfolder,
                                                           segmentation_file_names=filenames,
                                                           quant_avg=quant_avg,
                                                           addcolorimg=addcolorimg,
                                                           addgreyimg=addgreyimg,
                                                           )

        # Automatically load images from saved zarr files if using results from RAPID.
        if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "RawImages")):
            # Copy zarr files for segmented image being loaded to new output folder.
            shutil.copytree(os.path.join(os.path.split(filenames[0])[0], "RawImages"),
                            os.path.join(outfolder, "RawImages"),
                            )
            if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "MergedImage")):
                shutil.copytree(os.path.join(os.path.split(filenames[0])[0], "MergedImage"),
                                os.path.join(outfolder, "MergedImage"),
                                )
            if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "Features0")):
                features_paths = glob.glob(os.path.join(os.path.split(filenames[0])[0], "Features*"))
                for features_path in features_paths:
                    shutil.copytree(features_path,
                                    os.path.join(outfolder, os.path.split(features_path)[-1]),
                                    )

            # Retrieve raw image data and attributes from saved zarr file.
            rootfold = os.path.join(os.path.split(filenames[0])[0], "RawImages")
            subfolders = glob.glob(rootfold + "/*")
            subfolders.sort()
            fh = zarr.open(rootfold)
            self.nummarkers = len(subfolders)
            self.hasloadedimage = True
            self.filenames = fh.attrs['filenames']
            self.maximageshape = np.array(fh.attrs['maximageshape'])
            self.imageshapelist = fh.attrs['imageshapelist']
            self.markers = fh.attrs['markers']
            self.markernums = fh.attrs['markernums']
            self.numimgs = len(filenames)

            # Store file names.
            d = {}
            for name in self.filenames:
                n = os.path.split(name)[-1]
                d[n] = n
            self.groupslist.append(d)
            newfilenames = [fn for fn in self.filenames if
                            os.path.split(fn)[-1].split(".")[0] in [os.path.split(fn)[-1].split(".")[0][16:] for fn in
                                                                    filenames]]
            imginds = [self.filenames.index(fn) for fn in newfilenames]
            self.filenames = newfilenames

            # Add raw image data to the viewer.
            for i in range(self.nummarkers):
                file = os.path.split(subfolders[i])[-1]
                data = np.array(fh[file])
                cmap = Colormap(ColorArray([(0, 0, 0), (fh[file].attrs["Colormap0"] / 255.,
                                                        fh[file].attrs["Colormap1"] / 255.,
                                                        fh[file].attrs["Colormap2"] / 255.)]))
                self.viewer.add_image(data[imginds, :, :], contrast_limits=fh[file].attrs["CLRange"],
                                      gamma=fh[file].attrs["Gamma"], opacity=fh[file].attrs["Opacity"],
                                      colormap=cmap, visible=fh[file].attrs["Visible"], name=fh[file].attrs["Name"],
                                      blending="additive")
                self.viewer.layers[fh[file].attrs["Name"]].contrast_limits = fh[file].attrs["CL"]

            # Add merged image data to the viewer.
            fh = zarr.open(os.path.join(os.path.split(filenames[0])[0]))
            mergedimg = np.array(fh["MergedImage"])
            if len(np.unique(mergedimg[0, imginds, :, :])) == 1:
                self.viewer.add_image(mergedimg[1, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                      blending="additive")
            elif len(np.unique(mergedimg[1, imginds, :, :])) == 1:
                self.viewer.add_image(mergedimg[0, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                      blending="additive")
            else:
                self.viewer.add_image(mergedimg[:, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                      blending="additive")

            # Load segmented label images.
            self.tableparams += self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            self.sorttableimages.marker.choices = tuple(self.tableparams)

        # Prompt user to load raw image files if loading results that were not generated using RAPID.
        else:
            # Open selected images.
            GUIUtils.OKButtonPopup("Open Raw Images").exec()
            openedimgs = self.open_images(filenames)
            if not openedimgs:
                return False

            # Sort file names and segmented image names to be consistent with each other and alphabetical.
            imgfilenames = [os.path.split(name)[-1].split(".")[0] for name in self.filenames]
            fnames = copy.deepcopy(imgfilenames)
            fnames.sort()
            orders = [fnames.index(name) for name in imgfilenames]
            origimgnames = [fnames[i] for i in orders]
            filenames.sort()
            filenames = [filenames[i] for i in orders]
            for i in range(len(origimgnames)):
                # Make sure image names correspond to segmented images
                filename = os.path.split(filenames[i])[-1].split(".")[0]
                if not origimgnames[i] in os.path.split(filenames[i])[-1].split(".")[0]:
                    GUIUtils.display_error_message("Mismatching image names",
                                                   "Please ensure the raw images correspond to the segmented "
                                                   "image and are named consistently. Acceptable segmented "
                                                   "image names are in the format \"[prefix][Raw Image Name]"
                                                   "[Suffix], with the prefix and suffix consistent across all "
                                                   "images\"")
                    for j in range(len(self.viewer.layers)):
                        self.viewer.layers.pop(0)
                    self.groupslist = []
                    self.hasloadedimage = False
                    self.imageshapelist = []
                    self.numimgs = 0
                    return

                # Make sure all segmented image names have the same prefix and suffix.
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
                        for j in range(len(self.viewer.layers)):
                            self.viewer.layers.pop(0)
                        self.groupslist = []
                        self.hasloadedimage = False
                        self.imageshapelist = []
                        self.numimgs = 0
                        return

        self.apply_segmentation(addgreyimg,
                                addcolorimg,
                                quant_avg,
                                outfolder,
                                loadedresultspaths=filenames,
                                )

        return filenames

    def manual_annotation(self,
                          umapind=None,
                          addgreyimg=None,
                          addcolorimg=None,
                          labelnames=[],
                          shapeverts=[],
                          shapetypes=[],
                          ):
        """
        Allow user to draw shapes on a UMAP plot to define clusters, with each shape corresponding to a cluster.

        Args:
            umapind (int, optional): Index of UMAP plot being annotated (Default: None).
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            labelnames (list, optional): List of names for the clusters corresponding to each shape (Default: []).
            shapeverts (list, optional): List of vertices for each shape drawn by the user (Default: []).
            shapetypes (list, optional): List of geometries for each shape drawn by the user (Default: []).
        """
        # Ensure there is at least one UMAP plot to annotate.
        if self.umapcount == 1:
            GUIUtils.display_error_message("No UMAP detected",
                                           "You must first generate a UMAP in order to select cells to be displayed")
            return

        # Prompt user to select which UMAP plot they would like to use if more than one have been generated.
        if umapind is None:
            umapind = 0
            umapplots = [b for b in self.plotisumap if b]
            if len(umapplots) > 1:
                selectplot = GUIUtils.BiaxialUMAPIterations(umapplots)
                selectplot.exec()
                if not selectplot.OK:
                    return
                umapind = selectplot.iteration

        # Determine which plot index this corresponds to, factoring in biaxial plots.
        inds = [i for i, x in enumerate(self.plotisumap) if x]
        it = inds[umapind]
        self.viewer.status = "Annotating UMAP"

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        if shapeverts == [] or shapetypes == []:
            # Ensure there is at least one shape drawn in order to define the region to be quantified.
            ind = -1
            for i in reversed(range(len(self.viewer.layers))):
                if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and self.viewer.layers[
                    i].visible:
                    ind = i
                    break
            if ind == -1:
                GUIUtils.display_error_message("Please draw a shape first",
                                               "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
                return

            # Keep track of the bounding box vertices and geometries of each shape.
            shapeverts = [self.viewer.layers[ind].data[i][:, -2:] for i in range(len(self.viewer.layers[ind].data))]
            shapetypes = [self.viewer.layers[ind].shape_type[i] for i in range(len(self.viewer.layers[ind].data))]
            self.viewer.layers.pop(ind)
        else:
            shapeverts = [np.array(verts) for verts in shapeverts]

        # Label each shape and adjust their colors.
        labels = []
        for i in range(len(shapeverts)):
            labels.append(f"Region {i + 1}")
        properties = {'class': labels, }
        text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
        self.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, face_color=[np.array([0.2, 0.2, 0.2])],
                               name="Manual Annotation", properties=properties, text=text_properties)

        # Allow user to name the different regions and add them as labels to the shapes.
        if labelnames == []:
            regionnamespopup = GUIUtils.ManualAnnotationPopup(len(shapeverts))
            regionnamespopup.exec()
            if regionnamespopup.OK:
                labelnames = list(regionnamespopup.headernames)
                if not labelnames == labels:
                    self.viewer.layers.pop(len(self.viewer.layers) - 1)
                    properties = {'class': labelnames, }
                    text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    self.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, name="Manual Annotation",
                                           properties=properties, text=text_properties,
                                           face_color=[np.array([0.2, 0.2, 0.2])])
                labelnames += ["Other"]
            else:
                self.viewer.layers.pop(len(self.viewer.layers) - 1)
                return
        else:
            self.viewer.layers.pop(len(self.viewer.layers) - 1)
            properties = {'class': [name for name in labelnames if name != "Other"], }
            text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
            self.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, name="Manual Annotation",
                                   properties=properties, text=text_properties,
                                   face_color=[np.array([0.2, 0.2, 0.2])])

        # Create a new output folder to save output files to.
        outputpath = GUIUtils.create_new_folder("RAPIDObject_", self.outputfolder)
        self.objectclusterdirectories.append(outputpath)
        self.set_invisible(self.viewer)

        # Initialize list of arrays of cell IDs for each cluster ID.
        clusterids = [np.zeros(len(v)) for v in self.plotcoordinates[it]]

        # Find the cells corresponding to the vertices within each of the shapes to define clusters.
        for shape in range(len(shapeverts)):
            # Scale the vertices from 0-1 to map to coordinates on the plot.
            tupverts = copy.deepcopy(shapeverts[shape])
            tupverts[:, 0] = ((self.plotxmaxs[it] - tupverts[:, 0]) / (
                    self.plotxmaxs[it] - self.plotxmins[it])) * 1.1 - 0.05
            tupverts[:, 1] = ((tupverts[:, 1] - self.plotymins[it]) / (
                    self.plotymaxs[it] - self.plotymins[it])) * 1.1 - 0.05
            tupverts[:, [0, 1]] = tupverts[:, [1, 0]]
            tupverts = [tuple(x) for x in tupverts.tolist()]
            p = self.create_shape_path(tupverts, shapetypes[shape])
            for i in range(self.numimgs):
                # Find the vertices on the plot within the shape, and the cells corresponding to those vertices.
                rows = list(p.contains_points(self.plotcoordinates[it][i]))
                rows = [i for i, b in enumerate(rows) if b]
                clusterids[i][rows] = shape + 1

        # All remaining cells not within any of the shapes will be in one additional cluster together.
        for i in range(self.numimgs):
            for j in range(len(clusterids[i])):
                if clusterids[i][j] == 0:
                    clusterids[i][j] = len(shapeverts) + 1
        clusterids = np.hstack(clusterids)

        tabindex = self.plotsegmentationindices[it]
        # Stack segmented data tables for each image
        segmentedtab = []
        for i in range(self.numimgs):
            segmentedtab.append(self.datalist[self.segmentationindices[i + tabindex]])
        segmentedtab = np.vstack(segmentedtab)

        if np.max(clusterids) < len(labelnames):
            labelnames.remove("Other")
        self.clusternames.append(labelnames)

        self.apply_object_clustering(clusterids, tabindex, segmentedtab, outputpath, addcolorimg, addgreyimg,
                                     labelnames)

        GUIUtils.log_actions(self.actionloggerpath, f"gui.manual_annotation(umapind={umapind}, "
                                                    f"addgreyimg={addgreyimg}, addcolorimg={addcolorimg}, "
                                                    f"labelnames={labelnames}, "
                                                    f"shapeverts={[verts.tolist() for verts in shapeverts]}, "
                                                    f"shapetypes={shapetypes})")

    def merge_clusters(self,
                       checked=[],
                       addgreyimg=None,
                       addcolorimg=None,
                       ):
        """
        Merge together all clusters that are checked in the currently-displayed table.

        Args:
            checked (list, optional): List of cluster IDs that are currently checked in the table (Default: []).
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """
        # Can't merge cells together, only clusters.
        if self.analysismode == "Segmentation":
            GUIUtils.display_error_message("Cannot merge cells together",
                                           "Please ensure that the table being displayed represents clusters, not cells.")
            return

        # One table for each image, plus a combined average table if using multiple images.
        analysisnum, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)

        # Sort the selected clusters in descending order for easier re-indexing, and ensure multiple
        # clusters are selected.
        if checked == []:
            checked = self.currentlyselected[self.tableindex]
        checked.sort(reverse=True)
        if len(checked) <= 1:
            GUIUtils.display_error_message("Fewer than 2 clusters selected",
                                           "Please select at least 2 clusters from the table to be merged together.")
            return

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        GUIUtils.log_actions(self.actionloggerpath, f"gui.merge_clusters(checked={checked}, addgreyimg={addgreyimg}, "
                                                    f"addcolorimg={addcolorimg})")

        # If the user is merging pixel-based clusters.
        if self.analysismode == "Pixel":
            numclusters = len(self.datalist[self.tableindex]) - len(checked) + 1
            numcols = self.datalist[self.tableindex].shape[1] + 2
            fulltab = np.zeros((self.numimgs * numclusters, numcols))
            # Remove the checked clusters from the table and merge them together as a new entry at the end.
            count = 0
            for i in range(numtabs):
                data = copy.deepcopy(self.datalist[self.pixelclusterindices[analysisnum * numtabs + i]])
                table = np.zeros((len(data) + 1, data.shape[1]))
                table[:len(data), :] = data
                table[len(data), 0] = np.sum(data[checked, 0])
                if table[len(data), 0] > 0:
                    table[len(data), 1:] = np.average(data[checked, 1:], axis=0, weights=data[checked, 0])
                else:
                    table[len(data), 1:] = np.zeros_like(table[len(data), 1:])
                notremoved = [j for j in range(len(table)) if j not in checked]
                self.datalist[self.pixelclusterindices[analysisnum * numtabs + i]] = table[notremoved, :]
                if i < self.numimgs:
                    fulltab[count:count + len(notremoved), 0] = i + 1
                    fulltab[count:count + len(notremoved), 1] = np.arange(1, len(notremoved) + 1)
                    fulltab[count:count + len(notremoved), 2:] = table[notremoved, :]
                    count += len(notremoved)
            my_data = pd.DataFrame(np.nan_to_num((np.vstack(fulltab))))

            # Save updated table to output folder.
            markernames = self.pixelclustermarkers[analysisnum]
            my_data.columns = np.hstack([["Sample", "Cluster", "# Pixels"], markernames])
            outfolder = GUIUtils.create_new_folder(
                os.path.join(os.path.split(self.pixelclusterdirectories[analysisnum])[-1], "Merged_"),
                self.outputfolder)
            my_data.to_csv(os.path.join(outfolder, "PixelClusterAvgExpressionVals.csv"))

            ind = [i for i, m in enumerate(self.clustersarepixelbased) if m][analysisnum]

            # Update the labeled image such that the clusters are merged at the end, removed, and relabeled.
            imganalysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][
                                 self.analysisindex // numtabs] * self.numimgs
            labelimg = self.concat_label_imgs(
                [self.labeledimgs[ind] for ind in range(imganalysisnum, imganalysisnum + self.numimgs)],
                pixelbased=True)
            newclusterval = int(np.max(labelimg) + 1)

            clusterorder = self.currenttableordersfiltered[self.tableindex]
            clusterorderfull = self.currenttableorderfull

            if not self.clusternames[ind] == []:
                newname = self.clusternames[ind][checked[-1]]
                for cluster in checked:
                    self.clusternames[ind].pop(cluster)
                self.clusternames[ind].append(newname)

            for cluster in checked:
                labelimg[labelimg == cluster + 1] = newclusterval
                labelimg[labelimg > cluster + 1] = labelimg[labelimg > cluster] - 1
                newclusterval -= 1

                clusterorder.remove(cluster)
                clusterorder = np.array(clusterorder)
                clusterorder[clusterorder > cluster - 1] -= 1
                clusterorder = list(clusterorder)

                clusterorderfull.remove(cluster)
                clusterorderfull = np.array(clusterorderfull)
                clusterorderfull[clusterorderfull > cluster - 1] -= 1
                clusterorderfull = list(clusterorderfull)

                index = f"Cluster {cluster + 1} (Pixel [{analysisnum}])"
                for i in reversed(range(len(self.viewer.layers))):
                    if self.viewer.layers[i].name == index:
                        self.viewer.layers.pop(i)
                        break

            clusterorder.append(newclusterval - 1)
            clusterorderfull.append(newclusterval - 1)
            self.currenttableordersfiltered[self.tableindex] = clusterorder
            self.currenttableorderfull = clusterorderfull

            for i in range(len(labelimg)):
                self.labeledimgs[imganalysisnum + i] = labelimg[i, :self.imageshapelist[i][0],
                                                       :self.imageshapelist[i][1]].astype(
                    self.labeledimgs[imganalysisnum + i].dtype) - 1

            # Create a colored image from the newly-labeled image, and add it to the viewer.
            newrgb = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], 3)).astype(np.uint8)

            color = self.pixelclustercolors[analysisnum]
            newcolor = color[[checked[-1]], :]
            color = np.delete(color, checked, 0)
            color = np.append(color, newcolor, 0)
            self.pixelclustercolors[analysisnum] = color
            for j in range(len(color)):
                newrgb[labelimg == j + 1] = color[j, :]

            np.save(os.path.join(outfolder, "color.npy"), color)
            samplenames = [os.path.splitext(os.path.split(imgname)[-1])[0] for imgname in self.filenames]
            tabledata, my_data_scaled, DistMatrix, uniqueClusters = prep_for_mst(clustertable=my_data,
                                                                                 minclustersize=1000,
                                                                                 clustersizes=my_data["# Pixels"],
                                                                                 includedmarkers=markernames)
            generate_mst(distancematrix=DistMatrix,
                         normalizeddf=my_data_scaled[my_data_scaled.columns],
                         colors=color,
                         randomseed=0,
                         outfolder=outfolder,
                         clusterheatmap=True,
                         displaymarkers=markernames,
                         uniqueclusters=uniqueClusters,
                         samplenames=samplenames,
                         displaysingle=False,
                         )

            # Add image(s) to the viewer
            self.set_invisible(self.viewer)
            if addgreyimg:
                self.viewer.add_image(labelimg, name=f"Merged Pixel Cluster IDs {analysisnum}", blending="additive",
                                      contrast_limits=[0, np.max(labelimg)])
            if addcolorimg:
                self.viewer.add_image(newrgb, name=f"Merged Pixel Clusters {analysisnum}", blending="additive")

            self.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                                  name=f"Merged Pixel Clusters {analysisnum} Heatmap",
                                  blending="additive",
                                  visible=False,
                                  )

            for i in range(self.numimgs):
                imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]
                GUIUtils.save_img(os.path.join(outfolder, f"PixelClusters_{imgname}.tif"),
                                  newrgb[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1], :],
                                  self.imageisflipped[i])
                GUIUtils.save_img(os.path.join(outfolder, f"PixelClusterLabels_{imgname}.tif"),
                                  labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1,
                                  self.imageisflipped[i])
            self.viewer.layers[-1].visible = True

            # Reset the current selected cells for each of the corresponding tables to be empty.
            pixelclusterindex = self.pixelclusterindices.index(self.tableindex)
            startind = self.tableindex - pixelclusterindex % numtabs
            for i in range(startind, startind + numtabs):
                self.currentlyselected[i] = []

            newdisplaydata = self.datalist[self.tableindex][clusterorder, :]
            self.update_table(newdisplaydata,
                              self.lowerboundslist[self.tableindex],
                              self.upperboundslist[self.tableindex],
                              len(clusterorder),
                              clusterorder,
                              headernames=self.clusternames[ind])

        # If the uer is merging object-based clusters.
        elif self.analysismode == "Object":
            numclusters = len(self.datalist[self.tableindex]) - len(checked) + 1
            numcols = self.datalist[self.tableindex].shape[1] + 2
            fulltab = np.zeros((self.numimgs * numclusters, numcols))
            # Remove the checked clusters from the table and merge them together as a new entry at the end.
            count = 0
            for i in range(numtabs):
                data = self.datalist[self.objectclusterindices[analysisnum * numtabs + i]]
                table = np.zeros((len(data) + 1, data.shape[1]))
                table[:len(data), :] = data
                table[len(data), 0] = np.sum(data[checked, 0])
                if table[len(data), 0] > 0:
                    table[len(data), 1:] = np.average(data[checked, 1:], axis=0, weights=data[checked, 0])
                else:
                    table[len(data), 1:] = np.zeros_like(table[len(data), 1:])
                notremoved = [j for j in range(len(table)) if j not in checked]
                self.datalist[self.objectclusterindices[analysisnum * numtabs + i]] = table[notremoved, :]
                if i < self.numimgs:
                    fulltab[count:count + len(notremoved), 0] = i + 1
                    fulltab[count:count + len(notremoved), 1] = np.arange(1, len(notremoved) + 1)
                    fulltab[count:count + len(notremoved), 2:] = table[notremoved, :]
                    count += len(notremoved)

            my_data = pd.DataFrame(np.nan_to_num((np.vstack(fulltab))))
            paramslist = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            my_data.columns = np.hstack([["Sample", "Cluster", "# Cells"], paramslist])
            outfolder = GUIUtils.create_new_folder(
                os.path.join(os.path.split(self.objectclusterdirectories[analysisnum])[-1], "Merged_"),
                self.outputfolder)
            my_data.to_csv(os.path.join(outfolder, "ObjectClusterAvgExpressionVals.csv"))

            # Update the labeled image such that the clusters are merged at the end, removed, and relabeled.
            tabdata = self.objectclusterdfs[analysisnum]
            ind = [i for i, m in enumerate(self.clustersarepixelbased) if not m][analysisnum]
            imganalysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][
                                 self.analysisindex // numtabs] * self.numimgs
            labelimg = self.concat_label_imgs(
                [self.labeledimgs[ind] for ind in range(imganalysisnum, imganalysisnum + self.numimgs)])
            newclusterval = int(np.max(labelimg) + 1)
            clusterorder = self.currenttableordersfiltered[self.tableindex]
            clusterorderfull = self.currenttableorderfull

            if not self.clusternames[ind] == []:
                newname = self.clusternames[ind][checked[-1]]
                for cluster in checked:
                    oldname = self.clusternames[ind].pop(cluster)
                    self.objectclusterdfs[analysisnum]['Cluster'][
                        self.objectclusterdfs[analysisnum]['Cluster'] == oldname] = newname
                    cluster += 1
                    labelimg[labelimg == cluster] = newclusterval
                    labelimg[labelimg > cluster] = labelimg[labelimg > cluster] - 1
                    newclusterval -= 1

                    clusterorder.remove(cluster - 1)
                    clusterorder = np.array(clusterorder)
                    clusterorder[clusterorder > cluster - 1] -= 1
                    clusterorder = list(clusterorder)

                    clusterorderfull.remove(cluster - 1)
                    clusterorderfull = np.array(clusterorderfull)
                    clusterorderfull[clusterorderfull > cluster - 1] -= 1
                    clusterorderfull = list(clusterorderfull)

                    for i in range(self.numimgs):
                        self.cellclustervals[imganalysisnum + i][
                            self.cellclustervals[imganalysisnum + i] == cluster] = newclusterval + 1
                        self.cellclustervals[imganalysisnum + i][
                            self.cellclustervals[imganalysisnum + i] > cluster] -= 1
                    index = f"Cluster {cluster} (Object [{analysisnum}])"
                    for i in reversed(range(len(self.viewer.layers))):
                        if self.viewer.layers[i].name == index:
                            self.viewer.layers.pop(i)
                            break
                self.clusternames[ind].append(newname)
                self.objectclusterdfs[analysisnum].to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))

            else:
                clusterids = np.array(tabdata["Cluster"]).astype(int) - 1
                for cluster in checked:
                    clusterids[clusterids == cluster] = newclusterval - 1
                    clusterids[clusterids > cluster] = clusterids[clusterids > cluster] - 1
                    cluster += 1
                    labelimg[labelimg == cluster] = newclusterval
                    labelimg[labelimg > cluster] = labelimg[labelimg > cluster] - 1
                    newclusterval -= 1

                    clusterorder.remove(cluster - 1)
                    clusterorder = np.array(clusterorder)
                    clusterorder[clusterorder > cluster - 1] -= 1
                    clusterorder = list(clusterorder)

                    clusterorderfull.remove(cluster - 1)
                    clusterorderfull = np.array(clusterorderfull)
                    clusterorderfull[clusterorderfull > cluster - 1] -= 1
                    clusterorderfull = list(clusterorderfull)

                    for i in range(self.numimgs):
                        self.cellclustervals[analysisnum * self.numimgs + i][
                            self.cellclustervals[analysisnum * self.numimgs + i] == cluster] = newclusterval + 1
                        self.cellclustervals[analysisnum * self.numimgs + i][
                            self.cellclustervals[analysisnum * self.numimgs + i] > cluster] -= 1
                    index = f"Cluster {cluster} (Object [{analysisnum}])"
                    for i in reversed(range(len(self.viewer.layers))):
                        if self.viewer.layers[i].name == index:
                            self.viewer.layers.pop(i)
                            break
                clusterids += 1
                self.objectclusterdfs[analysisnum]['Cluster'] = [str(id) for id in clusterids]
                self.objectclusterdfs[analysisnum].to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))

            for i in range(len(labelimg)):
                self.labeledimgs[imganalysisnum + i] = labelimg[i, :self.imageshapelist[i][0],
                                                       :self.imageshapelist[i][1]].astype(
                    self.labeledimgs[imganalysisnum + i].dtype)

            # Create a colored image from the newly-labeled image, and add it to the viewer.
            newrgb = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], 3)).astype(np.uint8)
            color = self.objectclustercolors[analysisnum]
            newcolor = color[[checked[-1]], :]
            color = np.delete(color, checked, 0)
            color = np.append(color, newcolor, 0)
            self.objectclustercolors[analysisnum] = color
            for j in range(1, len(np.unique(labelimg))):
                newrgb[labelimg == j] = color[j - 1, :]

            np.save(os.path.join(outfolder, "color.npy"), color)
            tabledata, my_data_scaled, distmatrix, uniqueclusters = \
                prep_for_mst(clustertable=my_data,
                             minclustersize=1,
                             clustersizes=my_data["# Cells"],
                             includedmarkers=paramslist,
                             )
            generate_mst(distancematrix=distmatrix,
                         normalizeddf=my_data_scaled,
                         colors=color,
                         randomseed=0,
                         clusterheatmap=True,
                         outfolder=outfolder,
                         displaymarkers=paramslist,
                         uniqueclusters=uniqueclusters,
                         samplenames=list(np.unique(my_data['Sample'])),
                         displaysingle=False,
                         values="# Cells",
                         )

            # Add image(s) to the viewer.
            self.set_invisible(self.viewer)
            if addgreyimg:
                self.viewer.add_image(labelimg, name=f"Merged Object Cluster IDs {analysisnum}", blending="additive",
                                      contrast_limits=[0, np.max(labelimg)])
            if addcolorimg:
                self.viewer.add_image(newrgb, name=f"Merged Object Clusters {analysisnum}", blending="additive")
            self.viewer.layers[-1].visible = True

            self.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                                  name=f"Merged Object Clusters {analysisnum} Heatmap",
                                  blending="additive",
                                  visible=False,
                                  )

            # Save both the label and colored images to the output folder.
            for i in range(self.numimgs):
                imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]
                GUIUtils.save_img(os.path.join(outfolder, f"ObjectClusters_{imgname}.tif"),
                                  newrgb[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1], :],
                                  self.imageisflipped[i])
                GUIUtils.save_img(os.path.join(outfolder, f"ObjectClusterLabels_{imgname}.tif"),
                                  labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1,
                                  self.imageisflipped[i])

            # Reset the current selected cells for each of the corresponding tables to be empty.
            clusterorder.append(newclusterval - 1)
            clusterorderfull.append(newclusterval - 1)
            self.currenttableordersfiltered[self.tableindex] = clusterorder
            self.currenttableorderfull = clusterorderfull
            objectclusterindex = self.objectclusterindices.index(self.tableindex)
            startind = self.tableindex - objectclusterindex % numtabs
            for i in range(startind, startind + numtabs):
                self.currentlyselected[i] = []

            # Update the table to reflect the merged clusters.
            newdisplaydata = self.datalist[self.tableindex][clusterorder, :]
            self.update_table(newdisplaydata,
                              self.lowerboundslist[self.tableindex],
                              self.upperboundslist[self.tableindex],
                              newclusterval,
                              clusterorder,
                              headernames=self.clusternames[ind])

        self.sort_table_image()

    def merge_markers(self,
                      nucmarkernums=[],
                      nucalg="",
                      memmarkernums=[],
                      memalg="",
                      nuccls=[],
                      memcls=[],
                      ):
        """
        Merge together all nuclear and/or membrane markers, as defined by the user, to prepare for segmentation.

        Args:
            nucmarkernums (list, optional): List of indices of each nuclear cell marker being combined (Default: []).
            nucalg (str, optional): Algorithm being used to combine the nuclear cell markers (Default: "").
            memmarkernums (list, optional): List of indices of each membrane cell marker being combined (Default: []).
            memalg (str, optional): Algorithm being used to combine the membrane cell markers (Default: "").
            nuccls (list, optional): List of lists containing lower and upper contrast limits for each of the nuclear markers being merged (Default: []).
            memcls (list, optional): List of lists containing lower and upper contrast limits for each of the membrane markers being merged (Default: []).
        """
        # At least one image must be loaded in order to merge markers.
        if len(self.markers) == 0:
            GUIUtils.display_error_message("Please open an image first",
                                           "Begin by opening the image(s) that you would like to train RAPID on")
            return

        if (nucmarkernums == [] or nucalg == "") and (memmarkernums == [] or memalg == ""):
            # Notify user that contrast limits are accounted for when merging markers.
            if len(self.mergememmarkers) == 0:
                GUIUtils.display_error_message("Double-check contrast limits before proceeding",
                                               "Current contrast limits for each of the markers being merged together will be "
                                               "accounted for when segmenting. If you would like to use the raw data values "
                                               "for this, exit out of the next popup window and reset the contrast limits "
                                               "either manually or by clicking the \"Reset Metadata\" button in the \"Image "
                                               "Visualization\" module")

            # Define which nuclear markers to use for segmentation
            nucmarkers = GUIUtils.MergeMarkers(self.viewer, self.markers, False, nucmarkernums, nucalg)
            nucmarkers.exec()
            if not nucmarkers.OK:
                return
            nucmarkernums = nucmarkers.markernums
            nucalg = nucmarkers.alg

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
        self.segmentcounts.append([-1, -1, -1])
        self.histogramcounts.append([-1, -1])

        # Merge nuclear markers together if any nuclear markers were selected.
        self.viewer.status = "Merging nuclear markers..."
        nucdata = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)

        if nuccls == []:
            for i in range(len(nucmarkernums)):
                nuccls.append(self.viewer.layers[nucmarkernums[i]].contrast_limits)

        if len(nucmarkernums) > 0:
            if nucalg == "avg":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, nuccls[i])
                    nucdata += (image / len(nucmarkernums)).astype(np.uint8)
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
            if nucalg == "sum":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, nuccls[i])
                    nucdata += np.minimum(255 - nucdata, image)
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
            if nucalg == "max":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, nuccls[i])
                    nucdata = np.maximum(nucdata, image)
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
            if nucalg == "median":
                img = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], len(nucmarkernums)),
                               dtype=np.uint8)
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, nuccls[i])
                    img[:, :, :, i] = image
                    self.viewer.status = f"Merged {self.markers[nucmarkernums[i]]}"
                nucdata = np.median(img, axis=3)
        fh.create_dataset("Nucleus", data=nucdata, dtype=np.uint8)
        self.mergenucmarkers.append(len(nucmarkernums) > 0)

        # Merge membrane markers together if any membrane markers were selected.
        self.viewer.status = "Merging membrane markers..."
        memdata = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]), dtype=np.uint8)

        if memcls == []:
            for i in range(len(memmarkernums)):
                memcls.append(self.viewer.layers[memmarkernums[i]].contrast_limits)

        if len(memmarkernums) > 0:
            if memalg == "avg":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, memcls[i])
                    memdata += (image / len(memmarkernums)).astype(np.uint8)
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
            if memalg == "sum":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, memcls[i])
                    memdata += np.minimum(255 - memdata, image)
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
            if memalg == "max":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, memcls[i])
                    memdata = np.maximum(memdata, image)
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
            if memalg == "median":
                img = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], len(memmarkernums)),
                               dtype=np.uint8)
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(self.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image, memcls[i])
                    img[:, :, :, i] = image
                    self.viewer.status = f"Merged {self.markers[memmarkernums[i]]}"
                memdata = np.median(img, axis=3)
        fh.create_dataset("Membrane", data=memdata, dtype=np.uint8)
        self.set_invisible(self.viewer)
        self.mergememmarkers.append(len(memmarkernums) > 0)

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

        GUIUtils.log_actions(self.actionloggerpath, f"gui.merge_markers(nucmarkernums={nucmarkernums}, "
                                                    f"nucalg=\"{nucalg}\", memmarkernums={memmarkernums}, "
                                                    f"memalg=\"{memalg}\", nuccls={nuccls}, memcls={memcls})")
        self.viewer.status = "Finished merging markers"

    def method_searchsort(self,
                          from_values,
                          to_values,
                          array,
                          ):
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

    def minimum_spanning_tree(self,
                              clusteringindex=None,
                              ):
        """
        Generate a minimum spanning tree plot to illustrate phenotypic similarity of clusters for a user-defined round
        of clustering.

        Args:
            clusteringindex (int, optional): Index of clustering round being used for analysis (Default: None).
        """
        # Random seed for reproducibility.
        np.random.seed(0)

        # Check that the user has performed at least one clustering algorithm.
        if len(self.clustersarepixelbased) == 0:
            GUIUtils.display_error_message("No clustering results found",
                                           "MST can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been performed once, use those results.
        if len(self.clustersarepixelbased) == 1:
            clusteringindex = 0

        # If multiple rounds of clustering have been performed, prompt the user to select which one to use.
        elif clusteringindex is None:
            selectclusteringround = GUIUtils.SelectClusteringRound(self.clustersarepixelbased)
            selectclusteringround.exec()
            if not selectclusteringround.OK:
                return
            clusteringindex = selectclusteringround.clusteringindex

        ispixelcluster = self.clustersarepixelbased[clusteringindex]
        clustermodeindex = [i for i, ispixelbased in enumerate(self.clustersarepixelbased) if
                            ispixelbased == ispixelcluster].index(clusteringindex)

        # Retrieve the dataset being used for MST and create the output folder where images will be saved.
        if ispixelcluster:
            if self.numimgs == 1:
                currentdata = np.expand_dims(self.datalist[self.pixelclusterindices[clustermodeindex]], axis=0)
            else:
                startindex = clustermodeindex * (self.numimgs + 1)
                s = self.datalist[self.pixelclusterindices[startindex]].shape
                currentdata = np.zeros((self.numimgs + 1, s[0], s[1]))
                for i in range(self.numimgs + 1):
                    currentdata[i, :, :] = self.datalist[self.pixelclusterindices[i + startindex]]
            outfolder = GUIUtils.create_new_folder("PixelMST", self.outputfolder)
        else:
            if self.numimgs == 1:
                currentdata = np.expand_dims(self.datalist[self.objectclusterindices[clustermodeindex]], axis=0)
            else:
                startindex = clustermodeindex * (self.numimgs + 1)
                s = self.datalist[self.objectclusterindices[startindex]].shape
                currentdata = np.zeros((self.numimgs + 1, s[0], s[1]))
                for i in range(self.numimgs + 1):
                    currentdata[i, :, :] = self.datalist[self.objectclusterindices[i + startindex]]
            outfolder = GUIUtils.create_new_folder("ObjectMST", self.outputfolder)

        # Generate an MST for each image, plus the combined results if using multiple images.
        pathlist = []
        for i in range(len(currentdata)):
            # Retrieve the clustered data table for the current image.
            tabdata = DataFrame(currentdata[i, :, 1:])

            # Convert data to a distance matrix, and use that to generate the MST.
            distmatrix = np.nan_to_num(distance.cdist(currentdata[i, :, 1:], currentdata[i, :, 1:], 'euclidean'))
            pd.DataFrame(distmatrix).to_csv(os.path.join(outfolder, f"DistMatrix{i + 1}.csv"))
            G = nx.from_numpy_matrix(distmatrix)
            rowname = tabdata.iloc[[i for i in range(len(tabdata.values))]].astype(int).index.tolist()
            rowname = [round(x) + 1 for x in rowname]
            dictionary = dict(zip(G.nodes, rowname))
            G = nx.relabel_nodes(G, dictionary)
            T = nx.minimum_spanning_tree(G)

            # Plot MST on a graph, with nodes colored consistently with their corresponding clusters.
            colorlist = generate_colormap(len(tabdata) + 1)[:, [2, 1, 0]]
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
                plt.savefig(os.path.join(outfolder, "MST_Combined.png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, "MST_Combined.png"))
            # Define name if using object-clustering results for single-image data, and save the plot.
            elif not ispixelcluster:
                imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]
                plt.title(f"Minimum spanning tree ({imgname}) - Object")
                plt.savefig(os.path.join(outfolder, imgname + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, imgname + ".png"))
            # Define name if using multi-image pixel-clustering results for combined average data, and save the
            # plot.
            elif ispixelcluster and i == len(currentdata) - 1 and self.numimgs > 1:
                plt.title("Minimum spanning tree (Combined Images) - Pixel")
                plt.savefig(os.path.join(outfolder, "MST_Combined.png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, "MST_Combined.png"))
            # Define name if using pixel-clustering results for single-image data, and save the plot.
            elif ispixelcluster:
                imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]
                plt.title(f"Minimum spanning tree ({imgname}) - Pixel")
                plt.savefig(os.path.join(outfolder, imgname + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, imgname + ".png"))

        # Add all MST plots to the viewer as a single stacked image.
        arrays = np.array([imread(fn) for fn in pathlist])
        self.set_invisible(self.viewer)
        self.viewer.add_image(arrays,
                              name=f"MST (Pixel {clustermodeindex + 1}" if ispixelcluster else f"MST (Object {clustermodeindex + 1})",
                              blending="additive")
        GUIUtils.log_actions(self.actionloggerpath, f"gui.minimum_spanning_tree(clusteringindex={clusteringindex})")

    def nearest_neighbours(self,
                           imgname="",
                           clusteringindex=None,
                           sourcecluster=None,
                           targetcluster=None,
                           radius=None,
                           numnn=None,
                           ):
        """
        Perform a nearest neighbours analysis to find the cells in one cluster that are within a specified radius or
        number of nearest neighbours from any cell in a different cluster, display those cells in the GUI, and quantify
        how the phenotypes of those cells compare to those of the cluster as a whole.

        Args:
            imgname (str, optional): Name of image to be used for NN analysis (Default: "").
            clusteringindex (int, optional): Round of clustering to be used for NN analysis (Default: None).
            sourcecluster (int, optional): ID for the source cluster (Default: None).
            targetcluster (int, optional): ID for the target cluster (Default: None).
            radius (float, optional): Maximum distance from source cluster to search for cells from target cluster (Default: None).
            numnn (int, optional): Maximum number of nearest neighbours from each cell in the source cluster to search for cells from target cluster (Default: None).
        """
        # Can either use an individual image, or all images combined.
        imgnames = [str(file.split("/")[-1].split(".")[0]) for file in self.filenames] + ["All"]
        if imgname == "":
            if len(self.filenames) > 1:
                imgname = GUIUtils.SelectNNImgs(self.filenames)
                imgname.exec()
                if not imgname.OK:
                    return
                imgname = imgname.selimg
            else:
                imgname = "All"

        if imgname == "All":
            selectedimgindex = len(self.filenames)
        else:
            selectedimgindex = imgnames.index(imgname)

        # Determine which round of segmentation to use.
        if clusteringindex is None:
            clusteredsegresults = [self.objectimgnames[i] for i, l in enumerate(self.segmentationclusteringrounds) if
                                   len(l) > 0]
            if len(clusteredsegresults) > 1:
                segmentedimage = GUIUtils.SelectSegmentedImage(clusteredsegresults)
                segmentedimage.exec()
                if not segmentedimage.OK:
                    return
                segindex = self.objectimgnames.index(segmentedimage.image)
            elif len(clusteredsegresults) == 1:
                segindex = self.objectimgnames.index(clusteredsegresults[0])
            else:
                GUIUtils.display_error_message("No object-based clustering results found.",
                                               "Must perform object-based clustering before running nearest neighbour analysis.")
                return

            if len(self.segmentationclusteringrounds[segindex]) > 1:
                iteration = GUIUtils.ObjectClusterIteration(self.segmentationclusteringrounds[segindex])
                iteration.exec()
                if not iteration.OK:
                    return
                clusteringindex = iteration.iteration
            else:
                clusteringindex = self.segmentationclusteringrounds[segindex][0]

        for i, segmentationclusteringrounds in enumerate(self.segmentationclusteringrounds):
            if clusteringindex in segmentationclusteringrounds:
                segindex = i
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][segindex] * self.numimgs

        # Get all the cluster IDs in the selected clustered image, and prompt the user to define source and
        # target clusters.
        tabdata = self.objectclusterdfs[clusteringindex]
        numtabs = 1
        if len(self.filenames) > 1:
            numtabs += len(self.filenames)
        clusteringround = clusteringindex * numtabs + selectedimgindex
        tableindex = self.objectclusterindices[clusteringround - 1]
        data = self.datalist[tableindex]

        # Find current names of clusters.
        annotatedobjectclusters = [self.clusternames[i] for i in range(len(self.clusternames)) if
                                   not self.clustersarepixelbased[i]]
        if len(annotatedobjectclusters[clusteringindex]) == 0:
            currentnames = [i + 1 for i in range(len(data)) if data[i, 0] != 0.0]
        else:
            currentnames = annotatedobjectclusters[clusteringindex]

        if any(param is None for param in (sourcecluster, targetcluster, radius, numnn)):
            nndis = GUIUtils.NNInRadius(currentnames)
            nndis.exec()
            if not nndis.OK:
                return
            sourcecluster = nndis.sourcecluster
            targetcluster = nndis.targetcluster
            radius = nndis.radius
            numnn = nndis.numnn

        # Generate heatmap demonstrating differential marker expression between NN cells and cluster average,
        # and add to the viewer.
        if imgname == "All":
            # Show all cells from the target cluster within specified radius and/or number of nearest neighbours
            # from a cell in the source cluster.
            for i in range(self.numimgs):
                cellind = GUIUtils.get_nn_in_radius(data=tabdata[tabdata['ImgID'] == i], clusterid1=sourcecluster,
                                                    clusterid2=targetcluster, radius=radius, nn=numnn)
                nnimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1]), dtype=np.bool)
                mask = np.in1d(self.labeledimgs[analysisnum + i], cellind)
                mask = mask.reshape((self.imageshapelist[i][0], self.imageshapelist[i][1]))
                nnimg[0, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = mask
                if i == 0:
                    self.viewer.add_image(nnimg, name="NN", blending="additive", visible=True)
                else:
                    self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, nnimg))
            sbb = GUIUtils.nn_to_heatmap(data=tabdata, clusterid1=sourcecluster, radius=radius, nn=numnn)
        else:
            # Show all cells from the target cluster within specified radius and/or number of nearest neighbours
            # from a cell in the source cluster.
            cellind = GUIUtils.get_nn_in_radius(data=tabdata[tabdata['ImgID'] == selectedimgindex],
                                                clusterid1=sourcecluster, clusterid2=targetcluster, radius=radius,
                                                nn=numnn)
            mask = np.in1d(self.labeledimgs[analysisnum + selectedimgindex].astype(np.uint32), cellind)
            mask = mask.reshape((self.imageshapelist[selectedimgindex][0], self.imageshapelist[selectedimgindex][1]))
            self.viewer.add_image(mask, name="NN", blending="additive", visible=True)
            sbb = GUIUtils.nn_to_heatmap(data=tabdata[tabdata['ImgID'] == selectedimgindex],
                                         clusterid1=sourcecluster, radius=radius, nn=numnn)
        plt.setp(sbb.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        buf = io.BytesIO()
        sbb.savefig(buf)
        buf.seek(0)
        heatimg = Image.open(buf)
        self.set_invisible(self.viewer)
        self.viewer.add_image(np.array(heatimg), name="NN Enrichment", blending="additive", visible=True)
        GUIUtils.log_actions(self.actionloggerpath, f"gui.nearest_neighbours(imgname=\"{imgname}\", "
                                                    f"clusteringindex={clusteringindex}, sourcecluster={sourcecluster}, "
                                                    f"targetcluster={targetcluster}, radius={radius}, numnn={numnn})")

    def object_clustering(self,
                          markernums=[],
                          segindex=None,
                          algname="",
                          modelpath="",
                          addgreyimg=None,
                          addcolorimg=None,
                          continuetraining=None,
                          normalize="",
                          pca=False,
                          modelparams=[],
                          ):
        """
        Perform object-based clustering on a segmented image using the algorithm selected by the user.

        Args:
            markernums (list, optional): List of indices of parameters to be considered for clustering (Default: []).
            segindex (int, optional): Index of segmentation round being clustered (Default: None).
            algname (str, optional): Name of the specified algorithm to be used for clustering (Default: "").
            modelpath (str, optional): Path to the model being used if loading a pretrained model (Default: "").
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            continuetraining (bool, optional): If True, continue training the model after loading it. Otherwise, predict without further training (Default: None).
            normalize (str, optional): Normalization algorithm to be used for data preprocessing (Default: "").
            pca (bool, optional): If True, apply PCA reduction to normalized data. Otherwise, do nothing (Default: None).
            modelparams (iterable, optional): List of parameters for the desired clustering algorithm (Default: []).
        """
        # Can only perform clustering if segmentation has been done
        if self.segmentcount == 0:
            GUIUtils.display_error_message("You must segment before running object-based clustering",
                                           "Object-based clustering cannot be done until the image has been segmented")
            return

        # Define which markers will be used for clustering
        if markernums == []:
            trainmarkers = GUIUtils.RAPIDObjectParams(self.markers)
            trainmarkers.exec()
            if not trainmarkers.OK:
                return
            markernums = trainmarkers.markernums

        # Define which algorithm will be used for clustering
        if segindex is None and algname == "" or algname == "Pretrained" and modelpath == "":
            alg = GUIUtils.ClusteringAlgorithm(self.objectimgnames)
            alg.exec()
            if not alg.OK:
                return
            segindex = alg.segindex
            algname = alg.algname
            if algname == "Pretrained":
                modelpath = alg.dirpath
        imagenum = segindex * self.numimgs

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        # Load model, indicate whether to continue training or use for prediction, and define parameters for
        # whichever algorithm was selected by the user
        if algname == "Pretrained":
            try:
                hf = zarr.open("/".join(modelpath[:-1]), 'r')
                loadedargs = hf.attrs['arg']
            except:
                return

            if continuetraining is None:
                loadoptions = GUIUtils.LoadModelOptions()
                loadoptions.exec()
                if not loadoptions.OK:
                    return
                continuetraining = not loadoptions.prediction

            args = Namespace(**loadedargs)

            if continuetraining:
                if modelparams == []:
                    params = GUIUtils.RAPIDObjectTrainLoadedParameters(args)
                    params.exec()
                    if not params.OK:
                        return
                    args.nit = int(params.nit)
                    args.bs = int(params.bs)
                    args.lr = float(params.lr)
                    args.blankpercent = float(params.blankpercent)
                    modelparams = args.nit, args.bs, args.lr, args.blankpercent
                else:
                    args.nit, args.bs, args.lr, args.blankpercent = modelparams
                args.epoch = 1
                args.GUI = True
                args.distance = 'YES'

        elif algname == "RAPID":
            continuetraining = True
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = GUIUtils.RAPIDObjectParameters(len(markernums))
                params.exec()
                if not params.OK:
                    return
                args.ncluster = int(params.nc)
                args.nit = int(params.nit)
                args.bs = int(params.bs)
                if params.mse == "True":
                    args.mse = True
                args.normalize = params.normalize
                args.lr = float(params.lr)
                args.blankpercent = float(params.blankpercent)
                pca = params.pca
                modelparams = args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent, pca
            else:
                args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent, pca = modelparams
            args.epoch = 1
            args.GUI = True
            args.distance = 'YES'

        elif algname == "SciPy":
            continuetraining = True
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = GUIUtils.SciPyParameters()
                params.exec()
                if not params.OK:
                    return
                args.normalize = params.normalize
                args.scipyalgo = params.scipyalgo
                args.scipykwarg = params.scipykwarg
                pca = params.pca
                modelparams = args.normalize, args.scipyalgo, args.scipykwarg, pca
            else:
                args.normalize, args.scipyalgo, args.scipykwarg, pca = modelparams
            args.GUI = True

        else:
            continuetraining = True
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = GUIUtils.PhenographParameters()
                params.exec()
                if not params.OK:
                    return
                args.PGdis = str(params.PGdis)
                args.PGnn = int(params.PGnn)
                args.PGres = float(params.PGres)
                args.normalize = params.normalize
                args.graphalgo = params.graphalgo
                pca = params.pca
                modelparams = args.PGdis, args.PGnn, args.PGres, args.normalize, args.graphalgo, pca
            else:
                args.PGdis, args.PGnn, args.PGres, args.normalize, args.graphalgo, pca = modelparams
            args.GUI = True

        # Count total number of cells for segmented image used for clustering
        numcells = 0
        for i in range(self.numimgs):
            numcells += len(self.datalist[self.segmentationindices[i + imagenum]])

        # Store normalized cell marker expression
        expressionavgs = np.zeros((numcells, len(markernums)))
        if args.normalize == "zscale":
            scaler = StandardScaler()
            count = 0
            for i in range(self.numimgs):
                numcells = len(self.datalist[self.segmentationindices[i + imagenum]])
                img = copy.deepcopy(self.datalist[self.segmentationindices[i + imagenum]][:, markernums])
                scaler.fit(img)
                expressionavgs[count:count + numcells, :] = scaler.transform(img)
                count += numcells
        else:
            count = 0
            for i in range(self.numimgs):
                numcells = len(self.datalist[self.segmentationindices[i + imagenum]])
                expressionavgs[count:count + numcells, :] = self.datalist[self.segmentationindices[i + imagenum]][:,
                                                            markernums]
                count += numcells

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
        outfolder = GUIUtils.create_new_folder("RAPIDObject_", self.outputfolder)
        self.objectclusterdirectories.append(outfolder)
        if not continuetraining:
            model = RAPIDMixNet(dimension=len(markernums), nummodules=5, mse=args.mse,
                                numclusters=int(args.ncluster))
            optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                    weight_decay=0.01, amsgrad=False)
            model.apply(weight_init)
            model = load_checkpoint("/".join(modelpath), model, optimizer)
            self.test_object(model, expressionavgs, args, list(range(len(self.markers) + 4)), addcolorimg, addgreyimg,
                             "RAPID", imagenum, optimizer=optimizer, outputpath=outfolder, predict=True)
        else:
            if algname == "Phenograph":
                model = 0
                self.test_object(model, expressionavgs, args, list(range(len(self.markers) + 4)), addcolorimg,
                                 addgreyimg, "Phenograph", imagenum, outputpath=outfolder)
                pass
            elif algname == "SciPy":
                model = 0
                self.test_object(model, expressionavgs, args, list(range(len(self.markers) + 4)), addcolorimg,
                                 addgreyimg, args.scipyalgo, imagenum, outputpath=outfolder)
                pass
            else:
                hf = zarr.open(outfolder, 'a')
                hf.attrs['arg'] = vars(args)
                hf.attrs['RAPIDObject'] = True
                torch.manual_seed(args.seed)
                np.random.seed(args.seed)
                torch.cuda.manual_seed(args.seed)
                model = RAPIDMixNet(dimension=len(markernums), nummodules=5, mse=args.mse,
                                    numclusters=int(args.ncluster))
                model.apply(weight_init)
                optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                        weight_decay=0.01, amsgrad=False)
                if algname == "Pretrained":
                    model = load_checkpoint("/".join(modelpath), model, optimizer)
                print(model)
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                model.to(device)
                self.train_object(model, expressionavgs, optimizer, args)
                self.test_object(model, expressionavgs, args, list(range(len(self.markers) + 4)), addcolorimg,
                                 addgreyimg, "RAPID", imagenum, optimizer=optimizer, outputpath=outfolder)

        GUIUtils.log_actions(self.actionloggerpath,
                             f"gui.object_clustering(markernums={markernums}, segindex={segindex}, "
                             f"algname=\"{algname}\", modelpath=\"{modelpath}\", "
                             f"addgreyimg={addgreyimg}, addcolorimg={addcolorimg}, "
                             f"continuetraining={continuetraining}, normalize=\"{normalize}\", "
                             f"pca={pca}, modelparams={modelparams})")
        self.viewer.status = "RAPID clustering done."

    def open_docs(self):
        """
        Open the RAPID documentation in a web browser.
        """
        rootfold = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(rootfold + "/../docs"):
            gdown.download("https://drive.google.com/uc?id=1JhpIjMd_Rq-i1_laivxzavwZDJPOa4b1",
                           rootfold + "/../docs.zip", verify=False)
            shutil.unpack_archive(rootfold + "/../docs.zip", rootfold + "/../")
        webbrowser.open(f"file://{rootfold}/../docs/_build/html/index.html", new=2)

    ### TODO: Delayed function? Pyramid/multiscale?
    def open_images_gui(self):
        """
        Trigger the "Open Images" popup from the GUI.
        """
        self.open_images()

    def open_images(self,
                    segmentedimgpaths=[],
                    filenames=[],
                    cfirst=None,
                    markerstring="",
                    loadedmatrix=None,
                    imagenames=[],
                    indiceslist=[],
                    markernums=[],
                    ):
        """
        Open a directory for the user to select which images they would like to use, and load them into the viewer.

        Args:
            segmentedimgpaths (list, optional): List of paths to segmented images if loading segmentation results (Default: []).
            filenames (list, optional): List of paths to each of the iamges being loaded (Default: []).
            cfirst (bool, optional): If True, assume (c,z,x,y) order for 4D images. Otherwise, assume (z,c,x,y) order (Default: None).
            markerstring (str, optional): Comma-separated names of cell markers for the image(s) being loaded (Default: "").
            loadedmatrix (bool, optional): If True, prompt user to load matrix of markers for each image. Otherwise, allow user to load a list of markers (Default: None).
            imagenames (list, optional): List of names of images being loaded in a matrix of markers (Default: []).
            indiceslist (list, optional): List of indices for each image in a matrix that are shared between all other images (Default: []).
            markernums (list, optional): List of indices of cell markers to include in the viewer (Default: []).

        :return: *(bool)*: \n
            True if user has loaded images, False if none are selected.
        """

        # Only open images at the start, not after performing downstream analysis.
        if len(self.viewer.layers) > len(self.markers):
            GUIUtils.display_error_message("Cannot open additional images",
                                           "If you have done downstream analysis, please open images in a new session")
            return

        # Prompt user to select paths to images to load.
        if len(filenames) == 0:
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

        # If loading segmentation, make sure the images being loaded correspond to the segmented images.
        if segmentedimgpaths and len(filenames) != len(segmentedimgpaths):
            GUIUtils.display_error_message("Mismatching number of images",
                                           "Please ensure the raw images correspond to the segmented image and are in the correct order")
            return False

        # User must load at least one image.
        if len(filenames) == 0:
            return False

        # If this is the first time loading images.
        if not self.hasloadedimage:
            # Initialize lists of image paths and image arrays, and keep track of number of cell markers being loaded.
            imagelist = []

            if markerstring == "" and (loadedmatrix == None or imagenames == [] or indiceslist == []):
                loadedimgnames = [os.path.split(path)[-1].split(".")[0] for path in filenames]
                markernames = GUIUtils.MarkerNames(self.outputfolder, loadedimgnames)
                markernames.exec()
                if not markernames.OK:
                    if markernames.matrix:
                        GUIUtils.display_error_message("No images loaded",
                                                       "Please ensure the image names in the matrix correspond with the names of the images being loaded.")
                    return
                markerstring = markernames.markers
                loadedmatrix = markernames.matrix
                if loadedmatrix:
                    imagenames = markernames.imagenames
                    indiceslist = markernames.indiceslist

            # Loop through each image path.
            for path in filenames:
                # Read the image into a numpy array.
                filename = os.path.join(os.path.abspath(path))

                if loadedmatrix and os.path.split(path)[-1].split(".")[0] not in imagenames:
                    continue

                img, imgisflipped = self.parse_img(filename)

                # If loading a single z-slice, load the image as is.
                if len(img.shape) == 3:
                    if indiceslist != []:
                        img = img[indiceslist[self.numimgs], :, :]
                    imagelist.append(img)
                    self.filenames.append(path)
                    if self.nummarkers == 0:
                        self.nummarkers = len(img)
                    self.imageisflipped.append(imgisflipped)
                    self.numimgs += 1

                # If loading multiple z-slices, load as separate images for each z-slice.
                elif len(img.shape) == 4:
                    name_ext = path.split(".")
                    if cfirst is None:
                        channelorder = GUIUtils.ChannelOrder4D()
                        channelorder.exec()
                        if not channelorder.OK:
                            return
                        cfirst = channelorder.cfirst

                    if cfirst:
                        for i in range(img.shape[1]):
                            currentz = copy.deepcopy(img[:, i, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[self.numimgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            self.filenames.append('.'.join(currentname))
                            self.imageisflipped.append(imgisflipped)
                            self.numimgs += 1

                    else:
                        for i in range(len(img)):
                            currentz = copy.deepcopy(img[i, :, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[self.numimgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            self.filenames.append('.'.join(currentname))
                            self.imageisflipped.append(imgisflipped)
                            self.numimgs += 1

                    if self.nummarkers == 0:
                        self.nummarkers = len(currentz)

                # self.numimgs += 1

                # If this image has a different number of markers than previous images, and a matrix was not loaded,
                # prompt user to load matrix of markers instead of one singular set of markers.
                if len(imagelist[-1]) != self.nummarkers and path != filenames[0]:
                    GUIUtils.display_error_message("Incompatible number of channels",
                                                   "Some images contain different numbers of channels. Please load a matrix containing ordered lists of cell markers for each image.")
                    self.filenames = []
                    self.imageisflipped = []
                    self.numimgs = 0
                    self.nummarkers = 0
                    return

            if self.numimgs == 0:
                GUIUtils.display_error_message("No images loaded",
                                               "If you are loading a cell marker matrix, please ensure the image names in the matrix correspond with the names of the images being loaded.")
                return

            inputmarkernames = markerstring.replace(" ", "").split(",")

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
            if markernums == []:
                removemarkernames = GUIUtils.RemoveMarkerNames(markers)
                removemarkernames.exec()
                if not removemarkernames.OK:
                    self.numimgs = 0
                    self.nummarkers = 0
                    return
                markernums = removemarkernames.markernums
            self.markers = [markers[ind].replace("/", "_").replace("\\", "_") for ind in markernums]
            self.markernums = copy.deepcopy(markernums)
            self.nummarkers = len(self.markers)

            # Store the shapes of each of the images being loaded.
            for i in range(len(imagelist)):
                imagelist[i] = imagelist[i][self.markernums, :, :]
                vdim = imagelist[i].shape[1]
                hdim = imagelist[i].shape[2]
                self.imageshapelist.append((vdim, hdim, len(self.markernums)))

            # Keep track of the maximum x- and y- dimensions to use for the shape of the image in the viewer.
            self.maximageshape = np.array([np.max(self.imageshapelist, 0)[0], np.max(self.imageshapelist, 0)[1]])

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
                # addarr_downsampled = np.stack([cv.pyrDown(addarr[i,:,:]) for i in range(len(addarr))])
                # self.viewer.add_image([addarr, addarr_downsampled], name=self.markers[ch], rgb=False, colormap=cmap, contrast_limits=[0, 255],
                #                      blending="additive", visible=False, multiscale=True)
                self.viewer.add_image(addarr, name=self.markers[ch], rgb=False, colormap=cmap, contrast_limits=[0, 255],
                                      blending="additive", visible=False)
            self.hasloadedimage = True

            # By default, initialize sample groupings so that each image is in its own group.
            d = {}
            for name in [os.path.split(path)[-1].split(".")[0] for path in self.filenames]:
                n = os.path.split(name)[-1]
                d[n] = n
            self.groupslist.append(d)

            # Update the dropdown options for the sort table widget.
            self.tableparams += self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            self.updatelogfile = False
            self.sorttableimages.marker.choices = tuple(self.tableparams)
            self.sorttableimages.reset_choices()
            self.updatelogfile = True
            self.viewer.dims.set_current_step(0, 0)

        # If at least one image has already been loaded.
        else:
            imagelist = []

            markerorder = GUIUtils.NewMarkerOrder()
            markerorder.exec()
            if not markerorder.OK:
                return

            if markerorder.usingdifferentorder:
                loadedimgnames = [os.path.split(path)[-1].split(".")[0] for path in filenames]
                markernames = GUIUtils.MarkerNames(self.outputfolder, loadedimgnames, currentmarkernames=self.markers)
                markernames.exec()
                if not markernames.OK:
                    if markernames.matrix:
                        GUIUtils.display_error_message("No images loaded",
                                                       "Please ensure the image names in the matrix correspond with the names of the images being loaded.")
                    return
                markerstring = markernames.markers
                loadedmatrix = markernames.matrix
                newmarkerlist = markerstring.replace(" ", "").split(",")
                if not all([newmarker in newmarkerlist for newmarker in self.markers]):
                    GUIUtils.display_error_message("Mismatching cell markers",
                                                   "Not all cell markers currently loaded are included in the image(s) you loaded")
                    return

                if loadedmatrix:
                    imagenames = markernames.imagenames
                    indiceslist = markernames.indiceslist
                else:
                    indices = []
                    currentmarkerslist = [re.sub('[^a-zA-Z0-9]', '', marker).lower() for marker in newmarkerlist]
                    for marker in [re.sub('[^a-zA-Z0-9]', '', cm).lower() for cm in self.markers]:
                        indices.append(currentmarkerslist.index(marker))
                    indiceslist = [indices] * len(loadedimgnames)

            # Loop through each image path.
            numnewimgs = 0
            filenamesadded = []
            imageisflipped = []
            for path in filenames:
                # Read the image into a numpy array.
                filename = os.path.join(os.path.abspath(path))

                if loadedmatrix and os.path.split(path)[-1].split(".")[0] not in imagenames:
                    continue

                img, imgisflipped = self.parse_img(filename)

                # If loading a single z-slice, load the image as is.
                if len(img.shape) == 3:
                    if indiceslist != []:
                        img = img[indiceslist[numnewimgs], :, :]
                    imagelist.append(img)
                    filenamesadded.append(path)
                    imageisflipped.append(imgisflipped)

                # If loading multiple z-slices, load as separate images for each z-slice.
                elif len(img.shape) == 4:
                    name_ext = path.split(".")
                    if cfirst is None:
                        channelorder = GUIUtils.ChannelOrder4D()
                        channelorder.exec()
                        if not channelorder.OK:
                            return
                        cfirst = channelorder.cfirst

                    if cfirst:
                        for i in range(img.shape[1]):
                            currentz = copy.deepcopy(img[:, i, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[numnewimgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            filenamesadded.append('.'.join(currentname))
                            imageisflipped.append(imgisflipped)

                    else:
                        for i in range(len(img)):
                            currentz = copy.deepcopy(img[i, :, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[numnewimgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            filenamesadded.append('.'.join(currentname))
                            imageisflipped.append(imgisflipped)
                numnewimgs += 1

                # If this image has a different number of markers than previous images, and a matrix was not loaded,
                # prompt user to load matrix of markers instead of one singular set of markers.
                if len(imagelist[-1]) < self.nummarkers:
                    GUIUtils.display_error_message("Incompatible number of channels",
                                                   "Some images contain different numbers of channels. Please ensure each image you load contains every cell marker that has already been loaded.")
                    return

            self.filenames += filenamesadded
            self.numimgs += numnewimgs
            self.imageisflipped += imageisflipped

            if self.numimgs == 0:
                GUIUtils.display_error_message("No images loaded",
                                               "If you are loading a cell marker matrix, please ensure the image names in the matrix correspond with the names of the images being loaded.")
                return

            # Store the shapes of each of the images being loaded.
            for i in range(len(imagelist)):
                vdim = imagelist[i].shape[1]
                hdim = imagelist[i].shape[2]
                self.imageshapelist.append((vdim, hdim, self.nummarkers))

            # Update the maximum x- and y- dimensions to use for the shape of the image in the viewer.
            self.maximageshape = np.array((np.max(self.imageshapelist, 0)[0], np.max(self.imageshapelist, 0)[1]))
            for ch in range(self.nummarkers):
                newarr = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1]),
                                  dtype=imagelist[0].dtype)
                prevarr = self.viewer.layers[ch].data
                newarr[:len(prevarr), :prevarr.shape[1], :prevarr.shape[2]] = prevarr
                for i in range(len(filenamesadded)):
                    newarr[i + len(prevarr), :imagelist[i].shape[1], :imagelist[i].shape[2]] = imagelist[i][0, :, :]
                    imagelist[i] = imagelist[i][1:, :, :]
                self.viewer.layers[ch].data = newarr

            # Add each of the new images to the default grouping.
            for name in [os.path.split(path)[-1].split(".")[0] for path in filenamesadded]:
                n = os.path.split(name)[-1]
                self.groupslist[0][n] = n

        GUIUtils.log_actions(self.actionloggerpath, f"gui.open_images(segmentedimgpaths={segmentedimgpaths}, "
                                                    f"filenames={filenames}, cfirst={cfirst}, "
                                                    f"markerstring=\"{markerstring}\", loadedmatrix={loadedmatrix}, "
                                                    f"imagenames={imagenames}, indiceslist={indiceslist}, "
                                                    f"markernums={markernums})")
        return True

    def on_cell_changed(self,
                        row,
                        column,
                        ):
        """
        Add actions for the case when a checkbox is toggled. When a box is checked, the corresponding cell/cluster
        should be made visible in the viewer, and if a box is unchecked then the corresponding cell/cluster should
        be made invisible.

        Args:
            row (int): Row of the checkbox being toggled.
            column (int): Column of the checkbox being toggled.
        """
        if self.addwhenchecked and (column == 0 and row > 2) or row == 2:
            item = self.tablewidget.item(row, column)
            col = column - 1
            r = row - 3
            if item.checkState() == QtCore.Qt.Checked:
                if column > 0:
                    if self.analysismode == "Segmentation":
                        self.viewer.layers[self.markers[col]].visible = True

                    elif column > 1:
                        self.viewer.layers[self.markers[col - 1]].visible = True

                else:
                    r = self.currenttableordersfiltered[self.tableindex][r]
                    if self.analysismode == "Segmentation":
                        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][
                            self.analysisindex // self.numimgs]
                        for i in range(self.numimgs):
                            cellimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1]), dtype=np.bool)
                            if i == self.analysisindex % self.numimgs:
                                mask = np.in1d(
                                    self.labeledimgs[analysisnum * self.numimgs + self.analysisindex % self.numimgs],
                                    r + 1)
                                mask = mask.reshape((1, self.imageshapelist[i][0], self.imageshapelist[i][1]))
                                cellimg[0, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = mask
                            if i == 0:
                                self.viewer.add_image(cellimg, name=f"Cell {r + 1}", blending="additive", visible=True)
                            else:
                                self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, cellimg))
                        self.currentlyselected[self.tableindex].append(r)

                    elif self.analysismode == "Object":
                        analysis_ind, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                        color = self.objectclustercolors[analysis_ind][r, :] / 255
                        overall_analysis_ind = [i for i, n in enumerate(self.analysislog) if n == "O"][
                                                   analysis_ind] * self.numimgs
                        cmap = Colormap(ColorArray([(0, 0, 0), (color[0], color[1], color[2])]))

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = GUIUtils.find_current_cluster_names(self.analysisindex,
                                                                           self.numimgs,
                                                                           self.clustersarepixelbased,
                                                                           self.clusternames,
                                                                           False,
                                                                           )
                        clustername = f"Cluster {r + 1}" if currentnames == [] else currentnames[r]
                        clustername += f"(Object [{analysis_ind}])"

                        for i in range(self.numimgs):
                            clusterimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1]))
                            clusterimg[0, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = self.labeledimgs[
                                overall_analysis_ind + i]
                            clusterimg = np.in1d(clusterimg, r + 1)
                            clusterimg = clusterimg.reshape((1, self.maximageshape[0], self.maximageshape[1]))

                            if i == 0:
                                self.viewer.add_image(clusterimg,
                                                      name=clustername,
                                                      blending="additive",
                                                      colormap=cmap,
                                                      visible=True,
                                                      )
                            else:
                                self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, clusterimg))

                        objectclusterindex = self.objectclusterindices.index(self.tableindex)
                        ind = self.tableindex - objectclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            self.currentlyselected[i].append(r)

                    else:
                        analysis_ind, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                        color = self.pixelclustercolors[analysis_ind][r, :] / 255
                        overall_analysis_ind = [i for i, n in enumerate(self.analysislog) if n == "P"][
                                                   analysis_ind] * self.numimgs
                        cmap = Colormap(ColorArray([(0, 0, 0), (color[0], color[1], color[2])]))

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = GUIUtils.find_current_cluster_names(self.analysisindex,
                                                                           self.numimgs,
                                                                           self.clustersarepixelbased,
                                                                           self.clusternames,
                                                                           True,
                                                                           )
                        clustername = f"Cluster {r + 1}" if currentnames == [] else currentnames[r]
                        clustername += f"(Pixel [{analysis_ind}])"

                        for i in range(self.numimgs):
                            clusterimg = np.zeros((1, self.maximageshape[0], self.maximageshape[1]))
                            clusterimg[0, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = self.labeledimgs[
                                                                                                        overall_analysis_ind + i] + 1
                            clusterimg = np.in1d(clusterimg, r + 1)
                            clusterimg = clusterimg.reshape((1, self.maximageshape[0], self.maximageshape[1]))
                            if i == 0:
                                self.viewer.add_image(clusterimg,
                                                      name=clustername,
                                                      blending="additive",
                                                      colormap=cmap,
                                                      visible=True,
                                                      )
                            else:
                                self.viewer.layers[-1].data = np.vstack((self.viewer.layers[-1].data, clusterimg))

                        pixelclusterindex = self.pixelclusterindices.index(self.tableindex)
                        ind = self.tableindex - pixelclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            self.currentlyselected[i].append(r)

            else:
                if column > 0:
                    if self.analysismode == "Segmentation" and col < len(self.markers):
                        self.viewer.layers[self.markers[col]].visible = False
                    elif column > 1:
                        self.viewer.layers[self.markers[col - 1]].visible = False

                else:
                    r = self.currenttableordersfiltered[self.tableindex][r]

                    if self.analysismode == "Segmentation":
                        self.currentlyselected[self.tableindex].remove(r)
                        index = f"Cell {r + 1}"

                    elif self.analysismode == "Object":
                        analysis_ind, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                        objectclusterindex = self.objectclusterindices.index(self.tableindex)
                        ind = self.tableindex - objectclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            self.currentlyselected[i].remove(r)

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = GUIUtils.find_current_cluster_names(self.analysisindex,
                                                                           self.numimgs,
                                                                           self.clustersarepixelbased,
                                                                           self.clusternames,
                                                                           False,
                                                                           )
                        clustername = f"Cluster {r + 1}" if currentnames == [] else currentnames[r]
                        clustername += f"(Object [{analysis_ind}])"

                    else:
                        analysis_ind, numtabs = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                        pixelclusterindex = self.pixelclusterindices.index(self.tableindex)
                        ind = self.tableindex - pixelclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            self.currentlyselected[i].remove(r)

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = GUIUtils.find_current_cluster_names(self.analysisindex,
                                                                           self.numimgs,
                                                                           self.clustersarepixelbased,
                                                                           self.clusternames,
                                                                           True,
                                                                           )
                        clustername = f"Cluster {r + 1}" if currentnames == [] else currentnames[r]
                        clustername += f"(Object [{analysis_ind}])"

                    for i in range(len(self.viewer.layers)):
                        if self.viewer.layers[i].name == clustername:
                            self.viewer.layers.pop(i)
                            break

    def parse_img(self,
                  imgpath,
                  islabel=False,
                  ):
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
            except:
                reader_function = napari_get_reader(imgpath)
                img = reader_function(imgpath)[0][0]
        except:
            msg = QMessageBox()
            msg.setWindowTitle("RAPID Alert")
            msg.setText("Please convert your file to .tif format")
            msg.setDetailedText("Because your Java path is not set, your file must be in .tif format")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return False

        if not islabel:
            img = img_as_ubyte(img)
        else:
            img = img.astype(np.uint32)

        imgisflipped = False
        if img.shape[-2] > img.shape[-1]:
            img = np.moveaxis(img, -1, -2)
            imgisflipped = True

        return img, imgisflipped

    ### TODO: Progress bar in GUI for pixel clustering.
    ### TODO: Markers used for clustering when applying pre-trained model?
    ### TODO: Save binarize/denoise to zarr so it can be loaded when loading model.
    def pixel_clustering(self,
                         isloadingmodel=None,
                         predict=None,
                         randompatchgeneration=None,
                         markerindices=[],
                         modelparams=[],
                         modelpath="",
                         patchesstart=[],
                         addgreyimg=None,
                         addcolorimg=None):
        """
        Perform RAPID pixel-based clustering, by either training a new model or loading a previously-trained model and
        applying it to each of the images loaded into the GUI.

        Args:
            isloadingmodel (bool, optional): If True, load pre-trained model weights. Otherwise, use random weight initialization (Default: None).
            predict (bool, optional): If True, use pre-trained model weights to predict without further training. Otherwise, train a new model (Default: None).
            randompatchgeneration (bool, optional): If True, randomly generate patches for the training set. Otherwise, use user-defined patches (Default: None).
            markerindices (list, optional): List of indices of cell markers to be considered for clustering (Default: []).
            modelparams (iterable, optional): List of parameters for the desired clustering algorithm (Default: []).
            modelpath (str, optional): Path to pretrained model, if loading a model (Default: "").
            patchesstart (list, optional): List of vertices defining top-left corner for each 64x64 patch, for each image. (Default: []).
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """
        # Can't use RAPID before opening an image.
        if len(self.markers) == 0:
            GUIUtils.display_error_message("Please open an image first",
                                           "Begin by opening the image(s) that you would like to train RAPID on")
            return

        # Allow user to either load a model and define the path to the model, or train a new model.
        if isloadingmodel is None:
            loadmodel = GUIUtils.LoadModel()
            loadmodel.exec()
            if not loadmodel.OK:
                return
            isloadingmodel = loadmodel.load

        # If loading a model, allow user to either continue training or predict. Otherwise, default to training.
        if isloadingmodel:
            if modelpath == "":
                modelpath = loadmodel.dirpath
            if predict is None:
                loadmodeloptions = GUIUtils.LoadModelOptions()
                loadmodeloptions.exec()
                if not loadmodeloptions.OK:
                    return
                predict = loadmodeloptions.prediction
            hf = zarr.open("/".join(modelpath[:-1]) + "/RAPID_Data", 'r')
            trainmarkernames = hf.attrs['selmarkernames']
            numtrainmarkers = len(trainmarkernames)
        else:
            predict = False

        # If training, allow user to define specific patches to train on, otherwise default to random patches.
        if not predict and randompatchgeneration is None:
            definepatches = GUIUtils.DefinePatches()
            definepatches.exec()
            if not definepatches.OK:
                return
            randompatchgeneration = definepatches.randompatchgeneration
        else:
            randompatchgeneration = True

        # Define which markers to use for pixel clustering.
        if markerindices == []:
            trainmarkers = GUIUtils.PixelTrainMarkers(self.viewer, self.markers)
            trainmarkers.exec()
            if not trainmarkers.OK:
                return
            markerindices = trainmarkers.markernums
        markernames = [self.markers[ind] for ind in markerindices]

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        # Must use at least 3 cell markers.
        if len(markerindices) < 3:
            GUIUtils.display_error_message("Not enough markers selected",
                                           "Please select at least three markers for clustering")
            return

        # If loading a model, must use the same number of markers as were used when the model was trained.
        if isloadingmodel:
            if len(markerindices) != numtrainmarkers:
                GUIUtils.display_error_message("Incompatible number of markers",
                                               "Please ensure you use the same number of markers as the model you loaded")
                return
        self.pixelclustermarkers.append(markernames)

        # Save image attributes to the output folder.
        outfolder = GUIUtils.create_new_folder("RAPIDPixel_", self.outputfolder)
        self.pixelclusterdirectories.append(outfolder)
        datafolder = os.path.join(outfolder, "RAPID_Data")
        hf = zarr.open(datafolder, 'w')
        hf.attrs['markers'] = self.markers
        hf.attrs['flipimg'] = self.imageisflipped

        # Add a separate popup window for the user to define patches to use for training.
        if not randompatchgeneration and patchesstart == []:
            self.modelparams = modelparams

            # Keep track of where the patches are located for each image.
            self.currentimage = 0
            shapesdata = []
            for i in range(self.numimgs):
                patchesstart.append([])
                shapesdata.append([])

            names = []
            for i in range(len(self.filenames)):
                names.append(self.filenames[i].split("/")[-1])

            contrastlimits = []
            cl = []
            for i in range(len(markerindices)):
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
                for i in range(len(markerindices)):
                    self.define_patches_viewer.layers[i].data = self.viewer.layers[markerindices[i]].data[
                                                                self.currentimage, :, :]
                    self.define_patches_viewer.layers[i].contrast_limits = contrastlimits[self.currentimage][i]

                # Store the shapes for the previous image so they can be added again if necessary.
                for i in range(len(self.define_patches_viewer.layers) - len(markerindices)):
                    if len(self.define_patches_viewer.layers[len(markerindices)].data) > 0:
                        shapesdata[self.currentimage - 1].append(
                            self.define_patches_viewer.layers[len(markerindices)].data)
                    self.define_patches_viewer.layers.pop(len(markerindices))

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

                modelparams = self.apply_clusters_defined_patches(patchesstart, isloadingmodel, outfolder,
                                                                  self.modelparams, markerindices, markernames,
                                                                  modelpath, addgreyimg, addcolorimg)
                GUIUtils.log_actions(self.actionloggerpath, f"gui.pixel_clustering(isloadingmodel={isloadingmodel}, "
                                                            f"predict={predict}, "
                                                            f"randompatchgeneration={randompatchgeneration}, "
                                                            f"markerindices={markerindices}, "
                                                            f"modelparams={modelparams}, "
                                                            f"modelpath=\"{modelpath}\", patchesstart={patchesstart})")
                del self.modelparams
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
            for i in markerindices:
                cmap = self.viewer.layers[i].colormap
                self.define_patches_viewer.add_image(self.viewer.layers[i].data[0, :, :], name=self.markers[i],
                                                     rgb=False, colormap=cmap, contrast_limits=[0, 255],
                                                     visible=True, blending="additive")

        elif patchesstart != []:
            modelparams = self.apply_clusters_defined_patches(patchesstart, isloadingmodel, outfolder, modelparams,
                                                              markerindices, markernames, modelpath, addgreyimg,
                                                              addcolorimg)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.pixel_clustering(isloadingmodel={isloadingmodel}, "
                                                        f"predict={predict}, "
                                                        f"randompatchgeneration={randompatchgeneration}, "
                                                        f"markerindices={markerindices}, modelparams={modelparams}, "
                                                        f"modelpath=\"{modelpath}\", patchesstart={patchesstart})")

        # If randomly generating patches.
        else:
            # If predicting without any further training.
            if isloadingmodel and predict:
                # Update parameters and save them to the output folder.
                hf = zarr.open("/".join(modelpath[:-1]) + "/RAPID_Data", 'r')
                args = Namespace(**hf.attrs['arg'])
                args.nchannels = hf["data"].shape[1]
                args.GUI = True
                args.rfold = "/".join(modelpath[:-1])
                copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(outfolder, "checkpoint.pth"))
                args.train = False
                args.predict = True
                args.testbs = 20000
                print(args)

                # Normalize data for RAPID input.
                self.viewer.status = "Generating RAPID data..."
                self.generate_RAPID_data(markerindices,
                                         markernames,
                                         datafolder,
                                         False,
                                         args.normalize,
                                         args.normalizeall,
                                         args.normtype,
                                         args.pca,
                                         )
                self.viewer.status = "Applying loaded model..."

            # If training a model.
            else:
                # If training a pretrained model.
                if isloadingmodel:
                    # Update parameters and save them to the output folder.
                    hf = zarr.open("/".join(modelpath[:-1]) + "/RAPID_Data", 'r')
                    args = Namespace(**hf.attrs['arg'])
                    args.rfold = "/".join(modelpath[:-1])
                    copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(outfolder, "checkpoint.pth"))
                    args.reassume = True
                    if modelparams == []:
                        params = GUIUtils.RAPIDTrainLoadedParams(args)
                        params.exec()
                        if not params.OK:
                            return
                        args.ncluster = int(params.nc)
                        args.nit = int(params.nit)
                        args.bs = int(params.bs)
                        args.patchsize = int(params.ps)
                        args.npatches = int(params.nop)
                        args.mse = params.mse == "True"
                        args.rescale = params.RC == "True"
                        args.rescalefactor = float(params.RCN)
                        args.lr = float(params.lr)
                        args.SCANloss = params.SCAN
                        denoise = params.denoise
                        modelparams = [args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse,
                                       args.rescale, args.rescalefactor, args.lr, args.SCANloss, denoise]
                    else:
                        args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse, \
                        args.rescale, args.rescalefactor, args.lr, args.SCANloss, denoise = modelparams

                # If training a new model.
                else:
                    # Update parameters and save them to the output folder.
                    args = runRAPIDzarr.get_parameters()
                    maximgshape = np.insert(self.maximageshape, 0, self.nummarkers)
                    args.rfold = self.outputfolder
                    args.loadmodel = False
                    if modelparams == []:
                        params = GUIUtils.RAPIDPixelParameters(len(markerindices), maximgshape)
                        params.exec()
                        if not params.OK:
                            return
                        args.ncluster = int(params.nc)
                        args.nit = int(params.nit)
                        args.bs = int(params.bs)
                        args.patchsize = int(params.ps)
                        args.npatches = int(params.nop)
                        args.mse = params.mse == "True"
                        args.rescale = params.RC == "True"
                        args.rescalefactor = float(params.RCN)
                        args.lr = float(params.lr)
                        args.SCANloss = params.SCAN
                        normalize = params.normalize
                        denoise = params.denoise
                        modelparams = [args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse,
                                       args.rescale, args.rescalefactor, args.lr, args.SCANloss, normalize, denoise]
                    else:
                        args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse, \
                        args.rescale, args.rescalefactor, args.lr, args.SCANloss, normalize, denoise = modelparams
                    args.normalize, args.normalizeall, args.normtype, args.pca = GUIUtils.pixel_normtype(normalize)

                self.viewer.status = "Generating RAPID data..."
                self.generate_RAPID_data(markerindices,
                                         markernames,
                                         datafolder,
                                         denoise,
                                         args.normalize,
                                         args.normalizeall,
                                         args.normtype,
                                         args.pca,
                                         )
                self.viewer.status = "Clustering pixels..."
                args.rescale = True
                args.distance = True
                args.epoch = 1
                args.testbs = 20000
                args.GUI = True
                args.predict = False
                hf = zarr.open(datafolder, mode='r+')
                args.nchannels = hf["data"].shape[1]
                hf.attrs['arg'] = vars(args)

            # Train RAPID algorithm.
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.viewer.window._status_bar._toggle_activity_dock(True)
            grey, prob, tab, colors, _ = runRAPIDzarr.train_rapid(args,
                                                                  device,
                                                                  datafolder,
                                                                  outfolder,
                                                                  )
            self.viewer.window._status_bar._toggle_activity_dock(False)
            if not self.hasaddedtable:
                self.analysismode = "Pixel"
            if not os.path.exists(args.rfold):
                os.mkdir(args.rfold)

            # Reshape results into multi-channel image array.
            count = 0
            for i in range(self.numimgs):
                vdim = self.imageshapelist[i][0]
                hdim = self.imageshapelist[i][1]
                self.labeledimgs.append(GUIUtils.convert_dtype(grey[count:count + vdim * hdim].reshape(vdim, hdim)))
                count += vdim * hdim

            # Save colors to the output folder.
            if isloadingmodel:
                colors = np.load("/".join(modelpath[:-1]) + "/color.npy")
            np.save(os.path.join(outfolder, "color.npy"), colors)

            # Update any relevant variables and close the window.
            self.apply_pixel_clustering(tab.values, args, colors, addgreyimg, addcolorimg, outfolder)
            self.pixelclustercount += 1
            self.analysislog.append("P")

            GUIUtils.log_actions(self.actionloggerpath, f"gui.pixel_clustering(isloadingmodel={isloadingmodel}, "
                                                        f"predict={predict}, "
                                                        f"randompatchgeneration={randompatchgeneration}, "
                                                        f"markerindices={markerindices}, modelparams={modelparams}, "
                                                        f"modelpath=\"{modelpath}\", patchesstart={patchesstart},"
                                                        f"addgreyimg={addgreyimg}, addcolorimg={addcolorimg})")

    def quantify_object_cluster_region(self,
                                       imgindex,
                                       shapetypes,
                                       clusteriteration,
                                       verts,
                                       ):
        """
        Find number of cells from each object-based cluster in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
            clusteriteration (int): Index for the round of object clustering being used for analysis.
            verts (list): List of coordinates for vertices being connected to form the shape(s).
        """
        # Find the round of segmentation that corresponds to the current clustering results.
        for i in range(len(self.segmentationclusteringrounds)):
            if clusteriteration in self.segmentationclusteringrounds[i]:
                segmentimgindex = i

        # Store segmented image with corresponding (x,y)-coordinates.
        shape = (self.imageshapelist[imgindex][0], self.imageshapelist[imgindex][1])
        segmentedimg = np.zeros((shape[0], shape[1], 3))
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][segmentimgindex] * self.numimgs + imgindex
        segmentedimg[:, :, 0] = self.labeledimgs[analysisnum]
        for i in range(shape[0]):
            segmentedimg[i, :, 1] = i
        for i in range(shape[1]):
            segmentedimg[:, i, 2] = i
        segmentedimg = np.reshape(segmentedimg, (shape[0] * shape[1], 3))

        # Find number of cells from each phenotype within each shape drawn by the user.
        avgs = []
        numcells = []
        celldata = []
        for i in range(len(verts)):
            # Find the indices of the cells that are contained within the current shape.
            p = self.create_shape_path(verts[i][:, -2:], shapetypes[i])
            mask = p.contains_points(segmentedimg[:, 1:])
            cellids = segmentedimg[:, 0][mask].astype(np.uint32)
            cellids = np.unique(cellids)
            cellids = copy.deepcopy(cellids[cellids > 0])
            tabdata = self.datalist[self.segmentationindices[segmentimgindex * self.numimgs + imgindex]]
            tabdata = np.c_[np.array([i + 1 for i in range(len(tabdata))]), tabdata]
            tabdata = pd.DataFrame(tabdata[[cellid - 1 for cellid in cellids], :])
            tabdata.columns = ["Cell ID"] + self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            celldata.append(tabdata)

            # Find the cluster IDs that correspond to each of the cells within the current shape.
            clustervals = np.zeros_like(cellids)
            clusternums = self.cellclustervals[clusteriteration * self.numimgs + imgindex]
            for i in range(len(clustervals)):
                clustervals[i] = clusternums[int(cellids[i]) - 1]

            # Count total number of cells from each cluster in the current shape, as well as the total number of cells.
            numcellspercluster = []
            analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][clusteriteration] * self.numimgs
            labelimg = self.concat_label_imgs(
                [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)])
            for i in range(int(np.max(labelimg))):
                numcellspercluster.append(np.count_nonzero(clustervals == i + 1))
            avgs.append(numcellspercluster)
            numcells.append(sum(numcellspercluster))
        return avgs, int(np.max(labelimg)), numcells, celldata

    def quantify_pixel_cluster_region(self,
                                      imgindex,
                                      shapetypes,
                                      clusteriteration,
                                      verts,
                                      ):
        """
        Find number of pixels from each pixel-based cluster in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
            clusteriteration (int): Index for the round of pixel clustering being used for analysis.
            verts (list): List of coordinates for vertices being connected to form the shape(s).
        """
        numpixels = []
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][clusteriteration] * self.numimgs
        labelimg = self.labeledimgs[analysisnum + imgindex]
        currentimg = np.zeros((self.imageshapelist[imgindex][0], self.imageshapelist[imgindex][1], 3))
        currentimg[:, :, 0] = labelimg
        for i in range(len(currentimg)):
            currentimg[i, :, 1] = i
        for i in range(currentimg.shape[1]):
            currentimg[:, i, 2] = i
        currentimg = np.reshape(currentimg, (self.imageshapelist[imgindex][0] * self.imageshapelist[imgindex][1], 3))
        avgs = []
        for i in range(len(verts)):
            p = self.create_shape_path(verts[i][:, -2:], shapetypes[i])
            mask = p.contains_points(currentimg[:, 1:])
            numpixels.append(np.count_nonzero(mask))
            currentimgavgs = []
            clustervals = currentimg[:, 0][mask]
            for i in range(0, int(np.max(labelimg)) + 1):
                currentimgavgs.append(np.count_nonzero(clustervals == i))
            avgs.append(currentimgavgs)
        return avgs, int(np.max(labelimg)) + 1, numpixels

    def quantify_raw_img_region(self,
                                imgindex,
                                shapetypes,
                                verts,
                                ):
        """
        Find average expression values for each cell marker in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
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
        currentimg = np.reshape(currentimg, (self.nummarkers, dim1 * dim2, currentimg.shape[3]))
        avgs = []
        numpixels = []
        for i in range(len(verts)):
            p = self.create_shape_path(verts[i][:, -2:], shapetypes[i])
            mask = p.contains_points(currentimg[0, :, 1:])
            numpixels.append(np.count_nonzero(mask))
            currentimgavgs = []
            for j in range(self.nummarkers):
                img = currentimg[j, :, 0]
                avg = np.mean(img[mask])
                currentimgavgs.append(round(avg, 2))
            avgs.append(currentimgavgs)
        return avgs, numpixels

    def quantify_region(self,
                        israwimg=None,
                        clusteringindex=None,
                        shapeverts=[],
                        shapetypes=[],
                        imgnum=None,
                        regionnames=[],
                        ):
        """
        Provide quantitative readouts for the phenotypes of pixels or cells in each shape drawn by the user, either for
        the raw image or for a clustered image.

        Args:
            israwimg (bool, optional): If True, quantify average expression for each marker in each region. Otherwise, use cluster assignments (Default: None).
            clusteringindex (int, optional): Index of clustering round being used for analysis (Default: None).
            shapeverts (list, optional): List of coordinates for vertices being connected to form the shape(s) (Default: None).
            shapetypes (list, optional): List of strings representing shapes for the connected series of vertices (Default: None).
            imgnum (int, optional): Index of the image being quantified (Default: None).
            regionnames (list, optional): List of names for each region being analyzed (Default: None).
        """
        # Find the bounding vertices and the geometries for each of the shapes drawn.
        removeshapeslayer = False
        if shapeverts == [] or shapetypes == [] or imgnum is None:
            # Ensure there is at least one shape drawn in order to define the region to be quantified.
            ind = -1
            for i in reversed(range(len(self.viewer.layers))):
                if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and self.viewer.layers[
                    i].visible:
                    ind = i
                    break
            if ind == -1:
                GUIUtils.display_error_message("Please draw a shape first",
                                               "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
                return
            shapeverts = [self.viewer.layers[ind].data[i] for i in range(len(self.viewer.layers[ind].data))]
            shapetypes = [self.viewer.layers[ind].shape_type[i] for i in range(len(self.viewer.layers[ind].data))]
            imgnum = self.viewer.dims.current_step[0]
            removeshapeslayer = True
        else:
            shapeverts = [np.array(verts) for verts in shapeverts]

        # Can only do this if an image has been loaded or if the current image ID is greater than the number of
        # images (ie, more UMAP plots than there are images).
        if imgnum > self.numimgs:
            GUIUtils.display_error_message("No image in the viewer",
                                           "Please make sure that there is a valid image being displayed in the viewer")
            return

        # Prompt user to define whether to quantify average marker expression from raw image, or cluster number
        # of objects from cluster assignments.
        if israwimg is None:
            if len(self.clustersarepixelbased) > 0:
                selectdatapopup = GUIUtils.SelectData()
                selectdatapopup.exec()
                if not selectdatapopup.OK:
                    return
                israwimg = selectdatapopup.rawimg
            else:
                israwimg = True

        # If using raw image, find average expression of each marker in each shape.
        if israwimg:
            # Find averages and number of pixels in each shape.
            avgs, numpixels = self.quantify_raw_img_region(imgnum, shapetypes, shapeverts)

            # Re-color and label each of the shapes.
            if removeshapeslayer:
                self.viewer.layers.pop(ind)
            labels = []
            for i in range(len(avgs)):
                labels.append(f"Region {i + 1}")
            properties = {'class': labels, }
            textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
            self.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, properties=properties,
                                   name=f"Quantified Regions {self.selectedregioncount}", text=textproperties,
                                   face_color=[np.array([0.2, 0.2, 0.2])])

            # Add labels for each of the regions for the saved csv file and to add to the shapes.
            outfolder = GUIUtils.create_new_folder("QuantifiedRawRegion_", self.outputfolder)
            addnewshapeslayer = True
            if regionnames == []:
                quantifypopup = GUIUtils.QuantifyRegionPopup(avgs, "raw", len(self.markers), self.markers, numpixels,
                                                             outfolder, self.selectedregioncount)
                quantifypopup.exec()
                if quantifypopup.saved:
                    regionnames = list(quantifypopup.headernames)[1:]
                addnewshapeslayer = quantifypopup.saved

            else:
                self.save_quantified_region(avgs, "raw", len(self.markers), self.markers, numpixels, outfolder,
                                            self.selectedregioncount)

            if not regionnames == labels and addnewshapeslayer:
                self.viewer.layers.pop(len(self.viewer.layers) - 1)
                properties = {'class': regionnames, }
                text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                self.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0,
                                       name=f"Quantified Regions {self.selectedregioncount}",
                                       properties=properties, text=text_properties,
                                       face_color=[np.array([0.2, 0.2, 0.2])])
            self.selectedregioncount += 1

        # If using clustered results, find number of pixels/cells from each cluster within each shape.
        else:
            if clusteringindex is None:
                # If clustering has only been done once, use that by default.
                if len(self.clustersarepixelbased) == 1:
                    clusteringindex = 0
                # If clustering has been done more than once, prompt the user to choose which one to use.
                else:
                    selectclusteringround = GUIUtils.SelectClusteringRound(self.clustersarepixelbased)
                    selectclusteringround.exec()
                    if not selectclusteringround.OK:
                        return
                    clusteringindex = selectclusteringround.clusteringindex
            ispixelcluster = self.clustersarepixelbased[clusteringindex]

            clustermodeindex = [i for i, ispixelbased in enumerate(self.clustersarepixelbased) if
                                ispixelbased == ispixelcluster].index(clusteringindex)

            clusteringind = [i for i, m in enumerate(self.clustersarepixelbased) if m == ispixelcluster][
                clustermodeindex]
            clusternames = self.clusternames[clusteringind]

            # If the user selected pixel-based clustering results.
            if ispixelcluster:
                # Find number of pixels from each cluster in each shape.
                avgs, numrows, numpixels = self.quantify_pixel_cluster_region(imgnum, shapetypes, clustermodeindex,
                                                                              shapeverts)

                # Re-color and label each of the shapes.
                if removeshapeslayer:
                    self.viewer.layers.pop(ind)
                labels = []
                for i in range(len(avgs)):
                    labels.append(f"Region {i + 1}")
                properties = {'class': labels}
                textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white'}
                self.viewer.add_shapes(shapeverts,
                                       shape_type=shapetypes,
                                       edge_width=0,
                                       properties=properties,
                                       name=f"Quantified Regions {self.selectedregioncount}",
                                       text=textproperties,
                                       face_color=[np.array([0.2, 0.2, 0.2])],
                                       )

                # Add labels for each of the regions for the saved csv file and to add to the shapes.
                outfolder = GUIUtils.create_new_folder("QuantifiedPixelRegion_",
                                                       self.outputfolder,
                                                       )
                addnewshapeslayer = True
                if regionnames == []:
                    quantifypopup = GUIUtils.QuantifyRegionPopup(avgs,
                                                                 "pixel",
                                                                 numrows,
                                                                 self.markers,
                                                                 numpixels,
                                                                 outfolder,
                                                                 self.selectedregioncount,
                                                                 clusternames=clusternames)
                    quantifypopup.exec()
                    if quantifypopup.saved:
                        regionnames = list(quantifypopup.headernames)[1:]
                    addnewshapeslayer = quantifypopup.saved
                else:
                    self.save_quantified_region(avgs,
                                                "pixel",
                                                numrows,
                                                self.markers,
                                                numpixels,
                                                outfolder,
                                                self.selectedregioncount,
                                                clusternames=clusternames)

                if not regionnames == labels and addnewshapeslayer:
                    self.viewer.layers.pop(len(self.viewer.layers) - 1)
                    properties = {'class': regionnames, }
                    textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    self.viewer.add_shapes(shapeverts,
                                           shape_type=shapetypes,
                                           edge_width=0,
                                           name=f"Quantified Regions {self.selectedregioncount}",
                                           properties=properties,
                                           text=textproperties,
                                           face_color=[np.array([0.2, 0.2, 0.2])],
                                           )
                self.selectedregioncount += 1

            else:
                # Find averages and number of pixels in each shape.
                avgs, numrows, numcells, celldata = self.quantify_object_cluster_region(imgnum,
                                                                                        shapetypes,
                                                                                        clustermodeindex,
                                                                                        shapeverts,
                                                                                        )

                # Re-color and label each of the shapes.
                if removeshapeslayer:
                    self.viewer.layers.pop(ind)
                labels = []
                for i in range(len(avgs)):
                    labels.append(f"Region {i + 1}")
                properties = {'class': labels, }
                textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                self.viewer.add_shapes(shapeverts,
                                       shape_type=shapetypes,
                                       edge_width=0,
                                       name=f"Quantified Regions {self.selectedregioncount}",
                                       properties=properties,
                                       text=textproperties,
                                       face_color=[np.array([0.2, 0.2, 0.2])],
                                       )

                # Add labels for each of the regions for the saved csv file and to add to the shapes.
                outfolder = GUIUtils.create_new_folder("QuantifiedObjectRegion_", self.outputfolder)

                addnewshapeslayer = True
                if regionnames == []:
                    quantifypopup = GUIUtils.QuantifyRegionPopup(avgs,
                                                                 "object",
                                                                 numrows,
                                                                 self.markers,
                                                                 numcells,
                                                                 outfolder,
                                                                 self.selectedregioncount,
                                                                 celldata=celldata,
                                                                 clusternames=clusternames,
                                                                 )
                    quantifypopup.exec()
                    if quantifypopup.saved:
                        regionnames = list(quantifypopup.headernames)[1:]
                    addnewshapeslayer = quantifypopup.saved
                else:
                    self.save_quantified_region(avgs,
                                                "object",
                                                numrows,
                                                self.markers,
                                                numcells,
                                                outfolder,
                                                self.selectedregioncount,
                                                celldata=celldata,
                                                clusternames=clusternames,
                                                )

                if not regionnames == labels and addnewshapeslayer:
                    self.viewer.layers.pop(len(self.viewer.layers) - 1)
                    properties = {'class': regionnames, }
                    textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    self.viewer.add_shapes(shapeverts,
                                           shape_type=shapetypes,
                                           edge_width=0,
                                           name=f"Quantified Regions {self.selectedregioncount}",
                                           properties=properties,
                                           text=textproperties,
                                           face_color=[np.array([0.2, 0.2, 0.2])],
                                           )
                self.selectedregioncount += 1
        GUIUtils.log_actions(self.actionloggerpath, f"gui.quantify_region(israwimg={israwimg}, "
                                                    f"clusteringindex={clusteringindex}, "
                                                    f"shapeverts={[verts.tolist() for verts in shapeverts]}, "
                                                    f"shapetypes={shapetypes}, imgnum={imgnum}, "
                                                    f"regionnames={regionnames})")

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
        >>> b = np.array([[0, 0, 0, 0, 0],
        ...               [1, 1, 1, 1, 0],
        ...               [1, 1, 1, 0, 1]], bool)
        >>> c = RAPIDGUI.remove_large_objects(a, 7)
        >>> c
        array([[False, False, False, True,  False],
               [ True,  True,  True, False, False],
               [ True,  True,  True, False, True]], dtype=bool)
        >>> d = RAPIDGUI.remove_large_objects(b, 7, connectivity=2)
        >>> d
        array([[False, False, False, False, False],
               [False, False, False, False, False],
               [False, False, False, False, True]], dtype=bool)
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

    ### TODO: Think of which analyses the cluster names should be used for, as well as with saved files.
    def rename_clusters_gui(self):
        """
        Trigger the "Rename Clusters" popup from the GUI.
        """
        self.rename_clusters()

    def rename_clusters(self,
                        clusteringindex=None,
                        newclusternames=[],
                        ):
        """
        Prompt the user to select a round of clustering and assign a name to each cluster.
        """
        # Check that the user has performed at least one clustering algorithm.
        if len(self.clustersarepixelbased) == 0:
            GUIUtils.display_error_message("No clustering results found",
                                           "Spatial analysis can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been executed once, use that by default.
        if clusteringindex is None:
            if len(self.clustersarepixelbased) == 1:
                clusteringindex = 0

            # If clustering has been executed multiple times, allow user to select which one.
            else:
                selectclusteringround = GUIUtils.SelectClusteringRound(self.clustersarepixelbased)
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                clusteringindex = selectclusteringround.clusteringindex

        ispixelcluster = self.clustersarepixelbased[clusteringindex]
        clustermodeindex = [i for i, ispixelbased in enumerate(self.clustersarepixelbased) if
                            ispixelbased == ispixelcluster].index(clusteringindex)

        # Find current names of clusters.
        currentnames = copy.deepcopy(self.clusternames[clusteringindex])

        # If list is empty, find number of clusters and use those for the names.
        if len(currentnames) == 0:
            if ispixelcluster:
                analysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][clustermodeindex] * self.numimgs
                labelimg = self.concat_label_imgs(
                    [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)], pixelbased=True)
                numclusters = len(np.unique(labelimg))
            else:
                analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][clustermodeindex] * self.numimgs
                labelimg = self.concat_label_imgs(
                    [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)])
                numclusters = len(np.unique(labelimg)) - 1
            currentnames = [f"Cluster {i + 1}" for i in range(numclusters)]
            oldnames = [str(i + 1) for i in range(numclusters)]
        else:
            oldnames = currentnames

        # Prompt user to rename clusters.
        if newclusternames == []:
            renameclusters = GUIUtils.RenameClusters(currentnames)
            renameclusters.exec()
            if not renameclusters.OK:
                return
            newclusternames = renameclusters.newclusternames

        # Store new names in list.
        self.clusternames[clusteringindex] = newclusternames

        if not ispixelcluster:
            self.objectclusterdfs[clustermodeindex]['Cluster'] = [newclusternames[oldnames.index(name)] for name in
                                                                  self.objectclusterdfs[clustermodeindex]['Cluster']]
            self.objectclusterdfs[clustermodeindex].to_csv(
                os.path.join(self.objectclusterdirectories[clustermodeindex], "SegmentationClusterIDs.csv"))

        # If table is currently visible, update the names accordingly.
        index, _ = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
        if index == clustermodeindex and ((self.analysismode == "Pixel" and ispixelcluster) or (
                self.analysismode == "Object" and not ispixelcluster)):
            self.currentverticalheaderlabels[3:] = [newclusternames[clusternum] for clusternum in
                                                    self.currenttableordersfiltered[self.tableindex]]
            self.tablewidget.setVerticalHeaderLabels(np.asarray(self.currentverticalheaderlabels))
            vwidth = GUIUtils.font_width("Helvetica", 12, self.currentverticalheaderlabels)
            self.tablewidget.verticalHeader().setMinimumWidth(vwidth + 15)

        GUIUtils.log_actions(self.actionloggerpath, f"gui.rename_clusters(clusteringindex={clusteringindex}, "
                                                    f"newclusternames={newclusternames})")

    ### TODO: Add other functionalities for this (grouped results for cluster averages, new table entries for combined average within groups, etc.).
    def sample_group_gui(self):
        """
        Trigger the "Sample Grouping" popup from the GUI.
        """
        self.sample_group()

    def sample_group(self,
                     namelist={},
                     name="",
                     ):
        """
        Open a popup window for the user to assign each image to different groups.

        Args:
            namelist (dict, optional): Dictionary mapping each group name to the names of all images in that group (Default: {}).
            name (str, optional):  (Default: "").
        """
        # No necessity to assign groups if fewer than 3 images are loaded.
        if self.numimgs < 3:
            GUIUtils.display_error_message("More images required",
                                           "At least 3 images needed to create groups")
            return

        # Prompt user to define the number of groups
        if namelist == {} or name == "":
            ng = GUIUtils.NumGroups(self.numimgs)
            ng.exec()
            if not ng.OK:
                return

            # Retrieve the names of all loaded images.
            imgnames = [fname.split("/")[-1] for fname in self.filenames]

            # Prompt user to assign each image to a group.
            gawidget = GUIUtils.GroupAssign(ng.ngroups, imgnames, self.groupsnames)
            gawidget.exec()
            if not gawidget.OK:
                return
            namelist = gawidget.namelist
            name = gawidget.name

        self.groupslist.append(namelist)
        self.groupsnames.append(name)
        GUIUtils.log_actions(self.actionloggerpath, f"gui.sample_group(namelist={namelist}, name=\"{name}\")")

    def save_data_gui(self):
        """
        Trigger the "Save Data" popup from the GUI.
        """
        self.save_data()

    def save_data(self,
                  savedimg="",
                  ispixelcluster=None,
                  clusteringnum=None,
                  filename="",
                  ):
        """
        Open a popup for the user to save data. Options include "Save Visible Window" (to save exactly what is currently
        visible in the viewer window), "Save Screenshot of GUI" (to save a screenshot of the entire RAPID GUI window),
        "Save Clusters" (to save each individual cluster from a selected round of clustering), "Save Table" (to export
        the exact data table currently being displayed as a csv file), and "Save Full Visible Images" (to save each
        user-selected raw image individually, including contrast limits and colormaps).

        Args:
            savedimg (str, optional) Indicator of what data will be saved (Default: "").
            ispixelcluster (bool, optional) If True, the clusters being saved are pixel-based. Otherwise, the clusters being saved are object-based (Default: "").
            clusteringnum (int, optional) Round of pixel/object clustering results being saved (Default: "").
            filename (str, optional) Path to root directory where clustering data will be saved (Default: "").
        """
        if savedimg == "":
            savedata = GUIUtils.SaveData()
            savedata.exec()
            if not savedata.OK:
                return
            savedimg = savedata.savedimg

        self.viewer.status = "Saving..."
        if savedimg == "Visible Window":
            GUIUtils.save_visible(self.viewer, self.outputfolder)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Screenshot":
            GUIUtils.save_window(self.viewer, self.outputfolder)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Table":
            GUIUtils.save_table(self.viewer, self.fulltab, self.outputfolder)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Full Visible Images":
            GUIUtils.save_visible_full(self.viewer, self.outputfolder, self.filenames, self.imageisflipped,
                                       self.imageshapelist)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Clusters":
            # User can only save clusters after having performed clustering.
            if len(self.clustersarepixelbased) == 0:
                GUIUtils.display_error_message("Clustering has not been executed",
                                               "Please run a clustering algorithm first")
                return

            # If clustering has been performed once, use that by default.
            if len(self.clustersarepixelbased) == 1:
                ispixelcluster = self.clustersarepixelbased[0]
                clusteringnum = 0

            # If clustering has been performed more than once, allow user to select which clustering results to use.
            elif ispixelcluster is None and clusteringnum is None:
                selectclusteringround = GUIUtils.SelectClusteringRound(self.clustersarepixelbased)
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                ispixelcluster = selectclusteringround.ispixelcluster
                clusteringnum = selectclusteringround.clusteringnum

            if ispixelcluster:
                analysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][clusteringnum]
            else:
                analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][clusteringnum]
            grey = self.concat_label_imgs([self.labeledimgs[i] for i in range(analysisnum, analysisnum + self.numimgs)],
                                          pixelbased=ispixelcluster)

            # Prompt user to choose path to output folder where clusters will be saved.
            if filename == "":
                filename, _ = QFileDialog.getSaveFileName(parent=self.viewer.window.qt_viewer, caption='Save clusters',
                                                          directory=self.outputfolder)
            outfolder = GUIUtils.create_new_folder(os.path.split(filename)[-1], os.path.split(filename)[0])

            GUIUtils.save_clusters(outfolder, grey, self.filenames, self.imageshapelist, self.imageisflipped)
            GUIUtils.log_actions(self.actionloggerpath, f"gui.save_data(savedimg=\"{savedimg}\", "
                                                        f"ispixelcluster={ispixelcluster}, "
                                                        f"clusteringnum={clusteringnum}, filename=\"{filename}\")")

    ### TODO: Do this continuously while using GUI. Store/load all global variables from there.
    def save_environment(self):
        """
        Save a RAPID GUI session so the user may resume it exactly as they are leaving it.
        """
        self.viewer.status = "Saving environment..."
        GUIUtils.log_actions(self.actionloggerpath, "gui.save_environment()")

        # Store variables.
        config = configparser.ConfigParser()
        config.add_section("Variables")
        config.set("Variables", 'hasaddedtable', unicode(self.hasaddedtable))
        config.set("Variables", 'haseditedimage', unicode(self.haseditedimage))
        config.set("Variables", 'hasloadedpixel', unicode(self.hasloadedpixel))
        config.set("Variables", 'hasloadedimage', unicode(self.hasloadedimage))

        config.set("Variables", 'actionloggerpath', unicode(self.actionloggerpath))
        config.set("Variables", 'analysisindex', unicode(self.analysisindex))
        config.set("Variables", 'analysismode', unicode(self.analysismode))
        config.set("Variables", 'biaxialcount', unicode(self.biaxialcount))
        config.set("Variables", 'displayselectedcount', unicode(self.displayselectedcount))
        config.set("Variables", 'editimagepath', unicode(self.editimagepath))
        config.set("Variables", 'numimgs', unicode(self.numimgs))
        config.set("Variables", 'nummarkers', unicode(self.nummarkers))
        config.set("Variables", 'objectclustercount', unicode(self.objectclustercount))
        config.set("Variables", 'pixelclustercount', unicode(self.pixelclustercount))
        config.set("Variables", 'resolution', unicode(self.resolution))
        config.set("Variables", 'segmentcount', unicode(self.segmentcount))
        config.set("Variables", 'selectedregioncount', unicode(self.selectedregioncount))
        config.set("Variables", 'tableimgcount', unicode(self.tableimgcount))
        config.set("Variables", 'tableindex', unicode(self.tableindex))
        config.set("Variables", 'umapcount', unicode(self.umapcount))

        config.set("Variables", 'analysislog', unicode(self.analysislog))
        config.set("Variables", 'cellclustervals', unicode([arr.tolist() for arr in self.cellclustervals]))
        config.set("Variables", 'cellcoordinates', unicode(self.cellcoordinates))
        config.set("Variables", 'clustersarepixelbased', unicode(self.clustersarepixelbased))
        config.set("Variables", 'clusternames', unicode(self.clusternames))
        config.set("Variables", 'currentlyselected', unicode(self.currentlyselected))
        config.set("Variables", 'currentstep', unicode(self.viewer.dims.current_step[:-2]))
        config.set("Variables", 'currenttableordersfiltered', unicode(self.currenttableordersfiltered))
        config.set("Variables", 'currenttableorderfull', unicode(self.currenttableorderfull))
        config.set("Variables", 'currentverticalheaderlabels', unicode(self.currentverticalheaderlabels.tolist()))
        config.set("Variables", 'datalist', unicode([arr.tolist() for arr in self.datalist]))
        config.set("Variables", 'editactions', unicode(self.editactions))
        config.set("Variables", 'filenames', unicode(self.filenames))
        config.set("Variables", 'fulltab', unicode(self.fulltab.to_json()))
        config.set("Variables", 'groupslist', unicode(self.groupslist))
        config.set("Variables", 'groupsnames', unicode(self.groupsnames))
        config.set("Variables", 'histogramcounts', unicode(self.histogramcounts))
        config.set("Variables", 'imageisflipped', unicode(self.imageisflipped))
        config.set("Variables", 'imageshapelist', unicode(self.imageshapelist))
        config.set("Variables", 'labeledimgs', unicode([arr.tolist() for arr in self.labeledimgs]))
        config.set("Variables", 'lowerboundslist', unicode(self.lowerboundslist))
        config.set("Variables", 'markers', unicode(self.markers))
        config.set("Variables", 'maximageshape', unicode([arr.tolist() for arr in self.maximageshape]))
        config.set("Variables", 'maxpixelclustervals', unicode(self.maxpixelclustervals))
        config.set("Variables", 'maxvals', unicode(self.maxvals))
        config.set("Variables", 'mergedimagespaths', unicode(self.mergedimagespaths))
        config.set("Variables", 'mergememmarkers', unicode(self.mergememmarkers))
        config.set("Variables", 'mergenucmarkers', unicode(self.mergenucmarkers))
        config.set("Variables", 'minvals', unicode(self.minvals))
        config.set("Variables", 'objectclustercolors', unicode([arr.tolist() for arr in self.objectclustercolors]))
        config.set("Variables", 'objectclusterdfs', unicode([d.to_json() for d in self.objectclusterdfs]))
        config.set("Variables", 'objectclusterdirectories', unicode(self.objectclusterdirectories))
        config.set("Variables", 'objectclusterindices', unicode(self.objectclusterindices))
        config.set("Variables", 'objectimgnames', unicode(self.objectimgnames).replace('%', '%%'))
        config.set("Variables", 'pixelclustercolors', unicode([arr.tolist() for arr in self.pixelclustercolors]))
        config.set("Variables", 'pixelclusterdirectories', unicode(self.pixelclusterdirectories))
        config.set("Variables", 'pixelclusterindices', unicode(self.pixelclusterindices))
        config.set("Variables", 'pixelclustermarkers', unicode(self.pixelclustermarkers))
        coords = []
        for i in range(len(self.plotcoordinates)):
            coords.append([arr.tolist() for arr in self.plotcoordinates[i]])
        config.set("Variables", 'plotcoordinates', unicode(coords))
        config.set("Variables", 'plotisumap', unicode(self.plotisumap))
        config.set("Variables", 'plotsegmentationindices', unicode(self.plotsegmentationindices))
        config.set("Variables", 'plotxmins', unicode(self.plotxmins))
        config.set("Variables", 'plotxmaxs', unicode(self.plotxmaxs))
        config.set("Variables", 'plotymins', unicode(self.plotymins))
        config.set("Variables", 'plotymaxs', unicode(self.plotymaxs))
        config.set("Variables", 'segmentationclusteringrounds', unicode(self.segmentationclusteringrounds))
        config.set("Variables", 'segmentationindices', unicode(self.segmentationindices))
        config.set("Variables", 'segmentationzarrpaths', unicode(self.segmentationzarrpaths))
        config.set("Variables", 'segmentcounts', unicode(self.segmentcounts))
        config.set("Variables", 'tableimagenames', unicode(self.tableimagenames).replace('%', '%%'))
        config.set("Variables", 'tableparams', unicode(self.tableparams))
        config.set("Variables", 'totalnumcells', unicode(self.totalnumcells))
        config.set("Variables", 'upperboundslist', unicode(self.upperboundslist))
        if self.hasaddedtable:
            config.set("Variables", 'currenttabdata', unicode(self.currenttabdata.tolist()))
            config.set("Variables", 'tableorder', unicode(self.tableorder))
            config.set("Variables", 'tablecurrentmarker', unicode(self.sorttableimages.marker.value))
            config.set("Variables", 'tablecurrentdata', unicode(self.sorttableimages.data.value).replace('%', '%%'))
            config.set("Variables", 'tablecurrentsort', unicode(self.sorttableimages.sort.value))
            config.set("Variables", 'totalnumrows', unicode(self.totalnumrows))

        # Save variables to a config file.
        outfolder = GUIUtils.create_new_folder("SavedEnvironment", self.outputfolder)
        cfgfile = open(os.path.join(outfolder, "savedenvironment.ini"), "w")
        config.write(cfgfile)
        cfgfile.close()

        # Store metadata for all layers in the GUI.
        fh = zarr.open(outfolder, mode='a')
        for i in range(len(self.viewer.layers)):
            if isinstance(self.viewer.layers[i], napari.layers.shapes.shapes.Shapes):
                data = fh.create_dataset(f"ShapeLayer_{i + 1}", data=np.array([0]))
                data.attrs["Data"] = [arr.tolist() for arr in self.viewer.layers[i].data]
                data.attrs["ShapeType"] = self.viewer.layers[i].shape_type
                data.attrs["Properties"] = self.viewer.layers[i].properties["class"].tolist() if "class" in \
                                                                                                 self.viewer.layers[
                                                                                                     i].properties else ""
                data.attrs["Name"] = self.viewer.layers[i].name
                data.attrs["Text"] = [self.viewer.layers[i].text.size,
                                      self.viewer.layers[i].text.color.tolist()]
                data.attrs["FaceColor"] = self.viewer.layers[i].face_color.tolist()
                data.attrs["Visible"] = self.viewer.layers[i].visible
            else:
                data = fh.create_dataset(f"ImageLayer_{i + 1}", data=self.viewer.layers[i].data)
                data.attrs["Visible"] = self.viewer.layers[i].visible
                data.attrs["Name"] = self.viewer.layers[i].name
                try:
                    data.attrs["CL"] = [float(j) for j in self.viewer.layers[i].contrast_limits]
                    data.attrs["CLRange"] = [float(j) for j in self.viewer.layers[i].contrast_limits_range]
                    data.attrs["Gamma"] = self.viewer.layers[i].gamma
                    data.attrs["Opacity"] = self.viewer.layers[i].opacity
                    data.attrs["Colormap0"] = int(self.viewer.layers[i].colormap.colors[-1][0] * 255)
                    data.attrs["Colormap1"] = int(self.viewer.layers[i].colormap.colors[-1][1] * 255)
                    data.attrs["Colormap2"] = int(self.viewer.layers[i].colormap.colors[-1][2] * 255)
                except:
                    pass
        self.viewer.status = "Completed saving environment"

    def save_quantified_region(self,
                               avgs,
                               imgtype,
                               numrows,
                               markernames,
                               numregions,
                               outfolder,
                               selectedregioncount,
                               celldata=np.array([]),
                               clusternames=[],
                               ):
        horizontalheaders = [f"Region {j + 1}" for j in range(len(avgs))]

        verticalheaders = []
        if imgtype == 'object':
            verticalheaders.append('# Cells')
        else:
            verticalheaders.append('# Pixels')
        for i in range(numrows):
            if imgtype == "raw":
                verticalheaders.append(markernames[i])
            else:
                if clusternames == []:
                    verticalheaders.append(f"Cluster {i + 1}")
                else:
                    verticalheaders.append(clusternames[i])

        arr = np.array(avgs)
        arr = np.transpose(arr)
        arr = np.vstack((np.array(numregions), arr))
        df = pd.DataFrame(arr)
        df.columns = horizontalheaders
        df.insert(0, '', verticalheaders)
        df.to_csv(os.path.join(outfolder, f"QuantifiedRegionClusters_{selectedregioncount}.csv"), index=False)
        if imgtype == 'object':
            for i in range(len(celldata)):
                celldata[i].to_csv(os.path.join(outfolder, f"QuantifiedRegionCellIDs_{i}.csv"), index=False)

    def segment(self,
                modelindex=None,
                imageres=None,
                mergemarkerindex=None,
                addgreyimg=None,
                addcolorimg=None,
                quantavg=None,
                probthreshold=None,
                minsize=None,
                maxsize=None,
                histogramnormalize=None,
                ):
        """
        Use the RAPID segmentation algorithm on the images loaded into the RAPID GUI.

        Args:
            modelindex (int, optional): Index corresponding to segmentation model being used (Default: None).
            imageres (float, optional): Resolution of the image, in units of nanometers per pixel (Default: None).
            mergemarkerindex (int, optional): Index of merged-marker image being used for segmentation (Default: None).
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            quantavg (bool, optional): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values (Default: None).
            probthreshold (float, optional): Value in the range [0,1] defining model prediction probability threshold for cells to include (Default: None).
            minsize (int, optional): Minimum pixel area of cells to include in segmentation (Default: None).
            maxsize (int, optional): Maximum pixel area of cells to include in segmentation (Default: None).
            histogramnormalize (bool, optional): If True, perform histogram normalization. Otherwise, do nothing (Default: False).
        """
        # Can only segment if markers have been merged.
        if len(self.segmentcounts) == 0:
            GUIUtils.display_error_message("Please merge markers first",
                                           "Begin by opening the image(s) that you would like to segment, then merge the markers to be used for segmentation.")
            return

        if modelindex is None:
            # Indicate whether to use RAPID or RAPID+ segmentation model.
            segmentationmodel = GUIUtils.SegmentationModel()
            segmentationmodel.exec()
            if not segmentationmodel.OK:
                return
            modelindex = segmentationmodel.modelindex

        if histogramnormalize is None:
            # Indicate whether to use RAPID or RAPID+ segmentation model.
            histogram = GUIUtils.HistogramNormalize()
            histogram.exec()
            if not histogram.OK:
                return
            histogramnormalize = histogram.normalize

        rootfolder = os.path.dirname(os.path.abspath(__file__))
        modelpaths = [rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6.pth",
                      rootfolder + "/../models/RAPID-O_RDSB_DC_Fin__MemMix_UnetPlus_Model__resnet50_nclass_2_nchannels_2_gpu_4_seed_100_DCBD38_theta_0.6.pth",
                      rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6_Plus.pth"]
        fileurls = ["https://drive.google.com/uc?id=1JiYrohWce5-uLjI_-yovDUUxroorwE5W",
                    "https://drive.google.com/uc?id=1MQjnmpmflQ-BvWgRbsQXwyeQjjfod4mw",
                    "https://drive.google.com/uc?id=1Ji6XmIITbcKR05wt86USEWuous_K5SWl"]
        for i, path in enumerate(modelpaths):
            if not os.path.exists(path):
                gdown.download(fileurls[i], path, verify=False)
        modelpath = modelpaths[modelindex]

        # Prompt user to indicate the resolution of the images.
        if self.segmentcount == 0:
            if imageres is None:
                res = GUIUtils.ImageRes()
                res.exec()
                if not res.OK:
                    return
                self.resolution = res.imageres
            else:
                self.resolution = imageres

        # If user has merged markers multiple times, prompt to indicate which one to use.
        if len(self.segmentcounts) == 1:
            mergemarkerindex = 0
        elif mergemarkerindex is None:
            mergememiteration = GUIUtils.MergeMarkerIteration(len(self.segmentcounts))
            mergememiteration.exec()
            if not mergememiteration.OK:
                return
            mergemarkerindex = mergememiteration.iteration

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        # Allow user to define wither to quantify using mean expression, or root-mean-square.
        if quantavg is None:
            quantmode = GUIUtils.QuantificationMode()
            quantmode.exec()
            if not quantmode.OK:
                return
            quantavg = quantmode.avg

        # Save images to zarr so they can be easily added when loading segmentation results in the future.
        outfolder = GUIUtils.create_new_folder("Segmentation", self.outputfolder)
        os.mkdir(os.path.join(outfolder, "RawImages"))
        fh = zarr.open(os.path.join(outfolder, "RawImages"), mode='a')
        for i in range(self.nummarkers):
            data = fh.create_dataset(f"{i + 1}_{self.viewer.layers[i].name}", data=self.viewer.layers[i].data)
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
        hf = zarr.open(self.mergedimagespaths[mergemarkerindex], mode='r')
        memimg = hf['Membrane']
        nucimg = hf['Nucleus']
        fh = zarr.open(outfolder, mode='a')
        fh.create_dataset("MergedImage", data=np.stack([memimg, nucimg], axis=0))

        if not self.hasaddedtable:
            self.analysismode = "Segmentation"

        # Check if the user has already segmented on the selected merged image.
        alreadysegmented = True
        if self.segmentcounts[mergemarkerindex][modelindex] == -1 or self.histogramcounts[mergemarkerindex][
            histogramnormalize] == -1:
            alreadysegmented = False
            self.segmentcounts[mergemarkerindex][modelindex] = np.max(np.array(self.segmentcounts) + 1)
            self.histogramcounts[mergemarkerindex][histogramnormalize] = 0

        # No need to segment again on a merged image that has already been passed through the algorithm.
        if not alreadysegmented:
            self.viewer.status = "Segmenting..."
            self.segmentationzarrpaths.append(outfolder)
            self.viewer.window._status_bar._toggle_activity_dock(True)
            with progress(self.filenames, desc='Image', total=0 if len(self.filenames) == 1 else None, ) as pbr:
                for name in pbr:
                    i = self.filenames.index(name)
                    memimage = memimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]]
                    nucimage = nucimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]]
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    feature = objectmodels.unet_featurize(memimg=memimage, nucimg=nucimage,
                                                          containsmem=self.mergememmarkers[mergemarkerindex],
                                                          containsnuc=self.mergenucmarkers[mergemarkerindex],
                                                          device=device, segmodelpath=modelpath,
                                                          histogramnormalize=histogramnormalize)
                    fh.create_dataset(f"Features{i}", data=feature, dtype=np.float)
            self.viewer.window._status_bar._toggle_activity_dock(False)
        zarrpath = self.segmentationzarrpaths[self.segmentcounts[mergemarkerindex][modelindex]]

        if all(prob is not None for prob in (probthreshold, minsize, maxsize)):
            self.apply_segmentation(addgreyimg,
                                    addcolorimg,
                                    quantavg,
                                    outfolder,
                                    zarrpath,
                                    probthreshold,
                                    minsize,
                                    maxsize,
                                    )
            GUIUtils.log_actions(self.actionloggerpath, f"gui.segment(modelindex={modelindex}, imageres={imageres}, "
                                                        f"mergemarkerindex={mergemarkerindex}, addgreyimg={addgreyimg}, "
                                                        f"addcolorimg={addcolorimg}, quantavg={quantavg}, "
                                                        f"probthreshold={probthreshold}, minsize={minsize}, "
                                                        f"maxsize={maxsize}, histogramnormalize={histogramnormalize})")

        else:
            # Initialize thresholds to use for segmentation preview popup window.
            self.probthreshold = 1.0
            self.currentimagenum = 0
            self.minsize = round(10 * 0.284 / self.resolution)
            self.maxsize = round(2000 * 0.284 / self.resolution)

            # Populate the segmentation preview popup window.
            fh = zarr.open(zarrpath, mode='r')
            binarized = np.array(fh["Features0"]) >= self.probthreshold
            blobs = measure.label(binarized, connectivity=1)
            blobs = morphology.remove_small_objects(blobs, min_size=int(self.minsize))
            blobs = self.remove_large_objects(blobs, maxsize=int(self.maxsize))
            binarized[blobs == 0] = 0
            self.segmentviewer = napari.Viewer()
            self.segmentviewer.add_image(binarized[:self.imageshapelist[0][0], :self.imageshapelist[0][1]],
                                         name="Segmentation", blending="additive", colormap="red",
                                         contrast_limits=[0, 1])
            if self.mergenucmarkers[mergemarkerindex]:
                self.segmentviewer.add_image(nucimg[0, :self.imageshapelist[0][0], :self.imageshapelist[0][1]],
                                             name="Merged Nuclear Markers", blending="additive")
            if self.mergememmarkers[mergemarkerindex]:
                self.segmentviewer.add_image(memimg[0, :self.imageshapelist[0][0], :self.imageshapelist[0][1]],
                                             name="Merged Membrane Markers", blending="additive")

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
                self.segmentviewer.layers["Segmentation"].data = segmented[
                                                                 :self.imageshapelist[self.currentimagenum][0],
                                                                 :self.imageshapelist[self.currentimagenum][1]]
                if self.mergenucmarkers[mergemarkerindex]:
                    self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :
                                                                                                            self.imageshapelist[
                                                                                                                self.currentimagenum][
                                                                                                                0], :
                                                                                                                    self.imageshapelist[
                                                                                                                        self.currentimagenum][
                                                                                                                        1]]
                if self.mergememmarkers[mergemarkerindex]:
                    self.segmentviewer.layers["Merged Membrane Markers"].data = memimg[self.currentimagenum, :
                                                                                                             self.imageshapelist[
                                                                                                                 self.currentimagenum][
                                                                                                                 0], :
                                                                                                                     self.imageshapelist[
                                                                                                                         self.currentimagenum][
                                                                                                                         1]]

            # Apply filters for final segmented results.
            @magicgui(call_button="Finish")
            def finish_segmentgui() -> Image:
                self.apply_segmentation(addgreyimg,
                                        addcolorimg,
                                        quantavg,
                                        outfolder,
                                        self.segmentationzarrpaths[self.segmentcounts[mergemarkerindex][modelindex]],
                                        self.probthreshold,
                                        self.minsize,
                                        self.maxsize,
                                        )

                GUIUtils.log_actions(self.actionloggerpath,
                                     f"gui.segment(modelindex={modelindex}, imageres={self.resolution}, "
                                     f"mergemarkerindex={mergemarkerindex}, addgreyimg={addgreyimg}, "
                                     f"addcolorimg={addcolorimg}, quantavg={quantavg}, "
                                     f"probthreshold={self.probthreshold}, minsize={self.minsize}, "
                                     f"maxsize={self.maxsize}, histogramnormalize={histogramnormalize})")

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
                if self.mergenucmarkers[mergemarkerindex]:
                    self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
                if self.mergememmarkers[mergemarkerindex]:
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
                if self.mergenucmarkers[mergemarkerindex]:
                    self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
                if self.mergememmarkers[mergemarkerindex]:
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
                if self.mergenucmarkers[mergemarkerindex]:
                    self.segmentviewer.layers["Merged Nuclear Markers"].data = nucimg[self.currentimagenum, :, :]
                if self.mergememmarkers[mergemarkerindex]:
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

    def sort_table_image(self,
                         data="",
                         marker="",
                         sort="",
                         ):
        """
        Populate the table according to the currently selected image and round of analysis, the parameter that it is
        sorted according to, and whether the user indicated for it to sort in ascending or descending order.

        Args:
            data (str, optional): Name of analysis round being displayed in the table (Default: "").
            marker (str, optional): Name of the cell marker or parameter that the table will be sorted by (Default: "").
            sort (str, optional): Indicator to sort in either increasing or decreasing order (Default: "").
        """
        if data == "":
            data = self.sorttableimages.data.value
        else:
            self.sorttableimages.data.value = data
        if marker == "":
            marker = self.sorttableimages.marker.value
        else:
            self.sorttableimages.marker.value = marker
        if sort == "":
            sort = self.sorttableimages.sort.value
        else:
            self.sorttableimages.sort.value = sort

        # Make sure analysis has been done and that there is a table to be displayed.
        if (self.segmentcount > 0 or self.pixelclustercount > 0) and not self.isloadingenv:
            # Get the index of the round of analysis being displayed in the table.
            index = self.tableimagenames.index(data)
            self.tableindex = copy.deepcopy(index)

            # If displaying segmentation results.
            if index in self.segmentationindices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                self.analysismode = "Segmentation"
                self.analysisindex = self.segmentationindices.index(index)
                datatab = copy.deepcopy(self.datalist[self.tableindex])

                # Get the column being used to sort the table and sort the clusters according to user selection.
                m = self.tableparams.index(marker)

                # Find the order by which to sort the cells in the table.
                if m > 0:
                    self.currenttableorderfull = np.argsort(self.datalist[self.tableindex][:, m - 1]).astype(
                        np.int).tolist()
                else:
                    self.currenttableorderfull = [i for i in range(len(self.datalist[self.tableindex]))]
                if sort == "▼":
                    self.currenttableorderfull.reverse()

                # Filter out cells that don't fall within the user-defined lower/upper bounds.
                filtereddata = np.append(self.datalist[self.tableindex][self.currenttableorderfull, :],
                                         np.expand_dims(np.arange(len(self.datalist[self.tableindex])), 1), 1)
                for chan in range(len(self.lowerboundslist[self.tableindex])):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(
                        self.upperboundslist[self.tableindex][chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(
                        self.lowerboundslist[self.tableindex][chan], 3))
                    filtereddata = filtereddata[filtermask]
                self.currenttableordersfiltered[self.tableindex] = [self.currenttableorderfull[j] for j in
                                                                    filtereddata[:, -1].astype(np.int).tolist()]

                # Get the cell indices to be used as the vertical header labels.
                cellnumlabels = [self.currenttableorderfull[j] + 1 for j in filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the cells according to user selection and update the table accordingly.
                displaytab = datatab[self.currenttableordersfiltered[self.tableindex], :]
                self.update_table(displaytab,
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(datatab),
                                  cellnumlabels)

            # If displaying object-based clustering results.
            elif index in self.objectclusterindices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                self.analysismode = "Object"
                self.analysisindex = self.objectclusterindices.index(index)
                currentdata = copy.deepcopy(self.datalist[self.tableindex])

                # Find any clusters for the current round of analysis that have at least one cell.
                clusters = []
                for i in range(len(currentdata)):
                    if currentdata[i, 0] != 0.0:
                        clusters.append(i)

                # Get the column being used to sort the table and sort the clusters according to user selection.
                m = self.tableparams.index(marker)
                if m == 0:
                    self.currenttableorderfull = np.arange(len(currentdata)).tolist()
                else:
                    self.currenttableorderfull = np.argsort(currentdata[:, m]).astype(np.int).tolist()
                if sort == "▼":
                    self.currenttableorderfull.reverse()

                # Filter out clusters that don't fall within the user-defined lower/upper bounds.
                filtereddata = currentdata[self.currenttableorderfull, 1:]
                filtereddata = np.append(filtereddata, np.expand_dims(np.arange(len(self.currenttableorderfull)), 1), 1)
                for chan in range(len(self.lowerboundslist[self.tableindex])):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(
                        self.upperboundslist[self.tableindex][chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(
                        self.lowerboundslist[self.tableindex][chan], 3))
                    filtereddata = filtereddata[filtermask]
                self.currenttableordersfiltered[self.tableindex] = [self.currenttableorderfull[i] for i in
                                                                    filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the clusters according to user selection and update the table accordingly.
                displaydata = currentdata[self.currenttableordersfiltered[self.tableindex], :]

                # Find names for the clusters for the round of clustering being displayed in the table.
                clusterindex, _ = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                annotationindex = [j for j, n in enumerate(self.clustersarepixelbased) if not n][clusterindex]

                # Update the display table in the GUI.
                self.update_table(displaydata,
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(clusters),
                                  self.currenttableordersfiltered[self.tableindex],
                                  headernames=self.clusternames[annotationindex])

            # If displaying pixel-based clustering results.
            elif index in self.pixelclusterindices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                self.analysismode = "Pixel"
                self.analysisindex = self.pixelclusterindices.index(index)
                currentdata = copy.deepcopy(self.datalist[self.tableindex])

                # Sort the clusters according to user selection.
                if marker in self.markers:
                    m = self.markers.index(marker) + 1
                    self.currenttableorderfull = np.argsort(currentdata[:, m]).astype(np.int).tolist()
                else:
                    self.currenttableorderfull = np.arange(len(currentdata)).tolist()
                if sort == "▼":
                    self.currenttableorderfull.reverse()

                # Filter out clusters that don't fall within the user-defined lower/upper bounds.
                filtereddata = currentdata[self.currenttableorderfull, 1:]
                filtereddata = np.append(filtereddata, np.expand_dims(np.arange(len(filtereddata)), 1), 1)
                for chan in range(len(self.lowerboundslist[self.tableindex])):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(
                        self.upperboundslist[self.tableindex][chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(
                        self.lowerboundslist[self.tableindex][chan], 3))
                    filtereddata = filtereddata[filtermask]
                self.currenttableordersfiltered[self.tableindex] = [self.currenttableorderfull[i] for i in
                                                                    filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the clusters according to user selection and update the table accordingly.
                displaydata = currentdata[self.currenttableordersfiltered[self.tableindex], :]

                # Find names for the clusters for the round of clustering being displayed in the table.
                clusterindex, _ = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
                annotationindex = [i for i, n in enumerate(self.clustersarepixelbased) if n][clusterindex]

                # Update the display table in the GUI.
                self.update_table(displaydata,
                                  self.lowerboundslist[self.tableindex],
                                  self.upperboundslist[self.tableindex],
                                  len(currentdata),
                                  self.currenttableordersfiltered[self.tableindex],
                                  headernames=self.clusternames[annotationindex])

            if self.updatelogfile:
                GUIUtils.log_actions(self.actionloggerpath, f"gui.sort_table_image(data=\"{data}\", "
                                                            f"marker=\"{marker}\", sort=\"{sort}\")")

    def spatial_analysis(self,
                         clusteringindex=None,
                         npix=None,
                         nsim=None,
                         ):
        """
        Perform spatial codistribution analysis on a user-defined clustered image.

        Args:
            clusteringindex (int, optional): Index of clustering round being used for analysis (Default: None).
            npix (int, optional): Number of pixels included per simulation (Default: None).
            nsim (int, optional): Number of simulations to use for spatial analysis (Default: None).
        """
        # Check that the user has performed at least one clustering algorithm.
        if len(self.clustersarepixelbased) == 0:
            GUIUtils.display_error_message("No clustering results found",
                                           "Spatial analysis can only be performed on the results of pixel or object clustering.")
            return

        if clusteringindex is None:
            # If clustering has only been executed once, use that by default.
            if len(self.clustersarepixelbased) == 1:
                clusteringindex = 0

            # If clustering has been executed multiple times, allow user to select which one.
            else:
                selectclusteringround = GUIUtils.SelectClusteringRound(self.clustersarepixelbased)
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                clusteringindex = selectclusteringround.clusteringindex
        ispixelcluster = self.clustersarepixelbased[clusteringindex]
        clustermodeindex = [i for i, ispixelbased in enumerate(self.clustersarepixelbased) if
                            ispixelbased == ispixelcluster].index(clusteringindex)

        # Retrieve the labeled cluster images for the selected round of clustering.
        if ispixelcluster:
            analysisnum = [i for i, n in enumerate(self.analysislog) if n == "P"][clustermodeindex] * self.numimgs
        else:
            analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][clustermodeindex] * self.numimgs

        for i in range(self.numimgs):
            clusterimg = np.zeros((self.maximageshape[0], self.maximageshape[1]),
                                  dtype=self.labeledimgs[analysisnum + i].dtype)
            if i == 0:
                rclusters = np.zeros((self.maximageshape[0], self.maximageshape[1]),
                                     dtype=self.labeledimgs[analysisnum + i].dtype)
                rclusters[:self.imageshapelist[0][0], :self.imageshapelist[0][1]] = self.labeledimgs[analysisnum]
            else:
                clusterimg[:self.imageshapelist[i][0], :self.imageshapelist[i][1]] = self.labeledimgs[analysisnum + i]
                rclusters = KNN.concat_images(rclusters, clusterimg)

        ### TODO: Make default parameters intelligent.
        if npix is None or nsim is None:
            spatialparams = GUIUtils.SpatialParameters()
            spatialparams.exec()
            if not spatialparams.OK:
                return
            npix = spatialparams.npix
            nsim = spatialparams.nsim
        pval, tab = KNN.random_kdtree_single(rclusters, npix, nsim, objectclusters=True)
        for i in range(len(tab)):
            val = copy.deepcopy(tab[i, i])
            tab[i:, i] = tab[i:, i] - val
            tab[i, :i] = tab[i, :i] - val
        outfolder = GUIUtils.create_new_folder("SpatialAnalysis", self.outputfolder)
        pd.DataFrame(tab).to_csv(os.path.join(outfolder, "FCVals.csv"))

        tab += tab.transpose()
        tab = np.max(tab) - tab
        lowerrange = np.median(tab) - np.min(tab)
        upperrange = np.max(tab) - np.median(tab)
        ratio = lowerrange / upperrange
        tab[tab > np.median(tab)] = (tab[tab > np.median(tab)] - np.median(tab)) * ratio + np.median(tab)
        self.set_invisible(self.viewer)

        DataTab = pd.DataFrame(tab)
        plt.figure(figsize=(40, 40))

        clustervals = np.array(DataTab.columns)
        clustervals[clustervals >= rclusters[5, 5]] += 1
        if ispixelcluster:
            clustervals += 1

        ClusterDend = sns.clustermap(DataTab, row_cluster=True, col_cluster=True, linewidth=0.05,
                                     center=np.median(tab), vmax=np.max(tab), vmin=0, yticklabels=clustervals,
                                     xticklabels=clustervals, cmap="RdBu_r")
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.show(block=False)
        plt.title("Spatial Analysis")
        plt.savefig(os.path.join(outfolder, "Codistribution.png"), format="PNG", dpi=300)
        heatmap = imread(os.path.join(outfolder, "Codistribution.png"))
        self.set_invisible(self.viewer)
        self.viewer.add_image(heatmap, name='Codistribution', blending="additive")

        df = pd.DataFrame(pval)
        df.to_csv(os.path.join(outfolder, "PVals.csv"))
        pval[pval < 0.00000001] = 255
        pval[pval < 0.000001] = 150
        pval[pval < 0.0001] = 75
        pval[pval < 0.05] = 25
        pval[pval < 25] = 0
        df_pval = pd.DataFrame(pval)
        df_pval.index.astype(str).str.replace(r"^", "RP-")
        df_pval.index = ([f"RP-{i + 1}" for i in df_pval.index])
        df_pval.columns = ([f"RP-{i + 1}" for i in df_pval.columns.values])
        df_pval.to_csv(os.path.join(outfolder, "NormalizedPVals.csv"))
        GUIUtils.log_actions(self.actionloggerpath, f"gui.spatial_analysis(clusteringindex={clusteringindex}, "
                                                    f"npix={npix}, nsim={nsim})")

    def subcluster(self,
                   segindex=None,
                   clusteringindex=None,
                   markernums=[],
                   clusternum=None,
                   algname="",
                   modelpath="",
                   addgreyimg=None,
                   addcolorimg=None,
                   continuetraining=None,
                   modelparams=[],
                   ):
        """
        Allow user to select an object-based cluster and clustering algorithm to further subdivide the chosen cluster.

        Args:
            segindex (int, optional): Index of segmentation round being clustered (Default: None).
            clusteringindex (int, optional): Index of object clustering round being subclustered (Default: None).
            markernums (list, optional): List of indices of parameters to be considered for clustering (Default: []).
            clusternum (int, optional): Index of cluster subclustered (Default: None).
            algname (str, optional): Name of the specified algorithm to be used for clustering (Default: "").
            modelpath (str, optional): Path to the model being used if loading a pretrained model (Default: "").
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            continuetraining (bool, optional): If True, continue training the model after loading it. Otherwise, predict without further training (Default: None).
            modelparams (iterable, optional): List of parameters for the desired clustering algorithm (Default: []).
        """
        # Determine which round of segmentation to use.
        if segindex is None:
            segindex = 0
            if len(self.objectimgnames) > 1:
                segmentedimage = GUIUtils.SelectSegmentedImage(self.objectimgnames)
                segmentedimage.exec()
                if not segmentedimage.OK:
                    return
                segindex = segmentedimage.imageindex

        # Determine which round of clustering to use.
        if len(self.segmentationclusteringrounds[segindex]) == 0:
            GUIUtils.display_error_message("Must run clustering first",
                                           "Please run a clustering algorithm (\"Object Clustering\" or \"UMAP Annotation\") first")
            return
        elif len(self.segmentationclusteringrounds[segindex]) == 1:
            clusteringindex = self.segmentationclusteringrounds[segindex][0]
        elif clusteringindex is None:
            iteration = GUIUtils.ObjectClusterIteration(self.segmentationclusteringrounds[segindex])
            iteration.exec()
            if not iteration.OK:
                return
            clusteringindex = self.segmentationclusteringrounds[segindex][iteration.iteration]

        # Define which markers to use to train the sub-clustering algorithm.
        if markernums == []:
            trainmarkers = GUIUtils.RAPIDObjectParams(self.markers)
            trainmarkers.exec()
            if not trainmarkers.OK:
                return
            markernums = trainmarkers.markernums
        startindex = clusteringindex * self.numimgs

        # Select which cluster to subdivide.
        analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][clusteringindex] * self.numimgs
        outfolder = GUIUtils.create_new_folder(
            os.path.join(os.path.split(self.objectclusterdirectories[clusteringindex])[-1], "Subclustered_"),
            self.outputfolder)
        if clusternum is None:
            labelimg = self.concat_label_imgs(
                [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)])
            clusternums = [i + 1 for i in range(len(np.unique(labelimg)) - 1)]
            selectcluster = GUIUtils.SubCluster(clusternums)
            selectcluster.exec()
            if not selectcluster.OK:
                return
            clusternum = selectcluster.cluster

        # Define the algorithm to be used to sub-divide the cluster.
        if algname == "" or algname == "Pretrained" and modelpath == "":
            alg = GUIUtils.ClusteringAlgorithm(self.objectimgnames, issubclustering=True)
            alg.exec()
            if not alg.OK:
                return
            algname = alg.algname
            if algname == "Pretrained":
                modelpath = alg.dirpath

        # Retrieve the full segmented data table for the defined cluster and the number of cells from that
        # cluster in each image.
        numcellsperimage = []
        currentimage = []
        cellids = []
        for i in range(self.numimgs):
            currentsegmentedimg = self.datalist[self.segmentationindices[i + segindex * self.numimgs]]
            numcellstotal = len(self.datalist[self.segmentationindices[i + segindex * self.numimgs]])
            clusterids = self.cellclustervals[startindex + i]
            cellids.append([j + 1 for j in range(numcellstotal) if int(clusterids[j]) == int(clusternum)])
            numcellsperimage.append(len(cellids[-1]))
            currentimage.append(currentsegmentedimg[[id - 1 for id in cellids[-1]], :])
        currentimage = np.vstack(currentimage)

        # Allow user to decide whether to add the labeled and/or colored image.
        if addgreyimg is None and addcolorimg is None:
            selectimagesadded = GUIUtils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            addgreyimg = selectimagesadded.grey
            addcolorimg = selectimagesadded.color
        if addgreyimg is None:
            addgreyimg = False
        if addcolorimg is None:
            addcolorimg = False

        # If using the RAPID algorithm for sub-clustering.
        if algname == "RAPID":
            # Define the parameters used to train the model.
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = GUIUtils.RAPIDObjectParameters(len(markernums))
                params.exec()
                if not params.OK:
                    return
                args.ncluster = int(params.nc)
                args.nit = int(params.nit)
                args.bs = int(params.bs)
                if params.mse == "True":
                    args.mse = True
                else:
                    args.mse = False
                args.lr = float(params.lr)
                args.blankpercent = float(params.blankpercent)
                modelparams = [args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent]
            else:
                args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent = modelparams
            args.epoch = 1
            args.GUI = True
            args.distance = 'YES'

            # Initialize the model and train the algorithm.
            self.viewer.status = "Training RAPID..."
            model = RAPIDMixNet(dimension=len(markernums), nummodules=5, mse=args.mse, numclusters=args.ncluster)
            model.apply(weight_init)
            print(model)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08,
                                    weight_decay=0.01, amsgrad=False)
            self.train_object(model, currentimage[:, markernums], optimizer, args)

        elif algname == "Phenograph":
            # Define the parameters used for phenograph clustering.
            model = 0
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = GUIUtils.PhenographParameters()
                params.exec()
                if not params.OK:
                    return
                args.PGdis = str(params.PGdis)
                args.PGnn = int(params.PGnn)
                args.PGres = float(params.PGres)
                args.graphalgo = params.graphalgo
                args.normalize = params.normalize
                modelparams = [args.PGdis, args.PGnn, args.PGres, args.graphalgo, args.normalize]
            else:
                args.PGdis, args.PGnn, args.PGres, args.graphalgo, args.normalize = modelparams
            args.GUI = True

        elif algname == "SciPy":
            # Define the parameters used for the specified SciPy clustering algorithm.
            model = 0
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = GUIUtils.SciPyParameters()
                params.exec()
                if not params.OK:
                    return
                args.normalize = params.normalize
                args.scipyalgo = params.scipyalgo
                args.scipykwarg = params.scipykwarg
                algname = params.scipyalgo
                modelparams = [args.normalize, args.scipyalgo, args.scipykwarg]
            else:
                args.normalize, args.scipyalgo, args.scipykwarg = modelparams
            args.GUI = True

        else:
            # Load a pretrained RAPID-O model.
            model = 0

            try:
                hf = zarr.open("/".join(modelpath[:-1]), 'r')
                loadedargs = hf.attrs['arg']
            except:
                return

            if continuetraining is None:
                loadoptions = GUIUtils.LoadModelOptions()
                loadoptions.exec()
                if not loadoptions.OK:
                    return
                continuetraining = not loadoptions.prediction

            args = Namespace(**loadedargs)
            if continuetraining:
                if modelparams == []:
                    params = GUIUtils.RAPIDObjectTrainLoadedParameters(args)
                    params.exec()
                    if not params.OK:
                        return
                    args.nit = int(params.nit)
                    args.bs = int(params.bs)
                    args.lr = float(params.lr)
                    args.blankpercent = float(params.blankpercent)
                    modelparams = [args.nit, args.bs, args.lr, args.blankpercent]
                else:
                    args.nit, args.bs, args.lr, args.blankpercent = modelparams
                args.epoch = 1
                args.GUI = True
                args.distance = 'YES'

        # If the cluster being subdivided is selected in the table, remove it from the layers list.
        index = f"Cluster {clusternum} (Object [{clusteringindex}])"
        for i in reversed(range(len(self.viewer.layers))):
            if self.viewer.layers[i].name == index:
                self.viewer.layers.pop(i)
                break

        # Apply subclustering algorithm and relabel cells.
        self.viewer.status = "Performing subclustering..."
        self.set_invisible(self.viewer)
        self.test_object_subcluster(model, currentimage, args, numcellsperimage, clusteringindex, clusternum, outfolder,
                                    segindex, startindex, markernums, algname, cellids, addcolorimg, addgreyimg)
        self.viewer.status = "RAPID subclustering complete"
        GUIUtils.log_actions(self.actionloggerpath, f"gui.subcluster(segindex={segindex}, "
                                                    f"clusteringindex={clusteringindex}, markernums={markernums}, "
                                                    f"clusternum={clusternum}, algname=\"{algname}\", "
                                                    f"modelpath=\"{modelpath}\", addgreyimg={addgreyimg}, "
                                                    f"addcolorimg={addcolorimg}, continuetraining={continuetraining}, "
                                                    f"modelparams={modelparams})")

    def test_object(self,
                    model,
                    quantifiedvals,
                    args,
                    markerindices,
                    addcolorimg,
                    addgreyimg,
                    alg,
                    tabindex=0,
                    optimizer="",
                    outputpath="",
                    predict=False,
                    ):
        """
        Apply a clustering algorithm to segmented results.

        Args:
            model (RAPID.network.f): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            args (Namespace): Additional user-defined parameters used for training.
            markerindices (list): List of ints corresponding to the indices of the markers being used for clustering.
            addcolorimg (bool): True if generating an RGB-colored image, otherwise False.
            addgreyimg (bool): True if generating a grey labeled image, otherwise False.
            tabindex (int, optional): Index value of the table for the first image being clustered on (Default: 0).
            optimizer (torch.optim.AdamW, optional): Initialized optimizer to be used for training (Default: "").
            outputpath (str, optional): Path to the folder where the model will be saved (Default: "").
            predict (bool, optional): True if the model is only being used to predict and no further training, otherwise False (Default: False).
        """
        np.random.seed(args.seed)

        # Stack segmented data tables for each image
        segmentedtab = []
        for i in range(self.numimgs):
            segmentedtab.append(self.datalist[self.segmentationindices[i + tabindex]][:, markerindices])
        segmentedtab = np.vstack(segmentedtab)

        # Pass segmentation results through clustering algorithm of choice.
        if alg == "Phenograph":
            os.chdir(self.outputfolder)
            phenopgraphin = segmentedtab[:, 1:]
            if args.normalize:
                phenopgraphin = MinMaxScaler().fit_transform(phenopgraphin)
            clusterids, graph, Q = phenograph.cluster(phenopgraphin, n_jobs=1, clustering_algo=str(args.graphalgo),
                                                      resolution_parameter=float(args.PGres), k=int(args.PGnn),
                                                      primary_metric=str(args.PGdis), seed=args.seed)

        elif alg == "RAPID":
            torch.manual_seed(args.seed)
            torch.cuda.manual_seed(args.seed)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            if device == "cuda":
                torch.set_deterministic(True)
                torch.backends.cudnn.deterministic = True
            model.eval()
            with torch.no_grad():
                testdata = quantifiedvals.reshape((-1, quantifiedvals.shape[1]))
                clusterids = np.zeros(len(testdata), dtype=np.uint8)
                for bstart in range(0, len(testdata), 50000):
                    x = torch.from_numpy(testdata[bstart:bstart + 50000, :]).float().to(device)
                    outputs, AA = model(torch.unsqueeze(x, 1))
                    clusterids[bstart:bstart + 50000] = outputs[0].argmax(dim=1).cpu()
            if not predict:
                checkpoint = {'model': RAPIDMixNet(dimension=len(markerindices), nummodules=5, mse=args.mse,
                                                   numclusters=int(args.ncluster)),
                              'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict()}
                torch.save(checkpoint, os.path.join(outputpath, 'checkpoint.pth'))

        else:
            import sklearn.cluster as cluster
            import json
            if alg == "KMeans":
                algo = cluster.KMeans
            if alg == "AffinityPropagation":
                algo = cluster.AffinityPropagation
            if alg == "SpectralClustering":
                algo = cluster.SpectralClustering
            if alg == "AgglomerativeClustering":
                algo = cluster.AgglomerativeClustering
            if alg == "DBSCAN":
                algo = cluster.DBSCAN
            if alg == "HDBSCAN":
                import hdbscan
                algo = hdbscan.HDBSCAN
            print(json.loads(str(args.scipykwarg)))
            clusterids = algo(**json.loads(args.scipykwarg)).fit_predict(segmentedtab[:, 1:])

        clusterids = clusterids.astype(np.uint8)
        self.apply_object_clustering(clusterids, tabindex, segmentedtab, outputpath, addcolorimg, addgreyimg, [])

    def test_object_subcluster(self,
                               model,
                               quantifiedvals,
                               args,
                               numcellsperimage,
                               iteration,
                               clusternum,
                               outfolder,
                               segindex,
                               objectclustersstartindex,
                               markerindices,
                               alg,
                               cellids,
                               addcolorimg,
                               addgreyimg,
                               ):
        """
        Apply a clustering algorithm to a specified cluster from an image that has already been passed through an object
        clustering algorithm.

        Args:
            model (RAPID.network.RAPIDMixNet): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            args (Namespace): Additional user-defined parameters used for training.
            numcellsperimage (list): List of the number of cells that are in each image.
            iteration (int): Index for the round of clustering being subclustered.
            clusternum (int): Index for the cluster that is being subclustered.
            segindex (int): Index value of the table for the first image being clustered on.
            objectclustersstartindex (int): Index for the table corresponding to the first object clustering round being subclustered.
            markerindices (list): List of indices of each of the cell markers included in the table.
            alg (str): String representing the algorithm being used. Options include "Phenograph", "RAPID", "KMeans", "AffinityPropagation", "SpectralClustering", "AgglomerativeClustering", "DBSCAN", and "HDBSCAN".
            cellids (list): List containing the IDs of the cells in the cluster being divided.
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
        """
        np.random.seed(args.seed)
        clusterimg = quantifiedvals[:, markerindices]

        if alg == "Phenograph":
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
                                                     primary_metric=str(args.PGdis), seed=args.seed)

        elif alg == "RAPID":
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            torch.manual_seed(args.seed)
            torch.cuda.manual_seed(args.seed)
            model.eval()
            with torch.no_grad():
                clusterimg = clusterimg.reshape((-1, clusterimg.shape[1]))
                to_values = np.zeros(len(clusterimg))
                for bstart in range(0, len(clusterimg), 50000):
                    x = torch.from_numpy(clusterimg[bstart:bstart + 50000, :]).float().to(device)
                    outputs, AA = model(torch.unsqueeze(x, 1))
                    to_values[bstart:bstart + 50000] = outputs[0].argmax(dim=1).cpu()

        else:
            import sklearn.cluster as cluster
            import json
            if alg == "KMeans":
                algo = cluster.KMeans
            if alg == "AffinityPropagation":
                algo = cluster.AffinityPropagation
            if alg == "SpectralClustering":
                algo = cluster.SpectralClustering
            if alg == "AgglomerativeClustering":
                algo = cluster.AgglomerativeClustering
            if alg == "DBSCAN":
                algo = cluster.DBSCAN
            if alg == "HDBSCAN":
                import hdbscan
                algo = hdbscan.HDBSCAN
            print(json.loads(str(args.scipykwarg)))
            to_values = algo(**json.loads(args.scipykwarg)).fit_predict(clusterimg)

        relabeled_table = np.hstack((to_values.reshape((len(to_values), 1)), quantifiedvals))
        startindex = 0
        images = [i for i in range(len(numcellsperimage)) if numcellsperimage[i] != 0]
        numtabs = 1
        if self.numimgs > 1:
            numtabs += self.numimgs
        data = np.zeros((numtabs, len(np.unique(to_values)), len(self.markers) + 5))
        it = iteration * numtabs
        numclusters = len(self.datalist[self.objectclusterindices[it]]) - 1 + len(np.unique(to_values))
        samplenums = []
        for i in range(self.numimgs):
            tmp_tab = relabeled_table[startindex:startindex + numcellsperimage[images[i]]]
            startindex += numcellsperimage[images[i]]
            tmp_tab_df = pd.DataFrame(tmp_tab)
            grouped = tmp_tab_df.groupby(0)
            tabres = grouped.apply(np.mean)
            unique, counts = np.unique(tmp_tab[:, 0], return_counts=True)
            count = 0
            for j in range(len(np.unique(to_values))):
                if j in unique:
                    data[i, j, 0] = counts[count]
                    count += 1
            data[i, [int(j) for j in unique], 1:] = tabres.values[:, 1:]
            samplenums += [i + 1] * numclusters
        if self.numimgs > 1:
            data[-1, :, 0] = np.sum(data[:-1, :, 0], axis=0)
            for i in range(data.shape[1]):
                data[-1, i, 1:] = np.average(data[:-1, i, 1:], axis=0, weights=data[:-1, i, 0])

        for i in range(numtabs):
            olddata = copy.deepcopy(self.datalist[self.objectclusterindices[it + i]])
            indices = [j for j in range(len(olddata))]
            indices.remove(clusternum - 1)
            newtable = np.zeros((numclusters, len(self.markers) + 5))
            newtable[:len(olddata) - 1, :] = copy.deepcopy(olddata)[indices, :]
            newtable[len(olddata) - 1:, :] = data[i, :, :]
            self.datalist[self.objectclusterindices[it + i]] = newtable
            minvals = []
            maxvals = []
            for j in range(1, newtable.shape[1]):
                minvals.append(np.min(newtable[:, j]))
                maxvals.append(np.max(newtable[:, j]))
            self.minvals[self.objectclusterindices[it + i]] = copy.deepcopy(minvals)
            self.maxvals[self.objectclusterindices[it + i]] = copy.deepcopy(maxvals)
            self.lowerboundslist[self.objectclusterindices[it + i]] = copy.deepcopy(minvals)
            self.upperboundslist[self.objectclusterindices[it + i]] = copy.deepcopy(maxvals)
            if self.analysismode == "Object" and self.analysisindex == it + i:
                self.update_table(newtable, minvals, maxvals, len(newtable))
                self.currenttableordersfiltered[self.tableindex] = [j for j in range(len(newtable))]

        clusterdata = [self.datalist[self.objectclusterindices[i]] for i in range(it, it + self.numimgs)]
        my_data = pd.DataFrame(np.nan_to_num(np.vstack(clusterdata)))
        paramslist = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        my_data.columns = np.hstack([["# Cells"], paramslist])
        my_data.insert(0, "Cluster", np.array([i + 1 for i in range(numclusters)] * self.numimgs))
        my_data.insert(0, "Sample", np.array(samplenums))
        my_data.to_csv(os.path.join(outfolder, "ObjectClusterAvgExpressionVals.csv"))

        ind = self.objectclusterindices[it]
        for i in range(ind, ind + numtabs):
            self.currentlyselected[i] = []

        objanalysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][iteration] * self.numimgs
        seganalysisnum = [i for i, n in enumerate(self.analysislog) if n == "S"][segindex] * self.numimgs
        labelimg = self.concat_label_imgs(
            [self.labeledimgs[ind] for ind in range(objanalysisnum, objanalysisnum + self.numimgs)])
        labelimg[labelimg == clusternum] = 0
        labelimg[labelimg > clusternum] = labelimg[labelimg > clusternum] - 1
        newstart = copy.deepcopy(np.max(labelimg)) + 1
        count = 0
        counter = 0
        tabdata = self.objectclusterdfs[iteration]
        for i in range(self.numimgs):
            updated_to_values = np.array(self.cellclustervals[objectclustersstartindex + i])
            updated_to_values[updated_to_values == clusternum] = -1
            updated_to_values[updated_to_values > clusternum] = updated_to_values[updated_to_values > clusternum] - 1
            segmentedimg = self.labeledimgs[seganalysisnum + i]
            currentgreyimg = labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]]
            for j in range(numcellsperimage[i]):
                currentcell = cellids[i][j]
                currentgreyimg[segmentedimg == currentcell] = int(to_values[count] + newstart)
                updated_to_values[currentcell - 1] = int(to_values[count] + newstart)
                count += 1
            self.cellclustervals[objectclustersstartindex + i] = updated_to_values
            labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] = currentgreyimg
            self.labeledimgs[objanalysisnum + i] = currentgreyimg
            tabdata['Cluster'][counter:counter + len(list(updated_to_values))] = [str(val) for val in updated_to_values]
            counter += len(updated_to_values)

        self.objectclusterdfs[iteration] = tabdata
        tabdata.to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))
        colorimg = np.zeros((self.numimgs, self.maximageshape[0], self.maximageshape[1], 3), dtype=np.uint8)

        colors = self.objectclustercolors[iteration]
        colors = np.append(colors, colors[[clusternum - 1], :], 0)
        colors = np.delete(colors, clusternum - 1, 0)
        newcolors = generate_colormap(len(np.unique(labelimg)))
        while len(colors) < len(np.unique(labelimg)):
            if not newcolors[0, :].tolist() in colors.tolist():
                colors = np.append(colors, newcolors[[0], :], 0)
            newcolors = newcolors[1:, :]
        self.objectclustercolors[iteration] = colors

        for i in range(len(np.unique(labelimg))):
            colorimg[:, :, :, 0][labelimg == i + 1] = colors[i, 0]
            colorimg[:, :, :, 1][labelimg == i + 1] = colors[i, 1]
            colorimg[:, :, :, 2][labelimg == i + 1] = colors[i, 2]

        np.save(os.path.join(outfolder, "color.npy"), colors)
        tabledata, my_data_scaled, distmatrix, uniqueclusters = \
            prep_for_mst(clustertable=my_data,
                         minclustersize=1,
                         clustersizes=my_data["# Cells"],
                         includedmarkers=paramslist,
                         )
        generate_mst(distancematrix=distmatrix,
                     normalizeddf=my_data_scaled,
                     colors=colors,
                     randomseed=0,
                     clusterheatmap=True,
                     outfolder=outfolder,
                     displaymarkers=paramslist,
                     uniqueclusters=uniqueclusters,
                     samplenames=list(np.unique(my_data['Sample'])),
                     displaysingle=False,
                     values="# Cells",
                     )

        clusteringround = int(objectclustersstartindex / self.numimgs)
        if addcolorimg:
            self.viewer.add_image(colorimg,
                                  name=f"Object {clusteringround + 1} Subclustered",
                                  blending="additive",
                                  contrast_limits=(0, 255),
                                  )
        if addgreyimg:
            self.viewer.add_image(labelimg,
                                  name=f"Object {clusteringround + 1} Subcluster IDs",
                                  blending="additive",
                                  contrast_limits=(0, np.max(labelimg)),
                                  )

        self.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                              name=f"Object {clusteringround + 1} Subclustered Heatmap",
                              blending="additive",
                              visible=False,
                              )

        # Save both the label and colored images to the output folder.
        for i in range(self.numimgs):
            imgname = os.path.splitext(os.path.split(self.filenames[i])[-1])[0]
            GUIUtils.save_img(os.path.join(outfolder, f"Subclustered_{imgname}.tif"),
                              colorimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1], :],
                              self.imageisflipped[i])
            GUIUtils.save_img(os.path.join(outfolder, f"SubclusterLabels_{imgname}.tif"),
                              labelimg[i, :self.imageshapelist[i][0], :self.imageshapelist[i][1]] + 1,
                              self.imageisflipped[i])

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

    def train_object(self,
                     model,
                     quantifiedvals,
                     optimizer,
                     args,
                     ):
        """
        Train the RAPID-O clustering model.

        Args:
            model (RAPID.network.RAPIDMixNet): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            optimizer (torch.optim.AdamW): Initialized optimizer to be used for training.
            args (Namespace): Additional user-defined parameters used for training.
        """

        # set the random seed so make results reproducible
        torch.cuda.manual_seed(1000)
        torch.manual_seed(1000)
        np.random.seed(1000)

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
                    loss1 += MSE
            loss1.backward()
            optimizer.step()
            lossAvg = lossAvg + loss1.item()
            if batch_idx % 1 == 0:
                print(
                    'Train Epoch {} -iteration {}/{} - LR {:.6f} -\ttotal loss: {:.6f} -\t IIC loss: {:.3f}'.format(
                        0, batch_idx, numiterations, 10, (lossAvg / 10), loss1))
                lossAvg = 0

    def umap_plot(self,
                  paramindices=[],
                  segindex=None,
                  min_dist=None,
                  n_neighbors=None,
                  metric="",
                  colorbymarkers=None,
                  colorbygroups=[],
                  colorbyindivclusters=None,
                  colorbycombclusters=None,
                  clusteringindex=None,
                  ):
        """
        Generate a UMAP plot according to parameters defined by the user.

        Args:
            paramindices (list, optional): Indices of markers and morphological parameters to be considered for UMAP (Default: []).
            segindex (int, optional): Index of segmentation round to be used for biaxial gating (Default: None).
            min_dist (float, optional): The effective minimum distance between embedded points (Default: None).
            n_neighbors (int, optional): The size of local neighborhood used for manifold approximation (Default: None).
            metric (str, optional): The metric to use to compute distances in high dimensional space (Default: "").
            colorbymarkers (bool, optional): If True, generate a plots for each marker, with color gradients representing expression levels for each respective marker. Otherwise, do nothing (Default: None).
            colorbygroups (list, optional): List of group assignment indices to use for coloring plot(s) (Default: []).
            colorbyindivclusters (bool, optional): If True, generate a plots for each cluster, with vertex colors representing membership of the respective cluster. Otherwise, do nothing (Default: None).
            colorbycombclusters (bool, optional): If True, generate a plot with vertices colored according to cluster assignment. Otherwise, do nothing (Default: None).
            clusteringindex (int, optional): Index of the round of clustering to be used for color assignment, if applicable (Default: None).
        """
        params = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]

        # User must first run object-based segmentation in order to generate a UMAP.
        if self.segmentcount == 0:
            GUIUtils.display_error_message("You must segment before running UMAP",
                                           "UMAP cannot be generated until the image has been segmented")
            return

        # Prompt user to select which cell markers to use as parameters for UMAP.
        if paramindices == []:
            umapmarkers = GUIUtils.RAPIDObjectParams(self.markers, True)
            umapmarkers.exec()
            if not umapmarkers.OK:
                return
            paramindices = umapmarkers.markernums
        paramnames = [params[ind] for ind in paramindices]

        # Prompt user to define the parameters and coloring schemes used for the UMAP.
        if any(param is None for param in (segindex, min_dist, n_neighbors, colorbymarkers)) or metric == "":
            setumapParams = GUIUtils.UMAPParameters(self.objectclustercount > 0, self.objectimgnames,
                                                    self.groupsnames[1:])
            setumapParams.exec()
            if not setumapParams.OK:
                return
            segindex = setumapParams.segmentationindex
            min_dist = setumapParams.min_dist
            n_neighbors = setumapParams.n_neighbors
            metric = setumapParams.metric
            colorbymarkers = setumapParams.colorbymarkers
            if self.objectclustercount > 0:
                colorbyindivclusters = setumapParams.colorbyindivclusters
                colorbycombclusters = setumapParams.colorbycombclusters
            if len(self.groupsnames[1:]) > 0:
                colorbygroups = setumapParams.colorbygroups

        # Count total number of cells in the segmented iteration being used across all images.
        totalcells = 0
        self.plotsegmentationindices.append(segindex * self.numimgs)
        for i in range(self.numimgs):
            totalcells += len(self.datalist[self.segmentationindices[segindex * self.numimgs + i]])

        # Compile quantified cells from each individual image into one combined data array.
        currentimage = np.zeros((totalcells, len(paramindices)))
        currentimage2 = np.zeros((totalcells, self.nummarkers + 4))
        count = 0
        col_list = generate_colormap(self.numimgs + 1)
        cols = np.zeros((totalcells, 3)).astype(np.float)
        cellsperimage = []
        for i in range(self.numimgs):
            cellsincurrimg = []
            numcells = len(self.datalist[self.segmentationindices[segindex * self.numimgs + i]])
            currentimage2[count:count + numcells, :] = self.datalist[
                self.segmentationindices[segindex * self.numimgs + i]]
            currentimage[count:count + numcells, :] = self.datalist[
                                                          self.segmentationindices[segindex * self.numimgs + i]][:,
                                                      paramindices]
            for j in range(count, count + numcells):
                cellsincurrimg.append(j)
                cols[j, :] = col_list[i, :] / np.array([255.0, 255.0, 255.0])
            count += numcells
            cellsperimage.append(cellsincurrimg)

        # Apply UMAP algorithm and remove rows with NaN values.
        reducer = umap.UMAP(min_dist=min_dist, n_neighbors=n_neighbors, metric=metric)
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
        outfolder = GUIUtils.create_new_folder("UMAP_", self.outputfolder)
        plt.savefig(os.path.join(outfolder, "UMAP.png"), format="PNG", dpi=300)
        im = imread(os.path.join(outfolder, "UMAP.png"))
        imarray = np.asarray(im)
        locs = np.where((imarray[:, :, 0] == 242) & (imarray[:, :, 1] == 255) & (imarray[:, :, 2] == 242))
        self.plotxmins.append(np.min(locs[0]))
        self.plotxmaxs.append(np.max(locs[0]))
        self.plotymins.append(np.min(locs[1]))
        self.plotymaxs.append(np.max(locs[1]))
        self.set_invisible(self.viewer)
        self.viewer.add_image(im, name=f"UMAP {self.umapcount}", blending="additive")

        # If selected by user, add an additional stack of scatterplots with vertices colored on a gradient
        # according to each cell marker or morphological parameter.
        if colorbymarkers:
            self.set_invisible(self.viewer)
            pathlist = []
            max = np.percentile(currentimage2[:, :-4], 97)
            min = np.min(currentimage2[:, :-4])
            adj = np.max(currentimage2[:, :-4])
            for i in range(1, 5):
                currentimage2[:, -i] = currentimage2[:, -i] / np.max(currentimage2[:, -i]) * adj
            currentimage2 = currentimage2[:, paramindices]
            for i in range(len(paramindices)):
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
                plt.title(paramnames[i])
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                plt.savefig(os.path.join(outfolder, paramnames[i] + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, paramnames[i] + ".png"))
            imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
            self.viewer.add_image(imx, name=f"UMAP {self.umapcount} (Cell Markers)", blending="additive")

        # If given segmented image iteration has been clustered, check if the user elected to use clustering as
        # a basis for vertex coloring.
        if len(self.segmentationclusteringrounds[segindex]) > 0:
            # If the user is coloring according to cluster assignment, prompt to define which clustering
            # iteration is being used.
            if colorbyindivclusters or colorbycombclusters:
                if len(self.segmentationclusteringrounds[segindex]) > 1:
                    if clusteringindex is None:
                        iteration = GUIUtils.ObjectClusterIteration(self.segmentationclusteringrounds[segindex])
                        iteration.exec()
                        if not iteration.OK:
                            return
                        clusteringindex = iteration.iteration
                    startindex = self.segmentationclusteringrounds[segindex][clusteringindex]
                else:
                    startindex = self.segmentationclusteringrounds[segindex][0]
                clusternums = []
                for i in range(self.numimgs):
                    curclusternums = self.cellclustervals[startindex * self.numimgs + i]
                    for n in curclusternums:
                        clusternums.append(n - 1)
                analysisnum = [i for i, n in enumerate(self.analysislog) if n == "O"][startindex] * self.numimgs
                labelimg = self.concat_label_imgs(
                    [self.labeledimgs[ind] for ind in range(analysisnum, analysisnum + self.numimgs)])
                numclusters = len(np.unique(labelimg)) - 1

            # If selected by user, add a stack of scatterplots with vertices colored red if corresponding to a cell in
            # the respective cluster, or blue otherwise.
            if colorbyindivclusters:
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
                    plt.savefig(os.path.join(outfolder, f"UMAP_Cluster{i + 1}.png"), format="PNG", dpi=300)
                    pathlist.append(os.path.join(outfolder, f"UMAP_Cluster{i + 1}.png"))
                imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
                self.viewer.add_image(imx, name=f"UMAP {self.umapcount} (Individual Clusters)", blending="additive")

            # If selected by user, add a scatterplot colored according to cluster assignment.
            if colorbycombclusters:
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
                filename = os.path.join(outfolder, "UMAPClusters.png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename), name=f"UMAP {self.umapcount} (Combined Clusters)",
                                      blending="additive")

        # If selected by user, add a scatterplot colored according to group assignment.
        if colorbygroups != []:
            for ind in colorbygroups:
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
                filename = os.path.join(outfolder, f"UMAPGroups_{self.groupsnames[ind + 1]}.png")
                plt.savefig(filename, format="PNG", dpi=300)
                self.viewer.add_image(imread(filename), name=f"UMAP {self.umapcount} ({self.groupsnames[ind + 1]})",
                                      blending="additive")

        # Keep track of coordinates on UMAP plot, and update variables.
        coordslist = []
        coords = np.hstack((np.expand_dims(x, 1), np.expand_dims(y, 1)))
        count = 0
        for i in range(self.numimgs):
            numcells = len(self.datalist[self.segmentationindices[segindex * self.numimgs + i]])
            coordslist.append(coords[count:count + numcells].astype(np.float))
            count += numcells
        self.plotcoordinates.append(coordslist)
        self.plotisumap.append(True)
        self.umapcount += 1
        GUIUtils.log_actions(self.actionloggerpath, f"gui.umap_plot(paramindices={paramindices}, segindex={segindex}, "
                                                    f"min_dist={min_dist}, n_neighbors={n_neighbors}, "
                                                    f"metric=\"{metric}\", colorbymarkers={colorbymarkers}, "
                                                    f"colorbygroups={colorbygroups}, "
                                                    f"colorbyindivclusters={colorbyindivclusters}, "
                                                    f"colorbycombclusters={colorbycombclusters}, "
                                                    f"clusteringindex={clusteringindex})")

    def update_table(self,
                     datavals,
                     lowerbounds,
                     upperbounds,
                     totalnumrows,
                     order=[],
                     headernames=[],
                     ):
        """
        Apply both lower- and upper-bound thresholds to an image array.

        Args:
            datavals (numpy.ndarray): Array containing the data values being represented in the table.
            lowerbounds (list): List of lower bounds for the values in each column in the table.
            upperbounds (list): List of upper bounds for the values in each column in the table.
            totalnumrows (int): Total number of cells/clusters for the image corresponding to the table.
            order (list, optional): List containing the indices corresponding to the cells/clusters that are included in the table, and in the correct order (Default: []).
            headernames (list, optional): List containing the annotated cluster names, if applicable (Default: []).
        """
        numrows = len(datavals)
        numcols = datavals.shape[1]
        vals = []
        for i in range(numrows + 3):
            vals.append(None)
        data = {'': vals}
        params = ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        for i in range(numcols):
            if self.analysismode == "Segmentation":
                if i < numcols - 4:
                    key = str(self.viewer.layers[self.markers[i]])
                else:
                    key = params[i + 4 - numcols]
            elif self.analysismode == "Object":
                if i == 0:
                    key = "# Cells"
                else:
                    keys = self.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
                    key = keys[i - 1]
            elif self.analysismode == "Pixel":
                if i == 0:
                    key = "# Pixels"
                else:
                    ind, _ = GUIUtils.find_analysis_round(self.analysisindex, self.numimgs)
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
        if self.analysismode == "Segmentation":
            if len(order) > 0:
                self.currentverticalheaderlabels = np.asarray(
                    [f"{numrows}/{totalnumrows}", "", ""] + [f"Cell {int(i)}" for i in order]).astype(np.str)
            else:
                self.currentverticalheaderlabels = np.asarray(
                    [f"{numrows}/{totalnumrows}", "", ""] + [f"Cell {int(i) + 1}" for i in range(numrows)]).astype(
                    np.str)
        else:
            if headernames != []:
                labels = [headernames[i] for i in order]
                self.currentverticalheaderlabels = np.asarray([f"{numrows}/{totalnumrows}", "", ""]
                                                              + labels).astype(np.str)
            elif len(order) > 0:
                self.currentverticalheaderlabels = np.asarray([f"{numrows}/{totalnumrows}", "", ""]
                                                              + [f"Cluster {int(i) + 1}" for i in order]).astype(np.str)
            else:
                self.currentverticalheaderlabels = np.asarray([f"{numrows}/{totalnumrows}", "", ""]
                                                              + [f"Cluster {int(i) + 1}" for i in
                                                                 range(numrows)]).astype(np.str)
                self.currenttableorderfull = []
                for i in range(numrows):
                    self.currenttableorderfull.append(i)
        self.tablewidget.setVerticalHeaderLabels(self.currentverticalheaderlabels)

        self.addwhenchecked = False
        if len(order) > 0:
            order = [int(i) for i in order]
            counter = 3
            for a in order:
                if a in self.currentlyselected[self.tableindex]:
                    self.tablewidget.item(counter, 0).setCheckState(QtCore.Qt.Checked)
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
        if self.hasaddedtable:
            self.viewer.window.remove_dock_widget(self.viewer.window._qt_window.findChildren(QDockWidget)[-1])
        self.viewer.window.add_dock_widget(self.tablewidget, area="top", name="Table")
        self.hasaddedtable = True
        self.fulltab = pd.DataFrame(data).fillna(0)
        self.fulltab.insert(0, "Labels", vstrings)
        self.currenttabdata = datavals
        self.totalnumrows = totalnumrows
        self.tableorder = order

    def testGUI(self,
                segmentationfilenames=[],
                envpath="",
                pixelresultspath="",
                outputfolder="",
                quant_avg=None,
                addgreyimg=None,
                addcolorimg=None,
                ):
        """
        Function containing magicgui elements, where the napari window gets populated with RAPID-specific widgets.

        Args:
            segmentationfilenames (list, optional): List of paths to segmentation label images being loaded (Default: []).
            envpath (str, optional): Path to the saved environment file being loaded (Default: "").
            pixelresultspath (str, optional): Path to data folder with RAPID results being loaded (Default: "").
            outputfolder (str, optional): Path to folder where results will be saved (Default: "").
            quant_avg (bool): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values.
            addgreyimg (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            addcolorimg (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
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
            def umap_plot_gui() -> Image:
                self.umap_plot()

            @magicgui(call_button="Edit Image")
            def edit_image_gui() -> Image:
                self.edit_image()

            @magicgui(call_button="Filter Table")
            def filter_table_gui() -> Image:
                self.filter_table()

            @magicgui(call_button="MST")
            def minimum_spanning_tree_gui():
                self.minimum_spanning_tree()

            @magicgui(call_button="Nearest Neighbours")
            def nearest_neighbours_gui() -> Image:
                self.nearest_neighbours()

            @magicgui(call_button="Load Clusters")
            def load_object_clusters_gui() -> Image:
                self.load_object_clusters()

            @magicgui(call_button="UMAP Annotation")
            def manual_annotation_gui() -> Image:
                self.manual_annotation()

            @magicgui(call_button="Merge Clusters")
            def merge_clusters_gui() -> Image:
                self.merge_clusters()

            @magicgui(call_button="Merge Markers")
            def merge_mem_gui() -> Image:
                self.merge_markers(nucmarkernums=[], nucalg="", memmarkernums=[], memalg="", nuccls=[], memcls=[])

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
                      marker={"choices": self.tableparams, "label": "Parameter:        "},
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
            umapwidget = umap_plot_gui.native
            umapwidget.setToolTip("Generate a UMAP from the segmented cells")
            objectBasedLayout.addWidget(umapwidget, 2, 1)
            displayselectedwidget = display_selected_cells_gui.native
            displayselectedwidget.setToolTip(
                "Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(displayselectedwidget, 2, 2)
            nngui = nearest_neighbours_gui.native
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
            mstgui = minimum_spanning_tree_gui.native
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

            if outputfolder == "" and envpath == "":
                while True:
                    openwindow = GUIUtils.OutFolder()
                    openwindow.exec()
                    if openwindow.OK:
                        if openwindow.loadseg:
                            segmentationfilenames = self.load_segmentation_results()
                            if segmentationfilenames:
                                break
                        elif openwindow.loadenv:
                            envpath = self.load_environment(envpath)
                            if not envpath == "":
                                break
                        elif openwindow.loadpixel:
                            pixelresultspath = self.load_pixel_results()
                            if not pixelresultspath == "":
                                break
                        else:
                            dialog = QFileDialog()
                            outputfolder = dialog.getExistingDirectory(None, "Select Output Folder")
                            if outputfolder != "":
                                self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
                                self.actionloggerpath = GUIUtils.initialize_logger(self.outputfolder)
                                break
                    else:
                        self.viewer.window.close()
                        self.viewer.close()
                        return
            elif outputfolder != "":
                if segmentationfilenames != []:
                    self.load_segmentation_results(segmentationfilenames,
                                                   outputfolder,
                                                   quant_avg,
                                                   addgreyimg,
                                                   addcolorimg,
                                                   )
                elif pixelresultspath != "":
                    self.load_pixel_results(pixelresultspath, outputfolder)
                else:
                    self.outputfolder = GUIUtils.create_new_folder("RAPID_GUI", outputfolder)
            else:
                self.load_environment(envpath)

            openimgs = QAction('Open File(s)', self.viewer.window._qt_window)
            openimgs.setShortcut('Ctrl+O')
            openimgs.setStatusTip('Open file(s)')
            openimgs.triggered.connect(self.open_images_gui)

            savedata = QAction('Save Data', self.viewer.window._qt_window)
            savedata.setShortcut('Ctrl+S')
            savedata.setStatusTip('Save Data')
            savedata.triggered.connect(self.save_data_gui)

            group = QAction('Sample grouping', self.viewer.window._qt_window)
            group.setShortcut('Ctrl+G')
            group.setStatusTip('Sample grouping')
            group.triggered.connect(self.sample_group_gui)

            saveenv = QAction('Save Environment', self.viewer.window._qt_window)
            saveenv.setShortcut('Ctrl+Shift+S')
            saveenv.setStatusTip('Save Environment')
            saveenv.triggered.connect(self.save_environment)

            cmgroup = QAction('Set colormap', self.viewer.window._qt_window)
            cmgroup.setShortcut('Ctrl+Shift+C')
            cmgroup.setStatusTip('Set colormap for clusters')
            cmgroup.triggered.connect(self.colormap_group_gui)

            rename = QAction('Rename clusters', self.viewer.window._qt_window)
            rename.setShortcut('Ctrl+R')
            rename.setStatusTip('Change names of clusters')
            rename.triggered.connect(self.rename_clusters_gui)

            opendocs = QAction('Open documentation', self.viewer.window._qt_window)
            opendocs.setShortcut('Ctrl+D')
            opendocs.setStatusTip('Open documentation')
            opendocs.triggered.connect(self.open_docs)

            changefolder = QAction('Change output folder', self.viewer.window._qt_window)
            changefolder.setStatusTip('Change output folder')
            changefolder.triggered.connect(self.change_folder_gui)

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
