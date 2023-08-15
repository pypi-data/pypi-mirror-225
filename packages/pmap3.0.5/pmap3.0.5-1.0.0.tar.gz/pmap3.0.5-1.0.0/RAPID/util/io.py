import copy
import os
import numpy as np
import pandas as pd
import tifffile
import zarr
from RAPID.util.utils import preprocess, save_preprocess, load_preprocess
import vaex
import vaex.ml
import shutil


def read_ome(filepath, z=None, t=None, chorder="zcxy"):
    """
    Read tiff files of various dimensions from the specified path.

    Args:
        filepath (str): File path of the input tiff file.
        z (int, optional): z slice to consider for analysis (Default: None).
        t (int, optional): Time slice to consider for analysis (Default: None).
        chorder (str, optional): Order of the channels (options: 'z', 'c', 't', 'x', 'y').

    :return: image *(numpy.ndarray)*: \n
        Image array from specified path.
    :return: ndim *(int)*: \n
        Number of dimensions in the image.
    """

    image = tifffile.imread(filepath)
    ndim = len(image.shape)
    # check if data is 4D (z, c, x, y), if 4D generate patches from each z slice
    if ndim == 4 and chorder == "czxy":
        image = np.moveaxis(image, 0, -1)
    elif ndim == 4 and chorder == "zcxy":
        image = np.moveaxis(image, 1, -1)
    # check if data is 5D (time, z, c, x, y), if 5D generate patches from each z/time slice
    elif ndim == 5:
        image = np.moveaxis(image, 1, -1)
        if z is not None:
            image = image[:, z, :, :, :]
        if t is not None:
            image = image[t, :, :, :]
    elif ndim == 3:
        image = np.moveaxis(image, 0, -1)
    else:
        raise ValueError(
            'image with shape %s is not compatible the rapid analysis, atleast it need to be 3 dimensional.' % (
                len(image.shape)))
    return image, ndim

### TODO: Submean is not used
def tiff_to_zarr(file_list, zarrpath, gaussianblur=False, gaussianblurstd=None, medianblur=False, normalize=False,
                 normtype=None, ndims=None, deletechannel=1000, normalizeacross=False, markernames=None, args=None,
                 pretrained=None, submean=True):
    """
    Read tiff file from the specified path and save as a zarr file. Zarr allows data to be stored in a Hierarchical Data
    Formats (hdf_) similar to hdf5. This format allows compression, which drastically reduces the memory usage.
    Specified zarr data chunks are read into memory.

    .. _hdf: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjpnMSNuvrqAhXLl3IEHU2cBZAQFjAAegQIEhAB&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FHierarchical_Data_Format&usg=AOvVaw0QsPeyiGcTrwVX_tppfXFf

    Args:
        file_list (list): List of tiff file paths.
        zarrpath (str): Output file path for zarr files.
        gaussianblur (bool, optional): If true, apply a gaussian blur on the input images (Default: False).
        gaussianblurstd (float, optional): Standard deviation to use for gaussian blur (Default: None).
        medianblur (bool, optional): If true, apply median blur on the input images (Default: True).
        normalize (bool, optional): If true, apply normalization (Default: False).
        normtype (str, optional): Normalization algorithm to use on the image. Options include 'zscore', 'log10', 'log2', 'inverse', 'sqrt' (Default: None).
        ndims (int, optional): Number of cell markers in the image (Default: None).
        deletechannel (list, optional): List of channels to delete (Default: 1000).
        normalizeacross (bool, optional): If true, apply zscore normalization across samples (Default: False).
        markernames (str, optional): Marker names separated by ',' (Default: None).
        args (argparse.ArgumentParser, optional): Stores arguments that are used to define properties of the network (Default: None).
        pretrained (str, optional): Pretrained vaex model path (Default: None).

    :return: imglist *(list)*: \n
        List of image file paths.
    :return: imgshapes *(numpy.ndarray)*: \n
        Shapes of each of the input files.
    :return: args *(argparse.ArgumentParser, optional)*: \n
        Stores arguments that are used to define properties of the network (Default: None).
    """

    trainmarkernums = [i for i in range(len(markernames[0]))]
    if not deletechannel.any() == 1000:
        removechannels = copy.deepcopy(deletechannel).tolist()
        removechannels.sort(reverse=True)
        for marker in removechannels:
            trainmarkernums.pop(marker)

    if zarrpath:
        fh = zarr.open(zarrpath, mode='w')
    else:
        exit("Please provide the path for zarr file")

    imgshapes = np.zeros((len(file_list), 3))

    totalpixel = 0
    for file in file_list:
        isize = tifffile.imread(file).shape
        if len(isize) > 3:
            totalpixel += int(np.prod(isize[0:3]) / isize[1])
        else:
            totalpixel += int(np.prod(isize[1:]))

    fhd = fh.create_dataset('data_normalized', shape=(totalpixel, len(trainmarkernums)), dtype='f8')
    if read_ome(file_list[0])[0].dtype == 'uint16':
        fhdr = fh.create_dataset('data', shape=(totalpixel, len(trainmarkernums)), dtype='uint16')
    else:
        fhdr = fh.create_dataset('data', shape=(totalpixel, len(trainmarkernums)), dtype='uint8')
    fh.attrs['markers'] = markernames[0]
    trainmarkernums = [i for i in range(len(markernames[0]))]
    fh.create_dataset('minmax', data=np.ones(len(trainmarkernums)) * 255, dtype='f8')
    lastindex = 0
    imglist = []
    flipimg = []
    imgslist = []
    imgind = 0
    for file in range(len(file_list)):
        print("Reading image '" + str(imgind) + ".." + file_list[file] + "'...")
        imgind += 1
        readslice, ndim = read_ome(file_list[file])
        readslice[:10, :10, :] = 0
        print(readslice.shape)
        if ndim > 3:
            imgshapes = np.zeros((readslice.shape[0], 3))
            for zch in range(readslice.shape[0]):
                imglist.append(os.path.split(file_list[file])[-1].split(".")[0] + "_" + str(zch))
                flipimg.append(readslice.shape[1] > readslice.shape[2])
                print(zch)
                imgslist.append(copy.deepcopy(readslice[zch, :, :, :]))
                if not deletechannel.any() == 1000:
                    readslice_z = np.delete(readslice[zch, :, :, :], deletechannel, axis=-1)
                else:
                    readslice_z = readslice[zch, :, :, :]
                print(readslice_z.shape)
                num_of_dims = len(readslice.shape[1:])
                fhd[lastindex: lastindex + readslice_z.shape[0] * readslice_z.shape[1], :] = readslice_z.reshape((-1, readslice_z.shape[2]))
                fhdr[lastindex: lastindex + readslice_z.shape[0] * readslice_z.shape[1], :] = readslice_z.reshape(
                    (-1, readslice_z.shape[2]))
                readslice_z = preprocess(zarrpath, medianblur=medianblur, gaussianblur=gaussianblur,
                                         gaussianblurstd=gaussianblurstd, img=readslice_z, normtype=normtype,
                                         normalize_first=False)
                if not normalizeacross and normalize:
                    fhd[lastindex: lastindex + readslice.shape[0] * readslice_z.shape[1], :] = readslice_z.reshape((-1, readslice_z.shape[2]))
                lastindex = lastindex + readslice_z.shape[0] * readslice_z.shape[1]

                if flipimg[-1]:
                    imgshapes[zch, :] = readslice_z.shape[1, 0, 2]
                else:
                    imgshapes[zch, :] = readslice_z.shape

                if not os.path.exists(os.path.join(zarrpath, "hdf5_files")):
                    os.mkdir(os.path.join(zarrpath, "hdf5_files"))
                vaex.from_pandas(pd.DataFrame(readslice_z.astype('float32').reshape((-1, readslice_z.shape[2]))).astype(
                    'float32')).export_hdf5(zarrpath + (f'/hdf5_files/analysis_{zch:04}.hdf5'))
                del readslice_z
        else:
            imglist.append(os.path.split(file_list[file])[-1].split(".tif")[0])
            flipimg.append(readslice.shape[0] > readslice.shape[1])
            imgslist.append(copy.deepcopy(readslice))
            if not deletechannel.any() == 1000:
                readslice = np.delete(readslice, deletechannel, axis=-1)
            if file == 0:
                num_of_dims = len(readslice.shape)
            else:
                if (num_of_dims != len(readslice.shape)):
                    raise ValueError('sample image dimensions %d are different from expected %d dimensions  .' % (
                        len(readslice.shape), num_of_dims))
            fhd[lastindex: lastindex + readslice.shape[0] * readslice.shape[1], :] = readslice.reshape((-1, readslice.shape[2]))
            fhdr[lastindex: lastindex + readslice.shape[0] * readslice.shape[1], :] = readslice.reshape((-1, readslice.shape[2]))
            readslice = preprocess(zarrpath, medianblur=medianblur, gaussianblur=gaussianblur,
                                   gaussianblurstd=gaussianblurstd, img=readslice, normtype=normtype,
                                   normalize_first=False, submean=args.submean, medianblursize=3)
            if (not normalizeacross) & (normalize):
                fhd[lastindex: lastindex + readslice.shape[0] * readslice.shape[1], :] = readslice.reshape((-1, readslice.shape[2]))
            lastindex = lastindex + readslice.shape[0] * readslice.shape[1]

            if flipimg[-1]:
                imgshapes[file, :] = readslice.shape[1, 0, 2]
            else:
                imgshapes[file, :] = readslice.shape

            if not os.path.exists(os.path.join(zarrpath, "hdf5_files")):
                os.mkdir(os.path.join(zarrpath, "hdf5_files"))
            vaex.from_pandas(pd.DataFrame(readslice.astype('float32').reshape((-1, readslice.shape[2]))).astype(
                'float32')).export_hdf5(zarrpath + (f'/hdf5_files/analysis_{file:02}.hdf5'))
            del readslice

    fh.attrs['flipimg'] = flipimg
    fh.create_dataset('imageshapelist', data=imgshapes, dtype='i4')
    if args.npc == 1:
        args.npc = int(args.nchannels)
    df = vaex.open(os.path.join(zarrpath, "hdf5_files", "analysis_*.hdf5"))
    if args.submean:
        df.values[:] = df - df.mean(df.column_names)
        df.values[df.values > 0] = 0
    percentlist = df.percentile_approx(df.column_names, args.percentile).tolist()
    if normalizeacross:
        if pretrained != None:
            print("Pretrained SCALAR")
            scaler = load_preprocess(pretrained, zscore=True, pca=False)
        else:
            scaler = vaex.ml.StandardScaler(features=df.column_names, prefix='scaled_')
            scaler.fit(df)
            save_preprocess(scaler, zarrpath + "/vmodels", zscore=True, pca=False)
        scalar_trans = scaler.transform(df)
        if args.pca:
            print("PCA")
            scaled__cols = [col for col in scalar_trans.column_names if 'scaled_' in col]
            print(scaled__cols)
            print(scalar_trans)
            if args.npc is None:
                args.npc = len(scaled__cols)
            print("NPCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", args.npc)
            if pretrained is not None:
                print("Pretrained PCA")
                pca = load_preprocess(pretrained, zscore=False, pca=True)
            else:
                if args.npc > 10:
                    pca = vaex.ml.PCAIncremental(features=scaled__cols, n_components=args.npc, batch_size=10000000)
                else:
                    pca = vaex.ml.PCA(features=scaled__cols, n_components=int(args.npc))
                pca.fit(scalar_trans, progress='widget')
                save_preprocess(pca, zarrpath + "/vmodels", zscore=False, pca=True)
            df_trans = pca.transform(scalar_trans)
            PCA__cols = [col for col in df_trans.column_names if 'PCA_' in col]
            #hf = zarr.open(zarrpath, 'r+')
            #try:
            #    del hf['data_normalized']
            #except Exception as ex:
            #    print(ex)
            #fhd = hf.create_dataset('data_normalized',
            #                        shape=(totalpixel,
            #                               np.asarray(df_trans[PCA__cols][0:10, :len(trainmarkernums)]).shape[1]),
            #                        dtype='f8',
            #                        )
            for btch in range(0, df_trans.shape[0], 10000000):
                btchsize = np.min((df_trans.shape[0] - btch, 10000000))
                tmpdata = df_trans[PCA__cols][btch:btch + btchsize, :len(trainmarkernums)]
                fhd[btch:btch + btchsize, :] = np.asarray(tmpdata)
        else:
            #hf = zarr.open(zarrpath, 'r+')
            #try:
            #    del hf['data_normalized']
            #except Exception as ex:
            #    print(ex)
            scaled__cols = [col for col in scalar_trans.column_names if 'scaled_' in col]
            #fhd = hf.create_dataset('data_normalized',
            #                        shape=(totalpixel,
            #                               np.asarray(scalar_trans[scaled__cols][0:10, :len(trainmarkernums)]).shape[1]),
            #                        dtype='f8',
            #                        )
            for btch in range(0, np.asarray(scalar_trans[scaled__cols][0:10, :len(trainmarkernums)]).shape[1],
                              10000000):
                btchsize = np.min(
                    (np.asarray(scalar_trans[scaled__cols][0:10, :len(trainmarkernums)]).shape[0] - btch, 10000000))
                tmpdata = np.asarray(scalar_trans[scaled__cols][0:10, :len(trainmarkernums)])[btch:btch + btchsize,
                          :len(trainmarkernums)]
                fhd[btch:btch + btchsize, :] = np.asarray(tmpdata)

    fh.attrs['flipimg'] = flipimg
    fh.attrs['totalpixels'] = lastindex
    fh.attrs['percentile'] = percentlist
    fh.attrs['imageslist'] = imglist
    if not deletechannel.any() == 1000:
        fh.attrs['selmarkernames'] = np.delete(markernames, deletechannel).tolist()
    else:
        fh.attrs['selmarkernames'] = markernames
    shutil.rmtree(os.path.join(zarrpath, "hdf5_files"))
    return imglist, imgshapes, args
# list(['TONSIL-1_40X_Field_01_02_ordered8bit.tif','TONSIL-1_40X_Field_02_01_ordered8bit.tif','TONSIL-1_40X_Field_02_02_ordered8bit.tif','TONSIL-1_40X_Field_02_03_ordered8bit.tif','TONSIL-1_40X_Field_03_03_ordered8bit.tif'])
