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
from skimage.morphology import dilation,erosion
from skimage.color import label2rgb
from skimage.morphology import disk
import argparse
from RAPID.util import io  as rio
import pandas as pd
from RAPID.util import denoise, utils


class DoubleConv(nn.Module):
    """
    Apply consecutive 3x3 convolutions on an image. The first convolution expands the number of channels, while the second preserves the number of channels.

    Arguments:
        :in_channels (int): Number of input channels for the convolution.
        :out_channels (int): Number of output channels for the convolution.
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
    Apply a down convolution, consisting of a 2x2 max pool followed by a double convolution.

    Arguments:
        :in_channels (int): Number of input channels for the convolution.
        :out_channels (int): Number of output channels for the convolution.
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
    Apply an up convolution, with the result concatenated with the corresponding tensor from the encoder.

    Arguments:
        :in_channels (int): Number of input channels for the convolution.
        :out_channels (int): Number of output channels for the convolution.
        :bilinear (bool, optional): If True, use bilinear upsampling algorithm (Default: True).
    """
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
        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,diffY // 2, diffY - diffY // 2])
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)

class OutConv(nn.Module):
    """
    Apply a 1x1 convolution.

    Arguments:
        :in_channels (int): Number of input channels for the convolution.
        :out_channels (int): Number of output channels for the convolution.
    """
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)
    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    """
    Define general nested U-Net architecture, with a series of down convolutions followed by a series of up convolutions and a final 1x1 convolution.

    Arguments:
        :n_channels (int): Number of input channels to the network.
        :n_classes (int): Number of output channels from the network.
        :bilinear (bool, optional): If True, use bilinear upsampling algorithm (Default: True).
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

#https://github.com/davidmashburn/SeedWaterSegmenter/
class obejctsegmentation():
    """
    Object-based segmentation class.
    """
    def __init__(self, img=None):
        pass

    '''
    def displayumap(self,Qtab):
        reducer = umap.UMAP(min_dist=0.05, n_neighbors=5)
        #reducer = umap.UMAP(min_dist=0.05, n_neighbors=5,metric="cosine")
        mapper = reducer.fit_transform(Qtab[:,3:])

        ymin = np.min(mapper[:, 1])
        ymax = np.max(mapper[:, 1])
        xmin = np.min(mapper[:, 0])
        xmax = np.max(mapper[:, 0])
        Xlen = xmax + np.abs(xmin)
        Ylen = ymax + np.abs(ymin)
        mapper[:, 1] = ((mapper[:, 1] - ymin) / (Ylen * 1.25)) * (200)
        mapper[:, 0] = ((mapper[:, 0] - xmin) / (Xlen * 1.25)) * (200)
        mapper = mapper.astype(np.int)
        mapper = mapper# + 25
        IMGW = np.zeros((200, 200))
        corUMAP = np.zeros((len(mapper),len(mapper)))
        for i in range(len(mapper)):
            IMGW[mapper[i, 0], mapper[i, 1]] = 255
            corUMAP[mapper[i, 0], mapper[i, 1]] = i

        return IMGW,corUMAP

    def trainRAPIDOBJECT(self, viewer):
        #model = models.RAPIDResnet(self.RAPIDData.shape[0],NCluster=int(self.nc), NMOD=2)
        model = models.RAPIDResnet(self.RAPIDData.shape[0],NCluster=int(self.nc), NMOD=2)
        model.apply(models.weight_init)
        print(model)
        model.to("cpu")
        optimizer = optim.AdamW(model.parameters(), lr=float(self.lr), betas=(0.9, 0.999), eps=1e-08, weight_decay=0.01,amsgrad=False)
        STDIMG=copy.deepcopy((self.Qtab[:,1:]))
        NMAX = np.max(STDIMG, axis=(0))
        print(NMAX)
        Batch_Size=int(self.bs)
        PS=int(self.ps)
        print(STDIMG.shape)
        print(".....")
        viewer.status = "RAPID training..."
        self.setinvisible()
        for epoch in range(1):
            for mode in ['train', 'test']:
                if (mode=="train"):
                    self.train_epochOobject(model,STDIMG,optimizer,epoch,Batch_Size,PS,int(self.nit),NMAX)
                else:
                    self.testobject(model, STDIMG, Batch_Size, STDIMG, PS, epoch)
        viewer.status = "RAPID training done."

    def testobject(self,model, OrgIMG, BS, OrgShape, PS, EPOC):
        model.eval()
        device="cpu"
        with torch.no_grad():
            testdata=copy.deepcopy(OrgIMG)
            TESTPATCHPRED = testdata.reshape((-1,testdata.shape[1]))
            TESTPATCHPREDO = np.zeros((TESTPATCHPRED.shape[0]))
            for BSTART in range(0, TESTPATCHPRED.shape[0], 50000):
                x = torch.from_numpy(TESTPATCHPRED[BSTART:BSTART + (50000), :]).float().to(device)
                outputs, AA = model(x)
                TESTPATCHPREDO[BSTART:BSTART + (50000)] = outputs[0].argmax(dim=1).cpu()
            #TESTPATCHPRED = TESTPATCHPREDO.reshape((self.RAPIDData.shape[1], self.RAPIDData.shape[2]))
        emptymask = np.zeros((self.img.shape[0],self.img.shape[1],3))
        colforinput = models.colors(int(self.nc))
        print(colforinput)
        try:
            for i in range(len(TESTPATCHPREDO)):
                 masktmp = ((self.expandobject == self.Qtab[i,0]))
                 #print(self.expandobject[i])
                 print(TESTPATCHPREDO[i])
                 print(i)
                 emptymask[masktmp] =  colforinput[int(TESTPATCHPREDO[i]),:]/255
            self.add_image(self.expandobject, name='RAPID cluster0', is_pyramid=False)
            self.layers['RAPID cluster0'].blending = "additive"
            self.add_image(emptymask, name='RAPID cluster', is_pyramid=False)
            self.layers['RAPID cluster'].blending = "additive"
        except Exception as ex:
            print(ex)

    def trainRAPID2(self, viewer):
        model = models.RAPID(2,self.RAPIDData.shape[0]+1,30)
        model.apply(models.weight_init)
        model.to("cpu")
        optimizer = optim.AdamW(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0.01,amsgrad=False)
        STDIMG=copy.deepcopy((self.RAPIDData))
        Add_Zeros=np.zeros((STDIMG.shape[1],STDIMG.shape[2]))
        self.ConcateZero=np.concatenate((STDIMG,Add_Zeros),axis=0)
        NMAX = np.max(self.ConcateZero, axis=(1,2))
        print(NMAX)
        Batch_Size=100
        PS=64
        print(self.ConcateZero.shape)
        print(".....")
        viewer.status = "RAPID training..."
        self.setinvisible()
        for epoch in range(1):
            for mode in ['train', 'test']:
                if (mode=="train"):
                    self.train_epoch(model,self.ConcateZero,optimizer,epoch,Batch_Size,PS,1000,NMAX)
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

    def unet_featurizeRAPID(image,
                            featurizer_path="/Users/thakurn2/Downloads/Biowulf/TMP/Model5.pt",
                            device="cpu"):
        model = _load_model(featurizer_path).float()
        # image = torch.Tensor(image).float()
        image = check_padding(image, 256)
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

    def segment(self, viewer):
        viewer.status = "Segmenting..."
        self.layers['output'].visible = False

        #image = viewer.layers['input'].data
        image = viewer.active_layer.data
        cv.imwrite("/tmp/sps2.png",image)
        MinCL,MaxCL=viewer.active_layer.contrast_limits
        image[image<=MinCL]=0
        image[image>MaxCL]=1

        print(MinCL)
        cv.imwrite("/tmp/r1.png",image*255)
        print(np.max(image))
        print(image.shape)
        print("........")
        #labels = viewer.layers['train'].data

        # fit and predict
        features = models.unet_featurize(image*255)
        print(np.min(features))
        print(np.max(features))

        cv.imwrite("/tmp/r.png",features*255)
        MP= self.layers['output'].data
        MP[MP>0.5]=1
        MP[MP<=0]=0

        self.layers['output'].data = features#[0].transpose(2, 0, 1)
        #segmentation, self.prob = predict(clf, features)
        self.layers['output'].contrast_limits = np.min(features), np.max(features)
        self.layers['output'].visible = True
        self.layers['output'].blending = "additive"
        self.add_labels(MP,name="LAB",is_pyramid=True)
        self.layers['LAB'].editable = True
        #print(np.unique(self.layers['TEST'].data))
        # show prediction
        #self.segmentation = np.squeeze(segmentation)
        #viewer.layers['output'].data = self.segmentation

        viewer.status = "Segmentation Completed"

    def train_epochOobject(self,model, OrgIMG, optimizer, epoch, BS, PS, NIT,NMAX1):
        model.train()
        device="cpu"
        lossAvg = 0
        for batch_idx in range(0, NIT):
            import timeit
            dataTrain = OrgIMG
            RANDINDEX = np.random.randint(0, len(OrgIMG), size=BS)
            data = np.squeeze(dataTrain[RANDINDEX, :])
            NZ = np.ones_like(data.reshape(-1))
            NZ[0:int(len(NZ) * 0.01)] = 0
            np.random.shuffle(NZ)
            NZ = NZ.reshape(data.shape)
            optimizer.zero_grad()
            HOWMANY=1
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
                    loss1 = torch.sum(torch.stack([models.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in zip(output, output_alt, AA, AA)])).mean()
                else:
                    TMP = loss1.clone()
                    loss1 = TMP + torch.sum(torch.stack([models.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in zip(output, output_alt, AA, AA)])).mean()
            loss1.backward()
            optimizer.step()
            lossAvg = lossAvg + loss1.item()
            if batch_idx %1 == 0:
                print(
                    'Train Epoch {} -iteration {}/{} - LR {:.6f} -\ttotal loss: {:.6f} -\t IIC loss: {:.3f}-\t MSE:{:.3f}'.format(epoch, batch_idx, NIT, 10, (lossAvg / 10), loss1, 10))
                lossAvg = 0

    def check_padding(self,image=None, PS=None):
        """
        Expression quantification of the segmented object image.

        Arguments:
            :image (numpy.ndarray, optional): Multiplex image data array.
            :PS (int, optional): Segmented image data array.

        Returns:
            :IMGMEAN (numpy.ndarray): Table array with marker expression quantified for each segmented cell.
            :cortab (numpy.ndarray): Table with coordinates for each segmented cell.
            :rgbimage (numpy.ndarray): Image array with segmented cells colored randomly.
            :expandobject (numpy.ndarray): Image array with segmented cells labeled according to cell IDs.
        """
        NC = int(image.shape[1] / PS)
        NR = int(image.shape[0] / PS)
        if (NR * PS) < image.shape[0]:
            NR += 1
        if (NC * PS) < image.shape[1]:
            NC += 1
        modimage = np.zeros((PS * NR, PS * NC,image.shape[2]))
        modimage[0:image.shape[0], 0:image.shape[1],:] = image
        return modimage

    def make_patches(self, image=None, PS=None):
        tmpimages = np.zeros((int(image.shape[0] / PS) * int(image.shape[1] / PS), PS, PS))
        p = 0
        for i in range(0, image.shape[0], PS):
            for j in range(0, image.shape[1], PS):
                tmpimages[p, :, :] = image[i:i + PS, j:j + PS]
                p = p + 1
        return tmpimages

    ### Almost same as same function in denoise but slightly different
    def clubpatches(self,image=None, imageshape=None):
        """
        Collate an array of patches back into a single full image array.

        Arguments:
            :image (numpy.ndarray, optional): Array of patches to be collated (Default: None).
            :imageshape (numpy.ndarray, optional): Reference image to determine the shape of the output (Default: None).

        Returns:
            :numpy.ndarray: Image with patches collated onto it.
        """
        tmpimages = np.zeros_like(imageshape)
        NC = int(imageshape.shape[1] / image.shape[2])
        NR = int(imageshape.shape[0] / image.shape[2])
        PS = image.shape[2]
        p = 0
        for R in range(NR):
            for C in range(NC):
                tmpimages[R * PS:(R * PS) + PS, C * PS:(C * PS) + PS] = image[p,1,:,:]
                p += 1
        return tmpimages
    '''

    def mergemem(self,image=None,channels=None,mode="avg"):
        """
        Merge cell markers to be used for image segmentation.

        Arguments:
            :image (numpy.ndarray, optional): Multiplex image data array.
            :channels (Iterable, optional): List of indices for the cell markers to be combined (Default: None).
            :mode (str, optional): Defines which algorithm is used to combine markers together. Options include {"avg", "sum", "max", and "median"} (Default: "avg").

        Returns:
            :img2 (numpy.ndarray): Single-channel image containing the specified markers combined.
        """
        img2=copy.deepcopy(image)
        if len(channels)!=1:
            img2 = img2[:,:,channels]
        if mode == "avg":
            print(img2.shape)
            img2 = np.mean(img2,axis=2)
        if mode == "sum":
            img2=np.sum(img2,axis=2)
        if mode == "max":
            img2=np.max(img2,axis=2)
        if mode == "median":
            img2=np.median(img2,axis=2)
        return img2

    def quantifyimage(self,image,objects,object_true=False):
        """
        Expression quantification of the segmented object image.

        Arguments:
            :image (numpy.ndarray): Multiplex image data array.
            :objects (numpy.ndarray): Segmented image data array.
            :object_true (bool, optional): If True, image is already binarized; otherwise, binarize the image (Default: False).

        Returns:
            :IMGMEAN (numpy.ndarray): Table array with marker expression quantified for each segmented cell.
            :cortab (numpy.ndarray): Table with coordinates for each segmented cell.
            :rgbimage (numpy.ndarray): Image array with segmented cells colored randomly.
            :expandobject (numpy.ndarray): Image array with segmented cells labeled according to cell IDs.
        """
        if not object_true:
            objects[objects >= 0.9] = 1
            objects[objects < 0.9] = 0
            objects = objects.astype(np.uint8)
            objects = measure.label(objects, connectivity=1)

        objects = morphology.remove_small_objects(objects, min_size=10)
        expandobject = self.expandobjects(objectimg=objects, numofiterations=2)
        print(np.unique(expandobject))
        all_labels, obejctcount = measure.label(objects, connectivity=1, return_num=True)
        dil = erosion(expandobject, disk(3))
        BIND = copy.deepcopy(dil)
        BIND[BIND > 0] = 1
        BIND = abs(BIND - 1)
        expandobject = expandobject * BIND
        proptab = np.zeros((image.shape[2]+4, obejctcount))

        all_labels=expandobject
        for ch in range(image.shape[2]):
            #proptab[ch, :] = [prop.mean_intensity for prop in measure.regionprops(all_labels, intensity_image=self.layers[self.MARKERS[ch]].data)]
            proptab[ch, :] = measure.regionprops_table(all_labels, image[:,:,ch],properties=['mean_intensity'])['mean_intensity']
            #props = measure.regionprops_table(label_image, image,properties=['label', 'inertia_tensor', 'inertia_tensor_eigvals'])
        proptab[ch + 1, :] = [prop.area for prop in
                              measure.regionprops(all_labels, intensity_image=image[:,:,0])]
        proptab[ch + 2, :] = [prop.eccentricity for prop in
                              measure.regionprops(all_labels, intensity_image=image[:,:,0])]
        proptab[ch + 3, :] = [prop.perimeter for prop in
                              measure.regionprops(all_labels, intensity_image=image[:,:,0])]
        proptab[ch + 4, :] = [prop.major_axis_length for prop in
                              measure.regionprops(all_labels, intensity_image=image[:,:,0])]
        cortab = [prop.centroid for prop in measure.regionprops(all_labels, intensity_image=image[:,:,0])]
        labtab = [prop.label for prop in measure.regionprops(all_labels, intensity_image=image[:,:,0])]
        print(proptab.shape)
        print(proptab[0:10,1:4])
        IMGMEAN=np.c_[np.asarray(labtab),np.asarray(cortab),proptab.T]
        rgbimage = label2rgb(expandobject, image=None, colors=None, alpha=0.3, bg_label=0, bg_color=(0, 0, 0),
                             image_alpha=1, kind='overlay')

        cv.imwrite("/tmp/test.png", expandobject.astype(np.uint16))
        allt = copy.deepcopy((IMGMEAN))
        RRRRR=5
        tt2 = np.squeeze(allt[:, RRRRR])
        RESIND = np.squeeze(np.asarray(np.where(tt2 > 0.1)))
        print(RESIND.shape)

        '''
        for i in range(len(RESIND)):
             masktmp = ((self.expandobject == allt[RESIND[i],0].astype(np.int)))
             print(i)
             emptymask[masktmp] =  allt[RESIND[i],0]
        '''
        mask1 = np.in1d(expandobject, allt[RESIND,0], invert=True)
        emptymask=copy.deepcopy(expandobject)
        emptymask.reshape(-1)[mask1]=0
        return IMGMEAN,cortab, rgbimage,expandobject

    def loadunetmodel(self):
        """
        Load a pretrained UNet model.

        Returns:
            :model (Torch.nn model): Loaded UNet model.
        """
        rootfolder = os.path.dirname(os.path.abspath(__file__))
        modelpath = rootfolder + "/../models/Model2_12.pt"
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

    def rununet(self,image,device="cpu"):
        """
        Pass an image array through a pretrained UNet.

        Arguments:
            :image (numpy.ndarray): Image array to be input to the UNet.
            :device (str): Device to use for analysis ("cpu" or "gpu").

        Returns:
            :features (numpy.ndarray): Output image from the UNet.
        """
        model = self.loadunetmodel().float()
        #*******
        paddedimage = denoise.check_padding(image)
        image2 = denoise.make_patches(paddedimage, 256)
        emptyresult = np.zeros((image2.shape[0], 2, image2.shape[1], image2.shape[2]))
        with torch.no_grad():
            for i in range(emptyresult.shape[0]):
                emptyresult[i,:,:,:] = F.softmax(model(torch.unsqueeze(torch.unsqueeze(torch.from_numpy(image2[i, :, :]),0),0).float()).to(device), dim=1).numpy()
        features = denoise.club_patches(emptyresult, paddedimage)
        return features

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
                              marker_list=None,mergedimage=None):
        """
        Expression quantification of the segmented object image .

        Arguments:
            :image (np.ndarray): Multiplex input image array [H,W,C].
            :membranechannel (list): List of channels to use for object identification.
            :outfolder (str, optional): Path to output folder where files will be saved (Default: "./").
            :gaussianblur (bool, optional): If True, apply gaussian blur (Default: False).
            :gaussianblurstd (float, optional): Standard deviation used for gaussian blur (Default: 1).
            :medianblur (bool, optional): If True, apply median blur (Default: True).
            :selectzslice (int, optional): z-slice used for analysis (Default: None).
            :selecttime (int, optional): t-slice used for analysis (Default: None).
            :marker_list (list, optional): List of names of markers used for quantification (Default: None).
            :mergedimage (numpy.ndarray, optional): Image with merged cell markers to be used for segmentation (Default: None).
        Returns:
            :table (pandas.DataFrame): Quantification table for segmented cells.
            :rapidobjects (numpy.ndarray): Raw RAPID segmented image.
            :expandobject (numpy.ndarray): RAPID segmented image with nuclei expanded, labeled according to cell IDs.
            :object2rgb (numpy.ndarray): RAPID segmented image with nuclei expanded, with cells randomly colored.
        """

        '''
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
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
            pass
        '''
        if not type(image) == np.ndarray:
            image = rio.read_ome(image, z=selectzslice, t=selecttime)
            image = utils.smoothing(image, gaussianblur=gaussianblur, gaussianblurstd=gaussianblurstd, medianblur=medianblur)
            '''
            if gaussianblur and medianblur:
                image = utils.smoothing(image, gaussianblur=True, gaussianblurstd=gaussianblurstd, medianblur=True)
            elif gaussianblur and not medianblur:
                image = utils.smoothing(image, gaussianblur=True, gaussianblurstd=gaussianblurstd, medianblur=False)
            elif medianblur and not gaussianblur:
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
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
            '''
        paddedimage = denoise.check_padding(image, 256)
        if type(mergedimage) != np.ndarray:
            mergedimage = self.mergemem(image=paddedimage,channels=membranechannel,mode="sum")
        predimg = self.rununet(mergedimage)
        if not os.path.exists(outfolder):
            os.mkdir(outfolder)
        rapidobjects = (predimg * 255).astype(np.uint8)
        cv.imwrite(outfolder + "/Objects.png", rapidobjects)
        if len(marker_list) == 0:
            marker_list = [i for i in range(image.shape[-1])]
        table, coordinates, object2rgb, expandobject = self.quantifyimage(paddedimage,predimg,object_true=False)
        table = pd.DataFrame(table)
        table.columns = np.hstack([["ID", "X", "Y"], marker_list])
        table.to_csv(outfolder + "/ObjectQuantification.csv")
        print(table.values)
        object2rgb = (object2rgb*255).astype(np.uint8)
        cv.imwrite(outfolder + "/Object2rgb.png", object2rgb)
        return table,rapidobjects,expandobject,object2rgb

    def run_object_prediction_from_mask(self, image, membranechannel, outfolder="./",
                              gaussianblur=False,
                              gaussianblurstd=1, medianblur=True,
                              selectzslice=None, selecttime=None,
                              marker_list=None,maskimage=None):
        """
        Expression quantification of the segmented object image .

        Arguments:
            :image (np.ndarray): Multiplex input image array [H,W,C].
            :membranechannel (list): List of channels to use for object identification.
            :outfolder (str, optional): Path to output folder where files will be saved (Default: "./").
            :gaussianblur (bool, optional): If True, apply gaussian blur (Default: False).
            :gaussianblurstd (float, optional): Standard deviation used for gaussian blur (Default: 1).
            :medianblur (bool, optional): If True, apply median blur (Default: True).
            :selectzslice (int, optional): z-slice used for analysis (Default: None).
            :selecttime (int, optional): t-slice used for analysis (Default: None).
            :marker_list (list, optional): List of names of markers used for quantification (Default: None).
            :mergedimage (numpy.ndarray, optional): Image with merged cell markers to be used for segmentation (Default: None).
        Returns:
            :table (pandas.DataFrame): Quantification table for segmented cells.
            :rapidobjects (numpy.ndarray): Raw RAPID segmented image.
            :expandobject (numpy.ndarray): RAPID segmented image with nuclei expanded, labeled according to cell IDs.
            :object2rgb (numpy.ndarray): RAPID segmented image with nuclei expanded, with cells randomly colored.
        """

        '''
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
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
            pass
        '''
        if not type(image) == np.ndarray:
            image = rio.read_ome(image, z=selectzslice, t=selecttime)
            image = utils.smoothing(image, gaussianblur=gaussianblur, gaussianblurstd=gaussianblurstd, medianblur=medianblur)
            '''
            if gaussianblur and medianblur:
                image = utils.smoothing(image, gaussianblur=True, gaussianblurstd=gaussianblurstd, medianblur=True)
            elif gaussianblur and not medianblur:
                image = utils.smoothing(image, gaussianblur=True, gaussianblurstd=gaussianblurstd, medianblur=False)
            elif medianblur and not gaussianblur:
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
            else:
                if (len(image.shape) == 5):
                    if (selecttime == None):
                        selecttime = int(image.shape[0] / 2)
                elif (len(image.shape) == 4):
                    selecttime = int(image.shape[0] / 2)
                else:
                    selectzslice = None
                    selecttime = None
            '''
        paddedimage = denoise.check_padding(image, 256)
        if type(maskimage) != np.ndarray:
            maskimage = cv.imread(maskimage,0)
        if not os.path.exists(outfolder):
            os.mkdir(outfolder)
        rapidobjects = (maskimage * 255).astype(np.uint8)
        cv.imwrite(outfolder + "/Obejects.png", rapidobjects)
        if len(marker_list) == 0:
            marker_list = [i for i in range(image.shape[-1])]
        table, coordinates, object2rgb,expandobject = self.quantifyimage(paddedimage,maskimage,object_true=True)
        table = pd.DataFrame(table)
        table.columns = np.hstack([["ID", "X", "Y"], marker_list])
        print(table.values)
        object2rgb = (object2rgb*255).astype(np.uint8)
        cv.imwrite(outfolder + "/Object2rgb.png", object2rgb.astype)
        return table,rapidobjects,expandobject,object2rgb

def RAPIDObject():
    """
    Entry point for object-based segmentation functionality.
    """
    parser = argparse.ArgumentParser(description='RAPID: deep learning algorithm for quantitative analysis of cell type and distribution from high content imaging data')
    parser.add_argument('--membranechannel', type=str, default=500, metavar='N',
                        help="memebrane channels to be merged, each marker must be separtetd by comma [,]  (default: %(default)s)")
    parser.add_argument('--imagepath', type=str, default=0.0001, metavar='LR',
                        help="Path to the tiff file")
    parser.add_argument('--outfolder', type= str, default="/tmp/output",
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
    membranechannel =np.array(args.membranechannel.split(','),dtype=int)
    markernames = np.array(args.markernames.split(','), dtype=str)
    markernames.append("Area")
    markernames.append("Eccentricity")
    markernames.append("Perimeter")
    markernames.append("Major_axis_length")
    for arg in vars(args):
        print(str(arg) + "=" + str(getattr(args, arg)))

    #image = rio.readimage(args.IMAGEPATH)
    objseg.run_object_prediction(image=args.imagepath,membranechannel=membranechannel,outfolder=args.outfolder,gaussianblur=args.gaussianblur,medianblur=args.medianblur,selectzslice=args.selectzslice,marker_list=markernames,mergedimage=None)

'''
def method_searchsort(from_values, to_values, array):
    sort_idx = np.argsort(from_values)
    idx = np.searchsorted(from_values, array, sorter=sort_idx)
    out = to_values[sort_idx][idx]
    return out


def runphenograph(Qtab,mergemarkerlist,expandobjects,outfolder):
    complete_tab =[]
    for tab_len in range(len(Qtab)):
        complete_tab.append(Qtab[tab_len][:, :])
    complete_tab_DF = pd.DataFrame(np.vstack(complete_tab))
    complete_tab_DF.columns = np.hstack(["Label", mergemarkerlist])
    complete_tab_DF.to_csv(outfolder + "/FullObject_segmentation_data.csv")
    complete_tab = np.vstack(complete_tab)
    if (args.normalize):
        phenopgraphin = StandardScaler().fit_transform(complete_tab_DF.values[:, 1:])
    else:
        phenopgraphin = complete_tab_DF.values[:, 1:]
    TESTPATCHPREDO, graph, Q = phenograph.cluster(phenopgraphin, n_jobs=1,resolution_parameter=int(args.PGres), k=int(args.PGnn),primary_metric=str(args.PGdis))
    to_values = TESTPATCHPREDO  # all values from 0 to 1000
    relabeled_table = copy.deepcopy(complete_tab)
    relabeled_table[:, 0] = to_values
    relabledimages = []
    relabledgreyimages = []
    PAL = generatecolormap(int(np.max(TESTPATCHPREDO) + 1) * 2)
    np.save(outfolder + "/" + "color.npy", PAL)
    PAL2 = PAL.flatten()
    PAL0 = np.zeros(768)
    PAL0[0:len(PAL2)] = PAL2
    count_lab = 0
    Slices_object = np.zeros((len(Qtab), int(np.max(TESTPATCHPREDO) + 1), len(mergemarkerlist[-1]) + 3))
    startindex = 0
    for imagelen in range(len(Qtab)):
        from_values = complete_tab_DF['Label'].values[startindex:startindex + len(Qtab[imagelen])]
        to_values = TESTPATCHPREDO[startindex:startindex + len(Qtab[imagelen])]
        relabeled = method_searchsort(from_values, to_values, expandobjects[imagelen].flatten().astype(int))
        startindex += len(Qtab[imagelen])
        relabledgreyimages.append(relabeled.reshape(expandobjects[imagelen].shape))
        cv.imwrite(outfolder + "/RELABELED_Grey" + str(imagelen) + ".png",
                   relabledgreyimages[imagelen][ :, :].astype(np.uint8))
        imgp = PImage.fromarray(relabeled.reshape(expandobjects[0].shape).astype(np.uint8), mode='P')
        imgp.putpalette(list(PAL0.flatten().astype(int)))
        imgp.save(outfolder + "/RELABELED_" + str(imagelen) + ".png")
        relab = cv.imread(outfolder + "/RELABELED_" + str(imagelen) + ".png")
        relabledimages.append(np.asarray(relab))
        tmp_tab = relabeled_table[
                  count_lab:count_lab + len(Qtab[imagelen]) + len(np.unique(relabeled_table[:, 0]))]
        nclusters = len(Slices_object[0, :, ])
        nclusters = np.max(TESTPATCHPREDO)+1
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
    my_data.columns = np.hstack([["Sample", "Cluster", "Pixels"], mergemarkerlist])
    my_data.to_csv(outfolder + "/RAPIDObject_cluster_table.csv")
    tabledata, my_data_scaled, DistMatrix, uniqueClusters = \
        preparedata4mst(
            clustertable=my_data, markerlist=mergemarkerlist,
            pixelcountthreshold=1, zscore=True, color_list=PAL,
            randomseed=0, outfolder=outfolder, clusterheatmap=True,
            include_names=mergemarkerlist)
    final = my_data_scaled.columns
    generatemst(DistMatrix=DistMatrix, normalizeddf=my_data_scaled[final], markerlist=mergemarkerlist,
                pixelcountthreshold=0, zscore=True, color_list=PAL, randomseed=0,
                outfolder=outfolder, clusterheatmap=True, displayMarkeOnMst=mergemarkerlist,
                uniqueClusters=uniqueClusters,
                samplenames=list(np.unique(my_data['Sample'])), displaysingle=False)

'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RAPID: deep learning algorithm for quantitative analysis of cell type and distribution from high content imaging data')
    parser.add_argument('--membranechannel', type=str, default=500, metavar='N',
                        help="memebrane channels to be merged, each marker must be separtetd by comma [,]  (default: %(default)s)")
    parser.add_argument('--imagepath', type=str, default=0.0001, metavar='LR',
                        help="Path to the tiff file")
    parser.add_argument('--outfolder', type= str, default="/tmp/output",
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
    membranechannel =np.array(args.membranechannel.split(','),dtype=int)
    markernames = np.array(args.markernames.split(','), dtype=str)
    for arg in vars(args):
        print(str(arg) + "=" + str(getattr(args, arg)))

    #image = rio.readimage(args.IMAGEPATH)
    #table, rapidobjects, expandobject, object2rgb=objseg.run_object_prediction(image=args.imagepath,membranechannel=membranechannel,outfolder=args.outfolder,gaussianblur=args.gaussianblur,medianblur=args.medianblur,selectzslice=args.selectzslice,marker_list=markernames,mergedimage=None)
    table, rapidobjects, expandobject, object2rgb=objseg.run_object_prediction_from_mask(image=args.imagepath, membranechannel=membranechannel, outfolder=args.outfolder, gaussianblur = args.gaussianblur, medianblur = args.medianblur, selectzslice = args.selectzslice, marker_list = markernames, mergedimage = None,maskimage=None)

