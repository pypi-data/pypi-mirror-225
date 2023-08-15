# RAPID-P folder /Volumes/NISHANT_MS/RAPID/Datasets/AB_multi/Domain/tiff/DomainLN_gbstd1WithJOJO_NoGP38_noise80_rf0.7_noNeigh_trim
# load packages
import copy

from scipy.spatial import cKDTree
import pandas as pd
import os
import numpy as np
import glob
from scipy import stats
import cv2 as cv
import argparse


# calculating KNN

### TODO: Check documentation
def gen_cord(mask):
    """
    Find (x,y)-coordinates of all elements of a given cluster.

    Args:
        mask (numpy.ndarray): Array containing only the cluster(s) of interest.

    :return: coords *(numpy.ndarray)*: \n
        Array containing the (x,y)-coordinates of interest and corresponding cluster IDs.
    """
    clusters = mask.flatten()
    # print(np.unique(clusters,return_counts=True))
    # generate list of the x,y indices of the given image
    y, x = np.indices(mask.shape).reshape(-1, len(clusters))

    # create a data table of coordinates and cluster IDs
    coords = np.c_[y, x, clusters]

    # select only those clusters which are present in an image
    coords = coords[np.isin(coords[:, 2], [1])]
    # print(DataTab.shape)
    return coords


def random_kdtree_single(rapid_clusters, numpixels, numsimulations, objectclusters=False):
    """
    Spatial co-distribution analysis using kd tree algorithm.

    Args:
        rapid_clusters (numpy.ndarray): RAPID's cluster data [2d].
        numpixels (int): Number of pixels to sample from in each simulation.
        numsimulations (int): Number of simulations to run.

    :return: pvals *(numpy.ndarray)*: \n
        Array of p-values for each pair of clusters.
    :return: fcvals *(numpy.ndarray)*: \n
        Array of fold change values for each pair of clusters.
    """

    print(rapid_clusters.shape)
    clusterimg = copy.deepcopy(rapid_clusters)
    clustermask = clusterimg != clusterimg[5, 5]
    mask = clusterimg == clusterimg[5, 5]
    clusterimg[clusterimg < clusterimg[5, 5]] = clusterimg[clusterimg < clusterimg[5, 5]] + 1
    clusterimg[mask] = 0
    print(np.unique(clustermask, return_counts=True))
    print("Unique clusters", sorted(np.unique(clusterimg)))


    unique_clusters = sorted(np.unique(clusterimg))
    if objectclusters:
        unique_clusters = unique_clusters[1:]
        Mat = np.tril(np.meshgrid(np.arange(1, np.max(clusterimg) + 1), np.arange(1, np.max(clusterimg) + 1)))[0]
    else:
        Mat = np.tril(np.meshgrid(np.arange(1, np.max(clusterimg) + 2), np.arange(1, np.max(clusterimg) + 2)))[0]
    Mat[0, 0] = 1
    print(Mat)
    iID, jID = np.nonzero(Mat)
    print(iID)
    print(jID)
    pvals = np.ones((np.max(iID) + 1, np.max(iID) + 1))
    fcvals = np.zeros((np.max(iID) + 1, np.max(iID) + 1))

    clusterTab_bg = gen_cord(np.array(clustermask, dtype=int))[:, :2]
    print(clusterTab_bg.shape)

    mask_list = []
    storeID = []
    print(np.unique(clusterimg[clustermask], return_counts=True))
    for miter in np.unique(iID):
        mask_list.append(gen_cord(np.array(clusterimg == unique_clusters[miter], dtype=int))[:, :2])
        storeID.append(miter)

    ### TODO: Does this do anything?
    boolDist = [True] * len(np.unique(iID))
    SelfDist = np.zeros(len(np.unique(iID)))
    for i in range(len(iID)):
        print("knn for cluster a ", unique_clusters[iID[i]])
        print("knn for cluster b ", unique_clusters[jID[i]])
        clusterTab_a = mask_list[iID[i]]
        clusterTab_b = mask_list[jID[i]]
        avgdist2clusta = []
        avgdist2clust_bg = []
        clustersize = np.min((len(clusterTab_a), len(clusterTab_b), numpixels))
        if boolDist[iID[i] - 1]:
            print(iID[i] - 1)
            randxpercent_a = clusterTab_a[np.random.choice(len(clusterTab_a), clustersize, replace=True),]
            randxpercent_b = clusterTab_a[np.random.choice(len(clusterTab_a), clustersize, replace=True),]
            treeactData_a = cKDTree(randxpercent_a)
            SelfDist[iID[i] - 1] = np.mean(treeactData_a.query(randxpercent_b, k=3, p=1)[0])
        for niter in range(numsimulations):
            randxpercent_a = clusterTab_a[np.random.choice(len(clusterTab_a), clustersize, replace=True),]
            randxpercent_b = clusterTab_b[np.random.choice(len(clusterTab_b), clustersize, replace=True),]
            randxpercent_bg = clusterTab_bg[np.random.choice(len(clusterTab_bg), clustersize, replace=True),]
            treeactData_a = cKDTree(randxpercent_a)
            avgdist2clusta.append(np.mean(treeactData_a.query(randxpercent_b, k=3, p=1)[0]) - SelfDist[iID[i] - 1])
            avgdist2clust_bg.append(np.mean(treeactData_a.query(randxpercent_bg, k=3, p=1)[0]) - SelfDist[iID[i] - 1])
        print("C:", avgdist2clusta)
        print("C:", avgdist2clust_bg)
        pvals[iID[i], jID[i]] = stats.ttest_ind(np.array(avgdist2clusta), np.array(avgdist2clust_bg)).pvalue
        fcvals[iID[i], jID[i]] = np.mean(avgdist2clusta) / np.mean(avgdist2clust_bg)
        fcvals[iID[i], jID[i]] = np.mean(avgdist2clusta) / np.mean(avgdist2clust_bg)
    print('distance is ', pvals)
    print('FC is ', fcvals)
    return pvals, fcvals


def concat_images(imga, imgb):
    """
    Combines two color image arrays side-by-side.

    Args:
        imga (numpy.ndarray): First input color array.
        imgb (numpy.ndarray): Second input color array.

    :return: new_img *(numpy.ndarray)*: \n
        Combined color image array.
    """
    ha, wa = imga.shape[:2]
    hb, wb = imgb.shape[:2]
    max_height = np.max([ha, hb])
    total_width = wa + wb
    new_img = np.zeros(shape=(max_height, total_width))
    new_img[:ha, :wa] = imga
    new_img[:hb, wa:wa + wb] = imgb
    return new_img


def concat_n_images(imgpaths):
    """
    Combines N color images from a list of image paths.

    Args:
        imgpaths (list): List of paths of images to concatenate.

    :return: output *(numpy.ndarray)*: \n
        Combined color image array.
    """
    output = None
    for i, path in enumerate(imgpaths):
        img = cv.imread(path, -1)
        if i == 0:
            output = img
        else:
            output = concat_images(output, img)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='RAPID: KNN calculation for RAPID-P clusters ( arguments with *** are important for RAPID analysis)')
    parser.add_argument('--greypath', type=str, default="./",
                        help="path to the RAPID-P Grey image folder (default: %(default)s)")
    parser.add_argument('--nsim', type=int, default=10, help="number of simulations (default: %(default)s)")
    parser.add_argument('--npix', type=int, default=1000,
                        help="max number of pixels from each cluster (default: %(default)s)")
    parser.add_argument('--outputname', type=str, default="Results_KNN",
                        help="output folder name (default: %(default)s)")
    args = parser.parse_args()
    print(args)
    ClusterFolder = args.greypath
    imglist = glob.glob(ClusterFolder + "/*_Gray.tif")
    print(imglist)
    outpath = ClusterFolder + '/' + args.outputname
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    Rclusters = concat_n_images(imglist)
    print(np.max(Rclusters))
    pval, FC = random_kdtree_single(Rclusters, args.npix, args.nsim)
    df_FC = pd.DataFrame(FC)
    df_FC.to_csv(outpath + "/_FC.csv")
    df = pd.DataFrame(pval)
    df.to_csv(outpath + "/_Pval.csv")
    pval[pval < 0.00000001] = 255
    pval[pval < 0.000001] = 150
    pval[pval < 0.0001] = 75
    pval[pval < 0.05] = 25
    pval[pval < 25] = 0
    df_pval = pd.DataFrame(pval)
    df_pval.index.astype(str).str.replace(r"^", "RP-")
    df_pval.index = (["RP-" + str(i + 1) for i in df_pval.index])
    df_pval.columns = (["RP-" + str(i + 1) for i in df_pval.columns.values])
    df_pval.to_csv(outpath + "/_PvalNorm.csv")
