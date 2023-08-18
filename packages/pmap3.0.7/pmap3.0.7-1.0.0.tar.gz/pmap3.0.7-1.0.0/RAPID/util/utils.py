import numpy as np
from sklearn.feature_extraction import image
from scipy import ndimage
import zarr
import tifffile
import dask_image
import platform
import psutil
import GPUtil
from tabulate import tabulate
import os
from math import sqrt, exp
from skimage import morphology
from RAPID.util.denoise import load_denoise_model, predict_mask
import copy
from sklearn.decomposition import PCA
from skimage.morphology import convex_hull_image
import pickle
import vaex
import vaex.ml
import pandas as pd
from scipy import ndimage as ndi


# https://hicraigchen.medium.com/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82


### TODO: Documentation
### TODO: Clean these up
### TODO: Is this different from the other function?
def cropandpaste_zarrSelected(zarrpath, patchsize, numberofpatches, rescale, rescalefactor, gaussianblurstd=0.5,
                              patcharray="", percent_ext=None):
    """
    Create random micropatches from image(s).

    Args:
        zarrpath (str): Zarr file path.
        patchsize (int): Patch size to use for crop.
        numberofpatches (int): Number of patches from each image.
        rescale (bool): Rescale cropped patches
        rescalefactor (float): Rescale factor.
        gaussianblurstd (float): Gaussian blur std to apply to the altered pixels.

    :return: EMPTY_ARRAY *()* \n

    :return: EMPTY_ARRAY_G *()* \n

    :return: INDICIES_ALL *()* \n

    """

    hf = zarr.open(zarrpath, 'r')
    print("Read hdf5 file for pacthes ...")
    rawdata = hf["data"]
    data_normalized = hf["data_normalized"]
    shapelist = hf["imageshapelist"][:, :]
    print("Shapelist ...", shapelist)

    if percent_ext == None:
        percentarray = hf.attrs['percentile']
    else:
        percentarray = [float(V) for V in percent_ext.split(",")]

    print("percentarray ...", percentarray)
    emptyarray = np.zeros((numberofpatches * len(shapelist), patchsize, patchsize, rawdata.shape[1]))
    patchcount = 0
    pixelscount = 0
    patch4rmeachimg = int((numberofpatches / 2) / emptyarray.shape[3])
    spnum = 0
    if patcharray == "":
        for i in range(len(shapelist)):
            normimg = data_normalized[pixelscount:int(pixelscount + (shapelist[i, 0] * shapelist[i, 1])), ].copy()
            normimg = normimg.reshape(shapelist[i, 0], shapelist[i, 1], normimg.shape[1])
            rawimg = rawdata[pixelscount:int(pixelscount + (shapelist[i, 0] * shapelist[i, 1])), ].copy()
            rawimg = rawimg.reshape(shapelist[i, 0], shapelist[i, 1], rawimg.shape[1])
            emptyarray[patchcount:patchcount + numberofpatches, :, :, :] = image.extract_patches_2d(image=normimg,
                                                                                                    max_patches=numberofpatches,
                                                                                                    patch_size=(
                                                                                                    patchsize,
                                                                                                    patchsize))
            print("Running patch selection with with max intensities ...", percentarray)
            selectedpatchlist = selectpatches(normimg, rawimg, percentarray, patchsize)
            print("Total channels for patch selection ...", len(selectedpatchlist))
            # spnum=0 fixed
            print("Checking each channels for equal number of patches  ...")
            for sp_pch in range(len(selectedpatchlist)):
                print("Channel ID ...", sp_pch, " total patches :", len(selectedpatchlist[sp_pch]))
                if (len(selectedpatchlist[sp_pch]) == 0):
                    continue
                minsize = min(len(selectedpatchlist[sp_pch]), patch4rmeachimg)
                randpnum = np.random.choice(len(selectedpatchlist[sp_pch]), minsize, replace=False)
                print("IDs of randomly selected patches  ...", randpnum)
                if len(randpnum) > 0:
                    print("Selected patches for channel  ...", sp_pch)
                    for pcounter in randpnum:
                        print("Selecting  patch number...", pcounter)
                        emptyarray[spnum, :, :, :] = selectedpatchlist[sp_pch][pcounter]
                        spnum += 1
            patchcount += numberofpatches
            print("Total patch count for the image  ...", numberofpatches)
    else:
        for i in range(len(shapelist)):
            normimg = data_normalized[pixelscount:int(pixelscount + (shapelist[i, 0] * shapelist[i, 1])), ].copy()
            normimg = normimg.reshape(shapelist[i, 0], shapelist[i, 1], normimg.shape[1])
            for patN in range(len(patcharray[i])):
                startx = patcharray[i][patN][0]
                starty = patcharray[i][patN][1]
                emptyarray[patchcount:patchcount + 1, :, :, :] = normimg[startx:startx + 64, starty:starty + 64, :]
                patchcount += 1
    emptyarray = emptyarray[0:patchcount, :, :, :]
    EMPTY_ARRAY = np.zeros((patchsize, patchsize * patchcount, rawdata.shape[1]))
    EMPTY_ARRAY_G = np.zeros((patchsize, patchsize * patchcount, rawdata.shape[1]))
    if rescale:
        EMPTY_ARRAY = np.zeros(
            (int(patchsize * rescalefactor), int(patchsize * rescalefactor) * patchcount, rawdata.shape[1]))
        EMPTY_ARRAY_G = np.zeros(
            (int(patchsize * rescalefactor), int(patchsize * rescalefactor) * patchcount, rawdata.shape[1]))
    j = 0
    for i in range(emptyarray.shape[0]):
        tmpvar = emptyarray[i, :, :, :]
        if rescale:
            tmpvar = ndimage.zoom(tmpvar, (rescalefactor, rescalefactor, 1))
        if gaussianblurstd > 0.1:
            filtersizeG = [gaussianblurstd, gaussianblurstd, 0]
            EMPTY_ARRAY[:, j:j + EMPTY_ARRAY.shape[0], :] = tmpvar
            EMPTY_ARRAY_G[:, j:j + EMPTY_ARRAY.shape[0], :] = ndimage.gaussian_filter(tmpvar, filtersizeG)
            j = j + int(patchsize * rescalefactor)
        else:
            EMPTY_ARRAY[:, j:j + EMPTY_ARRAY.shape[0], :] = tmpvar
            j = j + EMPTY_ARRAY.shape[0]
    EMPTY_ARRAY1 = np.ones((EMPTY_ARRAY.shape[0], EMPTY_ARRAY.shape[1]))
    for i in range(EMPTY_ARRAY1.shape[1]):
        if ((i % int(patchsize * rescalefactor) >= (int(patchsize * rescalefactor) - 3)) | (
                i % int(patchsize * rescalefactor) <= 3)):
            EMPTY_ARRAY1[:, i] = 0
    EMPTY_ARRAY1[0:6, :] = 0
    EMPTY_ARRAY1[EMPTY_ARRAY1.shape[0] - 6:EMPTY_ARRAY1.shape[0], :] = 0
    INDICIES_ALL = np.where(EMPTY_ARRAY1.reshape(-1) == 1)[0]
    return EMPTY_ARRAY, EMPTY_ARRAY_G, INDICIES_ALL


def selectpatches(normimg, rawimg, percentarray, ps):
    list_of_perch_patches = []
    [list_of_perch_patches.append([]) for i in range(rawimg.shape[2])]
    boolimage = np.zeros_like(rawimg)
    searchbool = []
    for ich in range(rawimg.shape[2]):
        boolimage[:, :, ich] = rawimg[:, :, ich] > percentarray[ich]
        if (sum(boolimage[:, :, ich].reshape(-1).astype(int)) > ((boolimage.shape[1] * boolimage.shape[1]) * 0.1)):
            searchbool.append(False)

        else:
            searchbool.append(True)
    print(searchbool)
    boolimage = boolimage.astype(int)
    for y in range(0, boolimage.shape[0], ps):
        for x in range(0, boolimage.shape[1], ps):
            patch = boolimage[y:y + ps, x:x + ps, :]
            if (patch.shape[0] == ps) and (patch.shape[1] == ps):
                skippatch = False
                # if(skippatch):
                #    continue
                randpnum = np.random.choice(rawimg.shape[2], rawimg.shape[2], replace=False)
                for ich in randpnum:
                    if (skippatch):
                        continue
                    if (searchbool[ich]):
                        if (np.sum(patch[:, :, ich]) > ((ps * ps) / 20)):
                            list_of_perch_patches[ich].append(normimg[y:y + ps, x:x + ps, :])
                            # tifffile.imsave("TIFF/"+str(x)+"_"+str(y)+"_ch_"+str(ich)+".tif",np.moveaxis(rawimg[y:y + ps, x:x + ps, :],-1,0))
                            skippatch = True
    return list_of_perch_patches


def cropandpaste_zarr(zarrpath, patchsize, numpatches, rescale, rescalefactor, gaussianblurstd=0.5, patcharray=""):
    """
    Create random micropatches from image array(s).

    Args:
        zarrpath (str): Path to image zarr file.
        patchsize (int): Size of patches to use for crop.
        numpatches (int): Number of patches form each image.
        rescale (bool): If True, rescale cropped images.
        rescalefactor (float): Factor by which to rescale images.
        gaussianblurstd (float): Gaussian blur standard deviation to apply to filtered pixels.
        patcharray (numpy.ndarray, optional): Pre-defined array to take patches from (Default: "").

    :return: patcharray *(numpy.ndarray)*: \n
        Array of patches taken from original image array(s).
    :return: blurredpatcharray *(numpy.ndarray)*: \n
        Array of patches taken from original image array(s) with gaussian filter applied.
    :return: indexarray *(numpy.ndarray)*: \n
        All indices in array.
    """

    hf = zarr.open(zarrpath, 'r')
    shapelist = hf["imageshapelist"][:, :]
    data_normalized = hf["data_normalized"]
    emptyarray = np.zeros((numpatches * len(shapelist), patchsize, patchsize, data_normalized.shape[1]))
    patchcount = 0
    pixelscount = 0
    if patcharray == "":
        for i in range(len(shapelist)):
            TMP = data_normalized[pixelscount:int(pixelscount + (shapelist[i, 0] * shapelist[i, 1])), ].copy()
            TMP = TMP.reshape(shapelist[i, 0], shapelist[i, 1], TMP.shape[1])
            emptyarray[patchcount:patchcount + numpatches, :, :, :] = image.extract_patches_2d(image=TMP,
                                                                                               max_patches=numpatches,
                                                                                               patch_size=(patchsize,
                                                                                                           patchsize))
            patchcount += numpatches
    else:
        for i in range(len(shapelist)):
            TMP = data_normalized[pixelscount:int(pixelscount + (shapelist[i, 0] * shapelist[i, 1])), ].copy()
            TMP = TMP.reshape(shapelist[i, 0], shapelist[i, 1], TMP.shape[1])
            for patN in range(len(patcharray[i])):
                startx = patcharray[i][patN][0]
                starty = patcharray[i][patN][1]
                emptyarray[patchcount, :, :, :] = TMP[startx:startx + 64, starty:starty + 64, :]
                patchcount += 1

    emptyarray = emptyarray[0:patchcount, :, :, :]

    if rescale:
        patcharray = np.zeros((int(patchsize * rescalefactor), int(patchsize * rescalefactor) * patchcount, data_normalized.shape[1]))
        blurredpatcharray = np.zeros((int(patchsize * rescalefactor), int(patchsize * rescalefactor) * patchcount, data_normalized.shape[1]))
    else:
        patcharray = np.zeros((patchsize, patchsize * patchcount, data_normalized.shape[1]))
        blurredpatcharray = np.zeros((patchsize, patchsize * patchcount, data_normalized.shape[1]))

    j = 0
    for i in range(emptyarray.shape[0]):
        tmpvar = emptyarray[i, :, :, :]
        if rescale:
            tmpvar = ndimage.zoom(tmpvar, (rescalefactor, rescalefactor, 1))
        if gaussianblurstd > 0.1:
            filtersizeG = [gaussianblurstd, gaussianblurstd, 0]
            patcharray[:, j:j + patcharray.shape[0], :] = tmpvar
            blurredpatcharray[:, j:j + patcharray.shape[0], :] = ndimage.gaussian_filter(tmpvar, filtersizeG)
            j += int(patchsize * rescalefactor)
        else:
            patcharray[:, j:j + patcharray.shape[0], :] = tmpvar
            j += patcharray.shape[0]

    indices = np.ones((patcharray.shape[0], patcharray.shape[1]))

    for i in range(indices.shape[1]):
        if ((i % int(patchsize * rescalefactor) >= (int(patchsize * rescalefactor) - 3)) | (
                i % int(patchsize * rescalefactor) <= 3)):
            indices[:, i] = 0

    indices[0:6, :] = 0
    indices[indices.shape[0] - 6:indices.shape[0], :] = 0
    indexarray = np.where(indices.reshape(-1) == 1)[0]

    return patcharray, blurredpatcharray, indexarray


def denoise_img(data, selected_ch=None, bs=1):
    """
    Denoise data with trained CNN network.

    Args:
        data (numpy.ndarray): Data array to be denoised.
        selected_ch (list, optional): Channels to denoise (Default: None).
        bs (int, optional): Number of patches to pass through the network at a time (Default: 1).

    :return: image *(numpy.ndarray)*: \n
        Data array with selected channels denoised.
    """
    # loading denoising model
    print("loading denoising model..")
    model = load_denoise_model()
    tmpdata = copy.deepcopy(data)

    if selected_ch == None:
        tmpdata = predict_mask(model, tmpdata, bs)
    else:
        for ch in selected_ch:
            print("Denoising channel " + str(ch) + ".")
            tmp = predict_mask(model, tmpdata[:, :, ch], bs)
            tmpdata[:, :, ch] = tmp[0:data.shape[0], 0:data.shape[1]]
    # print(np.unique(tmpdata))
    # tifffile.imsave("/tmp/denoise.tif",(tmpdata/np.max(tmpdata)*255).astype(np.uint8))
    tmpdata[tmpdata > 0.5] = 1
    tmpdata[tmpdata < 0.5] = 0
    cleantiff = data * tmpdata

    # tifffile.imsave("/tmp/denoise.tif",np.moveaxis(cleantiff,2,0))
    return cleantiff


### TODO: Documentation
def gaussian_LP(d0, shape):
    """


    Args:
        d0 (int):
        shape (Iterable):

    :return: base *(numpy.ndarray)*: \n

    """
    base = np.zeros(shape[:2])
    rows, cols = shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            dist = sqrt((y - center[0]) ** 2 + (x - center[1]) ** 2)
            base[y, x] = exp(((-dist ** 2) / (2 * (d0 ** 2))))
    return base


def generate_colormap(numcolors):
    """
    Generating colormap for the RAPID output image.

    Args:
        numcolors (int): Number of unique colors in the colormap.

    :return: color_list *(numpy.ndarray)*: \n
        Colormap to be used.
    """

    # check if the number of unique maps is more than 729
    if numcolors > 729:
        num = [1, 35, 70, 105, 140, 175, 210, 255]
    else:
        num = [1, 50, 100, 150, 200, 255]
    color = np.zeros((len(num) ** 3, 3))
    countcolor = 0
    # create unique colormap list
    for r in num:
        for g in num:
            for b in num:
                if r + g + b > 70 and r * .299 + g * .587 + b * .114 > 57.375:
                    color[countcolor, 0] = r
                    color[countcolor, 1] = g
                    color[countcolor, 2] = b
                    countcolor = countcolor + 1
                else:
                    pass
    color = color[0:countcolor]
    color_list = color[np.linspace(0, (len(color)) - 1, num=numcolors).astype(int), :]
    return color_list


def gpu_info():
    """
    Print GPU info.
    Taken from  https://www.thepythoncode.com/article/get-hardware-system-information-python
    """
    print("=" * 40, "GPU Details", "=" * 40)
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        # get the GPU id
        gpu_id = gpu.id
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load * 100}%"
        # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature, gpu_uuid
        ))

    print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                       "temperature", "uuid")))


def load_preprocess(vaexmodelpath, zscore=False, pca=False):
    """
    Load data preprocessing model.

    Args:
        vaexmodelpath (str): Path to root folder where model(s) will be loaded from.
        zscore (bool, optional): True if zscore normalization applied to image (Default: False).
        pca (bool, optional): True if pca normalization applied to image (Default: False).

    :return: model *(vaex.ml.StandardScaler)*: \n
        Loaded vaex model.
    """
    if not os.path.exists(vaexmodelpath):
        print("No pretrained model found")
        return
    if zscore:
        model = pickle.load(open(vaexmodelpath + "/" + "zscore.sav", 'rb'))
    if pca:
        model = pickle.load(open(vaexmodelpath + "/" + "pca.sav", 'rb'))
    return model


### TODO: Documentation
def lp_gauss(img):
    """


    Args:
        img (numpy.ndarray):

    :return: *(float)*: \n

    """
    original = np.fft.fft2(img)
    center = np.fft.fftshift(original)
    LowPassCenter = center * gaussian_LP(1000, img.shape)
    LowPass = np.fft.ifftshift(LowPassCenter)
    inverse_LowPass = np.fft.ifft2(LowPass)
    return np.abs(inverse_LowPass)


def neighbors(image, coords, r=3):
    """
    Get the pixels in an image within a specified bounding box centered around a given pixel.

    Args:
        image (numpy.ndarray): Original image array.
        coords (Iterable): x,y-coordinates of the specified pixel.
        r (int, optional): Distance in each direction from the specified pixel to draw the bounding box (Default: 3).

    :return: n *(numpy.ndarray)*: \n
        Flattened array of pixels within the bounding box.
    """

    i = coords[0]
    j = coords[1]
    n = image[i - r:i + r + 1, j - r:j + r + 1].flatten()

    # remove the element (i,j)
    n = np.hstack((n[:len(n) // 2], n[len(n) // 2 + 1:],))
    if len(n) == 0:
        n = [image[i, j]]
    return n


def system_info():
    """
    Print the system info
    Taken from https://www.thepythoncode.com/article/get-hardware-system-information-python
    """

    system = platform.uname()
    print("System: " + system.system)
    print(f"Node Name: " + system.node)
    print(f"Release: " + system.release)
    print(f"Version: " + system.version)
    print("Machine: " + system.machine)
    print("Processor:" + system.processor)

    print("" * 40, "CPU Info", "=" * 40)  #
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    print("=" * 40, "Memory Information", "=" * 40)
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("=" * 20, "SWAP", "=" * 20)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    Taken from https://www.thepythoncode.com/article/get-hardware-system-information-python

    Args:
        bytes (int): Number of bytes being converted.
        suffix (str, optional): Suffix to be used for units (Default: "B").
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def preprocess(imgpath, medianblur=False, gaussianblur=False, gaussianblurstd=1, img="", normtype=None,
               normalize_first=False, fft=False, denoise="", submean=True, medianblursize=3):
    """
    Preprocess a dataset for analysis.

    Args:
        imgpath (str): Path to the image file being preprocessed.
        medianblur (bool, optional): If true, apply a median blur to the array (Default: False).
        gaussianblur (bool, optional): If true, apply a gaussian blur to the array (Default: False).
        gaussianblurstd (float, optional): Standard deviation to be used for the gaussian blur (Default: 1).
        img (numpy.ndarray, optional): Array to be preprocessed (Default: "").
        normtype (str, optional): Normalization algorithm to be used on the image (Default: False).
        normalize_first (bool, optional): If True, normalize before applying smoothing on the image (Default: False).
        fft (bool, optional): If true, apply a Fast Fourier Transform on the image (Default: False).
        denoise (list, optional): Channels to denoise (Default: "").
        submean (bool, optional): If True, subtract the mean after smoothing (Default: True).
        medianblursize (int, optional): Length of square bounding box used for the median blur (Default: 3).

    :return: img *(numpy.ndarray)*: \n
        Array with preprocessed image data.

    :Example:

    >>> from RAPID.util.utils import preprocess
    >>> import tifffile
    >>> module_path = dirname(__file__)
    >>> imagepath = module_path+"/../Data/MouseLN/AB_CROP.tif"
    >>> img = tifffile.imread(imagepath)
    >>> filepath ="/tmp/Data"
    >>> denoised_img = preprocess(filepath,smooth=False,normalize=False,medianblur=True,gaussianblur=False,gaussianblurstd=1,img="",normtype=None,normalize_first=False)
    """

    if len(img) == 0:
        img = dask_image.imread.imread(imgpath)
        img = np.moveaxis(img, 0, -1)

    if denoise_img:
        if len(denoise) > 0:
            img = denoise_img(img, selected_ch=denoise, bs=4)

    if normalize_first:
        if normtype == "zscore":
            df = vaex.from_pandas(pd.DataFrame(img.reshape((-1, img.shape[2]))))
            scaler = vaex.ml.StandardScaler(features=df.column_names, prefix='scaled_')
            scaler.fit(df)
            normdata = scaler.transform(df)
            scaled_cols = [col for col in normdata.column_names if 'scaled_' in col]
            img = np.array(normdata[scaled_cols]).reshape(img.shape)
        elif normtype == "log10":
            img = np.nan_to_num(np.log10(img), nan=0, posinf=0, neginf=0)
        elif normtype == "log2":
            img = np.nan_to_num(np.log2(img), nan=0, posinf=0, neginf=0)
        img = smoothimg(img, medianblur=medianblur, gaussianblur=gaussianblur, gaussianblurstd=gaussianblurstd)
        for slice in range(img.shape[-1]):
            tmpslize = img[:, :, slice]
            if len(tmpslize[tmpslize > 0]) > 0:
                lowpercentile = np.percentile(tmpslize[tmpslize > 0], 3)
                tmpslize[tmpslize <= lowpercentile] = 0
            img[:, :, slice] = tmpslize

    else:
        img = smoothimg(img, medianblur=medianblur, gaussianblur=gaussianblur, gaussianblurstd=gaussianblurstd,
                         submean=submean, medianblursize=medianblursize)
        if fft:
            for slice in range(img.shape[-1]):
                img[:, :, slice] = lp_gauss(img[:, :, slice])
            img += 1
        if normtype == "zscore":
            df = vaex.from_pandas(pd.DataFrame(img.reshape((-1, img.shape[2]))))
            scaler = vaex.ml.StandardScaler(features=df.column_names, prefix='scaled_')
            scaler.fit(df)
            normdata = scaler.transform(df)
            scaled_cols = [col for col in normdata.column_names if 'scaled_' in col]
            img = np.array(normdata[scaled_cols]).reshape(img.shape)
        if normtype == "log10":
            img = np.nan_to_num(np.log10(img * 255 + 1), nan=0, posinf=0, neginf=0)
        if normtype == "log2":
            img = np.nan_to_num(np.log2(img + 1), nan=0, posinf=0, neginf=0)
        if normtype == "sqrt":
            img = img ** (1 / 2)
        if normtype == "inverse":
            img = 1 / img
    return img


def run_pca(data=None, numcomponents=0.99):
    """
    Run principal component analysis (PCA) dimensionality reduction on multidimensional data.

    Args:
        data (numpy.ndarray, optional): Input multidimensional data array (Default: None).
        numcomponents (int/float, optional): If int, number of components to be used in PCA. If float, amount of variance (Default: 0.99).

    :return: transformeddata *(numpy.ndarray)*: \n
        Data with PCA dimensionality reduction applied to it.
    """
    my_model = PCA(n_components=numcomponents, svd_solver='full')
    my_model.fit(data)
    print(my_model.explained_variance_ratio_)
    transformeddata = my_model.transform(data)
    return transformeddata


def save_preprocess(model, vaexmodelpath, zscore=False, pca=False):
    """
    Save data preprocessing model.

    Args:
        model (vaex.ml.StandardScaler): Vaex model to be saved.
        vaexmodelpath (str): Path to output folder where model(s) will be saved to.
        zscore (bool, optional): True if zscore normalization applied to image (default: False).
        pca (bool, optional): True if pca normalization applied to image (default: False).
    """
    if not os.path.exists(vaexmodelpath):
        os.mkdir(vaexmodelpath)
    if zscore:
        pickle.dump(model, open(vaexmodelpath + "/zscore.sav", 'wb'))
    if pca:
        pickle.dump(model, open(vaexmodelpath + "/pca.sav", 'wb'))


### TODO: submean
def smoothimg(img, medianblur=False, gaussianblur=False, gaussianblurstd=1, submean=True, medianblursize=3):
    """
    Apply a smoothing algorithm to a raw image array.

    Args:
        img (numpy.ndarray): Raw image array to be smoothed.
        medianblur (bool, optional): If true, apply a median blur to the array (Default: False).
        gaussianblur (bool, optional): If true, apply a gaussian blur to the array (Default: False).
        gaussianblurstd (float, optional): Standard deviation to be used for the gaussian blur (Default: 1).
        submean (bool, optional): If True, subtract the mean after smoothing (Default: True).
        medianblursize (int, optional): Length of square bounding box used for the median blur (Default: 3).

    :return: smoothedimg *(numpy.ndarary)*: \n
        Smoothed image array.
    """
    dims = len(img.shape)
    if dims == 3:
        filtersizeM = [medianblursize, medianblursize, 1]
        filtersizeG = [gaussianblurstd, gaussianblurstd, 0]
    if dims == 4:
        filtersizeM = [1, medianblursize, medianblursize, 1]
        filtersizeG = [0, gaussianblurstd, gaussianblurstd, 0]
    if dims == 5:
        filtersizeM = [1, 1, medianblursize, medianblursize, 1]
        filtersizeG = [0, 0, gaussianblurstd, gaussianblurstd, 0]
    if medianblur:
        img = ndimage.median_filter(img, filtersizeM)
    if gaussianblur:
        img = ndimage.gaussian_filter(img, filtersizeG)
    return img


'''
def selectpatches(normimg,rawimg,ps):
    list_of_perch_patches = []
    [list_of_perch_patches.append([]) for i in range(normimg.shape[2])]
    boolimage = np.zeros_like(rawimg)
    searchbool = []
    for ich in range(imgdata.shape[2]):
        boolimage[:, :, ich] = rawimg[:, :, ich] > percentarray[ich]
        if (sum(boolimage[:, :, ich]) > ((boolimage.shape[0] * boolimage.shape[1]) * 0.1)):
            searchbool[ich] = False
        else:
            searchbool[ich] = True
    for y in range(0, boolimage.shape[0], ps):
        for x in range(0, boolimage.shape[1], ps):
            patch = boolimage[y:y + ps, x:x + ps, :]
            if ((patch.shape[0] == ps) & (patch.shape[1] == ps)):
                for ich in range(imgdata.shape[2]):
                    if (searchbool[ich]):
                        if (np.sum(patch[:, :, ich]) > ((ps * ps) / 3)):
                            list_of_perch_patches[ich].append(normimg[y:y + ps, x:x + ps, :])
'''
