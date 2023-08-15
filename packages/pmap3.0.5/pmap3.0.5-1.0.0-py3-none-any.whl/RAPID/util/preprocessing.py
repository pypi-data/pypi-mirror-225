import numpy as np
from scipy import ndimage
from RAPID.util.denoise import load_denoise_model,predictmask
import copy
from scipy import stats
from skimage.morphology import convex_hull_image

def smoothimage(data,medianblur=None,gaussianblur=None,gaussianblurstd=1):
    """
    Smooth noisy images with median or/and gaussian filters.

    Args:
        data (numpy.ndarray): Array for image to be smoothed.
        medianblur (bool, optional): If True, apply a median blur to the image (Default: None).
        gaussianblur (bool, optional): If True, apply a Gaussian blur to the image (Default: None).
        gaussianblurstd (float, optional): Standard deviation used as a parameter for Gaussian blur (Default: 1).

    :return: data *(numpy.ndarray)*: \n
        Smoothed image array.

    :Examples:

    >>> from RAPID.util.preprocessing import smoothimage
    >>> from sklearn.datasets import make_blobs
    >>> blobs, _ = make_blobs(n_samples=10000, centers=100, n_features=3,random_state=0)
    >>> noisyblobs = X+np.random.normal(loc=0, scale=1, size=X.shape)
    >>> cleanblobs = smoothimage(noisyblobs,medianblur=False,gaussianblur=True,gaussianblurstd =1)
    """

    #for patchnum in range(data.shape[0]):
    print("smoothing sample across all channels")
    dims = len(data.shape)
    if dims==3:
        filtersizeM = [3,3,1]
        filtersizeG = [gaussianblurstd,gaussianblurstd,0]
    if dims==4:
        filtersizeM = [1,3,3,1]
        filtersizeG = [0,gaussianblurstd,gaussianblurstd,0]
    if dims==5:
        filtersizeM = [1,1,3,3,1]
        filtersizeG = [0,0,gaussianblurstd,gaussianblurstd,0]
    if medianblur:
        data = ndimage.median_filter(data, filtersizeM)
        datar = data.reshape((-1,data.shape[-1]))
        data = (datar - np.mean(datar, axis=0)).reshape(data.shape)
        data[data<0] = 0
    if gaussianblur:
        data = ndimage.gaussian_filter(data, filtersizeG)
    return data


def denoise_img(data,selected_ch=None,BS=1):
    """
    Use a pretrained neural network to denoise an image.

    Args:
        data (numpy.ndarray): Input data array to be denoised.
        selected_ch (list, optional): Indices of channels in the image to be denoised (Default: None).
        BS (int, optional): Number of patches to include in each pass through the neural network (Default: 1).

    :return: cleantiff *(numpy.ndarray)*: \n
        Denoised image array.

    :Examples:

    >>> from RAPID.util.preprocessing import denoise_img
    >>> import tifffile
    >>> module_path = dirname(__file__)
    >>> imagepath = module_path+"/../Data/MouseLN/AB_CROP.tif"
    >>> img = tifffile.imread(imagepath)
    >>> denoised_img = denoise_img(noisyblobs,selected_ch=4,BS =10)
    """

    # loading deoising model
    print("loading deoising model..")
    model = load_denoise_model()
    tmpdata = copy.deepcopy(data)
    for ch in selected_ch:
        print("Denoising channel "+str(ch)+".")
        tmp = predictmask(model, tmpdata[:,:,ch],BS) * 255
        tmpdata[:,:,ch] = tmp[0:data.shape[0], 0:data.shape[1]]
    tmpdata[tmpdata > 0] = 1
    cleantiff = data * tmpdata
    return cleantiff


def normalize(Data,normtype,arcsinfactor=2):
    """
    Normalize an image dataset along an individual dimension.

    Args:
        Data (numpy.ndarray): Data array to be normalized.
        normtype (str): Type of normalization to be used. Options include "percentile", "minmax", "zscore", "arcsinh", "log10", and "log2".
        arcsinfactor (int, optional): Arcsinh normalization factor (only applied if normtype is arcsinh) (Default: 2).

    :return: normdata *(numpy.ndarray)*: \n
        Normalized data array.
    """

    normdata = np.zeros((Data.shape[0]*Data.shape[1],Data.shape[2]))
    datatmp = Data.reshape((-1, Data.shape[-1]))
    releventpart = np.mean(Data, axis=2)
    releventpart = ndimage.median_filter(releventpart, size=20)

    chull = convex_hull_image(releventpart)
    releventdata = datatmp[chull.flatten(), :]

    for i in range(datatmp.shape[1]):
         print("Normalizing across channel " + str(i))
         tmpData = releventdata[:, i].astype(np.float)
         if len(tmpData)>0:
             if normtype=="percentile":
                lowpercentile = np.percentile(tmpData[tmpData > 0], 3)
                toppercentile = np.percentile(tmpData[tmpData > 0], 99.9)
                tmpData[tmpData<=lowpercentile]=0
                tmpData[tmpData>=toppercentile]=toppercentile
             elif normtype=="minmax":
                if np.max(tmpData) > 0:
                    tmpData = tmpData * (1 / np.max(tmpData))
             elif normtype=="zscore":
                if np.std(tmpData) > 0:
                    tmpData = stats.zscore(tmpData)
             elif normtype=="arcsinh":
                 tmpData = np.arcsinh(tmpData / arcsinfactor)
             elif normtype=="log10":
                 tmpData = np.nan_to_num(np.log10(tmpData), nan=0, posinf=0, neginf=0)
             elif normtype=="log2":
                 tmpData = np.nan_to_num(np.log2(tmpData), nan=0, posinf=0, neginf=0)
             else:
                 raise ValueError(normtype+" type normalization is not present, please select 'percentile, minmax, zscore or arcsin noormalization'")
             normdata[chull.flatten(), i] = tmpData

    normdata = normdata.reshape(Data.shape)
    return normdata
