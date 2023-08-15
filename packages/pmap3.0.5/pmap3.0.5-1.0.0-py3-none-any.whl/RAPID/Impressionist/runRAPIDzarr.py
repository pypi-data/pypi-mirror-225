import datetime
import os
import torch, torchvision
import torch.nn as nn
import torch.optim as optim
import glob
import argparse
import numpy as np
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
import dask.array as da
import copy
import cv2 as cv
import pandas as pd
import sys
import imageio as io
import PIL
import zarr
import seaborn as sns
from loguru import logger
from sklearn.metrics import normalized_mutual_info_score as NMI
from RAPID.util import io as rio
from RAPID.util import utils as util
from RAPID.network.IID_loss import IID_loss
from RAPID.util.utils import cropandpaste_zarr, cropandpaste_zarrSelected
from RAPID.util.utils import neighbors, generate_colormap, system_info, gpu_info
from RAPID.util.mst import prep_for_mst, generate_mst, save_clusters

### TODO: Should these be from KNN instead?
from RAPID.spatialanalysis.spatialocodistribution import randomkdtree, random_kdtree_single
from RAPID.network.pytorchtools import EarlyStopping
from RAPID.network.model import RAPIDMixNet, RAPIDFCNet, RAPIDResnet, weight_init, load_checkpoint
from RAPID.network.scanloss import SCANLoss
import vaex
import vaex.ml
import json
from scipy import ndimage

PIL.Image.MAX_IMAGE_PIXELS = 933120000
import tqdm
from napari.qt.progress import progress
import tifffile


### TODO: config file only saved when run from the command line, not from the GUI
### TODO: history_loss file does not save loss values, but instead saves parameters. Almost identical to config.


def test(args, model, device, datapath, outpath, batchsize=100000):
    """
    Apply trained model to dataset for cluster assignment.

    Args:
        args (argparse.ArgumentParser): Stores arguments that are used to define properties of the network.
        model (model): Torch nn model used for classification.
        device (str): Device to use for analysis ("cpu" or "gpu").
        datapath (str): Path to zarr file.
        outpath (str): Path to the output folder where the model file will be saved.
        batchsize (int, optional): Number of pixels in each batch at the time of prediction (Default: 100000).

    :return: grey *(numpy.ndarray)*: \n
        Array containing cluster IDs for each pixel in each image.
    :return: model *(numpy.ndarray)*: \n
        Array containing probabilities for each pixel in each image.
    :return: device *(pandas.DataFrame)*: \n
        Dataframe for the average intensity values and total pixel counts for each cluster.
    :return: datapath *(numpy.ndarray)*: \n
        Array containing the colors used to label each cluster in the resulting image.
    :return: batchsize *(list)*: \n
        List of strings of the names for each of the samples for which results are returned.
    """

    # set model for evaluation mode
    model = torch.nn.DataParallel(model)  # @@@@@@@@@@
    model.eval()
    for param in model.parameters():
        param.requires_grad = False

    # read the data zarr file
    print(datapath)
    hf = zarr.open(datapath, 'r')
    imageshapelist = np.array(hf["imageshapelist"])
    count = 0
    # run prediction
    with torch.no_grad():
        # define empty list for identified cluster quantification
        samplenames = []

        # generate random colormap
        if args.predict and args.color != None:
            col_list = np.load(args.color + "/color.npy")
        else:
            col_list = generate_colormap(args.ncluster + 1)[:-1]
        totalpixels = hf.attrs['totalpixels']
        hf = zarr.open(outpath + '/RAPID_Data', 'r+')
        try:
            del hf['grey']
            del hf['prob']
            del hf['color']
            del hf['tab']
        except Exception as ex:
            print(ex)
        # grey = hf.create_dataset('grey', shape=(int(totalpixels)), chunks=(10000), dtype='i4')
        grey = hf.create_dataset('grey', shape=(int(totalpixels)), dtype='i4')
        prob = hf.create_dataset('prob', shape=(int(totalpixels)), dtype='f8')
        hfcolor = hf.create_dataset('color', shape=(args.ncluster, 3), chunks=(1000), dtype='i4')
        hfcolor[:, :] = col_list

        # loop through each image
        currentindex = 0

        hf = zarr.open(datapath, 'r+')
        image_list = hf.attrs['imageslist']
        dataraw = hf["data"]
        Slices = np.zeros((len(imageshapelist), args.ncluster,
                           len(hf.attrs['selmarkernames']) + 3))
        hftab = hf.create_dataset('tab',
                                  shape=(args.ncluster * len(imageshapelist), hf["data"].shape[1] + 3),
                                  dtype='f4',
                                  )

        with progress(imageshapelist, desc='Image', total=0 if len(imageshapelist) == 1 else None, ) as pbr:
            for r, shape in enumerate(pbr):
                # extract the file name
                image_name = os.path.splitext(os.path.split(image_list[r])[-1])[0]
                samplenames.append(image_name[0:20])
                print(str(r) + ":" + image_name)

                # get the data for selected image from zarr file
                data = hf["data_normalized"][count:count + (imageshapelist[r, 0] * imageshapelist[r, 1]), ].copy()
                filtersizeG = [args.gbmi, args.gbmi, 0]
                data = ndimage.gaussian_filter(
                    data.reshape((imageshapelist[r, 0], imageshapelist[r, 1], hf["data"].shape[1])),
                    filtersizeG)
                data = data.reshape(
                    (int(imageshapelist[r, 0] * imageshapelist[r, 1]), hf["data"].shape[1]))
                print(data.shape)

                # define empty array to store the results
                TESTPATCHPRED = data.reshape((data.shape[0], -1))
                TESTPATCHPREDO = np.zeros((TESTPATCHPRED.shape[0]))
                TESTPATCHPREDO_Prob = np.zeros((TESTPATCHPRED.shape[0]))
                # TESTPATCHPREDO2 = np.zeros((TESTPATCHPRED.shape[0]))
                # TESTPATCHPREDO_Prob2 = np.zeros((TESTPATCHPRED.shape[0]))
                # TESTPATCHPREDO3 = np.zeros((TESTPATCHPRED.shape[0]))
                # TESTPATCHPREDO_Prob3 = np.zeros((TESTPATCHPRED.shape[0]))
                pbar = tqdm.tqdm(total=TESTPATCHPRED.shape[0])

                pixelinds = []
                for BSTART in range(0, TESTPATCHPRED.shape[0], batchsize):
                    pixelinds.append(BSTART)

                for BSTART in range(0, TESTPATCHPRED.shape[0], batchsize):
                    x = torch.from_numpy(TESTPATCHPRED[BSTART:BSTART + (batchsize), :].astype(np.float32)).float().to(
                        device)
                    if args.network == "rapidmixnet":
                        outputs, AA = model(torch.unsqueeze(x, 1))
                    else:
                        outputs, AA = model(x)
                    for nh in range(args.nhead):
                        TESTPATCHPREDO_Prob[BSTART:BSTART + x.shape[0]], TESTPATCHPREDO[BSTART:BSTART + x.shape[0]], = \
                            outputs[0].cpu().max(dim=1)
                        # if nh == 1:
                        #    TESTPATCHPREDO_Prob2[BSTART:BSTART + x.shape[0]], TESTPATCHPREDO2[
                        #                                                      BSTART:BSTART + x.shape[0]], = outputs[
                        #        1].cpu().max(dim=1)
                        # if nh == 2:
                        #    TESTPATCHPREDO_Prob3[BSTART:BSTART + x.shape[0]], TESTPATCHPREDO3[
                        #                                                      BSTART:BSTART + x.shape[0]], = outputs[
                        #        2].cpu().max(dim=1)
                    grey[currentindex:currentindex + x.shape[0]] = TESTPATCHPREDO[BSTART:BSTART + x.shape[0]]
                    prob[currentindex:currentindex + x.shape[0]] = TESTPATCHPREDO_Prob[BSTART:BSTART + x.shape[0]]
                    pbar.update(batchsize)
                    currentindex += x.shape[0]

                # print("busgshsshshshshshssh")
                # print("NMI12:", NMI(TESTPATCHPREDO, TESTPATCHPREDO2))
                # print("NMI13:", NMI(TESTPATCHPREDO, TESTPATCHPREDO3))
                # save colormap for later use
                np.save(outpath + "/" + "color.npy", col_list)

                TESTPATCHPRED = TESTPATCHPREDO.reshape((imageshapelist[r, 0], imageshapelist[r, 1]))

                ### TODO: Different backgroundclass for every image, not necessarily same cluster in all images. Maybe use cluster with lowest quantified values?
                # if r == 0:
                # backgroundclass = TESTPATCHPRED[5, 5]

                VolImage = np.zeros((imageshapelist[r, 0], imageshapelist[r, 1], 3))
                TESTPATCHPRED[-args.ncluster:, -1] = np.arange(args.ncluster)

                tifffile.imwrite(os.path.join(outpath, f"PixelClusterLabels_{image_name}.tif"),
                                 TESTPATCHPRED.astype(np.uint16))
                for i in range(len(col_list)):
                    mask = TESTPATCHPRED == i
                    # if i == backgroundclass:
                    #    col_list[i, :] = (0, 0, 0)
                    VolImage[mask] = col_list[i, :]
                tifffile.imwrite(os.path.join(outpath, f"PixelClusters_{image_name}.tif"), VolImage.astype(np.uint8))
                tab = vaex.from_pandas(pd.DataFrame(np.hstack([np.expand_dims(TESTPATCHPRED.reshape(-1), 1),
                                                               dataraw[count:count + (
                                                                       imageshapelist[r][0] * imageshapelist[r][1]),
                                                               0:len(hf.attrs['selmarkernames'])]])))
                count = count + (imageshapelist[r, 0] * imageshapelist[r, 1])
                grouped = tab.groupby("0", agg='mean')
                grouped = grouped.sort(by="0")
                mean__cols = [col for col in grouped.column_names if 'mean' in col][1:]
                mean__cols.insert(0, "0")
                tabres = grouped[mean__cols].to_pandas_df()
                tabres.insert(0, "Sample", r)
                unique, counts = np.unique(TESTPATCHPRED, return_counts=True)
                tabres.insert(2, "# Pixels", counts)
                Slices[r, :, :] = tabres.values

        my_data = pd.DataFrame(np.nan_to_num((np.vstack(Slices))))
        markers = hf.attrs['selmarkernames']
        markers = [marker for marker in markers]
        my_data.columns = np.hstack([["Sample", "Cluster", "# Pixels"], markers])
        my_data.to_csv(outpath + "/PixelClusterAvgExpressionVals.csv")
    tabledata, my_data_scaled, DistMatrix, uniqueClusters = prep_for_mst(clustertable=my_data,
                                                                         minclustersize=1000,
                                                                         clustersizes=my_data["# Pixels"],
                                                                         includedmarkers=markers,
                                                                         )
    generate_mst(distancematrix=DistMatrix,
                 normalizeddf=my_data_scaled[my_data_scaled.columns],
                 colors=col_list,
                 randomseed=0,
                 outfolder=outpath,
                 clusterheatmap=True,
                 displaymarkers=markers,
                 uniqueclusters=uniqueClusters,
                 samplenames=samplenames,
                 displaysingle=False,
                 )
    hfcolor[:, :] = col_list
    np.save(outpath + "/" + "color.npy", col_list)
    hftab[:, :] = my_data.values
    hftab.attrs['columns'] = list(my_data.columns.values)
    grey = np.array(grey)
    return grey, prob, my_data, col_list, samplenames


def train_rapid(args, device, datapath, outputfolder="", patcharray=""):
    """
    Train RAPID model.

    Args:
        args (argparse.ArgumentParser): Stores arguments that are used to define properties of the network.
        device (str): Device to use for analysis ("cpu" or "gpu").
        datapath (str): Path to zarr file.
        file_list (list): List of image files.
        outputfolder (str, optional): Path to the output folder where the model file will be saved (Default: "").
        patcharray (numpy.ndarray, optional): Array of pre-defined patches to use for training. Defaults to an empty string if using randomly-defined patches (Default: "").

    :return: TESTPATCHPREDO *(numpy.ndarray)*: \n
        Array containing cluster IDs for each pixel in each image.
    :return: prob *(numpy.ndarray)*: \n
        Array containing probabilities for each pixel in each image.
    :return: my_data *(pandas.DataFrame)*: \n
        Dataframe for the average intensity values and total pixel counts for each cluster.
    :return: COL_LIST *(numpy.ndarray)*: \n
        Array containing the colors used to label each cluster in the resulting image.
    :return: samplenames *(list)*: \n
        List of strings of the names for each of the samples for which results are returned.
    """

    # set the random seed so make results reproducible
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    # torch.cuda.manual_seed(args.seed)
    torch.manual_seed(1000)
    np.random.seed(1000)
    if device == "cuda":
        torch.cuda.manual_seed(1000)
        torch.set_deterministic(True)
        torch.backends.cudnn.deterministic = True

    print(system_info())
    print(gpu_info())
    print(args)

    if outputfolder == "":
        outputfolder = args.rfold

    logger.add(outputfolder + "/RAPID_{time}.log")
    # CD35,CD169,CD4,B220,CD31,CD3,MHCII

    # define the network architecture and initialize wieghts
    if args.network == "rapidmixnet":
        model = RAPIDMixNet(dimension=args.nchannels, nummodules=args.nhead, mse=args.mse, numclusters=args.ncluster)
        model.apply(weight_init)
        model.to(device)
        print(model)
        # define optimizer for the model
        optimizer = optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.999),
                                eps=1e-08, weight_decay=0.01, amsgrad=False)

        # define checkpoint for the model
        checkpoint = {
            'model': RAPIDMixNet(dimension=args.nchannels, nummodules=args.nhead, mse=args.mse,
                                 numclusters=args.ncluster),
            'state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}
    elif args.network == "RAPIDResnet":
        model = RAPIDResnet(dimension=args.nchannels, numclusters=args.ncluster, nummodules=5)
        model.apply(weight_init)
        model.to(device)
        print(model)
        optimizer = optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.999),
                                eps=1e-08, weight_decay=0.01, amsgrad=False)
        checkpoint = {'model': RAPIDResnet(dimension=args.nchannels, numclusters=args.ncluster, nummodules=5),
                      'state_dict': model.state_dict(),
                      'optimizer': optimizer.state_dict()}
    else:
        model = RAPIDFCNet(dimension=args.nchannels, nummodules=args.nhead, mse=args.mse, numclusters=args.ncluster)
        model.apply(weight_init)
        model.to(device)
        print(model)
        optimizer = optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.999),
                                eps=1e-08, weight_decay=0.01, amsgrad=False)
        checkpoint = {
            'model': RAPIDFCNet(dimension=args.nchannels, nummodules=args.nhead, mse=args.mse,
                                numclusters=args.ncluster),
            'state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}

    # load model if running RAPID in prediction mode or continue training
    if args.reassume | args.predict:
        if args.predmodpath is not None:
            model = load_checkpoint(args.predmodpath, model, optimizer)
        else:
            model = load_checkpoint(os.path.join(outputfolder, 'checkpoint.pth'), model, optimizer)
        model.to(device)

    # torch.save(checkpoint, args.rfold + '/checkpoint.pth')
    torch.save(checkpoint, os.path.join(outputfolder, 'checkpoint.pth'))
    noneigh = args.noneigh
    rescale = args.rescale

    ### TODO: This doesn't do anything
    '''
    if args.selectedchannel == "":
        selectedchannel = np.ones(args.nchannels)
    else:
        channelorder = np.array(args.selectedchannel.split(','), dtype=int)
        selectedchannel = np.zeros(args.nchannels)
        selectedchannel[channelorder] = 1
        print(selectedchannel)
    '''

    # training loop for specified number of epochs
    for epoch in range(0, args.epoch):
        print(epoch)

        # restrict the batch size to 20,000 to reduce training time
        if args.bs > 20000:
            args.bs = 20000
        if not args.predict:
            if epoch > 10:
                noneigh = False
                rescale = False
            if args.SCANloss:
                train_scan(args,
                           model,
                           datapath,
                           optimizer,
                           epoch,
                           outputfolder,
                           args.rescalefactor,
                           checkpoint,
                           noneigh,
                           logger,
                           patcharray,
                           )
            else:
                train(args,
                      model,
                      datapath,
                      optimizer,
                      epoch,
                      outputfolder,
                      rescale,
                      args.rescalefactor,
                      checkpoint,
                      noneigh,
                      logger,
                      patcharray,
                      )

            if (epoch + 1) % args.testinterval == 0:
                TESTPATCHPREDO, prob, my_data, COL_LIST, samplenames = test(args,
                                                                            model,
                                                                            device,
                                                                            datapath,
                                                                            outputfolder,
                                                                            args.testbs,
                                                                            )
        if args.predict:
            print("Running RAPID prediction on:")
            TESTPATCHPREDO, prob, my_data, COL_LIST, samplenames = test(args,
                                                                        model,
                                                                        device,
                                                                        datapath,
                                                                        outputfolder,
                                                                        args.testbs,
                                                                        )
    hf = zarr.open(datapath, "r+")
    del hf["data_normalized"]
    return TESTPATCHPREDO, prob, my_data, COL_LIST, samplenames


def run_rapid_analysis(args, mst=True, spatial=True):
    """
    Run RAPID in analysis mode. Once RAPID has clustered the given input images, this pipeline allows for spatial
    co-distribution and cluster analysis. This pipeline provides 3 main sub-modules: *MST*, which generates a minimum
    spanning tree for the identified clusters to illuminate the similarities between all identified clusters;
    *Spatial*, which helps us to understand the biology behind spatial phenotypic organisation of tissues by
    identifying the spatial co-distribution relation between identified clusters, with high scores meaning that two
    clusters are found in close proximity within the tissue; and *Saver Cluster*, which allows user to save specific
    cluster(s) to see its spatial distribution in a given tissue.

    Args:
        args (argparse.ArgumentParser): Stores arguments that are used to define properties of the network.
        mst (bool, optional): Run minimum spanning tree analysis (Default: True).
        spatial (bool, optional): Run spatial co-distribution analysis (Default: True).
    """
    rfold = args.rfold
    print(rfold)

    # read the RAPID result quantification matrix
    my_data = pd.read_csv(rfold + "/PixelClusterAvgExpressionVals.csv", sep=",", header=0, index_col=0)
    markernames = my_data.columns[3:]
    include_names = markernames
    color_list = np.load(rfold + "/color.npy")

    # generate data for minimum spanning tree and spatial analysis
    tabledata, my_data_scaled, DistMatrix, uniqueClusters = prep_for_mst(clustertable=my_data,
                                                                         minclustersize=10000,
                                                                         clustersizes=my_data["# Pixels"],
                                                                         includedmarkers=include_names,
                                                                         clustermin=args.clusmaxval,
                                                                         )

    # run minimum spanning tree module
    if mst:
        displayMarkeOnMst = "all"
        final = my_data_scaled.columns
        samplenames = np.unique(my_data["Sample"])
        mst = generate_mst(distancematrix=DistMatrix,
                           normalizeddf=my_data_scaled[final],
                           colors=color_list,
                           randomseed=0,
                           outfolder=args.rfold,
                           clusterheatmap=True,
                           displaymarkers=displayMarkeOnMst,
                           uniqueclusters=uniqueClusters,
                           samplenames=samplenames,
                           )

    # run spatial analysis module to generate spatial distribution table
    if spatial:
        rcpath = args.rfold
        avgwin = args.avgwin
        masklist = sorted(glob.glob(rfold + "/*_Gray.png"))
        radlist = np.array(args.radlist.split(','), dtype=str)
        RAPCDAPath = rcpath + "/spatialanalysis/"
        clusterlist = my_data_scaled.index

        if not os.path.exists(RAPCDAPath):
            os.mkdir(RAPCDAPath)
        cluster_order = [[0, 0], [0, 0]]
        codistribution_df = pd.DataFrame({'Distance': [], 'Score': [], 'Sample': []})
        for mask in range(len(masklist)):
            Name = os.path.split(masklist[mask])[-1][0:-4]
            print("Image: " + Name)
            img = io.imread(masklist[mask])
            if args.spat:
                Tab, retind, tab, cluster_order = randomkdtree(img, radlist, avgwin, outfolder=RAPCDAPath, Name=Name,
                                                               percentpixel=args.percentpixel, clusterlist=clusterlist,
                                                               cluster_order=cluster_order)
                sample_codist = random_kdtree_single(img, radlist, avgwin, outfolder=RAPCDAPath, Name=Name,
                                                     percentpixel=args.percentpixel, clusterlist=clusterlist,
                                                     cluster_order=cluster_order)
                print(sample_codist)
                codistribution_df = pd.concat([codistribution_df, sample_codist])
                print(codistribution_df)
                sns.lineplot(x="Distance", y="Score", hue="Sample", data=codistribution_df)
                plt.savefig(RAPCDAPath + '/SPAT_distribution_cmp.png', dpi=100)
                pd.DataFrame(tab.reshape(-1, 3)).to_csv(RAPCDAPath + "/" + Name + "_CODIST_tab.csv")

    # run savercluster module to save specified RAPID cluster image
    if args.savercluster:
        masklist = sorted(glob.glob(args.rfold + "/*_Gray.png"))
        for mask in range(len(masklist)):
            Name = os.path.split(masklist[mask])[-1][0:-4]
            print("Extracting clusters from image : " + Name)
            img = io.imread(masklist[mask])
            clusterlist = mst.columns
            clusterfold = rfold + "/clusters/"
            if not os.path.exists(clusterfold):
                os.mkdir(clusterfold)
            save_clusters(greyimg=img, colors=color_list, outfolder=clusterfold, randomseed=181, outfilename=Name,
                          clusters=clusterlist)


def get_parameters():
    """
    Define the arguments that are used to define properties of the network.

    :return: args *(argparse.ArgumentParser)*: \n
        Stores arguments that are used to define properties of the network.
    """
    parser = argparse.ArgumentParser(
        description='RAPID: deep learning algorithm for quantitative analysis of high content imaging data( arguments with *** are important for RAPID analysis)')
    parser.add_argument('--avgwin', type=int, default=3, help="Neighbour averaging window size (default: %(default)s)")
    parser.add_argument('--blankpercent', type=float, default=0.05,
                        help="Percent of channels to blankout (default: %(default)s)")
    parser.add_argument('--bs', type=int, default=100, help="Batch size (default: %(default)s)")
    parser.add_argument('--clusmaxval', type=float, default=0.2,
                        help="Threshold value for the the cluster maximum intensity(default: %(default)s)")
    parser.add_argument('--delc', type=str, default="1000", help="Delete channels %(default)s)")
    parser.add_argument('--denoise', type=str, default="",
                        help="Denoise channels? please provide channels number separated by [,] (default: %(default)s)")
    parser.add_argument('--epoch', type=int, default=1, help="Number of epochs to train (default: %(default)s)")
    parser.add_argument('--gaussianblur', action='store_true', default=False,
                        help="Median filtering follwed Gaussian filter  (default: %(default)s)")
    parser.add_argument('--gbstd', type=float, default=1, help="Gaussian blur STD (default: %(default)s)")
    parser.add_argument('--gbmi', type=float, default=1, help="Gaussian blur STD for network (default: %(default)s)")
    parser.add_argument('--imagepath', type=str, default="./",
                        help="***Absolute path to input multiplex tiff file (default: %(default)s)")
    parser.add_argument('--reassume', action='store_true', default=False, help="Load weights (default: %(default)s)")
    parser.add_argument('--loginterval', type=int, default=100,
                        help="How many batches to wait before logging ""training status (default: %(default)s)")
    parser.add_argument('--lr', type=float, default=0.00005, help="Learning rate (default: %(default)s)")
    parser.add_argument('--lamb', type=float, default=1, help="Lambda for IIC loss (default: %(default)s)")
    parser.add_argument('--markers', type=str, default="",
                        help="***Name of the markers, each marker separated by comma(,), please avoid special characters %(default)s)")
    parser.add_argument('--medianblur', action='store_true', default=False,
                        help="Median filtering follwed Gaussian filter  (default: %(default)s)")
    parser.add_argument('--mse', action='store_true', default=False, help="MSE loss (default: %(default)s)")
    parser.add_argument('--mst', action='store_true', default=False,
                        help="run minimum spanning tree analysis ? (default: %(default)s)")
    parser.add_argument('--nchannels', type=int, default=None,
                        help="***Number of channels in the input image(default: %(default)s)")
    parser.add_argument('--ncluster', type=int, default=None, help="***Number of output cluster (default: %(default)s)")
    parser.add_argument('--network', type=str, default="rapidmixnet",
                        help="***network type to use (default: %(default)s)")
    parser.add_argument('--nhead', type=int, default=5, help="Number of network output (default: %(default)s)")
    parser.add_argument('--nit', type=int, default=1000,
                        help="***Number of iterations per epoch (default: %(default)s)")
    parser.add_argument('--noiselevel', type=int, default=100,
                        help="Amount of noise to add to alternative image (lower is  better) (default: %(default)s)")
    parser.add_argument('--noneigh', action='store_false', default=True, help="No neighor(default: %(default)s)")
    parser.add_argument('--nonp', type=int, default=1, help="Number of nearest pixels rings (default: %(default)s)")
    parser.add_argument('--normalize', action='store_true', default=False,
                        help="Standardize data (default: %(default)s)")
    parser.add_argument('--normalizeall', action='store_true', default=False,
                        help="Standardize data across sample (default: %(default)s)")
    parser.add_argument('--normtype', type=str, default="none", help="Standardize data (default: %(default)s)")
    parser.add_argument('--npatches', type=int, default=200, help="Number of tiles to crop (default: %(default)s)")
    parser.add_argument('--patchsize', type=int, default=64, help="Image Tiles for random crop (default: %(default)s)")
    parser.add_argument('--percentpixel', type=float, default=0.05,
                        help="Percent of pixels to use for spatial analysis (default: %(default)s)")
    parser.add_argument('--percentile', type=float, default=99,
                        help="Percentile to define real signal (default: %(default)s)")
    parser.add_argument('--percentile_e', type=str, default=None,
                        help="Percentile to define real signal (default: %(default)s)")
    parser.add_argument('--predict', action='store_true', default=False,
                        help="***Precict with the trained model (default: %(default)s)")
    parser.add_argument('--prefix', type=str, default="RUN", help="Name of the folder (default: %(default)s)")
    parser.add_argument('--radlist', type=str, default="1,8,16,24,32,40,48",
                        help="number of epochs to train (default: %(default)s)")
    parser.add_argument('--rescale', action='store_true', default=True,
                        help="Rescale for traning (default: %(default)s)")
    parser.add_argument('--rescalefactor', type=float, default=1, help="Rescaling factor[0.1] (default: %(default)s)")
    parser.add_argument('--rfold', type=str, default="RAPID_output",
                        help="Output folder/directory (default: %(default)s)")
    parser.add_argument('--runanalysis', action='store_true', default=False,
                        help="***Run downstream analysis (default: %(default)s)")
    parser.add_argument('--savercluster', action='store_true', default=False,
                        help="save each cluster image ? (default: %(default)s)")
    parser.add_argument('--seed', type=int, default=120, help="Random seed (default: %(default)s)")
    parser.add_argument('--selectedchannel', type=str, default="",
                        help="Prediction only with selected channels %(default)s)")
    parser.add_argument('--smooth', action='store_true', default=False,
                        help="Apply median fileter (default: %(default)s)")
    parser.add_argument('--submean', action='store_false', default=True,
                        help="substract mean from the channel (default: %(default)s)")
    parser.add_argument('--spat', action='store_true', default=False,
                        help="run k d tree for spatial analysis ? (default: %(default)s)")
    parser.add_argument('--testinterval', type=int, default=1, help="test interval(default: %(default)s)")
    parser.add_argument('--testbs', type=int, default=100000, help="test batch size(default: %(default)s)")
    parser.add_argument('--train', action='store_true', default=False,
                        help="***Train RAPID on your data (default: %(default)s)")
    parser.add_argument('--pca', action='store_true', default=False, help="apply pca (default: %(default)s)")
    parser.add_argument('--SCANloss', action='store_true', default=False, help="apply pca (default: %(default)s)")
    parser.add_argument('--npc', type=int, default=None, help="apply pca (default: %(default)s)")
    parser.add_argument('--GUI', action='store_true', default=False,
                        help="***Train RAPID on your data (default: %(default)s)")
    parser.add_argument('--graphalgo', type=str, default="leiden",
                        help="Graph clustering algorithm (default: %(default)s)")
    parser.add_argument('--vmodels', type=str, default=None, help="pretrained Vaex model path  (default: %(default)s)")
    parser.add_argument('--predmodpath', type=str, default=None,
                        help="pretrained RAPID-P model path  (default: %(default)s)")
    parser.add_argument('--color', type=str, default=None, help="numpy color path  (default: %(default)s)")
    parser.add_argument('--config', type=str, default=None, help="config file path (default: %(default)s)")
    parser.add_argument('--gpu', type=int, default=0, help="gpu ID(default: %(default)s)")
    parser.add_argument('-f', '--fff', default=1, help="gpu ID(default: %(default)s)")
    args = parser.parse_args()
    return args


def run_rapid():
    """
    This function in the entry point for the RAPID algorithm. This module/function is called when user run RAPID from
    the command line.
    """

    # initialize the default RAPID parameters
    args = get_parameters()
    if not os.path.exists(args.rfold):
        os.mkdir(args.rfold)

    if args.config is not None:
        with open(args.config, 'r') as f:
            args.__dict__ = json.load(f)
        if not os.path.exists(args.rfold):
            os.mkdir(args.rfold)
        with open(args.rfold + '/config.txt', 'w') as f:
            json.dump(args.__dict__, f, indent=2)
    else:
        if not os.path.exists(args.rfold):
            os.mkdir(args.rfold)
        with open(args.rfold + '/config.txt', 'w') as f:
            json.dump(args.__dict__, f, indent=2)
    # search for the GPU is present otherwise set device to cpu
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(args)

    # check for the user defined RAPID mode, train/predict or analysis
    if not args.runanalysis:
        if len(glob.glob(args.imagepath + "/*.tif*")) == 0:
            sys.exit(
                "\nNo images are found in :'" + args.imagepath + "', please set the imagepath paratmeter carefully ")
        if args.nchannels == None:
            sys.exit("\nPlease define the number of channels in the input tiff file, it required argument.")

    print("RAPID is running...")
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
    # run RAPID segmentation module in train/predict/analysis mode
    if args.train and not args.predict:
        print("RAPID is set to run in training mode.")
    elif not args.train and args.predict:
        print("RAPID is set to run in prediction mode.")
    elif not args.train and not args.predict and args.runanalysis:
        print("RAPID is set to run in analysis mode.")
    else:
        sys.exit(
            "\nRAPID is exiting none of the 'train|predict|analysis' mode is selected, please select either of them.")

    # print the user defined parameters
    print("You have selected '" + args.imagepath + "' sample folder the RAPID for analysis.")
    print("Total number of samples in '" + args.imagepath + "' are " + str(len(glob.glob(args.imagepath + "/*.tif*"))))
    print("The channel dimensions for the imput samples is set to " + str(args.nchannels) + ".")
    print("Number of training epochs is  set to " + str(args.epoch) + ".")

    # define random marker names if not provided by user
    if args.markers == "":
        markernames = [[str("M_" + str(int(marker))) for marker in range(args.nchannels)]]
    else:
        markernames = [args.markers.split(',')]

    # check whether user wants to delete/exclude specific channel(s) from training or analysis
    if args.delc == "":
        delete_channel = 1000
    else:
        delete_channel = np.array(args.delc.split(','))
        delete_channel = np.nonzero(np.in1d(markernames, delete_channel))[0]

    # check if output folder already exist, if yes, define default or user defined
    if not os.path.exists(args.rfold):
        os.mkdir(args.rfold)

    # get the list of file list to be analysed
    file_list = sorted(glob.glob(args.imagepath + "/*.tif*"))

    # define the zarr file path
    zarrpath = args.rfold + "/RAPID_Data"

    # check if the RAPID mode is set to train or predict
    if args.train | args.predict:

        # check if the input data is already prepared for RAPID or else generate new datafile
        if os.path.exists(zarrpath):
            hf = zarr.open(zarrpath, mode='r')
            image_shape_list = np.array(hf["imageshapelist"])
            args.nchannels = hf['data'].shape[1]
            pass
        else:
            file_list, image_shape_list, args = rio.tiff_to_zarr(file_list,
                                                                 zarrpath,
                                                                 gaussianblur=args.gaussianblur,
                                                                 gaussianblurstd=args.gbstd,
                                                                 medianblur=args.medianblur,
                                                                 normalize=args.normalize,
                                                                 normtype=args.normtype,
                                                                 ndims=args.nchannels,
                                                                 deletechannel=delete_channel,
                                                                 normalizeacross=args.normalizeall,
                                                                 markernames=markernames,
                                                                 args=args,
                                                                 pretrained=args.vmodels,
                                                                 submean=args.submean,
                                                                 )
            print("h" * 200)
            hf = zarr.open(zarrpath, 'a')
            hf.attrs['arg'] = vars(args)

        out_loss = open(args.rfold + "/history_loss.txt", "a")
        for arg in vars(args):
            print(str(arg) + ": " + str(getattr(args, arg)))
            out_loss.write(str(arg) + "=" + str(getattr(args, arg)) + "\n")
        out_loss.close()

        # define the number of clusters for the RAPID if user did provide
        if args.ncluster == None:
            # number of cluster is somewhat arbitrary, we define at least 3 times the number of input channels expecting each marker to have low, mideium and high  expression level
            ncluster = int(image_shape_list[0, 2] * 3)
            args.ncluster = ncluster

    print("Aanlysis folder is set to " + str(args.rfold) + ".")

    # run RAPID in analysis mode
    if not args.runanalysis:
        print(zarrpath)
        hf = zarr.open(zarrpath, 'r')
        print("Markers are set to " + str(hf.attrs['selmarkernames']) + ".")
        print("Number of clusters is set to " + str(args.ncluster) + ".")

    # run RAPID in train/predict mode according to user selection
    if args.train | args.predict:
        print("Running RAPID train/test")
        train_rapid(args, device, zarrpath)

    if args.runanalysis:
        print("Running spatial analysis")
        run_rapid_analysis(args, mst=args.mst, spatial=args.spat)


def train(args, model, datapath, optimizer, epoch, outpath, rescale, rescalefactor, checkpoint, noneighbors, logger,
          patcharray=""):
    """
    Train RAPID model for pixel classification with IID loss.

    Args:
        args (argparse.ArgumentParser): Stores arguments that are used to define properties of the network.
        model (model): Torch nn model used for classification.
        datapath (str): Path to zarr file.
        optimizer (optimizer): AdamW optimizer used for the model.
        epoch (int): Number of epochs for the training phase.
        outpath (str): Path to the output folder where the model file will be saved.
        rescale (bool): If True, rescale the image for faster model optimization.
        rescalefactor (float): Rescaling factor, must be between 0-1.
        checkpoint (dict): Dictionary storing the model, optimizer, and weights for the neural network.
        noneighbors (bool): If False, include neighbour information during training.
        logger (loguru.Logger): Logs loss values for each training iteration.
        patcharray (numpy.ndarray, optional): Array of pre-defined patches to use for training. Defaults to an empty string if using randomly-defined patches (Default: "").
    """
    # set model to train mode
    model.train()

    # MSE loss if full autoencoder model is used
    loss_fn = nn.MSELoss()
    lossAvg = 0
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # generate random crops from multiple images from multiple input images stored in zarr file
    empty_array, empty_array_gb, IND = cropandpaste_zarrSelected(datapath,
                                                                 args.patchsize,
                                                                 args.npatches,
                                                                 rescale,
                                                                 rescalefactor,
                                                                 gaussianblurstd=args.gbmi,
                                                                 patcharray=patcharray,
                                                                 percent_ext=args.percentile_e,
                                                                 )

    # Generate index reference matrix to keep the track of the neighbouring pixels
    a = np.arange(empty_array.shape[0] * empty_array.shape[1]).reshape((empty_array.shape[0], empty_array.shape[1]))

    # Manage the number of training iteration if it is too high or low
    totalpixels = int(len(IND) / args.bs)
    print("Total number of selected pixels are :", totalpixels)
    if totalpixels / args.nit > 2 or totalpixels / args.nit < 0.5:
        num_of_train_iteration = args.nit
    else:
        print("Number if iterations are more tha")
        num_of_train_iteration = totalpixels

    # Epoch training loop
    early_stopping = EarlyStopping(patience=2000, verbose=True, path=outpath + '/checkpoint.pth')
    for batch_idx in range(0, num_of_train_iteration):

        # Reshape data to match the model input
        dataTrain = empty_array.reshape((-1, empty_array.shape[2]))
        dataTrain_G = empty_array_gb.reshape((-1, empty_array_gb.shape[2]))

        # sample random center pixels for training
        RANDINDEX = np.random.randint(0, len(IND), size=args.bs)
        RANDINDEX = IND[RANDINDEX]

        # Avoid using pixels which is close to patch border
        BORDER = 5
        RANDINDEX = RANDINDEX[(RANDINDEX % a.shape[1] > BORDER) & (RANDINDEX % a.shape[1] < a.shape[1] - BORDER) & (
                RANDINDEX / a.shape[0] > BORDER) & (RANDINDEX / a.shape[1] < a.shape[0] - BORDER)]

        # Indicies of all the pixels that are far from the border
        INDICIES = np.vstack([neighbors(a, np.unravel_index((RANDINDEX[x]), a.shape)) for x in range(len(RANDINDEX))])

        # NZ=np.ones_like(data.reshape(-1))
        optimizer.zero_grad()

        # How many neighouring pixels to use for training
        nrounds = args.nonp
        neighbors_cord = [16, 17, 18, 23, 25, 30, 31, 32]
        neighbors_cord = [17, 23, 25, 31]

        # Generate indices of the pixels to randomly blankout for robust training
        npone = np.ones(dataTrain.shape[1])
        npone[0:int(dataTrain.shape[1] * args.blankpercent)] = 0

        # loop through number of random neighbouring pixels
        for REP in range(nrounds):
            np.random.shuffle(npone)
            np.random.shuffle(neighbors_cord)
            # RAWData=dataTrain[INDICIES[:,MORE[0]],:]

            # Get the indicies of pixels of interest
            RAWData = dataTrain[RANDINDEX, :]  # *npone

            # Generate random noise that will be added to the input data to calculate mutual information loss
            noise = np.random.normal(loc=0, scale=0.5, size=dataTrain[INDICIES[:, neighbors_cord[0]], :].shape).astype(
                np.float32)

            # Whether to use neighbouring pixel for mutual information or not?
            if noneighbors:
                # define the level of noise
                noiseadd = dataTrain[RANDINDEX, :] / args.noiselevel
                noise = noise * noiseadd

                # add noise to the input data to generate perturbed input
                altdata = dataTrain_G[RANDINDEX, :] + noise
                altdata = altdata * npone
            else:
                noiseadd = dataTrain[INDICIES[:, neighbors_cord[0]], :] / args.noiselevel
                noise = noise * noiseadd
                altdata = dataTrain_G[INDICIES[:, neighbors_cord[0]], :] + noise
                altdata = altdata * npone

            RAWData = torch.from_numpy(RAWData).float().to(device)

            # check the model type requested by the user and accordingly change the input shape
            ############output,AA = model(RAWData)
            if args.network == "rapidmixnet":
                res, AA = model(torch.unsqueeze(RAWData, 1))
                altdata = torch.from_numpy(altdata).float().to(device)
                res_alt, BB = model(torch.unsqueeze(altdata, 1))
            else:
                res, AA = model(RAWData)
                altdata = torch.from_numpy(altdata).float().to(device)
                res_alt, BB = model(altdata)

            # If model is full autoencoder, add MSE loss to the IID loss
            if args.mse:
                mi_loss = torch.sum(torch.stack([IID_loss(r, a, lamb=1) for r, a in zip(res, res_alt)])).mean()
                mse = loss_fn(torch.unsqueeze(RAWData, 1), AA)
                loss1 = (mse * 0.7) + (mi_loss * 0.3)
            else:
                mse = 0
                loss1 = torch.sum(torch.stack([IID_loss(r, a, lamb=args.lamb) for r, a in zip(res, res_alt)])).mean()

        loss1.backward()
        optimizer.step()
        lossAvg = lossAvg + loss1.item()

        early_stopping(loss1, model)
        if early_stopping.early_stop:
            print("Early stopping")
            break

        if batch_idx % args.loginterval == 0:
            logger.info(
                'Traning Epoch {} and iteration {}/{},  \ttotal loss: {:.6f} -\t IIC loss: {:.3f}-\t MSE:{:.3f}', epoch,
                batch_idx + 1, args.nit, (lossAvg / args.loginterval), loss1, mse)
            lossAvg = 0
        if epoch % 2 == 1:
            pass
    torch.save(checkpoint, outpath + '/checkpoint.pth')


def train_scan(args, model, datapath, optimizer, epoch, outpath, rescalefactor, checkpoint, noneighbors, logger,
               patcharray=""):
    """
    Train RAPID model for pixel classification with SCAN loss.

    Args:
        args (argparse.ArgumentParser): Stores arguments that are used to define properties of the network.
        model (model): Torch nn model used for classification.
        datapath (str): Path to zarr file.
        optimizer (optimizer): AdamW optimizer used for the model.
        epoch (int): Number of epochs for the training phase.
        outpath (str): Path to the output folder where the model file will be saved.
        rescalefactor (float): Rescaling factor, must be between 0-1.
        checkpoint (dict): Dictionary storing the model, optimizer, and weights for the neural network.
        noneighbors (bool): If False, include neighbour information during training.
        logger (loguru.Logger): Logs loss values for each training iteration.
        patcharray (numpy.ndarray, optional): Array of pre-defined patches to use for training. Defaults to an empty string if using randomly-defined patches (Default: "").
    """
    # set model to train mode
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
    model.train()

    # MSE loss if full autoencoder model is used
    loss_fn = nn.MSELoss()
    lossAvg = 0
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # generate random crops from multiple images from multiple input images stored in zarr file
    empty_array, empty_array_gb, IND = cropandpaste_zarr(datapath,
                                                         args.patchsize,
                                                         args.npatches,
                                                         False,
                                                         rescalefactor,
                                                         gaussianblurstd=args.gbmi,
                                                         patcharray=patcharray,
                                                         )

    # Generate index reference matrix to keep the track of the neighbouring pixels
    a = np.arange(empty_array.shape[0] * empty_array.shape[1]).reshape((empty_array.shape[0], empty_array.shape[1]))

    # Manage the number of training iteration if it is too high or low
    totalpixels = int(len(IND) / args.bs)
    if (((totalpixels / args.nit) > 2) | ((totalpixels / args.nit) < 0.5)):
        num_of_train_iteration = args.nit
    else:
        num_of_train_iteration = totalpixels

    # Epoch training loop
    early_stopping = EarlyStopping(patience=2000, verbose=True, path=outpath + '/checkpoint.pth')
    criterion = SCANLoss()
    for batch_idx in range(0, num_of_train_iteration):

        # Reshape data to match the model input
        dataTrain = empty_array.reshape((-1, empty_array.shape[2]))
        dataTrain_G = empty_array_gb.reshape((-1, empty_array_gb.shape[2]))

        # sample random center pixels for training
        RANDINDEX = np.random.randint(0, len(IND), size=args.bs)
        RANDINDEX = IND[RANDINDEX]

        # Avoid using pixels which is close to patch border
        BORDER = 5
        RANDINDEX = RANDINDEX[(RANDINDEX % a.shape[1] > BORDER) & (RANDINDEX % a.shape[1] < a.shape[1] - BORDER) & (
                RANDINDEX / a.shape[0] > BORDER) & (RANDINDEX / a.shape[1] < a.shape[0] - BORDER)]

        # Indicies of all the pixels that are far from the border
        INDICIES = np.vstack([neighbors(a, np.unravel_index((RANDINDEX[x]), a.shape)) for x in range(len(RANDINDEX))])

        data = np.squeeze(dataTrain[RANDINDEX, :])
        # NZ=np.ones_like(data.reshape(-1))
        optimizer.zero_grad()

        # How many neighouring pixels to use for training
        nrounds = args.nonp
        neighbors_cord = [16, 17, 18, 23, 25, 30, 31, 32]
        neighbors_cord = [17, 23, 25, 31]

        # Generate indices of the pixels to randomly blankout for robust training
        npone = np.ones(dataTrain.shape[1])
        npone[0:int(dataTrain.shape[1] * args.blankpercent)] = 0

        # loop through number of random neighbouring pixels

        for REP in range(nrounds):
            np.random.shuffle(npone)
            np.random.shuffle(neighbors_cord)
            # RAWData=dataTrain[INDICIES[:,MORE[0]],:]

            # Get the indicies of pixels of interest
            RAWData = dataTrain[RANDINDEX, :]  # *npone

            # Generate random noise that will be added to the input data to calculate mutual information loss
            noise = np.random.normal(loc=0, scale=0.5, size=dataTrain[INDICIES[:, neighbors_cord[0]], :].shape).astype(
                np.float32)

            # Whether to use neighbouring pixel for mutual information or not?
            if noneighbors:

                # define the level of noise
                noiseadd = dataTrain[RANDINDEX, :] / args.noiselevel
                noise = noise * noiseadd

                # add noise to the input data to generate perturbed input
                altdata = dataTrain_G[RANDINDEX, :] + noise
                altdata = altdata * npone
            else:
                noiseadd = dataTrain[INDICIES[:, neighbors_cord[0]], :] / args.noiselevel
                noise = noise * noiseadd
                altdata = dataTrain_G[INDICIES[:, neighbors_cord[0]], :] + noise
                altdata = altdata * npone

            RAWData = torch.from_numpy(RAWData).float().to(device)

            # check the model type requested by the user and accordingly change the input shape
            ############output,AA = model(RAWData)
            if args.network == "rapidmixnet":
                res, AA = model(torch.unsqueeze(RAWData, 1))
                altdata = torch.from_numpy(altdata).float().to(device)
                res_alt, BB = model(torch.unsqueeze(altdata, 1))
            else:
                res, AA = model(RAWData)
                altdata = torch.from_numpy(altdata).float().to(device)
                res_alt, BB = model(altdata)

            # If model is full autoencoder, add MSE loss to the IID loss
            if args.mse:
                mi_loss = torch.sum(torch.stack([IID_loss(r, a, lamb=1) for r, a in zip(res, res_alt)])).mean()
                mse = loss_fn(torch.unsqueeze(RAWData, 1), AA)
                loss1 = (mse * 0.7) + (mi_loss * 0.3)
            else:
                mse = 0
                total_loss, consistency_loss, entropy_loss = [], [], []
                for anchors_output_subhead, neighbors_output_subhead in zip(res, res_alt):
                    total_loss_, consistency_loss_, entropy_loss_ = criterion(anchors_output_subhead,
                                                                              neighbors_output_subhead)
                    total_loss.append(total_loss_)
                    consistency_loss.append(consistency_loss_)
                    entropy_loss.append(entropy_loss_)

                loss1 = torch.sum(torch.stack(total_loss, dim=0))

        loss1.backward()
        optimizer.step()
        lossAvg = lossAvg + loss1.item()

        early_stopping(loss1, model)
        if early_stopping.early_stop:
            print("Early stopping")
            break

        if batch_idx % args.loginterval == 0:
            logger.info(
                'Traning Epoch {} and iteration {}/{},  \ttotal loss: {:.6f} -\t IIC loss: {:.3f}-\t MSE:{:.3f}', epoch,
                batch_idx + 1, args.nit, (lossAvg / args.loginterval), loss1, mse)
            lossAvg = 0
        if (epoch % 2 == 1):
            pass
    torch.save(checkpoint, outpath + '/checkpoint.pth')


if __name__ == "__main__":
    run_rapid()
