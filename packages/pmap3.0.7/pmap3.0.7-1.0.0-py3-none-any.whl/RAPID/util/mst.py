import cv2 as cv
import argparse
import networkx as nx
from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("Agg")
import seaborn as sns
import tqdm
from RAPID.util.utils import *
import os
import imageio as io
import pandas as pd


# https://stackoverflow.com/questions/29481485/creating-a-distance-matrix/45834105
# https://stackoverflow.com/questions/13513455/drawing-a-graph-or-a-network-from-a-distance-matrix

def prep_for_mst(clustertable=None, minclustersize=100, clustersizes=[], includedmarkers=None, clustermin=0.0):
    """
    Prepare data for minimum spanning tree analysis.

    Args:
        clustertable (pandas.DataFrame, optional): RAPID cluster data table (Default: None).
        minclustersize (int, optional): Minimum number of pixels for clusters used in MST analysis (Default: 100).
        clustersizes (list, optional): List of numbers of cells/pixels in each cluster (Default: []).
        outfolder (str, optional): Output folder where results will be saved (Default: None).
        includedmarkers (list, optional): List of names of markers to include in analysis (Default: None).
        clustermin (float, optional): Minimum marker expression threshold for clusters to be included in analysis (Default: 0.0).

    :return: clustertable *(pandas.DataFrame)*: \n
        Dataframe containing filtered and scaled cluster data with excluded clusters removed.
    :return: normdata *(pandas.DataFrame)*: \n
        Dataframe containing normalized RAPID cluster data.
    :return: distancematrix *(numpy.ndarray)*: \n
        Matrix containing pairwise Euclidian distances between clusters.
    :return: uniqueclusters *(pandas.DataFrame)*: \n
        Unique clusters to use for MST and heatmap generation.
    """

    # Filter out clusters with less than minimum number of pixels
    selectedcol = clustersizes > minclustersize
    uniqueclusters = clustertable[selectedcol].iloc[:, :3].astype(int)

    # Filter selected columns for column-wise mean intensity calculation
    clustertable = clustertable[selectedcol]

    # Calculate per-column mean intensity across samples
    clustertable = clustertable.groupby(["Cluster"]).mean()

    # Filter out non-important columns (sample number and pixel count)
    clustertable = clustertable.iloc[:, 2:]
    clustertable = clustertable.loc[:, includedmarkers]

    # Min-max normalization accross colums
    scaler = MinMaxScaler()
    scaler.fit(clustertable.values)
    normdata = scaler.transform(clustertable.values)

    # Cutoff the overflowing (>1) of values
    normdata[normdata > 1] = 1
    normdata = pd.DataFrame(normdata)
    normdata.columns = clustertable.columns
    normdata = normdata.loc[:, includedmarkers]

    # get the selected markers
    normdata.index = clustertable.index.values
    normdata.index = [int(round(x)) for x in normdata.index]

    # set the threshold for the relative expresssion level of the markers
    if len(normdata) <= 1:
        raise ValueError('no relevent clusters are found, please train model for longer time')

    # remove clusters with low expression level for each marker
    normdata = normdata[normdata.max(axis=1) > clustermin]
    normdata.values[normdata.values < 0.1] = 0

    # select the filtered clusters from the main tables
    clustertable = clustertable.loc[normdata.index.values, :]
    uniqueclusters = uniqueclusters[uniqueclusters['Cluster'].isin(normdata.index.values)]

    # Calculate the pairwise euclidean distance between clusters and replace nan with number to avoid error
    distancematrix = np.nan_to_num(distance.cdist(clustertable, clustertable, 'euclidean'))

    return clustertable, normdata, distancematrix, uniqueclusters


def generate_mst(distancematrix=None, normalizeddf=None, colors=None, randomseed=0, outfolder=None,
                 clusterheatmap=False, displaymarkers="all", uniqueclusters=None, samplenames=None,
                 displaysingle=False, values="# Pixels"):
    """
    Using prepared data, generate an MST plot.

    Args:
        distancematrix (numpy.ndarray, optional): Matrix containing pairwise Euclidian distances between clusters (Default: None).
        normalizeddf (pandas.DataFrame, optional): Dataframe containing normalized RAPID cluster data (Default: None).
        colors (numpy.ndarray, optional): List of colors for all the clusters (Default: None).
        randomseed (int, optional): Random seed to be used for reproducibility (Default: 0).
        outfolder: (str, optional): Path to the output folder where data will be saved (Default: None).
        clusterheatmap (bool, optional): If True, generate a heatmap for the quantification (Default: False).
        displaymarkers (list, optional): List of names of markers to be displayed on the MST (Default: "all").
        uniqueclusters (pandas.DataFrame, optional): Unique clusters to use for MST and heatmap generation (Default: None).
        samplenames (list, optional): List of names of the samples included in the analysis (Default: None).
        displaysingle (bool, optional): If true, display the expression os individual markers on MST (Default: False).
        values (str, optional): Objects ("# Pixels" or "# Cells") being used for analysis (Default: "# Pixels").

    :return: my_data_dend *(pandas.DataFrame)*: \n
        DataFrame used to generate MST.
    """

    # convert numpy matrix to networkx format
    G = nx.from_numpy_matrix(distancematrix)

    # Rename the rows to corresponding cluster ID
    RowName = normalizeddf.iloc[[i for i in range(normalizeddf.shape[0])]].astype(int).index.tolist()
    print(normalizeddf)
    if values == "# Pixels":
        newkeys = {}
        for ind in RowName:
            newkeys[ind] = ind+1
        normalizeddf = normalizeddf.rename(index=newkeys)
        print(normalizeddf)

    # Convert list rownames to list and dictionary
    RowName = [round(x) for x in RowName]
    dictionary = dict(zip(G.nodes, RowName))

    # Relabel nodes
    G = nx.relabel_nodes(G, dictionary)

    # Generate minimum spanning tree (MST)
    T = nx.minimum_spanning_tree(G)
    #colors = colors[:,[2,1,0]]

    # generate dendrogram if true
    if clusterheatmap:
        np.random.seed(randomseed)
        my_data_dend = pd.DataFrame(copy.deepcopy(normalizeddf)).T
        plt.figure(figsize=(40, 30))
        ax = plt.axes()
        ax.set_facecolor("grey")
        PerSampleCount = uniqueclusters.pivot(index='Cluster', columns='Sample', values=values)
        # PerSampleCount.columns.value=["40W16","6W3","6W7"]
        PerSampleCount.columns.value = samplenames
        # Min-max normalization per-sample counting
        PerSampleCount = PerSampleCount.fillna(1).astype(int)
        PerSampleCount = (PerSampleCount - PerSampleCount.min()) / (PerSampleCount.max() - PerSampleCount.min())
        PerSampleCount[PerSampleCount > 1] = 1
        color_map = [[] for i in range(PerSampleCount.shape[1])]
        # color_map = [[] for i in range(1)]

        # colormap for normalized pixel counts per-cluster
        for i in range(PerSampleCount.shape[1]):
            if PerSampleCount.shape[1] == 1:
                for j in range(len(PerSampleCount)):
                    color_map[i].append(matplotlib.colors.rgb2hex(
                        (PerSampleCount.iloc[j, 0], 0,
                         1 - PerSampleCount.iloc[j, 0])))
            else:
                for j in range(len(PerSampleCount)):
                    color_map[i].append(matplotlib.colors.rgb2hex(
                        (PerSampleCount.iloc[j, i], 0,
                         1 - PerSampleCount.iloc[j, i])))

        lut = [[] for i in range(PerSampleCount.shape[1])]
        species = pd.Series(np.arange(len(PerSampleCount)))
        for l in range(len(lut)):
            lut[l] = dict(zip(np.arange(len(PerSampleCount)), color_map[l]))
            lut[l] = species.map(lut[l])
        col_colorsR = pd.concat(lut, axis=1)
        col_colorsR.index = my_data_dend.columns.values
        if len(samplenames) > 20:
            ClusterDend = sns.clustermap(my_data_dend + 0.001, row_cluster=True, col_cluster=True, linewidth=0.05,
                                         yticklabels=True, xticklabels=True, cmap="coolwarm", metric='cosine',
                                         figsize=(int(my_data_dend.shape[1] / 2), int(my_data_dend.shape[0] / 2)),
                                         vmin=0, vmax=1)
        else:
            ClusterDend = sns.clustermap(my_data_dend + 0.001, row_cluster=True, col_cluster=True, linewidth=0.05,
                                         yticklabels=True, xticklabels=True, cmap="coolwarm", metric='cosine',
                                         figsize=(int(my_data_dend.shape[1] / 2), int(my_data_dend.shape[0] / 2)),
                                         vmin=0, vmax=1, col_colors=col_colorsR)
        for tick_label in ClusterDend.ax_heatmap.axes.get_xticklabels():
            tick_text = tick_label.get_text()
            tick_label.set_color(colors[int(tick_text)-1, :] / 255)
            if ((colors[int(tick_text)-1, 0] == 255) & (colors[int(tick_text)-1, 1] == 255) & (
                    colors[int(tick_text)-1, 2] == 255)):
                tick_label.set_color("black")
            ClusterDend.ax_heatmap.set_xticklabels(ClusterDend.ax_heatmap.get_xmajorticklabels(), fontsize=12)
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        ClusterDend.data2d.to_csv(outfolder + '/HeatmapRawDataVals.csv')
        plt.savefig(outfolder + '/MeanExpressionHeatmap.png', dpi=100)

    # Marker mean expression overlay onto MST
    plt.figure(figsize=(10, 10))
    ax = plt.axes()
    ax.set_facecolor("#F8F9F9")
    if displaysingle:
        if displaymarkers == "all":
            displaymarkers = normalizeddf.columns
        for marker in displaymarkers:
            color_map = []
            np.random.seed(randomseed)  # keep MST stable

            # Generate coloramap for each node based on mean expression level, bright red mean more expression
            for node in range(len(T.nodes)):
                color_map.append(matplotlib.colors.rgb2hex(
                    (normalizeddf[marker].values[node], 0.5, 1 - normalizeddf[marker].values[node])))

            # Overlay marker mean expression on each RAPID cluster in MST
            nx.draw_networkx(T, node_color=color_map, with_labels=True,
                             node_size=100, font_size=5, font_family='sans-serif')

            # Plot and save MST for each marker
            plt.show(block=True)
            plt.title(marker)
            plt.savefig(outfolder + "/Mst_" + marker + ".png",
                        format="PNG", dpi=300)

    # Get RAPID's colored output image as colormap
    plt.figure(figsize=(10, 10))
    ax = plt.axes()
    ax.set_facecolor("#BFC9CA")
    color_map = []
    # np.random.seed(randomseed)
    for node in T:
        color_map.append(matplotlib.colors.rgb2hex(colors[int(node)-1, :] / 255))

    # Draw mst with networkx function
    nx.draw_networkx(T, node_color=color_map, with_labels=True, node_size=50, font_size=5, font_family='sans-serif')

    # Plot and save MST to png file
    plt.show(block=False)
    plt.title("RAPID clusters")
    plt.savefig(outfolder + "/MinimumSpanningTree.png", format="PNG", dpi=300)
    return my_data_dend


def save_clusters(greyimg=None, colors=None, outfolder=None, randomseed=0, outfilename=None, clusters=None):
    """
    Save individual clusters from a specified labeled image, according to a user-defined colormap.

    Args:
        greyimg (numpy.ndarray, optional): RAPID greyscale cluster image array (Default: None).
        colors (list, optional): List of colors to be used for the clustered image (Default: None).
        outfolder (str, optional): Path to output folder where data will be saved (Default: None).
        randomseed (int, optional): Random seed to be used for reproducibility (Default: 0).
        outfilename (str, optional): Name of output file being saved (Default: None).
        clusters (int, optional): List of the cluster IDs to be included (Default: None).
    """
    np.random.seed(randomseed)
    # grab and save pixels for each cluster into respective png files
    pbar = tqdm.tqdm(total=len(clusters))
    for i in range(len(clusters)):
        img = np.zeros((greyimg.shape[0], greyimg.shape[1], 3), dtype=np.uint8)
        mask = (greyimg == clusters[i])
        img[mask] = colors[clusters[i], :].astype(np.uint8)
        name = os.path.split(outfilename)[-1][0:-4]
        cv.imwrite(f"{outfolder}/RAPID_Cluster{name}_{clusters[i]}.jpeg", img[:, :, [0, 1, 2]])
        pbar.update(1)
    pbar.close()


def spatial_mst(disttable=None, outfolder=None, name=None):
    """
    Generate Minimum Spanning Tree (MST) for spatial clustering.

    Args:
        disttable (numpy.ndarray, optional): Matrix of distances between clusters for spatial co-distribution (Default: None).
        outfolder (str, optional): Path for output folder where data will be saved (Default: None).
        name (str, optional): Name of file being saved (Default: None).

    :return: T *(NetworkX.Graph)*: \n
        MST graph.
    """

    color_list = np.load(outfolder + "/../color.npy")
    disttable = pd.DataFrame(disttable)
    distancematrix = np.nan_to_num(distance.cdist(disttable, disttable, 'euclidean'))

    # convert numpy matrix to networkx format
    G = nx.from_numpy_matrix(distancematrix)

    # Rename the rows to corresponding cluster ID
    RowName = disttable.iloc[[i for i in range(disttable.shape[0])]].astype(int).index.tolist()

    # Convert list rownames to list and dictionary
    # RowName = list(map(round, RowName))
    RowName = [round(x) for x in RowName]

    dictionary = dict(zip(G.nodes, RowName))

    # Relabel nodes
    G = nx.relabel_nodes(G, dictionary)

    # Generate minimum spanning tree (MST)
    T = nx.minimum_spanning_tree(G)
    color_list2 = np.zeros_like(color_list)
    color_list2[:, 0] = color_list[:, 2]
    color_list2[:, 1] = color_list[:, 1]
    color_list2[:, 2] = color_list[:, 0]

    # plt.figure(figsize=(10, 10))
    # ax = plt.axes()
    # ax.set_facecolor("#F8F9F9")

    # Get RAPID's colored output image as colormap
    plt.figure(figsize=(10, 10))
    ax = plt.axes()
    ax.set_facecolor("#BFC9CA")
    color_map = []
    # np.random.seed(randomseed)

    for node in T:
        color_map.append(matplotlib.colors.rgb2hex(color_list2[int(node), :] / 255))

    # Draw mst with networkx function
    nx.draw_networkx(T, node_color=color_map, with_labels=True, node_size=50,
                     font_size=5, font_family='sans-serif')

    # Plot and save MST to png file
    plt.show(block=False)
    plt.title("Minimum spanning tree for Spatial co-distribution ")
    plt.savefig(outfolder + "/" + name + "RAPID_SPATMST.png", format="PNG", dpi=300)
    return T


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RAPID_MST: RAPID sub-package to create minimum spanning tree')
    parser.add_argument('--rcg', type=str, default=None, metavar='N',
                        help="RAPID cluster image mask (default: %(default)s)")
    parser.add_argument('--rfold', type=str, default=None, metavar='N',
                        help="RAPID quantification table (default: %(default)s)")
    parser.add_argument('--OUTFOLD', type=str, default="./", help="Output folder/directory (default: %(default)s)")
    parser.add_argument('--clusterlist', type=str, default="", metavar='N',
                        help="Cluster list to generate minimum spanning tree (separated by ',') (default: %(default)s)")
    parser.add_argument('--saverc', type=bool, default=False, metavar='N',
                        help="Save individual RAPIDcluster images (default: %(default)s)")

    args = parser.parse_args()
    rcg = args.rcg
    rfold = args.rfold

    my_data = pd.read_csv(rfold + "/PixelClusterAvgExpressionVals.csv",
                          sep=",", header=0, index_col=0)
    markernames = my_data.columns[3:]

    grey = io.imread(rcg)

    clusters = np.unique(grey)
    if args.clusterlist == "":
        clusterlist = clusters
    else:
        clusterlist = np.array(args.clusterlist.split(','), dtype=str)

    include_names = markernames
    colors = np.load(rfold + "/color.npy")

    tabledata, my_data_scaled, distancematrix, uniqueclusters = prep_for_mst(clustertable=my_data, minclustersize=10000,
                                                                             clustersizes=my_data["# Pixels"],
                                                                             includedmarkers=include_names)
    clusters = my_data_scaled.index
    displayMarkeOnMst = "all"
    exclude = markernames
    final = include_names
    samplenames = np.unique(my_data["Sample"])
    mst = generate_mst(distancematrix=distancematrix, normalizeddf=my_data_scaled[final], colors=colors,
                       randomseed=0, outfolder="/tmp/", clusterheatmap=True, displaymarkers=displayMarkeOnMst,
                       uniqueclusters=uniqueclusters, samplenames=samplenames)
    if args.saverc:
        save_clusters(greyimg=grey, colors=colors, outfolder=rfold, randomseed=181, outfilename=rcg,
                      clusters=clusterlist)

'''
https://stackoverflow.com/questions/48173798/additional-row-colors-in-seaborn-cluster-map
'''
