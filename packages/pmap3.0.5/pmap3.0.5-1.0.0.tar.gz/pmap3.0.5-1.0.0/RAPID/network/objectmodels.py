import logging
from skimage.exposure import equalize_adapthist
from skimage.exposure import rescale_intensity
import torch.nn.functional as F
from skimage.segmentation import find_boundaries
import numpy as np
from skimage.morphology import dilation
import copy
from skimage.morphology import disk
import torch
import torch.nn as nn
from napari.qt.progress import progress
from RAPID.util import denoise
import os


class Net(nn.Module):
    """
    Define neural network architecture consisting of repeated convolutions of various sizes.
    """

    def __init__(self):
        super(Net, self).__init__()
        self.conv01 = nn.Conv2d(1, 256, 7, 1, 3, bias=False)
        self.bn01 = nn.BatchNorm2d(256)
        self.conv1 = nn.Conv2d(256, 128, 5, 2, bias=False)
        self.bn1 = nn.BatchNorm2d(128)
        self.conv2 = nn.Conv2d(128, 128, 5, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 128, 5, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256, 4, 1, bias=False)
        self.bn4 = nn.BatchNorm2d(256)
        self.fc1 = nn.Linear(256, 512, bias=False)
        self.bn_fc = nn.BatchNorm1d(512)
        self.fc2 = nn.ModuleList([nn.Linear(512, 30) for _ in range(5)])
        self.fc2_alt = nn.ModuleList([nn.Linear(512, 40) for _ in range(5)])

    def forward(self, x):
        x = F.relu(self.bn01(self.conv01(x)))
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = x.view(x.size(0), -1)
        x_prefinal = F.relu(self.bn_fc(self.fc1(x)))

        x = [F.softmax(fc(x_prefinal), dim=1) for fc in self.fc2]
        x_alt = [F.softmax(fc(x_prefinal), dim=1) for fc in self.fc2_alt]
        return x, x_alt


def apply_filter_nuc(mem, nuc, containsmem, containsnuc):
    """
    Combine nuclear and membrane layers into one image array together

    Args:
        mem (numpy.ndarray): Merged membrane marker image array.
        nuc (numpy.ndarray): Merged nuclear marker image array.
        containsnuc (bool): True if nuclear layer included in merged image.
        boolmemlayer (bool): True if membrane layer included in merged image.

    :return: *(numpy.ndarray)*: \n
        Image array with nuclear and membrane images combined in different channels.
    """
    print(containsnuc, "boolnuc")
    print(containsmem, "boolmem")
    img = np.zeros((mem.shape[0], mem.shape[1], mem.shape[2], 2)).astype(np.float32)
    for i in range(len(mem)):
        if containsnuc:
            currentnuc = nuc[i, :, :] / 255
        else:
            currentnuc = np.zeros_like(nuc[i, :, :])
        if containsmem:
            currentmem = mem[i, :, :] / 255
        else:
            currentmem = np.zeros_like(mem[i, :, :])
        img[i, :, :, 0] = currentmem
        img[i, :, :, 1] = currentnuc
    return np.moveaxis(img, -1, 1)


def expand_objects(objectimg=None, numiterations=2):
    """
    Expand identified cell nuclei so that the objects include entire cells.

    Args:
        objectimg (numpy.ndarray, optional): Segmented image array before expansion of identified objects (Default: None).
        numofiterations (int, optional): Number of times to dilate initially-identified objects (Default: 1).

    :return: dilatedobjectimg *(numpy.ndarray)*: \n
        Segmented image array after expansion of identified objects.
    """
    objcopy = copy.deepcopy(np.squeeze(objectimg))
    print(objcopy.shape)
    for _ in range(numiterations):
        objcopy = dilation(objcopy, disk(1))
    objboundries = find_boundaries(objcopy, mode='outer')
    boundpixels = abs(objboundries - 1)
    dilatedobjectimg = objcopy.astype(np.int) * boundpixels.astype(np.int)
    return dilatedobjectimg


def histogram_normalization(image):
    """
    Pre-process images using Contrast Limited Adaptive Histogram Equalization (CLAHE). If one of the inputs is a
    constant-value array, it will be normalized as an array of all zeros of the same shape.

    Args:
        image (numpy.array): numpy array of phase image data.

    :return: normalizedimage *(numpy.ndarray)*: \n
        Pre-processed image data with dtype float32.
    """
    print(image.dtype)
    if not np.issubdtype(image.dtype, np.floating):
        logging.info('Converting image dtype to float')
    if len(image) < 250:
        normalizedimage = np.zeros_like(image)
    else:
        x = rescale_intensity(image / 255, out_range=(0.0, 1))
        x = equalize_adapthist(x, clip_limit=0.1, kernel_size=128)
        normalizedimage = x * 255
    return normalizedimage


def load_checkpoint(modelpath):
    """
    Load a pretrained model from the specified file path.

    Args:
        modelpath (str): Path to the pretrained model being loaded.

    :return: model *(torch.nn model)*: \n
        Loaded pretrained model from specified path.
    """
    model = Net()
    print(model)
    checkpoint = torch.load(modelpath, map_location={'cuda:0': 'cpu'})
    model = checkpoint['model']
    model.load_state_dict(checkpoint['state_dict'])
    for parameter in model.parameters():
        parameter.requires_grad = False
    model.eval()
    return model


def unet_featurize(memimg=None, nucimg=None, containsmem=False, containsnuc=False, device="cpu", bs=4, numclasses=2,
                   segmodelpath="", histogramnormalize=False):
    """
    Apply segmentation model on combined membrane and/or nuclear images to identify cells in an image.

    Args:
        memimg (numpy.ndarray, optional): Merged membrane markers from image to be segmented (Default: None).
        nucimg (numpy.ndarray, optional): Merged nuclear markers from image to be segmented (Default: None).
        device (str, optional): Device to use for analysis ("cpu" or "gpu") (Default: "cpu").
        bs (int, optional): Number of patches to pass through the network at a time (Default: 4).
        numclasses (int, optional): Number of classes in output image from the network (Default: 2).
        containsnuc (bool, optional): True if including nuclear markers in merged image (Default: False).
        containsmem (bool, optional): True if including membrane markers in merged image (Default: False).
        segmodelpath (str, optional): Path to pretrained segmentation model if using an alternative to RAPID algorithm (Default: "").
        histogramnormalize (bool, optional): If True, perform histogram normalization. Otherwise, do nothing (Default: False).

    :return: features *(numpy.ndarray)*: \n
        Segmented image array.
    """
    rootfolder = os.path.dirname(os.path.abspath(__file__))
    if segmodelpath == "":
        modelpath = rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6.pth"
    else:
        modelpath = segmodelpath

    model = load_checkpoint(modelpath)

    if containsmem and histogramnormalize:
        memimg = histogram_normalization(memimg)
        pass
    elif not containsmem:
        memimg = np.zeros_like(memimg)

    if containsnuc and histogramnormalize:
        nucimg = histogram_normalization(nucimg)
    elif not containsnuc:
        nucimg = np.zeros_like(nucimg).astype(np.uint8)

    memimg = denoise.check_padding(memimg, 1024)
    shape = memimg.shape
    memimg = denoise.make_patches(memimg, 1024)
    nucimg = denoise.check_padding(nucimg, 1024)
    nucimg = denoise.make_patches(nucimg, 1024)

    model.to(device)
    features = np.zeros((memimg.shape[0], numclasses, memimg.shape[1], memimg.shape[2])).astype(float)
    with torch.no_grad():
        indiceslist = []
        for i in range(0, len(memimg), bs):
            indiceslist.append(i)
        for i in progress(indiceslist, desc='Segmenting', total=0 if len(indiceslist) == 1 else None, ):
            tmpbatch = apply_filter_nuc(memimg[i:i + bs, :, :], nucimg[i:i + bs, :, :], containsmem, containsnuc)[:,
                       0:2, :, :]
            features[i:i + bs, :, :, :] = F.softmax(model(torch.from_numpy(tmpbatch).float().to(device)), dim=1).to(
                "cpu").numpy()
    features = np.nan_to_num(features)
    features = denoise.club_patches(features, shape)
    print("image shape output")
    return features
