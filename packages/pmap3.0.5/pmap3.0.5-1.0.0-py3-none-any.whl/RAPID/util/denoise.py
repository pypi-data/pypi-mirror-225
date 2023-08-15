import torch.nn.functional as F
import os
import torch
import torch.nn as nn
import numpy as np
import tifffile
import copy
import argparse


'''
class DoubleConv(nn.Module):
    """
    Convolution block consisting of (convolution => [BN] => ReLU) * 2

    Args:
        in_channels (int): Number of channels input to the convolution.
        out_channels (int): Number of output channels for the convolution.
    """

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
    """
    Maxpool downscaling followed by a double convolution block.

    Args:
        in_channels (int): Number of channels input to the convolution.
        out_channels (int): Number of output channels for the convolution.
    """

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)


class Up(nn.Module):
    """
    Upscaling followed by a double convolution block.

    Args:
        in_channels (int): Number of channels input to the convolution.
        out_channels (int): Number of output channels for the convolution.
        bilinear (bool, optional): If True, use the normal convolutions to reduce the number of channels (Default: True).
    """

    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()

        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        else:
            self.up = nn.ConvTranspose2d(in_channels // 2, in_channels // 2, kernel_size=2, stride=2)

        self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        # input is CHW
        diffY = torch.tensor([x2.size()[2] - x1.size()[2]])
        diffX = torch.tensor([x2.size()[3] - x1.size()[3]])

        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        # if you have padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class OutConv(nn.Module):
    """
    1x1 convolution.

    Args:
        in_channels (int): Number of channels input to the convolution.
        out_channels (int): Number of output channels for the convolution.
    """

    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        # return torch.sigmoid(self.conv(x))
        return self.conv(x)


class UNet(nn.Module):
    """
    Define the overall architecture of the neural network.

    Args:
        in_channels (int, optional): Number of channels input to the convolution (Default: 2).
        n_classes (int, optional): Number of output channels from the network (Default: 2).
        bilinear (bool, optional): If True, use the normal convolutions to reduce the number of channels (Default: True).
    """
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
'''


class UNetBlock(nn.Module):
    """
    Define the architecture of a block of the neural network.

    Args:
        inchans (int): Number of channels input to the block.
        intermediatechans (int): Number of channels output from the first convolution of the block.
        outchans (int): Number of channels output from the block.
    """

    def __init__(self, inchans, intermediatechans, outchans):
        super(UNetBlock, self).__init__()
        self.act = nn.ReLU(inplace=True)
        self.conv = nn.Conv2d(inchans, intermediatechans, kernel_size=3, padding=1, bias=True)
        self.bn = nn.BatchNorm2d(intermediatechans)
        self.conv2 = nn.Conv2d(intermediatechans, outchans, kernel_size=3, padding=1, bias=True)
        self.bn2 = nn.BatchNorm2d(outchans)

    def forward(self, x):
        x = self.conv(x)
        x = self.act(x)
        x = self.bn(x)
        x = self.conv2(x)
        x = self.act(x)
        blockout = self.bn2(x)
        return blockout


class UNet(nn.Module):
    """
    Define the overall architecture of the neural network.

    Args:
        inchans (int): Number of channels input to the network.
        outchans (int): Number of output channels from the network.
    """

    def __init__(self, inchans=1, outchans=2):
        super(UNet, self).__init__()
        incount = 64
        ncount = [incount, incount * 2, incount * 4, incount * 8, incount * 16]
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.block00 = UNetBlock(inchans, ncount[0], ncount[0])
        self.block10 = UNetBlock(ncount[0], ncount[1], ncount[1])
        self.block20 = UNetBlock(ncount[1], ncount[2], ncount[2])
        self.block30 = UNetBlock(ncount[2], ncount[3], ncount[3])
        self.block40 = UNetBlock(ncount[3], ncount[4], ncount[4])
        self.block01 = UNetBlock(ncount[0] + ncount[1], ncount[0], ncount[0])
        self.block11 = UNetBlock(ncount[1] + ncount[2], ncount[1], ncount[1])
        self.block21 = UNetBlock(ncount[2] + ncount[3], ncount[2], ncount[2])
        self.block31 = UNetBlock(ncount[3] + ncount[4], ncount[3], ncount[3])
        self.block02 = UNetBlock(ncount[0] * 2 + ncount[1], ncount[0], ncount[0])
        self.block12 = UNetBlock(ncount[1] * 2 + ncount[2], ncount[1], ncount[1])
        self.block22 = UNetBlock(ncount[2] * 2 + ncount[3], ncount[2], ncount[2])
        self.block03 = UNetBlock(ncount[0] * 3 + ncount[1], ncount[0], ncount[0])
        self.block13 = UNetBlock(ncount[1] * 3 + ncount[2], ncount[1], ncount[1])
        self.block04 = UNetBlock(ncount[0] * 4 + ncount[1], ncount[0], ncount[0])
        self.final = nn.Conv2d(ncount[0], outchans, kernel_size=1)

    def forward(self, x):
        lout00 = self.block00(x)
        lout10 = self.block10(self.pool(lout00))
        lout01 = self.block01(torch.cat([lout00, self.upsample(lout10)], 1))
        lout20 = self.block20(self.pool(lout10))
        lout11 = self.block11(torch.cat([lout10, self.upsample(lout20)], 1))
        lout02 = self.block02(torch.cat([lout00, lout01, self.upsample(lout11)], 1))
        lout30 = self.block30(self.pool(lout20))
        lout21 = self.block21(torch.cat([lout20, self.upsample(lout30)], 1))
        lout12 = self.block12(torch.cat([lout10, lout11, self.upsample(lout21)], 1))
        lout03 = self.block03(torch.cat([lout00, lout01, lout02, self.upsample(lout12)], 1))
        lout40 = self.block40(self.pool(lout30))
        lout31 = self.block31(torch.cat([lout30, self.upsample(lout40)], 1))
        lout22 = self.block22(torch.cat([lout20, lout21, self.upsample(lout31)], 1))
        lout13 = self.block13(torch.cat([lout10, lout11, lout12, self.upsample(lout22)], 1))
        lout04 = self.block04(torch.cat([lout00, lout01, lout02, lout03, self.upsample(lout13)], 1))
        output = self.final(lout04)
        return output


def check_padding(image, ps):
    """
    Adds padding to the bottom and right edges of the image so that it may be divided evenly into patches of a specified dimension.

    Args:
        image (numpy.ndarray): Image array to be padded.
        ps (int): Specified patch size. Padded image dimensions will be integer multiples of this value.

    :return: paddedimg *(numpy.ndarray)*: \n
        Input image with padding added along the edges.
    """
    numcols = int(image.shape[1] / ps)
    numrows = int(image.shape[0] / ps)
    if not ((numrows * ps) >= image.shape[0]):
        numrows += 1
    if not ((numcols * ps) >= image.shape[1]):
        numcols += 1
    paddedimg = np.zeros((ps * numrows, ps * numcols))
    paddedimg[0:image.shape[0], 0:image.shape[1]] = image
    return paddedimg


def make_patches(image, ps):
    """
    Split an image array into square patches.

    Args:
        image (numpy.ndarray): Image array being split into patches.
        ps (int): Size of the patches the image will be split into.

    :return: tmpimages *(numpy.ndarray)*: \n
        Array of patches extracted from input array.
    """
    tmpimages = np.zeros((int(image.shape[0] / ps) * int(image.shape[1] / ps), ps, ps))
    patchcount = 0
    for i in range(0, image.shape[0], ps):
        for j in range(0, image.shape[1], ps):
            tmpimages[patchcount, :, :] = image[i:i + ps, j:j + ps]
            patchcount += 1
    return tmpimages


def club_patches(image, shape):
    """
    Collate an array of patches back into a single full image array.

    Args:
        image (numpy.ndarray): Array of patches to be collated.
        shape (numpy.ndarray): Shape of the output image.

    :return: collatedimg *(numpy.ndarray)*: \n
        Image with patches collated together.
    """
    ps = image.shape[2]
    collatedimg = np.zeros(shape, dtype=image.dtype)
    patchcount = 0
    for row in range(int(shape[0] / ps)):
        for col in range(int(shape[1] / ps)):
            collatedimg[row * ps: row * ps + ps, col * ps: col * ps + ps] = image[patchcount, 1, :, :]
            patchcount += 1
    return collatedimg


def predict_mask(model, image, bs):
    """
    Apply a pretrained model on an image.

    Args:
        model (model): Pretrained torch nn model.
        image (numpy.ndarray): Image array that the pretrained model will be applied to.
        bs (int): Number of patches being passed through the retrained network together.

    :return: features *(numpy.ndarray)*: \n
        Resulting image array from passing input image through the pretrained model.
    """
    modimage = check_padding(image, 256)
    patches = make_patches(modimage, 256)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.eval()
    result = np.zeros((len(patches), 2, patches.shape[1], patches.shape[2]))
    with torch.no_grad():
        for i in range(0, len(result), bs):
            result[i:i + bs, :, :, :] = F.softmax(
                model(torch.unsqueeze(torch.from_numpy(patches[i:i + bs, :, :]), 1).float().to(device)).to(device),
                dim=1).cpu().numpy()
    # features = emptyresult#[:,0,:,:]
    features = club_patches(result, modimage.shape)[0:image.shape[0], 0:image.shape[1]]
    return features


def load_denoise_model():
    """
    Load the pretrained denoising model included in the RAPID package.

    :return: model *(torch.nn.Module)*: \n
        Pretrained denoising neural network model.
    """
    rootfolder = os.path.dirname(os.path.abspath(__file__))
    # denoisemodelpath =rootfolder+"/..//models/Model3_2Class24.pt"
    denoisemodelpath = rootfolder + "/..//models/ModelDenoise_UnetPlus40.pt"
    # denoisemodelpath =rootfolder+"/..//models/ModelX_UnetPlus9.pt"
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = UNet()
    print(model)
    if (str(device) == "cpu"):
        model.load_state_dict(torch.load(denoisemodelpath, map_location=torch.device('cpu')))
    else:
        model.load_state_dict(torch.load(denoisemodelpath))
    model = model.to(device)
    return model


def run_denoise():
    """
    Execute the denoising algorithm on the indicated dataset(s).
    """
    parser = argparse.ArgumentParser(description='RAPIDD: denoise the image based on trained model')
    parser.add_argument('--IN', type=str, default=None, help="input tifffile file path ")
    parser.add_argument('--OUT', type=str, default=None, help='denoised output tifffile file path ')
    parser.add_argument('--ch', type=str, default=None, help='channel indicies(int) separated by ","  to denoise')
    args = parser.parse_args()
    IN = args.IN
    OUT = args.OUT

    image = tifffile.imread(IN)
    if args.ch is None:
        CH = range(0, image.shape[0])
    else:
        CH = np.array(args.ch.split(','))
    model = load_denoise_model()
    emptytiff = copy.deepcopy(image)
    for i in CH:
        print("Denoising channel " + str(i) + "..")
        results = predict_mask(model, image[i, :, :], 10)
        emptytiff[i, :, :] = results[0:image.shape[1], 0:image.shape[2]]
    emptytiff[emptytiff > 0.5] = 1
    emptytiff[emptytiff <= 0.5] = 0
    cleantiff = image * emptytiff
    tifffile.imwrite(OUT, cleantiff.astype(np.uint8))


if __name__ == "__main__":
    run_denoise()
