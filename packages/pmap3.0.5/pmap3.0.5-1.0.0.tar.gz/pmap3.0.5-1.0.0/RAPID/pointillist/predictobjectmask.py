import os
import torch.nn.functional as F
from skimage import measure
from skimage.segmentation import find_boundaries
import numpy as np
import cv2 as cv
import copy

from skimage import morphology
import torch
import torch.nn as nn
from skimage.morphology import dilation
from skimage.color import label2rgb
from skimage.morphology import disk
import argparse
from RAPID.util import io as rio
import pandas as pd
import umap
from sklearn.preprocessing import StandardScaler
import phenograph
from PIL import Image as PImage
from RAPID.util.utils import generate_colormap
from sklearn.preprocessing import MinMaxScaler
from RAPID.util.mst import prep_for_mst, generate_mst
import glob
from RAPID.Impressionist import runRAPIDzarr
from RAPID.network import model as models
from RAPID.network import objectmodels
from torch import optim
from RAPID.network import IID_loss
from RAPID.util import utils


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(out_channels),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(out_channels),
        )

    def forward(self, x):
        return self.double_conv(x)


class Down(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)


class Up(nn.Module):
    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        else:
            self.up = nn.ConvTranspose2d(in_channels // 2, in_channels // 2, kernel_size=2, stride=2)
        self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        diffY = torch.tensor([x2.size()[2] - x1.size()[2]])
        diffX = torch.tensor([x2.size()[3] - x1.size()[3]])
        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2, diffY // 2, diffY - diffY // 2])
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class OutConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        return self.conv(x)


class UNet(nn.Module):
    def __init__(self, n_channels=2, n_classes=2, bilinear=True):
        super(UNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.bilinear = bilinear
        self.inc = DoubleConv(n_channels, 64)
        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        self.down4 = Down(512, 512)
        self.up1 = Up(1024, 256, bilinear)
        self.up2 = Up(512, 128, bilinear)
        self.up3 = Up(256, 64, bilinear)
        self.up4 = Up(128, 64, bilinear)
        self.outc = OutConv(64, n_classes)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        logits = self.outc(x)
        return logits


# https://github.com/davidmashburn/SeedWaterSegmenter/

class obejctsegmentation():
    def __init__(self, img=None):
        pass

    def mergemem(self, image=None, channels=None, mode="avg"):

        img2 = copy.deepcopy(image)

        if (len(channels) == 1):
            img2 = image
        else:
            img2 = img2[:, :, channels]

        if (mode == "avg"):
            print(img2.shape)
            img2 = np.mean(img2, axis=2)

        if (mode == "sum"):
            img2 = np.sum(img2, axis=2)

        if (mode == "max"):
            img2 = np.max(img2, axis=2)

        if (mode == "median"):
            img2 = np.median(img2, axis=2)

        return img2

    def quantifyimage(self, image, objects, object_true=False):
        """
        Expression quantification of the segmented object image.

        Arguments:
            :image (np.ndarray): multiplex input image [H,W,C]
            :objects (np.ndarray): unet segmented object image [H,W]
            :outfolder (str): Output folder
            :clusterID (list): list of the cluster IDs

        Returns:
            Quantification table [#objec, markers].
        """
        if (object_true):
            objects = objects
        else:
            objects = objects
            objects[objects >= 0.9] = 1
            objects[objects < 0.9] = 0

            objects = objects.astype(np.uint8)
            objects = measure.label(objects, connectivity=1)

        objects = morphology.remove_small_objects(objects, min_size=10)
        expandobject = self.expandobjects(objectimg=objects, numofiterations=2)
        print(np.unique(expandobject))
        uniqueexpandobject = np.unique(expandobject)
        all_labels, obejctcount = measure.label(objects, connectivity=1, return_num=True)
        expandobject = all_labels
        proptab = np.zeros((image.shape[2] + 4, obejctcount))
        cortab = np.zeros((2, obejctcount))
        first_category = all_labels

        all_labels = expandobject
        for ch in range(image.shape[2]):
            # proptab[ch, :] = [prop.mean_intensity for prop in measure.regionprops(all_labels, intensity_image=self.layers[self.MARKERS[ch]].data)]
            proptab[ch, :] = measure.regionprops_table(all_labels, image[:, :, ch], properties=['mean_intensity'])[
                'mean_intensity']
            # props = measure.regionprops_table(label_image, image,properties=['label', 'inertia_tensor', 'inertia_tensor_eigvals'])
        proptab[ch + 1, :] = [prop.area for prop in
                              measure.regionprops(all_labels, intensity_image=image[:, :, 0])]
        proptab[ch + 2, :] = [prop.eccentricity for prop in
                              measure.regionprops(all_labels, intensity_image=image[:, :, 0])]
        proptab[ch + 3, :] = [prop.perimeter for prop in
                              measure.regionprops(all_labels, intensity_image=image[:, :, 0])]
        proptab[ch + 4, :] = [prop.major_axis_length for prop in
                              measure.regionprops(all_labels, intensity_image=image[:, :, 0])]
        cortab = [prop.centroid for prop in measure.regionprops(all_labels, intensity_image=image[:, :, 0])]
        labtab = [prop.label for prop in measure.regionprops(all_labels, intensity_image=image[:, :, 0])]
        print(proptab.shape)
        print(proptab[0:10, 1:4])
        IMGMEAN = np.c_[np.asarray(labtab), np.asarray(cortab), proptab.T]
        # print(expandobject.shape)
        rgbimage = label2rgb(expandobject, image=None, colors=None, alpha=0.3, bg_label=0, bg_color=(0, 0, 0),
                             image_alpha=1, kind='overlay')

        cv.imwrite("/tmp/test.png", expandobject.astype(np.uint16))
        allt = copy.deepcopy((IMGMEAN))
        # print(allt[:10,:])
        RRRRR = 5
        tt2 = np.squeeze(allt[:, RRRRR])
        RESIND = np.squeeze(np.asarray(np.where(tt2 > 0.1)))
        print(RESIND.shape)
        emptymask = np.zeros_like(expandobject)

        '''
        for i in range(len(RESIND)):
             masktmp = ((self.expandobject == allt[RESIND[i],0].astype(np.int)))
             print(i)
             emptymask[masktmp] =  allt[RESIND[i],0]
        '''
        mask1 = np.in1d(expandobject, allt[RESIND, 0], invert=True)
        emptymask = copy.deepcopy(expandobject)
        emptymask.reshape(-1)[mask1] = 0
        # emptymask=emptymask#.reshape(self.expandobject.shape)
        # self.expandobject[self.expandobject == RESIND[:, None]]
        rgbimagemasked = label2rgb(emptymask, image=None, colors=None, alpha=0.3, bg_label=0, bg_color=(0, 0, 0),
                                   image_alpha=1, kind='overlay')
        return IMGMEAN, cortab, rgbimage, expandobject

    def displayumap(self, Qtab):
        reducer = umap.UMAP(min_dist=0.05, n_neighbors=5)
        # reducer = umap.UMAP(min_dist=0.05, n_neighbors=5,metric="cosine")
        mapper = reducer.fit_transform(Qtab[:, 3:])

        ymin = np.min(mapper[:, 1])
        ymax = np.max(mapper[:, 1])
        xmin = np.min(mapper[:, 0])
        xmax = np.max(mapper[:, 0])
        Xlen = xmax + np.abs(xmin)
        Ylen = ymax + np.abs(ymin)
        mapper[:, 1] = ((mapper[:, 1] - ymin) / (Ylen * 1.25)) * (200)
        mapper[:, 0] = ((mapper[:, 0] - xmin) / (Xlen * 1.25)) * (200)
        mapper = mapper.astype(np.int)
        mapper = mapper  # + 25
        IMGW = np.zeros((200, 200))
        corUMAP = np.zeros((len(mapper), len(mapper)))
        for i in range(len(mapper)):
            IMGW[mapper[i, 0], mapper[i, 1]] = 255
            corUMAP[mapper[i, 0], mapper[i, 1]] = i

        return IMGW, corUMAP

    def segment(self, viewer):
        viewer.status = "Segmenting..."
        self.layers['output'].visible = False

        # image = viewer.layers['input'].data
        image = viewer.active_layer.data
        cv.imwrite("/tmp/sps2.png", image)
        MinCL, MaxCL = viewer.active_layer.contrast_limits
        image[image <= MinCL] = 0
        image[image > MaxCL] = 1

        print(MinCL)
        cv.imwrite("/tmp/r1.png", image * 255)
        print(np.max(image))
        print(image.shape)
        print("........")
        # labels = viewer.layers['train'].data

        # fit and predict
        features = objectmodels.unet_featurize(image * 255)
        print(np.min(features))
        print(np.max(features))

        cv.imwrite("/tmp/r.png", features * 255)
        MP = self.layers['output'].data
        MP[MP > 0.5] = 1
        MP[MP <= 0] = 0

        self.layers['output'].data = features  # [0].transpose(2, 0, 1)
        # segmentation, self.prob = predict(clf, features)
        self.layers['output'].contrast_limits = np.min(features), np.max(features)
        self.layers['output'].visible = True
        self.layers['output'].blending = "additive"
        self.add_labels(MP, name="LAB", is_pyramid=True)
        self.layers['LAB'].editable = True
        # print(np.unique(self.layers['TEST'].data))
        # show prediction
        # self.segmentation = np.squeeze(segmentation)
        # viewer.layers['output'].data = self.segmentation

        viewer.status = "Segmentation Completed"

    def train_epochOobject(self, model, OrgIMG, optimizer, epoch, BS, PS, NIT, NMAX1):
        model.train()
        device = "cpu"
        lossAvg = 0
        for batch_idx in range(0, NIT):
            dataTrain = OrgIMG
            RANDINDEX = np.random.randint(0, len(OrgIMG), size=BS)
            data = np.squeeze(dataTrain[RANDINDEX, :])
            NZ = np.ones_like(data.reshape(-1))
            NZ[0:int(len(NZ) * 0.01)] = 0
            np.random.shuffle(NZ)
            NZ = NZ.reshape(data.shape)
            optimizer.zero_grad()
            HOWMANY = 1
            for REP in range(HOWMANY):
                RAWData = dataTrain[RANDINDEX, :]
                RAWData = RAWData * NZ
                RAWData = torch.from_numpy(RAWData).float().to(device)
                output, AA = model(RAWData)
                NOISE = np.random.normal(loc=0, scale=2, size=dataTrain[RANDINDEX, :].shape).astype(
                    np.float32)
                NOISEADD = NMAX1 / 20
                NOISE = NOISE * NOISEADD
                newdata = dataTrain[RANDINDEX, :] + NOISE
                newdata = newdata * NZ
                data_perturb = torch.from_numpy(newdata).float().to(device)
                output_alt, BB = model(data_perturb)
                if (REP == 0):
                    loss1 = torch.sum(torch.stack([IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                                                   zip(output, output_alt, AA, AA)])).mean()
                else:
                    TMP = loss1.clone()
                    loss1 = TMP + torch.sum(torch.stack([IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                                                         zip(output, output_alt, AA, AA)])).mean()
            loss1.backward()
            optimizer.step()
            lossAvg = lossAvg + loss1.item()
            if batch_idx % 1 == 0:
                print(
                    'Train Epoch {} -iteration {}/{} - LR {:.6f} -\ttotal loss: {:.6f} -\t IIC loss: {:.3f}-\t MSE:{:.3f}'.format(
                        epoch, batch_idx, NIT, 10, (lossAvg / 10), loss1, 10))
                lossAvg = 0

    def testobject(self, model, OrgIMG, BS, OrgShape, PS, EPOC):
        model.eval()
        device = "cpu"
        with torch.no_grad():
            testdata = copy.deepcopy(OrgIMG)
            TESTPATCHPRED = testdata.reshape((-1, testdata.shape[1]))
            TESTPATCHPREDO = np.zeros((TESTPATCHPRED.shape[0]))
            for BSTART in range(0, TESTPATCHPRED.shape[0], 50000):
                x = torch.from_numpy(TESTPATCHPRED[BSTART:BSTART + (50000), :]).float().to(device)
                outputs, AA = model(x)
                TESTPATCHPREDO[BSTART:BSTART + (50000)] = outputs[0].argmax(dim=1).cpu()
            # TESTPATCHPRED = TESTPATCHPREDO.reshape((self.RAPIDData.shape[1], self.RAPIDData.shape[2]))
        emptymask = np.zeros((self.img.shape[0], self.img.shape[1], 3))
        colforinput = utils.generate_colormap(int(self.nc))
        print(colforinput)
        try:
            for i in range(len(TESTPATCHPREDO)):
                masktmp = ((self.expandobject == self.Qtab[i, 0]))
                # print(self.expandobject[i])
                print(TESTPATCHPREDO[i])
                print(i)
                emptymask[masktmp] = colforinput[int(TESTPATCHPREDO[i]), :] / 255
            self.add_image(self.expandobject, name='RAPID cluster0', is_pyramid=False)
            self.layers['RAPID cluster0'].blending = "additive"
            self.add_image(emptymask, name='RAPID cluster', is_pyramid=False)
            self.layers['RAPID cluster'].blending = "additive"
        except Exception as ex:
            print(ex)

    def trainRAPIDOBJECT(self, viewer):
        model = models.RAPIDResnet(dimension=self.RAPIDData.shape[0], numclusters=int(self.nc), nummodules=2)
        model.apply(models.weight_init)
        print(model)
        model.to("cpu")
        optimizer = optim.AdamW(model.parameters(), lr=float(self.lr), betas=(0.9, 0.999), eps=1e-08, weight_decay=0.01,
                                amsgrad=False)
        STDIMG = copy.deepcopy((self.Qtab[:, 1:]))
        NMAX = np.max(STDIMG, axis=(0))
        print(NMAX)
        Batch_Size = int(self.bs)
        PS = int(self.ps)
        print(STDIMG.shape)
        print(".....")
        viewer.status = "RAPID training..."
        self.setinvisible()
        for epoch in range(1):
            for mode in ['train', 'test']:
                if (mode == "train"):
                    self.train_epochOobject(model, STDIMG, optimizer, epoch, Batch_Size, PS, int(self.nit), NMAX)
                else:
                    self.testobject(model, STDIMG, Batch_Size, STDIMG, PS, epoch)
        viewer.status = "RAPID training done."

    def trainRAPID2(self, viewer):
        model = models.RAPID(2, self.RAPIDData.shape[0] + 1, 30)
        model.apply(models.weight_init)
        model.to("cpu")
        optimizer = optim.AdamW(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0.01,
                                amsgrad=False)
        STDIMG = copy.deepcopy((self.RAPIDData))
        Add_Zeros = np.zeros((STDIMG.shape[1], STDIMG.shape[2]))
        self.ConcateZero = np.concatenate((STDIMG, Add_Zeros), axis=0)
        NMAX = np.max(self.ConcateZero, axis=(1, 2))
        print(NMAX)
        Batch_Size = 100
        PS = 64
        print(self.ConcateZero.shape)
        print(".....")
        viewer.status = "RAPID training..."
        self.setinvisible()
        for epoch in range(1):
            for mode in ['train', 'test']:
                if (mode == "train"):
                    self.train_epoch(model, self.ConcateZero, optimizer, epoch, Batch_Size, PS, 1000, NMAX)
                else:
                    self.test(model, self.ConcateZero, Batch_Size, self.ConcateZero, PS, epoch)
        viewer.status = "RAPID training done."

    def segment2(self, viewer):
        viewer.status = "Segmenting..."
        image = viewer.layers['input'].data
        labels = viewer.layers['train'].data

        # fit and predict
        clf, features = fit(image, labels, featurizer=self.cur_featurizer)
        self.layers['features'].data = features[0].transpose(2, 0, 1)
        segmentation, self.prob = predict(clf, features)

        # show prediction
        self.segmentation = np.squeeze(segmentation)
        viewer.layers['output'].data = self.segmentation

        viewer.status = "Segmentation Completed"

    def loadunetmodel(self):
        rootfolder = os.path.dirname(os.path.abspath(__file__))
        modelpath = rootfolder + "/../models/Model2_12.pt"
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        device = torch.device('cpu')
        model = UNet(1, 2).float()
        model = model.to(device).float()
        if (str(device) == "cpu"):
            model.load_state_dict(torch.load(modelpath, map_location=torch.device('cpu')))
            model = model.to(device).float()
        else:
            model.load_state_dict(torch.load(modelpath))
            model = model.to(device).float()
        model.eval()
        return model

    def checkpadding(self, image=None, PS=None):
        NC = int(image.shape[1] / PS)
        NR = int(image.shape[0] / PS)
        if ((NR * PS) >= image.shape[0]):
            NR = NR
        else:
            NR = NR + 1
        if ((NC * PS) >= image.shape[1]):
            NC = NC
        else:
            NC = NC + 1
        print(image.shape)
        modimage = np.zeros((PS * NR, PS * NC, image.shape[2]))
        modimage[0:image.shape[0], 0:image.shape[1], :] = image
        return modimage

    def make_patches(self, image=None, PS=None):
        tmpimages = np.zeros(
            (int(image.shape[0] / PS) * int(image.shape[1] / PS), PS, PS))
        p = 0
        for i in range(0, image.shape[0], PS):
            for j in range(0, image.shape[1], PS):
                tmpimages[p, :, :] = image[i:i + PS, j:j + PS]
                p = p + 1
        return tmpimages

    def clubpatches(self, image=None, imageshape=None):
        tmpimages = np.zeros_like(imageshape)
        print(image.shape)
        print(imageshape.shape)
        # modimage=np.zeros((PS*NR,PS*NC,image.shape[2]))
        p = 0
        NC = int(imageshape.shape[1] / image.shape[2])
        NR = int(imageshape.shape[0] / image.shape[2])
        PS = image.shape[2]
        p = 0
        for R in range(NR):
            for C in range(NC):
                # print(R)
                # print(C)
                tmpimages[R * PS:(R * PS) + PS, C * PS:(C * PS) + PS] = image[p,
                                                                        1, :, :]
                p = p + 1
        # for i in range(image.shape[0]):
        #    ROWN=int(i/NR)
        #    COLN=int(i%NC)
        #    tmpimages[ROWN*PS:PS, COLN*PS:PS] = image[0, 1, :, :]
        return tmpimages

    def clubpatches2(image=None, imageshape=None):
        tmpimages = np.zeros_like(imageshape)
        print(image.shape)
        print(imageshape.shape)
        # modimage=np.zeros((PS*NR,PS*NC,image.shape[2]))
        p = 0
        NC = int(imageshape.shape[1] / 256)
        NR = int(imageshape.shape[0] / 256)
        PS = 256
        p = 0
        for R in range(NR):
            for C in range(NC):
                print(R)
                print(C)
                tmpimages[R * PS:(R * PS) + PS, C * PS:(C * PS) + PS] = image[p,
                                                                        :, :]
                p = p + 1
        # for i in range(image.shape[0]):
        #    ROWN=int(i/NR)
        #    COLN=int(i%NC)
        #    tmpimages[ROWN*PS:PS, COLN*PS:PS] = image[0, 1, :, :]
        tmpimages[0:PS, 0:PS] = image[0, 1, :, :]
        tmpimages[0:PS, PS:PS + PS] = image[1, 1, :, :]
        tmpimages[PS:PS + PS, 0:PS] = image[2, 1, :, :]
        tmpimages[PS:PS + PS, PS:PS + PS] = image[3, 1, :, :]
        return tmpimages

    def rununet(self, image, featurizer_path="/Users/thakurn2/PycharmProjects/RAPID/RAPID/models/Model2_12.pt",
                device="cpu"):  #
        model = self.loadunetmodel().float()
        # *******
        paddedimage = self.checkpadding(image)
        image2 = self.make_patches(paddedimage, 256)
        emptyresult = np.zeros(
            (image2.shape[0], 2, image2.shape[1], image2.shape[2]))
        with torch.no_grad():
            for i in range(emptyresult.shape[0]):
                emptyresult[i, :, :, :] = F.softmax(model(torch.unsqueeze(
                    torch.unsqueeze(torch.from_numpy(image2[i, :, :]), 0),
                    0).float()).to(device), dim=1).numpy()
        features = emptyresult
        features = self.clubpatches(features, paddedimage)
        return features

    def unet_featurizeRAPID(image,
                            featurizer_path="/Users/thakurn2/Downloads/Biowulf/TMP/Model5.pt",
                            device="cpu"):
        model = _load_model(featurizer_path).float()
        # image = torch.Tensor(image).float()
        image = checkpadding(image, 256)
        image2 = make_patches(image, 256)
        # print(model)
        emptyresult = np.zeros(
            (image2.shape[0], 2, image2.shape[1], image2.shape[2]))
        with torch.no_grad():
            for i in range(emptyresult.shape[0]):
                emptyresult[i, :, :, :] = model(torch.unsqueeze(
                    torch.unsqueeze(torch.from_numpy(image2[i, :, :]), 0),
                    0).float()).to(device).numpy()
        features = emptyresult
        features = clubpatches(features, image)
        # print(features.shape)

        # features = np.transpose(features, (0,2,3,1))
        return features

    def predict(classifier, features):
        X = features.reshape([-1, features.shape[-1]])
        try:
            y = classifier.predict(X)
            prob = classifier.predict_proba(X)
            labels = y.reshape(features.shape[:-1])
            prob_shape = features.shape[:-1] + (prob.shape[-1],)
            prob = prob.reshape(prob_shape)
        except:
            labels = np.zeros(features.shape[:-1], dtype=int)
            prob = np.zeros(features.shape[:-1], dtype=int)
        return labels, prob

    def quantifylabels(segmentedimage=None, intensityimage=None,
                       properties=("mean", "centroid")):
        blobs = copy.deepcopy(segmentedimage)
        blobs[blobs > 0] = 1
        all_labels, obejctcount = measure.label(blobs, connectivity=1,
                                                return_num=True)
        blobs_labels = measure.label(blobs, background=0)
        proptab = np.zeros((intensityimage.shape[0], obejctcount))
        print(proptab.shape)
        # skimage.measure.regionprops_table(label_image, intensity_image=None, properties=('label', 'bbox'), *, cache=True,separator='-')
        for ch in range(intensityimage.shape[0]):
            proptab[ch, :] = [prop.mean_intensity for prop in
                              measure.regionprops(all_labels,
                                                  intensity_image=intensityimage[
                                                                  ch, :, :])]
            # print([prop.mean_intensity for prop in measure.regionprops(
            # all_labels, intensity_image=image[ch,:,:])])
        return proptab.T

    def expandobjects(self, objectimg=None, numofiterations=1):
        # objboundries = find_boundaries(objectimg, mode='outer')
        objcopy = copy.deepcopy(np.squeeze(objectimg))
        print(objcopy.shape)
        for iter in range(numofiterations):
            objcopy = dilation(objcopy, disk(2))
            # boundpixels = abs(objboundries - 1)
            # objcopy = objcopy * boundpixels
        objboundries = find_boundaries(objcopy, mode='outer')
        boundpixels = abs(objboundries - 1)
        dilatedobjimage = objcopy.astype(np.int) * boundpixels.astype(np.int)
        return dilatedobjimage

    def run_object_prediction(self, image, membranechannel, outfolder="./",
                              gaussianblur=False,
                              gaussianblurstd=1, medianblur=True,
                              selectzslice=None, selecttime=None,
                              marker_list=None, mergedimage=None):
        """
        Expression quantification of the segmented object image.

        Arguments:
            :image (numpy.ndarray): multiplex input image [H,W,C]
            :membranechannel (list): channels to use for object identification ["A","B","C",...."Z"]
            :gaussianblur (bool): apply gaussian blur [True, False]
            :medianblur (bool): apply median blur [True, False]
            :outfolder (str): Output folder
            :selectzslice (int): select z slice for analysis [default number of z/2]
            :selecttimeslice (int): select t slice for analysis [default number of t/2]
            :mergedimage (numpy.ndarray): if merged image is provided

        Returns:
            :numpy.ndarray: for RAPID object based analysis.
        """

        if (type(image) == np.ndarray):
            if (selectzslice == None):
                if (len(image.shape) == 4):
                    selectzslice = int(image.shape[0] / 2)
                elif (len(image.shape) == 5):
                    selectzslice = int(image.shape[1] / 2)
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image
            pass
        else:

            image = rio.readome(image, selectz=selectzslice,
                                selecttime=selecttime)
            if ((gaussianblur == True) & (medianblur == True)):
                image = utils.smoothing(image, gaussianblur=True, gaussianblurstd=gaussianblurstd, medianblur=True)
            elif ((gaussianblur == True) & (medianblur == False)):
                image = utils.smoothing(image, gaussianblur=True, gaussianblurstd=gaussianblurstd, medianblur=False)
            elif ((gaussianblur == False) & (medianblur == True)):
                image = utils.smoothing(image, gaussianblur=False, gaussianblurstd=gaussianblurstd, medianblur=True)
            if (selectzslice == None):
                if (len(image.shape) == 4):
                    selectzslice = int(image.shape[0] / 2)
                elif (len(image.shape) == 5):
                    selectzslice = int(image.shape[1] / 2)
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image

        paddedimage = self.checkpadding(image, 256)
        if (type(mergedimage) != np.ndarray):
            mergedimage = self.mergemem(image=paddedimage,
                                        channels=membranechannel,
                                        mode="sum")
        else:
            mergedimage = mergedimage
        predimg = self.rununet(mergedimage)

        if not os.path.exists(outfolder):
            os.mkdir(outfolder)

        rapidobjects = predimg * 255
        cv.imwrite(outfolder + "/Obejects.png", rapidobjects.astype(np.uint8))

        if (len(marker_list) == 0):
            marker_list = [i for i in range(image.shape[-1])]

        table, coordinates, object2rgb, expandobject = self.quantifyimage(paddedimage,
                                                                          predimg, object_true=False)
        table = pd.DataFrame(table)

        table.columns = np.hstack([["ID", "X", "Y"], marker_list])

        table.to_csv(outfolder + "/ObjectQuantification.csv")

        print(table.values)
        object2rgb = object2rgb * 255
        cv.imwrite(outfolder + "/Object2rgb.png", object2rgb.astype(np.uint8))

        return table, rapidobjects, expandobject, object2rgb

    def run_object_prediction_from_mask(self, image, membranechannel, outfolder="./",
                                        gaussianblur=False,
                                        gaussianblurstd=1, medianblur=True,
                                        selectzslice=None, selecttime=None,
                                        marker_list=None, maskimage=None):
        """
        Expression quantification of the segmented object image.

        Arguments:
            :image (numpy.ndarray): multiplex input image [H,W,C]
            :membranechannel (list): channels to use for object identification ["A","B","C",...."Z"]
            :gaussianblur (bool): apply gaussian blur [True, False]
            :medianblur (bool): apply median blur [True, False]
            :outfolder (str): Output folder
            :selectzslice (int): select z slice for analysis [default number of z/2]
            :selecttimeslice (int): select t slice for analysis [default number of t/2]
            :mergedimage (numpy.ndarray): if merged image is provided

        Returns:
            :numpy.ndarray: for RAPID object based analysis.
        """

        if (type(image) == np.ndarray):
            if (selectzslice == None):
                if (len(image.shape) == 4):
                    selectzslice = int(image.shape[0] / 2)
                elif (len(image.shape) == 5):
                    selectzslice = int(image.shape[1] / 2)
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image
            pass
        else:

            image = rio.readome(image, selectz=selectzslice,
                                selecttime=selecttime)
            if ((gaussianblur == True) & (medianblur == True)):
                image = utils.smoothing(image, gaussianblur=False, gaussianblurstd=gaussianblurstd, medianblur=True)
            elif ((gaussianblur == True) & (medianblur == False)):
                image = utils.smoothing(image, gaussianblur=False, gaussianblurstd=gaussianblurstd, medianblur=True)
            elif ((gaussianblur == False) & (medianblur == True)):
                image = utils.smoothing(image, gaussianblur=False, gaussianblurstd=gaussianblurstd, medianblur=True)
            if (selectzslice == None):
                if (len(image.shape) == 4):
                    selectzslice = int(image.shape[0] / 2)
                elif (len(image.shape) == 5):
                    selectzslice = int(image.shape[1] / 2)
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
                    image = image

        paddedimage = self.checkpadding(image, 256)
        if (type(maskimage) != np.ndarray):
            maskimage = cv.imread(maskimage, 0)
            emptymask = np.zeros((paddedimage.shape[0:2]))
            emptymask[:maskimage.shape[0], :maskimage.shape[1]] = maskimage
        else:
            maskimage = maskimage
            emptymask = np.zeros((paddedimage.shape[0:2])).astype(np.uint16)
            emptymask[:maskimage.shape[0], :maskimage.shape[1]] = maskimage
        maskimage = emptymask
        predimg = maskimage
        print(paddedimage.shape)
        print(emptymask.shape)

        if not os.path.exists(outfolder):
            os.mkdir(outfolder)

        rapidobjects = predimg * 255
        print("sdsdsd")
        cv.imwrite(outfolder + "/Obejects.png", rapidobjects.astype(np.uint8))

        if (len(marker_list) == 0):
            marker_list = [i for i in range(image.shape[-1])]

        table, coordinates, object2rgb, expandobject = self.quantifyimage(paddedimage,
                                                                          predimg, object_true=True)
        table = pd.DataFrame(table)

        table.columns = np.hstack([["ID", "X", "Y"], marker_list])

        # table.to_csv(outfolder + "/ObjectQuantification.csv")

        print(table.values)
        object2rgb = object2rgb * 255
        cv.imwrite(outfolder + "/Object2rgb.png", object2rgb.astype(np.uint8))

        return table, rapidobjects, expandobject, object2rgb


def RAPIDObject():
    parser = argparse.ArgumentParser(
        description='RAPID: deep learning algorithm for quantitative analysis of cell type and distribution from high content imaging data')
    parser.add_argument('--membranechannel', type=str, default=500, metavar='N',
                        help="memebrane channels to be merged, each marker must be separtetd by comma [,]  (default: %(default)s)")
    parser.add_argument('--imagepath', type=str, default=0.0001, metavar='LR',
                        help="Path to the tiff file")
    parser.add_argument('--outfolder', type=str, default="/tmp/output",
                        help="Output folder path (default: %(default)s)")
    parser.add_argument('--gaussianblur', type=bool, default=False, metavar='S',
                        help="Gaussian smothing of the image (default: %(default)s)")
    parser.add_argument('--medianblur', type=bool, default=True, metavar='N',
                        help=" median filter on the input image  (default: %(default)s)")
    parser.add_argument('--selectzslice', type=int, default=True, metavar='N',
                        help="number of Z slice to use if multiple z present in the image, else, set to Nome (default: %(default)s)")

    parser.add_argument('--markernames', type=str, default=True, metavar='N',
                        help="marker names for the input tiff image, each marker must be separtetd by comma [,] (default: %(default)s)")

    args = parser.parse_args()
    objseg = obejctsegmentation()

    # image = rio.readimage(args.PATH)
    # image = np.moveaxis(image, 0, 2)
    # print(image.shape)
    # channels = [0, 3, 4, 6, 7]
    membranechannel = np.array(args.membranechannel.split(','), dtype=int)
    markernames = np.array(args.markernames.split(','), dtype=str)
    markernames.append("Area")
    markernames.append("Eccentricity")
    markernames.append("Perimeter")
    markernames.append("Major_axis_length")
    for arg in vars(args):
        print(str(arg) + "=" + str(getattr(args, arg)))

    # image = rio.readimage(args.IMAGEPATH)
    objseg.run_object_prediction(image=args.imagepath, membranechannel=membranechannel, outfolder=args.outfolder,
                                 gaussianblur=args.gaussianblur, medianblur=args.medianblur,
                                 selectzslice=args.selectzslice, marker_list=markernames, mergedimage=None)


def method_searchsort(from_values, to_values, array):
    sort_idx = np.argsort(from_values)
    idx = np.searchsorted(from_values, array, sorter=sort_idx)
    out = to_values[sort_idx][idx]
    return out


def train_object(model, OrgIMG, optimizer, epoch, BS, PS, NIT, NMAX1, args):
    model.train()
    device = "cpu"
    lossAvg = 0
    loss_fn = nn.MSELoss()
    for batch_idx in range(0, NIT):
        dataTrain = OrgIMG
        RANDINDEX = np.random.randint(0, len(OrgIMG), size=BS)
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
            # output, AA = model(RAWData)
            output, AA, RR = model(RAWData, torch.unsqueeze(RAWData, 1))
            NOISE = np.random.normal(loc=0, scale=1, size=dataTrain[RANDINDEX, :].shape).astype(
                np.float32)
            NOISEADD = dataTrain[RANDINDEX, :] / 80
            NOISE = NOISE * NOISEADD
            newdata = dataTrain[RANDINDEX, :] + NOISE
            newdata = newdata * NZ
            data_perturb = torch.from_numpy(newdata).float().to(device)
            # output_alt, BB = model(data_perturb)
            output_alt, BB, SS = model(data_perturb, torch.unsqueeze(data_perturb, 1))
            CLUS = output[0].argmax(dim=1).detach().cpu().numpy()
            if (args.distance != None):
                # COR=clustercosinedistance(dataTrain[RANDINDEX,:],CLUS)
                # COR=pairwise_dists(dataTrain[RANDINDEX,:],dataTrain[RANDINDEX,:])
                COR = runRAPIDzarr.clustercosinedistancetorch(dataTrain[RANDINDEX, :], CLUS)
            if (REP == 0):
                loss1 = torch.sum(torch.stack([IID_loss.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                                               zip(output, output_alt, AA, AA)])).mean()
                loss1 += torch.sum(torch.stack(
                    [IID_loss.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                     zip(RR, SS, AA, AA)])).mean()
            else:
                TMP = loss1.clone()
                loss1 = TMP + torch.sum(torch.stack(
                    [IID_loss.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                     zip(output, output_alt, AA, AA)])).mean()
            if (args.mse):
                MSE = loss_fn(RAWData, AA)
                loss1 += MSE + COR
                # COR=MSE.item()
            else:
                loss1 += COR
                # loss1 +=MSE
                # loss1 +=loss_fn(RAWData,AA)
                # COR=MSE
        loss1.backward()
        optimizer.step()
        lossAvg = lossAvg + loss1.item()
        if batch_idx % 1 == 0:
            print(
                'Train Epoch {} -iteration {}/{} - LR {:.6f} -\ttotal loss: {:.6f} -\t IIC loss: {:.3f}-\t MSE:{:.3f}'.format(
                    epoch, batch_idx, NIT, 10, (lossAvg / 10), loss1, COR))
            lossAvg = 0


def trainRAPIDObject(Qtab, objectmarkernums):
    numCells = 0
    for i in range(len(Qtab)):
        numCells += Qtab[i].shape[0]
    currentImage = np.zeros((numCells, len(objectmarkernums)))
    count = 0
    for i in range(len(Qtab)):
        currentImage[count:count + Qtab[i].shape[0], :] = Qtab[i][:, objectmarkernums]
        count += Qtab[i].shape[0]
    if (args.normalize):
        STDIMG = StandardScaler().fit_transform(currentImage)
    else:
        STDIMG = currentImage
    NMAX = np.max(STDIMG, axis=(0))
    Batch_Size = int(args.bs)
    PS = 10
    if args.phenograph == 'True':
        model = 0
        pass
    else:
        model = models.RAPIDMixNet(dimension=len(objectmarkernums), nummodules=2, mse=args.mse,
                                   numclusters=int(args.ncluster))
        model.apply(models.weight_init)
        print(model)
        model.to("cpu")
        optimizer = optim.AdamW(model.parameters(), lr=float(args.lr), betas=(0.9, 0.999), eps=1e-08, weight_decay=0.01,
                                amsgrad=False)
        train_object(model, STDIMG, optimizer, 0, Batch_Size, PS, int(args.nit), NMAX, args)
    testobject(model, STDIMG, Batch_Size, STDIMG, PS, 0, args, setParams)


def testobject(model, OrgIMG, BS, OrgShape, PS, EPOC, args, objecttrainmarkers):
    # model.eval()
    device = "cpu"
    torch.manual_seed(100)
    np.random.seed(100)
    torch.cuda.manual_seed(100)
    mergemarkerlist = objecttrainmarkers[-1]
    if (args.phenograph == 'True'):
        pass
    else:
        model.eval()
        with torch.no_grad():
            testdata = copy.deepcopy(OrgIMG)
            TESTPATCHPRED = testdata.reshape((-1, testdata.shape[1]))
            TESTPATCHPREDO = np.zeros((TESTPATCHPRED.shape[0]))
            for BSTART in range(0, TESTPATCHPRED.shape[0], 50000):
                x = torch.from_numpy(TESTPATCHPRED[BSTART:BSTART + (50000), :]).float().to(device)
                outputs, AA, SS = model(x, torch.unsqueeze(x, 1))
                TESTPATCHPREDO[BSTART:BSTART + (50000)] = outputs[0].argmax(dim=1).cpu()
    complete_tab = []
    qtabindices = [0]
    for ind in objecttrainmarkers:
        qtabindices.append(ind)
    for tab_len in range(viewer.window.qt_viewer.numImgs):
        complete_tab.append(viewer.Qtab[tab_len][:, qtabindices])
    from_values = np.vstack(complete_tab)[:, 0]
    complete_tab_DF = pd.DataFrame(np.vstack(complete_tab))
    complete_tab_DF.columns = np.hstack(["Label", mergemarkerlist])
    complete_tab_DF.to_csv(outputfolder.hdfpath + "/FullObject_segmentation_data.csv")
    complete_tab = np.vstack(complete_tab)
    if (args.phenograph == 'True'):
        if (args.normalize):
            phenopgraphin = StandardScaler().fit_transform(complete_tab_DF.values[:, 1:])
        else:
            phenopgraphin = complete_tab_DF.values[:, 1:]
        TESTPATCHPREDO, graph, Q = phenograph.cluster(phenopgraphin, n_jobs=1,
                                                      resolution_parameter=int(args.PGres), k=int(args.PGnn),
                                                      primary_metric=str(args.PGdis))
    # pair values from 0 to 2000
    to_values = TESTPATCHPREDO  # all values from 0 to 1000
    relabeled_table = copy.deepcopy(complete_tab)
    relabeled_table[:, 0] = to_values
    relabledimages = np.zeros(
        (viewer.window.qt_viewer.numImgs, viewer.expandobjects[0].shape[0], viewer.expandobjects[0].shape[1], 3))
    relabledgreyimages = np.zeros(
        (viewer.window.qt_viewer.numImgs, viewer.expandobjects[0].shape[0], viewer.expandobjects[0].shape[1]))
    PAL = generate_colormap(int(np.max(TESTPATCHPREDO) + 1) * 2)
    np.save(outputfolder.hdfpath + "/" + "color.npy", PAL)
    PAL2 = PAL.flatten()
    PAL0 = np.zeros(768)
    PAL0[0:len(PAL2)] = PAL2
    viewer.COL_LIST = PAL
    count_lab = 0
    Slices_object = np.zeros(
        (viewer.window.qt_viewer.numImgs, int(np.max(TESTPATCHPREDO) + 1), len(viewer.objecttrainmarkers[-1]) + 3))
    startindex = 0
    viewer.objclusterstartindex = len(viewer.window.qt_viewer.objectClusters)
    for imagelen in range(viewer.window.qt_viewer.numImgs):
        from_values = complete_tab_DF['Label'].values[startindex:startindex + len(viewer.Qtab[imagelen])]
        to_values = TESTPATCHPREDO[startindex:startindex + len(viewer.Qtab[imagelen])]
        viewer.window.qt_viewer.objectClusters.append(copy.deepcopy(to_values))
        relabeled = method_searchsort(from_values, to_values, viewer.expandobjects[imagelen].flatten().astype(int))
        startindex += len(viewer.Qtab[imagelen])
        relabledgreyimages[imagelen, :, :] = relabeled.reshape(viewer.expandobjects[imagelen].shape)
        cv.imwrite(outputfolder.hdfpath + "/RELABELED_Grey" + str(imagelen) + ".png",
                   relabledgreyimages[imagelen, :, :].astype(np.uint8))
        imgp = PImage.fromarray(relabeled.reshape(viewer.expandobjects[0].shape).astype(np.uint8), mode='P')
        imgp.putpalette(list(PAL0.flatten().astype(int)))
        imgp.save(outputfolder.hdfpath + "/RELABELED_" + str(imagelen) + ".png")
        relab = cv.imread(outputfolder.hdfpath + "/RELABELED_" + str(imagelen) + ".png")
        relabledimages[imagelen, :, :, :] = np.asarray(relab)
        tmp_tab = relabeled_table[
                  count_lab:count_lab + len(viewer.Qtab[imagelen]) + len(np.unique(relabeled_table[:, 0]))]
        nclusters = len(Slices_object[0, :, ])
        tmp_tab[-nclusters:, 0] = np.arange(nclusters)
        tmp_tab_df = pd.DataFrame(tmp_tab)
        count_lab += len(viewer.Qtab[imagelen])
        grouped = tmp_tab_df.groupby(0)
        tabres = grouped.apply(np.mean)
        tabres.insert(0, "Sample", imagelen)
        unique, counts = np.unique(tmp_tab[:, 0], return_counts=True)
        tabres.insert(2, "Pixels", counts)
        StandardScaler().fit_transform(tabres.values[:, 3:])
        scaler = MinMaxScaler()
        scaler.fit(StandardScaler().fit_transform(tabres.values[:, 3:]))
        min_max_normdata = scaler.transform(StandardScaler().fit_transform(tabres.values[:, 3:]))
        # Cutoff the overflowing (>1) of values
        min_max_normdata[min_max_normdata > 1] = 1
        Slices_object[imagelen, :, :] = tabres.values

    if not viewer.window.qt_viewer.trainedObject:
        for i in range(viewer.displayselectedcount):
            ind = len(viewer.window.qt_viewer.orders) + i - viewer.displayselectedcount
            cellnums = list(viewer.Qtab[ind][:, 0].astype(np.uint8))
            objclusters = []
            for j in cellnums:
                objclusters.append(viewer.window.qt_viewer.objectClusters[i % 2][j])
            viewer.window.qt_viewer.objectClusters.append(objclusters)

    viewer.window.qt_viewer.objectclustertable = np.nan_to_num((np.vstack(Slices_object)))
    my_data = pd.DataFrame(np.nan_to_num((np.vstack(Slices_object))))
    ''' Find weighted average data '''
    data = viewer.window.qt_viewer.objectclustertable
    numSamples = len(np.unique(data[:, 0]))
    weighted_average = np.zeros((int(data.shape[0] / numSamples), data.shape[1] - 2))
    for i in range(data.shape[0]):
        currcluster = i % weighted_average.shape[0]
        weighted_average[currcluster, 0] += data[i, 2]
    for i in range(data.shape[0]):
        currcluster = i % weighted_average.shape[0]
        weighted_average[currcluster, 1:] += data[i, 3:] * data[i, 2] / weighted_average[currcluster, 0]
    viewer.window.qt_viewer.trainobjectcomb = weighted_average
    minvals = []
    maxvals = []
    for i in range(viewer.window.qt_viewer.trainobjectcomb.shape[1] - 1):
        minvals.append(np.min(viewer.window.qt_viewer.trainobjectcomb[:, i + 1]))
        maxvals.append(np.max(viewer.window.qt_viewer.trainobjectcomb[:, i + 1]))
    viewer.minvalsobject.append(copy.deepcopy(minvals))
    viewer.maxvalsobject.append(copy.deepcopy(maxvals))
    viewer.window.qt_viewer.lowerBoundsList.append(copy.deepcopy(minvals))
    viewer.window.qt_viewer.upperBoundsList.append(copy.deepcopy(maxvals))
    mergemarkerlist = viewer.objecttrainmarkers[-1]

    relabledgreyimages[viewer.expandobjects == 0] = -1
    relabledimages[viewer.expandobjects == 0] = 0

    viewer.greyobjects.append(relabledgreyimages)
    my_data.columns = np.hstack([["Sample", "Cluster", "Pixels"], mergemarkerlist])
    viewer.add_image((relabledgreyimages.astype(np.uint8) + 1), name='Object_cluster', is_pyramid=False,
                     blending="additive")
    viewer.add_image(relabledimages / 255, name='RAPID cluster', is_pyramid=False, blending="additive")
    my_data.to_csv(outputfolder.hdfpath + "/RAPIDObject_cluster_table.csv")
    tabledata, my_data_scaled, DistMatrix, uniqueClusters = \
        prep_for_mst(clustertable=my_data, minnumpixels=1, outfolder=outputfolder.hdfpath,
                     includedmarkers=mergemarkerlist)
    final = my_data_scaled.columns
    viewer.window.qt_viewer.index = 0
    viewer.window.qt_viewer.objectClusterList = []
    for i in range(int(np.max(relabledgreyimages)) + 1):
        viewer.window.qt_viewer.objectClusterList.append([i])
    generate_mst(distancematrix=DistMatrix, normalizeddf=my_data_scaled[final], colors=PAL, randomseed=0,
                 outfolder=outputfolder.hdfpath, clusterheatmap=True, displaymarkers=mergemarkerlist,
                 uniqueclusters=uniqueClusters, samplenames=list(np.unique(my_data['Sample'])), displaysingle=False)
    viewer.window.qt_viewer.objectdatalist.append(viewer.window.qt_viewer.trainobjectcomb)


def runphenograph(Qtab, mergemarkerlist, expandobjects, outfolder, args):
    complete_tab = []
    print(Qtab[0])
    for tab_len in range(len(Qtab)):
        complete_tab.append(Qtab[tab_len][:, :])
    complete_tab_DF = pd.DataFrame(np.vstack(complete_tab))
    # complete_tab_DF.columns = np.hstack(["Label", mergemarkerlist])
    complete_tab_DF.columns = mergemarkerlist
    complete_tab_DF.to_csv(outfolder + "/FullObject_segmentation_data.csv")
    complete_tab = np.vstack(complete_tab)
    if (args.normalize):
        phenopgraphin = StandardScaler().fit_transform(complete_tab_DF.values[:, 1:])
    else:
        phenopgraphin = complete_tab_DF.values[:, 1:]
    TESTPATCHPREDO, graph, Q = phenograph.cluster(phenopgraphin, n_jobs=1, resolution_parameter=int(args.PGres),
                                                  k=int(args.PGnn), primary_metric=str(args.PGdis))
    to_values = TESTPATCHPREDO  # all values from 0 to 1000
    relabeled_table = copy.deepcopy(complete_tab)
    relabeled_table[:, 0] = to_values
    relabledimages = []
    relabledgreyimages = []
    PAL = generate_colormap(int(np.max(TESTPATCHPREDO) + 1) * 2)
    np.save(outfolder + "/" + "color.npy", PAL)
    PAL2 = PAL.flatten()
    PAL0 = np.zeros(768)
    PAL0[0:len(PAL2)] = PAL2
    count_lab = 0
    Slices_object = np.zeros((len(Qtab), int(np.max(TESTPATCHPREDO) + 1), len(mergemarkerlist) + 2))
    startindex = 0
    for imagelen in range(len(Qtab)):
        from_values = complete_tab_DF['ID'].values[startindex:startindex + len(Qtab[imagelen])]
        to_values = TESTPATCHPREDO[startindex:startindex + len(Qtab[imagelen])]
        relabeled = method_searchsort(from_values, to_values, expandobjects[imagelen].flatten().astype(int))
        startindex += len(Qtab[imagelen])
        relabledgreyimages.append(relabeled.reshape(expandobjects[imagelen].shape))
        cv.imwrite(outfolder + "/RELABELED_Grey" + str(imagelen) + ".png",
                   relabledgreyimages[imagelen][:, :].astype(np.uint8))
        imgp = PImage.fromarray(relabeled.reshape(expandobjects[0].shape).astype(np.uint8), mode='P')
        imgp.putpalette(list(PAL0.flatten().astype(int)))
        imgp.save(outfolder + "/RELABELED_" + str(imagelen) + ".png")
        relab = cv.imread(outfolder + "/RELABELED_" + str(imagelen) + ".png")
        relabledimages.append(np.asarray(relab))
        tmp_tab = relabeled_table[
                  count_lab:count_lab + len(Qtab[imagelen]) + len(np.unique(relabeled_table[:, 0]))]
        nclusters = len(Slices_object[0, :, ])
        nclusters = np.max(TESTPATCHPREDO) + 1
        tmp_tab[-nclusters:, 0] = np.arange(nclusters)
        tmp_tab_df = pd.DataFrame(tmp_tab)
        count_lab += len(Qtab[imagelen])
        grouped = tmp_tab_df.groupby(0)
        tabres = grouped.apply(np.mean)
        tabres.insert(0, "Sample", imagelen)
        unique, counts = np.unique(tmp_tab[:, 0], return_counts=True)
        tabres.insert(2, "Pixels", counts)
        StandardScaler().fit_transform(tabres.values[:, 3:])
        scaler = MinMaxScaler()
        scaler.fit(StandardScaler().fit_transform(tabres.values[:, 3:]))
        min_max_normdata = scaler.transform(StandardScaler().fit_transform(tabres.values[:, 3:]))
        # Cutoff the overflowing (>1) of values
        min_max_normdata[min_max_normdata > 1] = 1
        Slices_object[imagelen, :, :] = tabres.values
    my_data = pd.DataFrame(np.nan_to_num((np.vstack(Slices_object))))
    my_data.columns = np.hstack([["Sample", "Cluster", "Pixels"], mergemarkerlist[1:]])
    my_data.to_csv(outfolder + "/RAPIDObject_cluster_table.csv")
    tabledata, my_data_scaled, DistMatrix, uniqueClusters = \
        prep_for_mst(clustertable=my_data, minnumpixels=1, outfolder=outfolder, includedmarkers=mergemarkerlist)
    final = my_data_scaled.columns
    generate_mst(distancematrix=DistMatrix, normalizeddf=my_data_scaled[final], colors=PAL, randomseed=0,
                 outfolder=outfolder, clusterheatmap=True, displaymarkers=mergemarkerlist,
                 uniqueclusters=uniqueClusters, samplenames=list(np.unique(my_data['Sample'])), displaysingle=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='RAPID: deep learning algorithm for quantitative analysis of cell type and distribution from high content imaging data')
    parser.add_argument('--membranechannel', type=str, default=500, metavar='N',
                        help="memebrane channels to be merged, each marker must be separtetd by comma [,]  (default: %(default)s)")
    parser.add_argument('--imagepath', type=str, metavar='LR',
                        help="Path to the tiff file")
    parser.add_argument('--maskpath', type=str, metavar='LR',
                        help="Path to the png file")
    parser.add_argument('--outfolder', type=str, default="/tmp/output",
                        help="Output folder path (default: %(default)s)")
    parser.add_argument('--gaussianblur', type=bool, default=False, metavar='S',
                        help="Gaussian smothing of the image (default: %(default)s)")
    parser.add_argument('--medianblur', type=bool, default=False, metavar='N',
                        help=" median filter on the input image  (default: %(default)s)")
    parser.add_argument('--PGnn', type=int, default=30, metavar='N',
                        help=" number of nn for phenograph  (default: %(default)s)")
    parser.add_argument('--PGres', type=int, default=1, metavar='N',
                        help=" Phenograph resolution  (default: %(default)s)")
    parser.add_argument('--PGdis', type=str, default="euclidean", metavar='N',
                        help=" median filter on the input image  (default: %(default)s)")
    parser.add_argument('--selectzslice', type=int, default=True, metavar='N',
                        help="number of Z slice to use if multiple z present in the image, else, set to Nome (default: %(default)s)")
    parser.add_argument('--markernames', type=str, default=True, metavar='N',
                        help="marker names for the input tiff image, each marker must be separtetd by comma [,] (default: %(default)s)")
    parser.add_argument('--normalize', action='store_true', default=True,
                        help="***Run downstream analysis (default: %(default)s)")

    args = parser.parse_args()
    objseg = obejctsegmentation()

    # image = rio.readimage(args.PATH)
    # image = np.moveaxis(image, 0, 2)
    # print(image.shape)
    # channels = [0, 3, 4, 6, 7]
    # membranechannel =np.array(args.membranechannel.split(','),dtype=int)

    # markernames = np.array(args.markernames.split(','), dtype=str)
    markernames = list(np.array(args.markernames.split(','), dtype=str))
    print(markernames)
    markernames.append("Area")
    markernames.append("Eccentricity")
    markernames.append("Perimeter")
    markernames.append("Major_axis_length")
    membranechannel = markernames

    for arg in vars(args):
        print(str(arg) + "=" + str(getattr(args, arg)))

    # image = rio.readimage(args.IMAGEPATH)
    tablelist = []
    expandobjectlist = []
    for image in (glob.glob(args.imagepath + ".tif")):
        Name = os.path.split(image)[-1][0:-4]
        maskpath = args.maskpath + "/" + Name + '.npy'
        maskimage = np.load(maskpath)[:, :, 0]
        # maskimage=cv.imread(maskpath,-1)
        table, rapidobjects, expandobject, object2rgb = objseg.run_object_prediction_from_mask(image=args.imagepath,
                                                                                               membranechannel=membranechannel,
                                                                                               outfolder=args.outfolder,
                                                                                               gaussianblur=args.gaussianblur,
                                                                                               medianblur=args.medianblur,
                                                                                               selectzslice=args.selectzslice,
                                                                                               marker_list=markernames,
                                                                                               maskimage=maskimage)
        tablelist.append(table.values)
        expandobjectlist.append(expandobject)
    # table.to_csv(args.outfolder+"/table.csv")
    runphenograph(tablelist, table.columns, expandobjectlist, args.outfolder, args)
