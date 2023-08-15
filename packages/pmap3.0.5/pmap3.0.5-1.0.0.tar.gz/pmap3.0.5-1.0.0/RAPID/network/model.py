import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from math import floor
import copy


### TODO: Documentation
class Conv1DLayer(nn.Module):
    def __init__(self, inchannel, outchannel, k, s, p):
        super(Conv1DLayer, self).__init__()
        self.conv1d = nn.Conv1d(inchannel, outchannel, k, s, p)
        self.bnconv1d = nn.BatchNorm1d(outchannel)

    def forward(self, xx):
        return self.bnconv1d(F.relu(self.conv1d(xx)))


### TODO: Documentation
class RAPIDFCNet(nn.Module):
    def __init__(self, dimension=None, nummodules=5, numclusters=30, mse=False):
        self.AF = "relu"

        super(RAPIDFCNet, self).__init__()
        self.conv1 = nn.Linear(dimension, 256, bias=True)
        self.bn1 = nn.BatchNorm1d(256)
        self.mse = mse
        self.conv2 = nn.Linear(256, 256, bias=True)
        self.bn2 = nn.BatchNorm1d(256)
        self.conv3 = nn.Linear(256 + dimension, 256, bias=True)
        self.bn3 = nn.BatchNorm1d(256)
        self.conv3_01 = nn.Linear(256 + dimension, 256, bias=True)
        self.bn3_01 = nn.BatchNorm1d(256)
        self.conv3_02 = nn.Linear(256 + dimension, 128, bias=True)
        self.bn3_02 = nn.BatchNorm1d(128)
        self.conv4 = nn.Linear(128 + dimension, 128, bias=True)
        self.bn4 = nn.BatchNorm1d(128)
        self.conv4_01 = nn.Linear(128 + dimension, 128, bias=True)
        self.bn4_01 = nn.BatchNorm1d(128)
        self.conv4_02 = nn.Linear(128 + dimension, 128, bias=True)
        self.bn4_02 = nn.BatchNorm1d(128)
        self.conv5 = nn.Linear(128 + dimension, 256, bias=True)
        self.bn5 = nn.BatchNorm1d(256)
        self.fc1 = nn.Linear(256, 512, bias=True)
        self.bn_fc = nn.BatchNorm1d(512)
        self.fc2 = nn.ModuleList([nn.Linear(512, numclusters) for _ in range(nummodules)])
        self.fc2_alt = nn.ModuleList([nn.Linear(512, int(numclusters + (numclusters / 3))) for _ in range(nummodules)])
        self.fc2_alt_2 = nn.ModuleList([nn.Linear(512, int(numclusters + (numclusters / 2))) for _ in range(nummodules)])
        self.fc2_alt_3 = nn.ModuleList([nn.Linear(512, int(numclusters + (numclusters / 1))) for _ in range(nummodules)])
        if mse:
            self.Dfc5L = nn.Linear(512, 256, bias=True)
            self.Dbn_5L = nn.BatchNorm1d(256)
            self.DfcFL = nn.Linear(256, 256, bias=True)
            self.Dbn_fcFL = nn.BatchNorm1d(256)
            self.DfcTL = nn.Linear(256, 256, bias=True)
            self.Dbn_fcTL = nn.BatchNorm1d(256)
            self.DfcSL1 = nn.Linear(256, 256, bias=True)
            self.Dbn_fcSL = nn.BatchNorm1d(256)
            self.DfFin = nn.Linear(256, numclusters, bias=True)

    def forward(self, xx):
        x = self.bn1(F.relu(self.conv1(xx)))
        x = self.bn2(F.relu(self.conv2(x)))
        x = torch.cat([x, xx], 1)
        x = self.bn3(F.relu(self.conv3(x)))
        x = torch.cat([x, xx], 1)
        x = self.bn3_02(F.relu(self.conv3_02(x)))
        x = torch.cat([x, xx], 1)
        x = self.bn4(F.relu(self.conv4(x)))
        x = torch.cat([x, xx], 1)
        x = self.bn5(F.relu(self.conv5(x)))
        ff = x.view(x.size(0), -1)
        x_prefinal = self.bn_fc(F.relu(self.fc1(ff)))
        ff = [F.softmax(fc(x_prefinal), dim=1) for fc in self.fc2]
        ff_alt = [F.softmax(fc2(x_prefinal), dim=1) for fc2 in self.fc2_alt]
        ff_alt_2 = [F.softmax(fc3(x_prefinal), dim=1) for fc3 in self.fc2_alt_2]
        ff_alt_3 = [F.softmax(fc4(x_prefinal), dim=1) for fc4 in self.fc2_alt_3]
        if self.mse:
            x = self.Dbn_5L(F.relu(self.Dfc5L(x_prefinal)))
            x = self.DfcFL(F.relu(self.DfcFL(x)))
            x = self.Dbn_fcTL(F.relu(self.DfcTL(x)))
            x = self.Dbn_fcSL(F.relu(self.Dbn_fcSL(x)))
            x = self.DfFin(x)
            return ff, ff_alt, x, ff_alt_2, ff_alt_3
        else:
            return ff, ff_alt, ff, ff_alt_2, ff_alt_3


### TODO: Documentation
class RAPIDMixNet(nn.Module):
    def __init__(self, dimension=None, nummodules=5, mse=False, numclusters=None):
        super(RAPIDMixNet, self).__init__()
        outdim = copy.deepcopy(dimension)
        self.rapmodule1 = RAPIDModule(1, 128)
        self.rapmodule3 = RAPIDModule(128 * 4, 64)
        self.outdim = 64 * 4
        self.modlist = nn.ModuleList()
        self.mse = mse
        while dimension > 3:
            dimension, k, s, p = single_layer_dim(dim=dimension)
            print(dimension, " ", k, " ", s, " ", p)
            self.modlist.append(Conv1DLayer(self.outdim, 256, k, s, p))
            self.outdim = 256
        self.finconv1d = nn.Conv1d(256, 256, 3, 1, 0)
        outsize = 256
        self.fc3 = nn.Linear(outsize, 512, bias=True)
        self.bn3 = nn.BatchNorm1d(512)
        self.dropout1 = nn.Dropout(p=0.2)
        self.fcout = nn.ModuleList([nn.Linear(512, numclusters) for _ in range(nummodules)])
        if mse:
            self.Dfc5L = nn.Linear(512, 256, bias=True)
            self.Dbn_5L = nn.BatchNorm1d(256)
            self.DfcFL = nn.Linear(256, 256, bias=True)
            self.Dbn_fcFL = nn.BatchNorm1d(256)
            self.DfcTL = nn.Linear(256, 256, bias=True)
            self.Dbn_fcTL = nn.BatchNorm1d(256)
            self.DfcSL1 = nn.Linear(256, 256, bias=True)
            self.Dbn_fcSL = nn.BatchNorm1d(256)
            self.DfFin = nn.Linear(256, outdim, bias=True)

    def forward(self, xx):
        x1dc = self.rapmodule1(xx)
        x1dc = self.rapmodule3(x1dc)
        for layer in self.modlist:
            x1dc = layer(x1dc)
        x1dc = self.finconv1d(x1dc)
        fc = x1dc.view(x1dc.size(0), -1)
        X = self.bn3(F.relu(self.fc3(fc)))

        x_prefinal = self.dropout1(X)
        ff = [F.softmax(fc(x_prefinal), dim=1) for fc in self.fcout]
        if self.mse:
            x = self.Dbn_5L(F.relu(self.Dfc5L(x_prefinal)))
            x = self.DfcFL(F.relu(self.DfcFL(x)))
            x = self.Dbn_fcTL(F.relu(self.DfcTL(x)))
            x = self.Dbn_fcSL(F.relu(self.Dbn_fcSL(x)))
            x = self.DfFin(x)
            return ff, x
        else:
            return ff, ff


### TODO: Documentation
class RAPIDResnet(nn.Module):
    def __init__(self, dimension=None, numclusters=50, nummodules=5):
        super(RAPIDResnet, self).__init__()
        self.conv1 = nn.Linear(dimension, 512, bias=True)
        self.bn1 = nn.BatchNorm1d(512)
        self.ll0 = nn.Linear(512, 256, bias=True)
        self.bnll0 = nn.BatchNorm1d(256)
        self.res1 = ResidualBlock(256, 256)
        self.res2 = ResidualBlock(256, 256)
        self.res3 = ResidualBlock(256, 256)

        self.ll = nn.Linear(256 + dimension, 128, bias=True)
        self.bnll = nn.BatchNorm1d(128)
        self.res4 = ResidualBlock(128, 128)
        self.res5 = ResidualBlock(128, 128)
        self.res6 = ResidualBlock(128, 128)
        self.fc1 = nn.Linear(128 + dimension, 512, bias=True)
        self.bn_fc = nn.BatchNorm1d(512)
        self.fc2 = nn.ModuleList([nn.Linear(512, numclusters) for _ in range(nummodules)])

    def forward(self, xx):
        x = self.bn1(F.relu(self.conv1(xx)))
        x = self.bnll0(F.relu(self.ll0(x)))
        x = self.res1(x)
        x = self.res2(x)
        x = self.res3(x)
        x = self.bnll(F.relu(self.ll(torch.cat([x, xx], 1))))
        x = self.res4(x)
        x = self.res5(x)
        x = self.res6(x)
        ff = x.view(x.size(0), -1)
        x_prefinal = self.bn_fc(F.relu(self.fc1(torch.cat([ff, xx], 1))))
        ff = [F.softmax(fc(x_prefinal), dim=1) for fc in self.fc2]
        return ff, ff  # x  # ,x# ff_alt#,X


### TODO: Documentation
class RAPIDModule(nn.Module):
    def __init__(self, inchannels, outchannels):
        super(RAPIDModule, self).__init__()
        self.rapmodule = []
        self.conv1d = nn.Conv1d(inchannels, outchannels, 3, 1, 1)  # x,128,9
        self.bnconv1d = nn.BatchNorm1d(outchannels)
        self.conv1d_2s = nn.Conv1d(inchannels, outchannels, 5, 1, 2)  # x,128,9
        self.bnconv1d_2s = nn.BatchNorm1d(outchannels)
        self.conv1d_1s2d = nn.Conv1d(inchannels, outchannels, 3, stride=1, padding=2, dilation=2)  # x,128,9
        self.bnconv1d_1s2d = nn.BatchNorm1d(outchannels)
        self.conv1d_1s3d = nn.Conv1d(inchannels, outchannels, 3, stride=1, padding=3, dilation=3)  # x,128,9
        self.bnconv1d_1s3d = nn.BatchNorm1d(outchannels)

    def forward(self, xx):
        c1d_0 = self.bnconv1d(F.relu(self.conv1d(xx)))
        c1d_1 = self.bnconv1d_2s(F.relu(self.conv1d_2s(xx)))
        c1d_2 = self.bnconv1d_1s2d(F.relu(self.conv1d_1s2d(xx)))
        c1d_3 = self.bnconv1d_1s3d(F.relu(self.conv1d_1s3d(xx)))
        return torch.cat([c1d_0, c1d_1, c1d_2, c1d_3], 1)


### TODO: Documentation
class ResidualBlock(nn.Module):
    def __init__(self, inchannels, outchannels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Linear(inchannels, outchannels)
        self.relu = nn.ReLU(inplace=True)
        self.bn1 = nn.BatchNorm1d(outchannels)
        self.dropout1 = nn.Dropout(p=0.3)
        self.conv2 = nn.Linear(outchannels, outchannels)
        self.relu = nn.ReLU(inplace=True)
        self.bn2 = nn.BatchNorm1d(outchannels)
        self.dropout2 = nn.Dropout(p=0.3)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.relu(out)
        out = self.bn1(out)
        out = self.dropout1(out)
        out = self.conv2(out)
        out = F.relu(out)
        out = self.bn2(out)
        out = self.dropout2(out)
        out += residual
        return out


### TODO: Documentation
def load_checkpoint(filepath, model, optimizer):
    checkpoint = torch.load(filepath)
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    return model


### TODO: Documentation
def single_layer_dim(dim):
    if dim == 1:
        p = 1
        s = 1
        k = 3
    elif dim == 2:
        p = 1
        s = 1
        k = 2
    elif dim == 3:
        p = 1
        s = 1
        k = 3
        dim = 3
    elif dim == 4:
        p = 1
        s = 1
        k = 4
        dim = 3
    elif dim == 5:
        p = 0
        s = 1
        k = 3
    elif dim % 2 == 0:
        p = 0
        s = 1
        k = 4
    else:
        p = 1
        s = 2
        k = 3
    print(dim, " ", k, " ", s, " ", p)
    newdim = floor(((dim + (2 * p) - (k - 1) - 1) / s) + 1)
    return newdim, k, s, p


### TODO: Documentation
def weight_init(m):
    if isinstance(m, nn.Conv1d):
        init.normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.Conv2d):
        init.xavier_normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.Conv3d):
        init.xavier_normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.ConvTranspose1d):
        init.normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.ConvTranspose2d):
        init.xavier_normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.ConvTranspose3d):
        init.xavier_normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.BatchNorm1d):
        init.normal_(m.weight.data, mean=1, std=0.02)
        init.constant_(m.bias.data, 0)
    elif isinstance(m, nn.BatchNorm2d):
        init.normal_(m.weight.data, mean=1, std=0.02)
        init.constant_(m.bias.data, 0)
    elif isinstance(m, nn.BatchNorm3d):
        init.normal_(m.weight.data, mean=1, std=0.02)
        init.constant_(m.bias.data, 0)
    elif isinstance(m, nn.Linear):
        # init.xavier_normal_(m.weight.data)
        init.kaiming_uniform_(m.weight.data, mode='fan_in', nonlinearity='relu')
        init.normal_(m.bias.data)
    elif isinstance(m, nn.LSTM):
        for param in m.parameters():
            if len(param.shape) >= 2:
                init.orthogonal_(param.data)
            else:
                init.normal_(param.data)
    elif isinstance(m, nn.LSTMCell):
        for param in m.parameters():
            if len(param.shape) >= 2:
                init.orthogonal_(param.data)
            else:
                init.normal_(param.data)
    elif isinstance(m, nn.GRU):
        for param in m.parameters():
            if len(param.shape) >= 2:
                init.orthogonal_(param.data)
            else:
                init.normal_(param.data)
    elif isinstance(m, nn.GRUCell):
        for param in m.parameters():
            if len(param.shape) >= 2:
                init.orthogonal_(param.data)
            else:
                init.normal_(param.data)