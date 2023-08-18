"""
Author: Nishant Thakur
Purpose: calculating spatial co-distribution of RAPID identified clusters
"""
import imageio as io
import numpy as np
from scipy.spatial import cKDTree
import argparse
import tqdm
import seaborn as sns
import warnings
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import copy
import os
from numpy import inf
from RAPID.util.mst import spatial_mst

matplotlib.use("Agg")
warnings.filterwarnings("ignore")


### TODO: Is this file even necessary? Only used in runrapidzarr, which could just use KNN instead.

### return vals
def randomkdtree(rapid_clusters, radlist, avgwindow=3, outfolder="./", Name=None, percentpixel=0.05, clusterlist=None,
                 cluster_order=None):
    """
    Run spatial co-distribution analysis using a kd tree algorithm.

    Args:
        rapid_clusters (numpy.ndarray): RAPID cluster image array.
        radlist (list): List of radii from the pixel/cluster of interest.
        avgwindow (int, optional): Window size used to calculate the running average of the co-distribution score across different distances (Default: 3).
        outfolder (str, optional): Path to folder where retults will be saved (Default: "./").
        Name (str, optional): Image name to be used for output file (Default: None).
        percentpixel (float, optional): Fraction of random pixels being used for analysis (Default: 0.05).
        clusterlist (list, optional): Total number of clusters identified by the RAPID algorithm (Default: None).
        cluster_order (list, optional): RAPID cluster order, used to keep cross-sample consistency (Default: None).

    :return: *(numpy.ndarray)*:
    :return: *(emptyind)*:
    :return: *(empty)*:
    :return: *(ClusterDend.data2d)*:
    """

    clusters = rapid_clusters.flatten()

    # print ("Total pixels in the image: "+str(len(clusters)))

    # generate list of the x,y indicies of the given image
    y, x = np.indices(rapid_clusters.shape).reshape(-1, len(clusters))

    # create a data table of coordinates anf cluster IDs
    DataTab = np.c_[y, x, clusters]

    # select only those cluster which are present in a image
    DataTab = DataTab[np.isin(DataTab[:, 2], clusterlist)]  # @@@@@@@@@@@@@@@@@@@@@@@@@@

    # remove the background cluster @@@@@@@
    # bgcluster = DataTab[rapid_clusters.shape[0]*5,2]
    # DataTab= DataTab[(DataTab[:,2] !=bgcluster),:]#@@@@@@@@@@@@@@@@@@@@@@@@@@
    print("Total number of pixels in the image: " + str(len(DataTab)))
    randxpercent = DataTab[np.random.choice(len(DataTab), int(len(DataTab) * percentpixel), replace=False),]
    randxpercent[0:len(clusterlist), 2] = clusterlist
    print("Sampled (" + str(percentpixel * 100) + "%) pixels: " + str(len(randxpercent)))

    uni_cluster = clusterlist
    print(str(len(uni_cluster)) + " unique clusters ")

    empty = np.zeros((len(uni_cluster), len(uni_cluster), 3))
    emptyind = np.zeros((len(uni_cluster), len(uni_cluster), 3))

    plt.figure(figsize=(40, 40))
    corMat = np.tril(np.meshgrid(uni_cluster, uni_cluster))[0]
    corMat[0, 0] = 1
    iID, jID = np.nonzero(corMat)
    pbar = tqdm.tqdm(total=len(jID))

    for i in range(len(iID)):
        # for j in range(len(jID)):
        imask = (randxpercent[:, 2] == uni_cluster[iID[i]]);
        iactData = randxpercent[imask, :2]
        jmask = (randxpercent[:, 2] == uni_cluster[jID[i]]);
        jactData = randxpercent[jmask, :2]
        irand = randxpercent[np.random.choice(len(randxpercent), len(iactData), replace=False),]
        jrand = randxpercent[np.random.choice(len(randxpercent), len(jactData), replace=False),]
        treeactDatai = cKDTree(iactData)
        treeactDataj = cKDTree(jactData)
        treerandDatai = cKDTree(irand[:, :2])
        treerandDataj = cKDTree(jrand[:, :2])
        prob_clus = np.log2(treeactDatai.count_neighbors(treeactDataj, radlist, cumulative=False) + 0.01)
        prob_bg = np.log2(treerandDatai.count_neighbors(treerandDataj, radlist, cumulative=False) + 0.01)
        prob = (prob_clus - prob_bg)
        prob[prob == -np.inf] = -10
        prob[prob == np.inf] = 10
        prob[prob == np.nan] = 0
        # print(prob)

        if (len(irand[:, :2]) > 100):
            if (len(jrand[:, :2]) > 100):
                # empty[iID[i], jID[i], 2] = np.max(np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid'))
                # empty[iID[i], jID[i], 2] = np.min(np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid'))
                empty[iID[i], jID[i], 2] = np.max(np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid'))
                # $$$$$empty[iID[i], jID[i], 2] = max(np.max(np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid')), np.min(np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid')), key=abs)
                emptyind[iID[i], jID[i], 2] = np.argmax(
                    np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid'))
                emptyind[iID[i], jID[i], 2] = np.argmin(
                    np.convolve(prob, np.ones((avgwindow,)) / avgwindow, mode='valid'))
                empty[iID[i], jID[i], 0] = uni_cluster[iID[i]]
                empty[iID[i], jID[i], 1] = uni_cluster[jID[i]]
                emptyind[iID[i], jID[i], 0] = uni_cluster[iID[i]]
                emptyind[iID[i], jID[i], 1] = uni_cluster[jID[i]]
            else:
                empty[iID[i], jID[i], 0] = 10
                empty[iID[i], jID[i], 1] = 10
                emptyind[iID[i], jID[i], 0] = 10
                emptyind[iID[i], jID[i], 1] = 10
        else:
            empty[iID[i], jID[i], 0] = 0
            empty[iID[i], jID[i], 1] = 0
            emptyind[iID[i], jID[i], 0] = 0
            emptyind[iID[i], jID[i], 1] = 0
        pbar.update(1)
    pbar.close()
    print("Spatial analysis done..")

    DataTab = np.nan_to_num(empty[:, :, 2].reshape(len(emptyind[0, :]), len(emptyind[1, :])))
    DataTab = DataTab + DataTab.T
    DataTab[DataTab == inf] = 10
    DataTab[DataTab == -inf] = -10
    DataTab[DataTab < -10] = -10
    DataTab[DataTab > 10] = 10
    DataTab = np.nan_to_num(DataTab, 0)
    DataTab = pd.DataFrame(DataTab)
    df = copy.deepcopy(DataTab)
    df.insert(0, "Index", df.index)
    df = pd.melt(df, id_vars="Index")
    df.to_csv(outfolder + "/" + Name + "_CODIST2__tab.csv")
    out = DataTab.unstack().reset_index()
    out.to_csv(outfolder + "/" + Name + "_CODIST_tab.csv")
    pdf_coclus = DataTab
    pdf_coclus.columns = uni_cluster
    pdf_coclus.index = uni_cluster
    pdf_coclus = pdf_coclus.replace(np.inf, 5)
    pdf_coclus = pdf_coclus.replace(-np.inf, -5)
    pdf_coclus = pdf_coclus.replace(np.nan, 0)
    if (len(cluster_order) < 3):
        ClusterDend = sns.clustermap(pdf_coclus + 0.01, row_cluster=True,
                                     col_cluster=True, linewidth=0.05,
                                     yticklabels=True, xticklabels=True,
                                     cmap="RdBu_r", figsize=(pdf_coclus.shape[0] / 2, pdf_coclus.shape[0] / 2),
                                     vmin=-10, center=0, vmax=10)
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.savefig(outfolder + "/" + Name + '_ClusterCodistributionHEATMAP.png', dpi=100)
        spatial_mst(disttable=pdf_coclus, outfolder=outfolder, name=Name)
        pdf_coclus.to_csv(outfolder + "/" + Name + "_CODIST_act_table.csv")
    else:
        pdf_coclus = pdf_coclus.reindex(cluster_order.index)
        pdf_coclus = pdf_coclus[cluster_order.columns]
        ClusterDend = sns.clustermap(pdf_coclus + 0.01, row_cluster=False,
                                     col_cluster=False, linewidth=0.05,
                                     yticklabels=True, xticklabels=True,
                                     cmap="RdBu_r", figsize=(pdf_coclus.shape[0] / 2, pdf_coclus.shape[0] / 2),
                                     vmin=-10, center=0, vmax=10)
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.savefig(outfolder + "/" + Name + '_ClusterCodistributionHEATMAP.png', dpi=100)
        pdf_coclus.to_csv(outfolder + "/" + Name + "_CODIST_act_table.csv")
        spatial_mst(disttable=pdf_coclus, outfolder=outfolder, name=Name)

    return np.round(pdf_coclus.astype(np.int16), 2), emptyind, empty, ClusterDend.data2d


### return val
def random_kdtree_single(rapid_clusters, radlist, avgwindow=3, outfolder="./", Name=None, percentpixel=1,
                         clusterlist=None, cluster_order=None):
    """
    Run spatial co-distribution analysis using a kd tree algorithm.

    Args:
        rapid_clusters (numpy.ndarray): RAPID cluster image array.
        radlist (list): List of radii from the pixel/cluster of interest.
        avgwindow (int, optional): Window size used to calculate the running average of the co-distribution score across different distances (Default: 3).
        outfolder (str, optional): Path to folder where results will be saved (Default: "./").
        Name (str, optional): Image name to be used for output file (Default: None).
        percentpixel (float, optional): Fraction of random pixels being used for analysis (Default: 1).
        clusterlist (list, optional): Total number of clusters identified by the RAPID algorithm (Default: None).
        cluster_order (list, optional): RAPID cluster order, used to keep cross-sample consistency (Default: None).

    Returns:
        :return: finalDf *(pandas.DataFrame)*:
    """

    clusters = rapid_clusters.flatten()
    radlist = np.arange(100)

    # print ("Total pixels in the image: "+str(len(clusters)))

    # generate list of the x,y indicies of the given image
    y, x = np.indices(rapid_clusters.shape).reshape(-1, len(clusters))

    # create a data table of coordinates anf cluster IDs
    DataTab = np.c_[y, x, clusters]

    # select only those cluster which are present in a image
    DataTab = DataTab[np.isin(DataTab[:, 2], clusterlist)]  # @@@@@@@@@@@@@@@@@@@@@@@@@@

    # remove the background cluster @@@@@@@
    bgcluster = DataTab[rapid_clusters.shape[0] * 5, 2]
    DataTab = DataTab[(DataTab[:, 2] != bgcluster), :]  # @@@@@@@@@@@@@@@@@@@@@@@@@@
    print("Total number of pixels in the image: " + str(len(DataTab)))
    randxpercent = DataTab[np.random.choice(len(DataTab), int(len(DataTab) * percentpixel), replace=False),]
    randxpercent[0:len(clusterlist), 2] = clusterlist
    print("Sampled (" + str(percentpixel * 100) + "%) pixels: " + str(len(randxpercent)))

    uni_cluster = clusterlist
    print(str(len(uni_cluster)) + " unique clusters ")

    plt.figure(figsize=(10, 10))
    corMat = np.tril(np.meshgrid(uni_cluster, uni_cluster))[0]
    corMat[0, 0] = 1
    iID, jID = np.nonzero(corMat)
    pbar = tqdm.tqdm(total=len(jID))

    imask = (randxpercent[:, 2] == clusterlist[0]);
    iactData = randxpercent[imask, :2]
    jmask = (randxpercent[:, 2] == clusterlist[1]);
    jactData = randxpercent[jmask, :2]
    irand = randxpercent[np.random.choice(len(randxpercent), len(iactData), replace=False),]
    jrand = randxpercent[np.random.choice(len(randxpercent), len(jactData), replace=False),]
    treeactDatai = cKDTree(iactData)
    treeactDataj = cKDTree(jactData)

    treerandDatai = cKDTree(irand[:, :2])
    treerandDataj = cKDTree(jrand[:, :2])
    prob_clus = np.log2(treeactDatai.count_neighbors(treeactDataj, radlist, cumulative=False)) + 0.00000001
    prob_bg = np.log2(treerandDatai.count_neighbors(treerandDataj, radlist, cumulative=False)) + 0.00000001

    prob = (prob_clus - prob_bg)
    prob[prob == inf] = 10
    prob[prob == -inf] = -10
    prob[prob < -10] = -10
    prob[prob > 10] = 10
    print(radlist, prob)
    finalDf = pd.DataFrame(np.vstack([radlist, prob])).T
    finalDf['Sample'] = Name
    finalDf.columns = ['Distance', 'Score', 'Sample']

    return finalDf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='RAPID: deep learning algorithm for quantitative analysis of cell type and distribution from high content imaging data')
    parser.add_argument('--rcpath', type=str, default=None, metavar='N', help="batch size (default: %(default)s)")
    parser.add_argument('--radlist', type=str, default="1,8,16,24,32,40,48", metavar='N',
                        help="number of epochs to train (default: %(default)s)")
    parser.add_argument('--outfold', type=str, default="Output folder/directory (default: %(default)s)")
    parser.add_argument('--avgwin', type=int, default=3, metavar='LR', help="learning rate (default: %(default)s)")
    args = parser.parse_args()
    rcpath = args.rcpath
    avgwin = args.avgwin

    Name = os.path.split(rcpath)[-1][0:-4]

    img = io.imread(rcpath)
    radlist = np.array(args.radlist.split(','), dtype=str)

    Tab, retind = randomkdtree(img, radlist, avgwin, outfolder=args.outfold, Name=Name)
