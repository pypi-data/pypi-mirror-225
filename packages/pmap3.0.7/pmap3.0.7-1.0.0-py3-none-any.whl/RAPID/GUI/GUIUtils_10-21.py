import os
import PyQt5
import copy
import matplotlib
matplotlib.use("Agg")
import re
import pandas as pd
import seaborn as sns
from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QFontMetrics
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QGridLayout, QCheckBox
from scipy.spatial import cKDTree
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QSizePolicy, QGroupBox, QScrollArea, QVBoxLayout
from RAPID.util.utils import generate_colormap
import tifffile
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import gc
import logging

gc.enable()


### TODO: Compare with previous version from Drive to make sure names of variables referenced elsewhere weren't changed



### TODO: Change "add" to something more pertinent.
### TODO: Reformat function names.

class BiaxialGate(QDialog):
    """
    Prompt user to define which cell markers and parameters for Biaxial Gating.

    Args:
        markernames (list): List of names of each of the cell markers.
        imagenames (list): List of names of each of the images.
        hasclustered (bool): True if object clustering has been run at least once, otherwise False.
        groupsnames (list): List of names of experimental conditions to use for coloring.
    """

    def __init__(self, markernames, imagenames, hasclustered, groupsnames):
        QDialog.__init__(self)
        self.setWindowTitle("Biaxial Gate Parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formlayout = QFormLayout(self)
        labelchan1 = QLabel("Marker 1: ")
        labelchan2 = QLabel("Marker 2: ")
        labelcolor = QLabel("Color: ")
        scalingnormlabel = QLabel("Axis Scaling: ")
        paramnames = markernames + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        self.chans1 = QComboBox(self)
        self.chans2 = QComboBox(self)
        self.color = QComboBox(self)
        self.scalingnorm = QComboBox(self)
        self.OK = False
        self.dict = {}
        self.hasclustered = hasclustered
        self.groupsnames = groupsnames
        self.color.addItem("---(Optional)---")
        for marker in paramnames:
            self.chans1.addItem(marker)
            self.chans2.addItem(marker)
            self.color.addItem(marker)
            self.dict[marker] = paramnames.index(marker) + 1
        self.scalingnorm.addItem("None")
        self.scalingnorm.addItem("Log2")
        self.scalingnorm.addItem("Log10")
        formlayout.addRow(labelchan1, self.chans1)
        formlayout.addRow(labelchan2, self.chans2)
        formlayout.addRow(labelcolor, self.color)
        self.buttonlist = []
        if hasclustered:
            box1 = QCheckBox("Color according to individual clusters")
            box1.setChecked(True)
            formlayout.addRow(box1)
            self.buttonlist.append(box1)
            box2 = QCheckBox("Color according to combined clusters")
            box2.setChecked(True)
            formlayout.addRow(box2)
            self.buttonlist.append(box2)
        if len(groupsnames) > 0:
            for i in range(len(groupsnames)):
                box = QCheckBox("Color according to group assignment: " + groupsnames[i])
                box.setChecked(True)
                formlayout.addRow(box)
                self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formlayout.addRow("", QLabel(""))
        self.imagenames = imagenames
        if len(imagenames) > 1:
            self.imageslist = imagenames
            labelimage = QLabel("Image: ")
            self.images = QComboBox(self)
            for image in imagenames:
                self.images.addItem(image)
            formlayout.addRow(labelimage, self.images)
        formlayout.addRow(scalingnormlabel, self.scalingnorm)
        formlayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.colorbygroups = []
        if self.hasclustered:
            self.colorbyindivclusters = self.buttonlist[0].isChecked()
            self.colorbycombclusters = self.buttonlist[1].isChecked()
            if len(self.groupsnames) > 0:
                for i in range(2, len(self.buttonlist)):
                    if self.buttonlist[i].isChecked():
                        self.colorbygroups.append(i - 2)
        elif len(self.groupsnames) > 0:
            for i in range(len(self.buttonlist)):
                if self.buttonlist[i].isChecked():
                    self.colorbygroups.append(i)
        if len(self.imagenames) > 1:
            self.imageindex = self.imageslist.index(self.images.currentText())
        else:
            self.imageindex = 0
        self.chan1 = self.chans1.currentText()
        self.chan2 = self.chans2.currentText()
        self.color = self.color.currentText()
        self.norm = self.scalingnorm.currentText()
        self.OK = True
        self.close()


class BiaxialUMAPIterations(QDialog):
    """
    Prompt user to indicate which plot they would like to use when conducting analysis that depends on user-defined
    shapes overlaid on plots.

    Args:
        areumapplots (list): List representing which plots correspond to UMAP or Biaxial Gating.
    """

    def __init__(self, areumapplots):
        QDialog.__init__(self)
        self.setWindowTitle("Select plot to display from")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.iteration = 0
        formLayout = QFormLayout(self)
        labelimage = QLabel("Plot: ")
        self.iterations = QComboBox(self)
        self.OK = False
        umapcount = 1
        biaxialcount = 1
        for isumap in areumapplots:
            if isumap:
                self.iterations.addItem(f"UMAP {umapcount}")
                umapcount += 1
            else:
                self.iterations.addItem(f"Biaxial {biaxialcount}")
                biaxialcount += 1
        formLayout.addRow(labelimage, self.iterations)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user selection.
        """
        self.iteration = int(self.iterations.currentIndex())
        self.OK = True
        self.close()


class ChannelOrder4D(QDialog):
    """
    If loading 4D images, prompt user to indicate whether the images are in (c,z,x,y) or (z,c,x,y) order.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Select Channel Order")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.cfirst = False
        button1 = QPushButton()
        button1.setText("(C, Z, X, Y)")
        button1.clicked.connect(self.c_first)
        button2 = QPushButton()
        button2.setText("(Z, C, X, Y)")
        button2.clicked.connect(self.z_first)
        formLayout = QFormLayout(self)
        formLayout.addRow(button1)
        formLayout.addRow(button2)

    def c_first(self):
        """
        Called when user indicates (c,z,x,y) channel order. Close window and store this as a boolean variable.
        """
        self.cfirst = True
        self.OK = True
        self.close()

    def z_first(self):
        """
        Called when user indicates (z,c,x,y) channel order. Close window and store this as a boolean variable.
        """
        self.OK = True
        self.close()


class ClusteringAlgorithm(QDialog):
    """
    Prompt user to indicate which object-based clustering algorithm to use and which round of segmented results to
    analyze.

    Args:
        segresultnames (list): List of names of segmentation results.
        issubclustering (bool, optional): True if performing subclustering, False if clustering full segmented image.
    """

    def __init__(self, segresultnames, issubclustering=False):
        QDialog.__init__(self)
        self.issubclustering = issubclustering
        self.setWindowTitle("Select Algorithm")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.alg = ""
        self.dirpath = ""
        self.segresultnames = segresultnames
        rapidbutton = QPushButton()
        rapidbutton.setText("RAPID")
        rapidbutton.clicked.connect(self.useRAPID)
        phenobutton = QPushButton()
        phenobutton.setText("Phenograph")
        phenobutton.clicked.connect(self.usePhenograph)
        scipybutton = QPushButton()
        scipybutton.setText("SciPy algos")
        scipybutton.clicked.connect(self.useSciPy)
        loadmodelbutton = QPushButton()
        loadmodelbutton.setText("Load Model")
        loadmodelbutton.clicked.connect(self.useLoadedModel)
        formLayout = QFormLayout(self)
        if not issubclustering and len(segresultnames) > 1:
            labelimage = QLabel("Image:")
            self.images = QComboBox(self)
            for image in segresultnames:
                self.images.addItem(image)
            formLayout.addRow(labelimage, self.images)
            formLayout.addRow("", QLabel(""))
        formLayout.addRow(rapidbutton)
        formLayout.addRow(scipybutton)
        formLayout.addRow(phenobutton)
        formLayout.addRow(loadmodelbutton)

    def useRAPID(self):
        """
        Called when user chooses to use the RAPID algorithm. Close window and store this selection.
        """
        self.OK = True
        self.alg = "RAPID"
        if not self.issubclustering:
            if len(self.segresultnames) > 1:
                self.image = self.images.currentText()
                self.imageindex = self.segresultnames.index(self.image)
            else:
                self.image = self.segresultnames[0]
                self.imageindex = 0
        self.close()

    def usePhenograph(self):
        """
        Called when user chooses to use the Phenograph algorithm. Close window and store this selection.
        """
        self.alg = "Phenograph"
        self.OK = True
        if not self.issubclustering:
            if len(self.segresultnames) > 1:
                self.image = self.images.currentText()
                self.imageindex = self.segresultnames.index(self.image)
            else:
                self.image = self.segresultnames[0]
                self.imageindex = 0
        self.close()

    ### TODO: Add these as separate options.
    def useSciPy(self):
        """
        Called when user chooses to use a SciPy algorithm. Close window and store this selection.
        """
        self.alg = "SciPy"
        self.OK = True
        if not self.issubclustering:
            if len(self.segresultnames) > 1:
                self.image = self.images.currentText()
                self.imageindex = self.segresultnames.index(self.image)
            else:
                self.image = self.segresultnames[0]
                self.imageindex = 0
        self.close()

    def useLoadedModel(self):
        """
        Called when user chooses to load a previously-trained RAPID model. Close window and store this selection.
        """
        self.alg = "Pretrained"
        self.OK = True
        self.dirpath = QFileDialog().getOpenFileName(filter="*.pth")[0].split("/")
        if not self.issubclustering:
            if len(self.segresultnames) > 1:
                self.image = self.images.currentText()
                self.imageindex = self.segresultnames.index(self.image)
            else:
                self.image = self.segresultnames[0]
                self.imageindex = 0
        self.close()


class ColorAssign(QDialog):
    """
    Drag-and-drop popup window to allow the user to indicate the colors for each of the clusters in the indicated
    results.
    https://pythonpyqt.com/pyqt-qlistwidget/

    Args:
        numclusters (int): Number of clusters to define the number of drag-and-drop boxes.
        colorlistdf (pandas.DataFrame): List of colors that the user may choose from.
        viewer (napari.Viewer): Viewer object for the RAPID GUI.
    """

    def __init__(self, numclusters, colorlistdf, viewer):
        self.viewer = viewer
        self.numclusters = numclusters
        self.colorlistdf = colorlistdf
        self.OK = False
        super(ColorAssign, self).__init__()
        self.setWindowTitle('Assign colors to clusters')
        self.main_layout = QVBoxLayout()
        self.main_layout = QFormLayout(self)
        self.colorlist = colorlistdf.index.values
        print(self.colorlist)
        self.nametextbox = QLineEdit("Colormap list " + str(len(self.colorlist)))
        self.main_layout.addWidget(self.nametextbox)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.labeltlist = {}
        self.widgetlist = {}

        for nw in range(self.numclusters):
            key = str(nw)
            if nw < numclusters:
                dropwidget = QListWidget()
                dropwidget.setAcceptDrops(True)
                self.widgetlist[key] = dropwidget
                print(self.colorlist[nw])
                self.widgetlist[key].addItem(self.colorlist[nw])
                item = self.widgetlist[key].item(0)
                rgb_list = colorlistdf.loc[self.colorlist[nw],].values
                print("COLOR......", rgb_list)
                item.setBackground(QtGui.QColor(rgb_list[0], rgb_list[1], rgb_list[2]))
                self.widgetlist[key].setDragEnabled(True)
                self.widgetlist[key].setDragDropOverwriteMode(True)
                self.widgetlist[key].setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.widgetlist[key].setDefaultDropAction(Qt.MoveAction)
                self.main_layout.addRow(QLineEdit("Cluster" + str(key)), self.widgetlist[key])

        key = str(nw + 1)
        dropwidget = QListWidget()
        dropwidget.setAcceptDrops(True)
        self.widgetlist[key] = dropwidget
        itemid = 0
        for cl in range(nw + 1, len(self.colorlist)):
            print(self.colorlist[cl])
            self.widgetlist[key].addItem(self.colorlist[cl])
            item = self.widgetlist[key].item(itemid)
            rgb_list = colorlistdf.loc[self.colorlist[cl],].values
            print(rgb_list)
            item.setBackground(QtGui.QColor(rgb_list[0], rgb_list[1], rgb_list[2]))
            itemid += 1
        self.widgetlist[key].setDragEnabled(True)
        self.widgetlist[key].setDragDropOverwriteMode(True)
        self.widgetlist[key].setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.widgetlist[key].setDefaultDropAction(Qt.MoveAction)
        self.main_layout.addRow(QLineEdit("Colormap"), self.widgetlist[key])
        self.main_layout.addWidget(okButton)
        groupbox = QGroupBox()
        groupbox.setLayout(self.main_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        self.newcolorlist = np.zeros((self.numclusters, 3))
        for nw in range(self.numclusters):
            if self.widgetlist[str(nw)].count() > 0:
                print(self.widgetlist[str(nw)].item(0).text())
                self.newcolorlist[nw, :] = self.colorlistdf.loc[
                    self.widgetlist[str(nw)].item(0).text(),].values.reshape(-1).astype(int)
            else:
                self.newcolorlist[nw, :] = (255, 255, 255)
        self.OK = True
        self.close()


class DefinePatches(QDialog):
    """
    When performing pixel-based clustering, prompt user to indicate whether they would like to define patches manually
    to use for training, or to have pixels randomly sampled.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Define Training Patches")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.randompatchgeneration = True
        randombutton = QPushButton()
        randombutton.setText("Random patch generation")
        randombutton.clicked.connect(self.random)
        userdefinedbutton = QPushButton()
        userdefinedbutton.setText("User-defined patches")
        userdefinedbutton.clicked.connect(self.userDefined)
        formLayout = QFormLayout(self)
        formLayout.addRow(randombutton)
        formLayout.addRow(userdefinedbutton)

    def random(self):
        """
        Called when user indicates random patch generation. Close window and store selection.
        """
        self.OK = True
        self.close()

    def userDefined(self):
        """
        Celled when user indicates self-defined training patches. Close window and store selection.
        """
        self.OK = True
        self.randompatchgeneration = False
        self.close()


class EditOptions(QDialog):
    """
    Prompt user to indicate whether to edit all images individually, apply edits from one image to all other images,
    or load conditions for edits that have previously been applied.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Image Edit Options")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.allimages = True
        self.loadedits = False
        allbutton = QPushButton()
        allbutton.setText("Edit all images")
        allbutton.clicked.connect(self.all_images)
        onebutton = QPushButton()
        onebutton.setText("Apply edits from one image to all others")
        onebutton.clicked.connect(self.one_image)
        loadeditsbutton = QPushButton()
        loadeditsbutton.setText("Load edits from previous session")
        loadeditsbutton.clicked.connect(self.load_edits)
        formLayout = QFormLayout(self)
        formLayout.addRow(allbutton)
        formLayout.addRow(onebutton)
        formLayout.addRow(loadeditsbutton)

    def all_images(self):
        """
        Called when user chooses to edit all images. Close window and store selection.
        """
        self.OK = True
        self.close()

    def one_image(self):
        """
        Called when user chooses to apply edits from one image to all others. Close window and store selection.
        """
        self.allimages = False
        self.OK = True
        self.close()

    def load_edits(self):
        """
        Called when user chooses to load edits from a previous session. Close window and store selection.
        """
        self.loadedits = True
        self.OK = True
        self.close()


### TODO: "Both" option first.
class GreyColorImages(QDialog):
    """
    Prompt user to indicate whether they would like to generate colored images, greyscale label images, or both, for
    their results.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.OK = False
        self.setWindowTitle("Output Image(s) to generate")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formlayout = QFormLayout(self)

        colbutton = QPushButton()
        colbutton.setText("Colored Image (larger)")
        colbutton.clicked.connect(self.color_selected)
        formlayout.addRow(colbutton)

        greybutton = QPushButton()
        greybutton.setText("Greyscale Label Image (smaller)")
        greybutton.clicked.connect(self.grey_selected)
        formlayout.addRow(greybutton)

        bothbutton = QPushButton()
        bothbutton.setText("Both")
        bothbutton.clicked.connect(self.both_selected)
        formlayout.addRow(bothbutton)

    def color_selected(self):
        """
        Called when user selects to generate only the colored image. Close window and store selection.
        """
        self.color = True
        self.grey = False
        self.OK = True
        self.close()

    def grey_selected(self):
        """
        Called when user selects to generate only the grey image. Close window and store selection.
        """
        self.color = False
        self.grey = True
        self.OK = True
        self.close()

    def both_selected(self):
        """
        Called when user selects to generate both grey and colored images. Close window and store selection.
        """
        self.color = True
        self.grey = True
        self.OK = True
        self.close()


class GroupAssign(QDialog):
    """
    Create a widget to allows the user to assign each image to different experimental groups.

    Args:
        numclusters (int): Number of user-defined groups.
        imagenames (list): List of names of each of the images.
        viewer (napari.Viewer): Viewer object for the RAPID GUI.
        groupsnames (list): List of names of experimental conditions that have already been defined.
    """

    # https://pythonpyqt.com/pyqt-qlistwidget/
    def __init__(self, numclusters, imagenames, viewer, groupsnames):
        self.viewer = viewer
        self.numclusters = numclusters
        self.groupsnames = groupsnames
        super(GroupAssign, self).__init__()
        self.setWindowTitle('Drag and Drop Images into Groups')
        self.main_layout = QVBoxLayout()
        self.imagenames = imagenames
        self.nametextbox = QLineEdit(f"Experimental Conditions {len(groupsnames)}")
        self.main_layout.addWidget(self.nametextbox)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.labeltlist = {}
        self.widgetlist = {}
        for nw in range(self.numclusters):
            # self.right_widget.addItems(pre_list)
            key = str(nw)
            if nw == 0:
                self.widgetlist[key] = QListWidget()
                self.widgetlist[key].setAcceptDrops(True)
                self.widgetlist[key].addItems(self.imagenames)
                self.widgetlist[key].setDragEnabled(True)
                self.widgetlist[key].setDragDropOverwriteMode(True)
                self.widgetlist[key].setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.widgetlist[key].setDefaultDropAction(Qt.MoveAction)
                self.labeltlist[key] = QLineEdit(f"group{key}")
                self.main_layout.addWidget(self.labeltlist[key])
                self.main_layout.addWidget(self.widgetlist[key])
            else:
                self.widgetlist[key] = QListWidget()
                self.widgetlist[key].setAcceptDrops(True)
                self.widgetlist[key].setDragEnabled(True)
                self.widgetlist[key].setDragDropOverwriteMode(True)
                self.widgetlist[key].setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.widgetlist[key].setDefaultDropAction(Qt.MoveAction)
                self.labeltlist[key] = QLineEdit(f"group{key}")
                self.main_layout.addWidget(self.labeltlist[key])
                self.main_layout.addWidget(self.widgetlist[key])
        self.main_layout.addWidget(okButton)
        self.setLayout(self.main_layout)

    def add(self):
        """
        Close window and store user selections.
        """
        if self.nametextbox.text() in self.groupsnames:
            display_error_message("Name already exists",
                                  "Please provide a name that is not already being used")
            self.close()
            self.__init__(self.numclusters, self.imagenames, self.viewer, self.groupsnames)
            self.exec()
        self.namelist = {}
        for nw in range(self.numclusters):
            if self.widgetlist[str(nw)].count() > 0:
                for x in range(self.widgetlist[str(nw)].count()):
                    self.namelist[self.widgetlist[str(nw)].item(x).text()] = self.labeltlist[str(nw)].text()
        self.name = self.nametextbox.text()
        self.close()


class ImageEditingMarkers(QDialog):
    """
    Prompt user to select which cell markers to apply edits to.

    Args:
        viewer (napari.Viewer): Viewer object for the RAPID GUI.
        markernames (list): List of names of cell markers that the filter will be applied to.
    """

    def __init__(self, viewer, markernames):
        QDialog.__init__(self)
        self.setWindowTitle("Markers to apply filter to:")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        for marker in markernames:
            box = QCheckBox(marker)
            box.setChecked(viewer.layers[marker].visible)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton, okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall, selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall, deselall)
        groupbox = QGroupBox()
        groupbox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        self.markernums = []
        for i in range(len(self.buttonlist)):
            if self.buttonlist[i].isChecked():
                self.markernums.append(i)
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)


class ImageRes(QDialog):
    """
    Prompt user to indicate the resolution of their image(s), to be used for nucleus expansion during segmentation.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Image Resolution")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.resolution = QLineEdit("0.284")
        reslabel = QLabel("Pixel resolution (μm):")
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(reslabel, self.resolution)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user input.
        """
        newstr = re.sub('[^0-9.]', '', self.resolution.text())
        newstr = newstr.replace("/", "")
        newstr = newstr.replace("\\", "")
        subs = newstr.split(".")
        subs.insert(1, ".")
        self.imageres = float("".join(subs))
        self.OK = True
        self.close()


### TODO: Test this
class LoadMatrix(QDialog):
    """
    Prompt user to select the path for the file containing the ordered list of cell markers for each image being loaded.

    Args:
        outfolder (str): Path to the output folder to serve as the default in the popup dialog.
    """

    def __init__(self, outfolder):
        QDialog.__init__(self)
        self.OK = False
        self.outfolder = outfolder

        loadmatrixbutton = QPushButton()
        loadmatrixbutton.setText("Load matrix of markers (.csv, .txt)")
        loadmatrixbutton.clicked.connect(self.load_matrix)
        formLayout = QFormLayout(self)
        formLayout.setAlignment(Qt.AlignCenter)
        formLayout.addRow(loadmatrixbutton)

    def load_matrix(self):
        """
        Called when user selects to load a matrix of markers. Provide popup window to allow them to select the path to
        the matrix.
        """
        dialog = QFileDialog()
        dirpath = dialog.getOpenFileName(filter="*.csv *.txt")
        log_actions(self.outfolder, f"Markers Matrix: Path ({dirpath}), ")
        if dirpath[0] != '':
            with open(dirpath[0], encoding='utf-8-sig') as f:
                markerslist = []
                line = f.readline()
                while line:
                    markers = line.replace("\"", "").rstrip().split(",")
                    if len(markers[1:]) != len(set(markers[1:])):
                        display_error_message("Duplicate marker names detected",
                                              "Please make sure each marker has a distinct name for each image")
                        self.close()
                        self.__init__()
                        self.exec()
                    markerslist.append(line.replace("\"", "").rstrip().split(","))
                    line = f.readline()
            markerslist = [x for x in markerslist if x != ['']]
            print(markerslist)
            self.imagenames = [markers[0] for markers in markerslist]
            print(self.imagenames)
            markerslist = [markers[1:] for markers in markerslist]
            print(markerslist)
            intersection = markerslist[0]
            for i in range(1, len(markerslist)):
                list = []
                for j in intersection:
                    l = [re.sub('[^a-zA-Z0-9]', '', marker).lower() for marker in markerslist[i]]
                    if re.sub('[^a-zA-Z0-9]', '', j).lower() in l:
                        list.append(j)
                intersection = list
            print(intersection)
            indiceslist = []
            for i in range(len(markerslist)):
                indices = []
                currentmarkerslist = [re.sub('[^a-zA-Z0-9]', '', marker).lower() for marker in markerslist[i]]
                intersect = [re.sub('[^a-zA-Z0-9]', '', cm).lower() for cm in intersection]
                for marker in intersect:
                    indices.append(currentmarkerslist.index(marker))
                indiceslist.append(indices)
            print(indiceslist)
            self.matrix = True
            self.markers = ",".join(intersection).rstrip()
            self.indiceslist = indiceslist
            self.OK = True
            self.close()
        else:
            pass


class LoadModel(QDialog):
    """
    When performing pixel-based clustering, prompt user to indicate whether they would like to train a new model, or to
    load a previously-trained model.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Define Training Patches")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.load = False
        newmodelbutton = QPushButton()
        newmodelbutton.setText("Train New Model")
        newmodelbutton.clicked.connect(self.newmodel)
        loadmodelbutton = QPushButton()
        loadmodelbutton.setText("Load Model")
        loadmodelbutton.clicked.connect(self.loadingmodel)
        formLayout = QFormLayout(self)
        formLayout.addRow(newmodelbutton)
        formLayout.addRow(loadmodelbutton)

    def newmodel(self):
        """
        Called when user selects to train a new model. Close window and store selection.
        """
        self.OK = True
        self.close()

    def loadingmodel(self):
        """
        Called when user selects to use a pre-trained model. Close window and store selection.
        """
        self.load = True
        self.dirpath = QFileDialog().getOpenFileName(filter="*.pth")[0].split("/")
        if self.dirpath != [""]:
            self.OK = True
        self.close()


class LoadModelNormalize(QDialog):
    """
    Prompt user to select which normalization algorithm, if any, to use for data preprocessing before clustering.

    Args:
        ispixelbased (bool): True if preprocessing for pixel-based clustering, False if for object-based.
    """

    def __init__(self, ispixelbased):
        QDialog.__init__(self)
        self.setWindowTitle("Normalization")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.ispixelbased = ispixelbased
        okbutton = QPushButton()
        okbutton.setText("OK")
        okbutton.clicked.connect(self.add)
        Labelnorm = QLabel("Normalization:")
        self.Textnorm = QComboBox()
        if ispixelbased:
            self.Textnorm.addItem("None")
            self.Textnorm.addItem("zscore")
            self.Textnorm.addItem("log2")
            self.Textnorm.addItem("log10")
            self.Textnorm.addItem("all (PCA)")
            self.Textnorm.addItem("all (no PCA)")
        else:
            self.Textnorm.addItem("True")
            self.Textnorm.addItem("False")
        formLayout = QFormLayout(self)
        formLayout.addRow(Labelnorm, self.Textnorm)
        if ispixelbased:
            self.Denoise = QComboBox()
            self.Denoise.addItem("None")
            self.Denoise.addItem("Denoise")
            self.Denoise.addItem("Binarize")
            formLayout.addRow(QLabel("Denoising:"), self.Denoise)
        formLayout.addRow(okbutton, okbutton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.OK = True
        if self.ispixelbased:
            self.denoise = self.Denoise.currentText()
        self.normalize = self.Textnorm.currentText()
        self.pca = False
        if self.normalize == "all (PCA)":
            self.normalize = "all"
            self.pca = True
        elif self.normalize == "all (no PCA)":
            self.normalize = "all"
        self.close()


class LoadModelOptions(QDialog):
    """
    Prompt user to indicate whether to use a pretrained model only for prediction, or to use it as a starting point for
    further training.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Use model for...")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.prediction = True
        prediction = QPushButton()
        prediction.setText("Prediction")
        prediction.clicked.connect(self.predict)
        training = QPushButton()
        training.setText("Further training")
        training.clicked.connect(self.furthertraining)
        formLayout = QFormLayout(self)
        formLayout.addRow(prediction)
        formLayout.addRow(training)

    def predict(self):
        """
        Called when user selects to use the loaded model for prediction. Close window and store selection.
        """
        self.OK = True
        self.close()

    def furthertraining(self):
        """
        Called when user selects to train with the pretrained model as the starting point. Close window and store
        selection.
        """
        self.prediction = False
        self.OK = True
        self.close()


### TODO: Test this out (loadcsv moved)
class LoadObjectClusters(QDialog):
    """
    Prompt user to define the path to object-based clustering results to load into the RAPID GUI.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Define object reclustered csv file path")
        self.csvpath = QLineEdit("")
        self.csvpath.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.csvpath.setMinimumWidth(400)
        label = QLabel("CSV path:")
        self.OK = False

        csvloadbutton = QPushButton()
        csvloadbutton.setText("Load csv object reclustering file")
        csvloadbutton.clicked.connect(self.loadcsv)
        okbutton = QPushButton()
        okbutton.setText("Load")
        okbutton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(label, self.csvpath)
        formLayout.addRow(csvloadbutton, csvloadbutton)
        formLayout.addRow(okbutton, okbutton)

    def loadcsv(self):
        """
        Called when user selects to load a csv path.
        """
        dialog = QFileDialog()
        self.csvpath.setText(dialog.getOpenFileName(filter="*.csv")[0])

    def add(self):
        """
        Close window and store user input.
        """
        self.csvpath = self.csvpath.text().rstrip()
        self.OK = True
        self.close()


### TODO: Test this out (functions moved)
class MarkerNames(QDialog):
    """
    Prompt user to define the list or matrix of cell marker names after selecting which images to load into RAPID.

    Args:
        ismultiimage (bool): True if the user has selected multiple images to load, otherwise False.
        outfolder (str): Path to the output folder where results will be saved.
    """

    def __init__(self, ismultiimage, outfolder):
        QDialog.__init__(self)
        self.setWindowTitle("Define marker names")
        self.markertxt = QLineEdit("")
        self.markertxt.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.markertxt.setMinimumWidth(400)
        self.matrix = False
        self.outfolder = outfolder
        self.ismultiimage = ismultiimage
        label = QLabel("Marker Names:")
        self.OK = False

        markerlistbutton = QPushButton()
        markerlistbutton.setText("Load markers for all images (.csv, .txt)")
        markerlistbutton.clicked.connect(self.load_from_file)
        multiimagemarkersbutton = QPushButton()
        multiimagemarkersbutton.setText("Load matrix of markers (.csv, .txt)")
        multiimagemarkersbutton.clicked.connect(self.load_matrix)
        okbutton = QPushButton()
        okbutton.setText("OK")
        okbutton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(label, self.markertxt)
        formLayout.addRow(markerlistbutton, markerlistbutton)
        if ismultiimage:
            formLayout.addRow(multiimagemarkersbutton, multiimagemarkersbutton)
        formLayout.addRow(okbutton, okbutton)

    def load_from_file(self):
        """
        Called when user selects to load a list of cell marker names from a file. Close window and store selection.
        """
        dialog = QFileDialog()
        dirpath = dialog.getOpenFileName(filter="*.csv *.txt")
        if dirpath[0] != '':
            with open(dirpath[0], encoding='utf-8-sig') as f:
                line = f.readline()
                s = ""
                while line:
                    s += line.rstrip()
                    line = f.readline()
            self.markertxt.setText(s.replace("\"", "").rstrip())
        else:
            pass
        self.matrix = False

    def load_matrix(self):
        """
        Called when user selects to load a matrix of cell marker names for each image. Close window and store selection.
        """
        dialog = QFileDialog()
        dirpath = dialog.getOpenFileName(filter="*.csv *.txt")
        if dirpath[0] != '':
            with open(dirpath[0], encoding='utf-8-sig') as f:
                markerslist = []
                line = f.readline()
                while line:
                    markers = line.replace("\"", "").rstrip().split(",")
                    if len(markers[1:]) != len(set(markers[1:])):
                        display_error_message("Duplicate marker names detected",
                                              "Please make sure each marker has a distinct name for each image")
                        self.close()
                        self.__init__(self.ismultiimage, self.outfolder)
                        self.exec()
                    markerslist.append(line.replace("\"", "").rstrip().split(","))
                    line = f.readline()
            markerslist = [x for x in markerslist if x != ['']]
            self.imagenames = [markers[0] for markers in markerslist]
            markerslist = [markers[1:] for markers in markerslist]
            print(markerslist)
            intersection = markerslist[0]
            for i in range(1, len(markerslist)):
                list = []
                for j in intersection:
                    l = [re.sub('[^a-zA-Z0-9]', '', marker).lower() for marker in markerslist[i]]
                    if re.sub('[^a-zA-Z0-9]', '', j).lower() in l:
                        list.append(j)
                intersection = list
            print(intersection)
            indiceslist = []
            for i in range(len(markerslist)):
                indices = []
                currentmarkerslist = [re.sub('[^a-zA-Z0-9]', '', marker).lower() for marker in markerslist[i]]
                intersect = [re.sub('[^a-zA-Z0-9]', '', cm).lower() for cm in intersection]
                for marker in intersect:
                    indices.append(currentmarkerslist.index(marker))
                indiceslist.append(indices)
            print(indiceslist)
            self.matrix = True
            self.markers = ",".join(intersection).rstrip()
            self.indiceslist = indiceslist
            self.OK = True
            self.close()
        else:
            pass

    def add(self):
        """
        Close window and store user inputs.
        """
        self.markers = self.markertxt.text().rstrip()
        inputmarkernames = self.markers.replace(" ", "").split(",")
        if len(inputmarkernames) != len(set(inputmarkernames)):
            display_error_message("Duplicate marker names detected",
                                  "Please make sure each marker has a distinct name")
            self.close()
            self.__init__(self.ismultiimage, self.outfolder)
            self.exec()
        log_actions(self.outfolder, f"Marker List: Names ({inputmarkernames})")
        # self.log_actions(self.outfolder, f"Marker List: Names ({inputmarkernames})")
        self.OK = True
        self.close()


class ManualAnnotationPopup(QDialog):
    """
    Editable popup to allow users to rename each of the regions to serve as the names for the clusters.

    Args:
        numshapes (int): Number of shapes that have been drawn on the image.
    """

    def __init__(self, numshapes):
        QDialog.__init__(self)
        self.setWindowTitle("Names of annotated regions")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.headernames = ''
        self.OK = False
        gridLayout = QGridLayout(self)
        self.horizontalheaders = []
        for j in range(numshapes):
            header = QLineEdit(f"Region {j + 1}")
            self.horizontalheaders.append(header)
            gridLayout.addWidget(header, 0, j)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.ok_clicked)
        gridLayout.addWidget(okButton, 1, 1)

    def ok_clicked(self):
        """
        Close window and save user inputs
        """
        self.headernames = [h.text() for h in self.horizontalheaders]
        if not len(self.headernames) == len(set(self.headernames)):
            display_error_message("Duplicate names entered",
                                  "Please each cluster has a unique name.")
            self.close()
            self.__init__(self.clusternames)
            self.exec()
        self.OK = True
        self.close()


class MergeMarkerIteration(QDialog):
    """
    Prompt user to indicate which merged cell marker images they would like to use for segmentation.

    Args:
        numiterations (int): Number of merged marker images that have been generated.
    """

    def __init__(self, numiterations):
        QDialog.__init__(self)
        self.setWindowTitle("Select membrane image to use")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.iteration = 0
        formLayout = QFormLayout(self)
        labelimage = QLabel("Merged Image ")
        self.iterations = QComboBox(self)
        self.OK = False
        for i in range(numiterations):
            self.iterations.addItem(str(i + 1))
        formLayout.addRow(labelimage, self.iterations)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user input.
        """
        self.iteration = int(self.iterations.currentText()) - 1
        self.OK = True
        self.close()


class MergeMarkers(QDialog):
    """
    Prompt user to select cell markers to define the nuclear layer, and algorithm to use for merging them.

    Args:
        viewer (napari.Viewer): Viewer object for the RAPID GUI.
        markernames (list): List of names of cell markers being merged together.
    """

    def __init__(self, viewer, markernames, membrane, markernums, alg):
        QDialog.__init__(self)
        self.markernames = markernames
        self.markernums = markernums
        self.alg = alg
        if membrane:
            self.setWindowTitle("Marker(s) to define membrane:")
        else:
            self.setWindowTitle("Marker(s) to define nucleus:")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.alg = "max"
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        if self.markernums is None:
            for marker in markernames:
                box = QCheckBox(marker)
                box.setChecked(viewer.layers[marker].visible)
                self.formLayout.addRow(box)
                self.buttonlist.append(box)
        if self.alg is None:
            alglabel = QLabel("Merging Method:")
            self.mergealg = QComboBox()
            self.mergealg.addItem("Max")
            self.mergealg.addItem("Sum")
            self.mergealg.addItem("Average")
            self.mergealg.addItem("Median")
            self.mergealg.setFixedWidth(134)
            self.formLayout.addRow(alglabel, self.mergealg)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall)
        if self.markernums is None:
            nomergedmarkers = QPushButton()
            if membrane:
                nomergedmarkers.setText("No Membrane")
            else:
                nomergedmarkers.setText("No Nucleus")
            nomergedmarkers.clicked.connect(self.noMergedMarkers)
            self.formLayout.addRow(nomergedmarkers)
        groupbox = QGroupBox()
        groupbox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        if self.markernums is None:
            self.markernums = []
            for i in range(len(self.buttonlist)):
                if self.buttonlist[i].isChecked():
                    self.markernums.append(i)
        if self.alg is None:
            if self.mergealg.currentText() == "Sum":
                self.alg = "sum"
            if self.mergealg.currentText() == "Average":
                self.alg = "avg"
            if self.mergealg.currentText() == "Median":
                self.alg = "median"
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)

    def noMergedMarkers(self):
        """
        Called when user selects to not merge any markers. Close window and store selection.
        """
        self.markernums = []
        self.OK = True
        self.close()


class NNInRadius(QDialog):
    """
    Prompt user to select which clusters and parameters to use for Nearest Neighbour analysis.

    Args:
        clusterindices (list): List of integer values corresponding to each cluster ID for the results being analyzed.
        clusternames (list): List of names of clusters for the results being analyzed.
    """

    def __init__(self, clusternames):
        QDialog.__init__(self)
        self.setWindowTitle("NN Parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formlayout = QFormLayout(self)
        sourceclusterlabel = QLabel("Source cluster: ")
        targetclusterlabel = QLabel("Target cluster: ")
        radlabel = QLabel("Radius: ")
        nnlabel = QLabel("#NN: ")

        self.sourceclusteroptions = QComboBox(self)
        self.targetclusteroptions = QComboBox(self)
        self.radius = QLineEdit("10.0")
        self.retnn = QLineEdit("0")
        self.OK = False
        for cluster in clusternames:
            self.sourceclusteroptions.addItem(str(cluster))
            self.targetclusteroptions.addItem(str(cluster))

        formlayout.addRow(sourceclusterlabel, self.sourceclusteroptions)
        formlayout.addRow(targetclusterlabel, self.targetclusteroptions)
        formlayout.addRow(radlabel, self.radius)
        formlayout.addRow(nnlabel, self.retnn)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formlayout.addRow("", QLabel(""))
        formlayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.sourcecluster = self.sourceclusteroptions.currentText()
        self.targetcluster = self.targetclusteroptions.currentText()
        self.radius = float(self.radius.text())
        self.numnn = float(self.retnn.text())
        self.OK = True
        self.close()


class NumGroups(QDialog):
    """
    Prompt user to indicate the number of groups to assign images to.

    Args:
        numimgs (int): Number of images that have been loaded into the RAPID GUI.
    """

    def __init__(self, numimgs):
        QDialog.__init__(self)
        self.setWindowTitle("Number of groups")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.ngroup = QComboBox(self)
        for i in range(1, numimgs):
            self.ngroup.addItem(str(i))
        reslabel = QLabel("Number of groups:")
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(reslabel, self.ngroup)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user input.
        """
        self.OK = True
        self.ngroups = int(self.ngroup.currentText())
        self.close()


class ObjectTrainIteration(QDialog):
    """
    Prompt user to indicate which object-based clustering results they would like to use for downstream analyses that
    require object-based clustering.

    Args:
        clusterindices (int): Clustering indices associated with the user-selected round of segmentation.
    """

    def __init__(self, clusterindices):
        QDialog.__init__(self)
        self.setWindowTitle("Select object-based clustering iteration to use")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formLayout = QFormLayout(self)
        labelimage = QLabel("Object Clusters")
        self.iterations = QComboBox(self)
        self.OK = False

        for ind in clusterindices:
            self.iterations.addItem(str(ind+1))

        #for i in range(numiterations):
        #    self.iterations.addItem(str(i + 1))
        formLayout.addRow(labelimage, self.iterations)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user input.
        """
        self.iteration = int(self.iterations.currentText()) - 1
        self.OK = True
        self.close()


class OKButtonPopup(QDialog):
    """
    Popup window with only an OK button to notify the user about the subsequent popup window.
    """

    def __init__(self, title):
        """
        Arguments:
            :title (str): Title of the popup window.
        """
        QDialog.__init__(self)
        self.setWindowTitle(title)
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.setAlignment(Qt.AlignCenter)
        formLayout.addRow(okButton)

    def add(self):
        """
        Close window.
        """
        self.close()


class OutFolder(QDialog):
    """
    Upon launching the GUI, prompt the user to decide whether to load results or to generate new results.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.loadenv = False
        self.loadseg = False
        self.loadpixel = False
        self.OK = False
        okButton = QPushButton()
        okButton.setText("Define Output Folder")
        okButton.clicked.connect(self.add)
        loadstate = QPushButton()
        loadstate.setText("Load Environment")
        loadstate.clicked.connect(self.load_env)
        loadsegmentation = QPushButton()
        loadsegmentation.setText("Load Segmentation")
        loadsegmentation.clicked.connect(self.load_segmentation)
        loadpixelresults = QPushButton()
        loadpixelresults.setText("Load Pixel-based Results")
        loadpixelresults.clicked.connect(self.load_pixel)
        formLayout = QFormLayout(self)
        formLayout.setAlignment(Qt.AlignCenter)
        formLayout.addRow(okButton)
        formLayout.addRow(loadstate)
        formLayout.addRow(loadsegmentation)
        formLayout.addRow(loadpixelresults)

    def add(self):
        """
        Close window.
        """
        self.OK = True
        self.close()

    def load_env(self):
        """
        Called when user selects to load a saved environment. Close window and store selection.
        """
        self.loadenv = True
        self.OK = True
        self.close()

    def load_segmentation(self):
        """
        Called when user selects to load segmentation results. Close window and store selection.
        """
        self.loadseg = True
        self.OK = True
        self.close()

    def load_pixel(self):
        """
        Called when user selects to load pixel-based results. Close window and store selection.
        """
        self.loadpixel = True
        self.OK = True
        self.close()


class PhenographParameters(QDialog):
    """
    Prompt user to define parameters for phenograph clustering.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Set Phenograph parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        LabelPG_nn = QLabel("Phenograph nn:")
        self.TextPG_nn = QLineEdit("30")
        LabelPG_res = QLabel("Phenograph resolution:")
        self.TextPG_res = QLineEdit("0.2")
        LabelPG_dis = QLabel("Phenograph distance:")
        self.TextPG_dis = QComboBox()
        self.TextPG_dis.addItem("euclidean")
        self.TextPG_dis.addItem("cosine")
        self.TextPG_dis.addItem("manhattan")
        self.TextPG_dis.addItem("correlation")
        self.TextPG_dis.addItem("manhattan")

        Labelalgo = QLabel("Graph algorithm:")
        self.Textalgo = QComboBox()
        self.Textalgo.addItem("leiden")
        self.Textalgo.addItem("louvain")

        Labelnorm = QLabel("Normalization:")
        self.Textnorm = QComboBox()
        self.Textnorm.addItem("None")
        self.Textnorm.addItem("zscore")
        self.Textnorm.addItem("log2")
        self.Textnorm.addItem("log10")
        self.Textnorm.addItem("all (PCA)")
        self.Textnorm.addItem("all (no PCA)")
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(LabelPG_nn, self.TextPG_nn)
        formLayout.addRow(Labelalgo, self.Textalgo)
        formLayout.addRow(LabelPG_res, self.TextPG_res)
        formLayout.addRow(LabelPG_dis, self.TextPG_dis)
        formLayout.addRow(Labelnorm, self.Textnorm)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.PGnn = self.TextPG_nn.text()
        self.PGres = self.TextPG_res.text()
        self.PGdis = self.TextPG_dis.currentText()
        self.graphalgo = self.Textalgo.currentText()
        self.normalize = self.Textnorm.currentText()
        self.pca = False
        if self.normalize == "all (PCA)":
            self.normalize = "all"
            self.pca = True
        elif self.normalize == "all (no PCA)":
            self.normalize = "all"
        self.OK = True
        self.close()


class PixelTrainMarkers(QDialog):
    """
    Prompt user to select which cell markers to use for pixel-based clustering.

    Args:
        viewer (napari.Viewer): Viewer object for the RAPID GUI.
        markernames (list): List of names of cell markers being used for clustering.
    """

    def __init__(self, viewer, markernames):
        QDialog.__init__(self)
        self.markernames = markernames
        self.setWindowTitle("Markers used for clustering")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        for marker in markernames:
            box = QCheckBox(marker)
            box.setChecked(viewer.layers[marker].visible)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall)
        groupbox = QGroupBox()
        groupbox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        self.markernums = []
        self.pixeltrainmarkers = []
        for i in range(len(self.buttonlist)):
            if self.buttonlist[i].isChecked():
                self.pixeltrainmarkers.append(self.markernames[i])
                self.markernums.append(i)
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)


class QuantificationMode(QDialog):
    """
    After segmenting images, prompt user to indicate whether to quantify phenotypes according to average expression
    value, or by calculating the root-mean-square values for each cell marker in each cell.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Select Quantification Algorithm")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.avg = True
        averagebutton = QPushButton()
        averagebutton.setText("Average")
        averagebutton.clicked.connect(self.average)
        rmsvbutton = QPushButton()
        rmsvbutton.setText("Root Mean Square Values")
        rmsvbutton.clicked.connect(self.rmsv)
        formLayout = QFormLayout(self)
        formLayout.addRow(averagebutton)
        formLayout.addRow(rmsvbutton)

    def average(self):
        """
        Called when user selects to calculate mean values. Close window and store selection.
        """
        self.avg = False
        self.OK = True
        self.close()

    def rmsv(self):
        """
        Called when user selects to calculate root mean square values. Close window and store selection.
        """
        self.OK = True
        self.close()


class QuantifyRegionPopup(QDialog):
    """
    Display a popup window with region-based analysis information according to user specification, and give the option
    to save as a .csv file.

    Args:
        avgs (list): Average expression values or cell/pixel counts for each cell marker or cluster in the image.
        imgtype (str): 'pixel' if quantifying pixel-based clustering results, 'object' if quantifying object-based clustering results, or 'raw' if quantifying average marker expression in each region.
        numrows (int): Number of cell markers (for raw image) or clusters (for clustered results).
        markernames (list): List of names of cell markers being quantified.
        numregions (int): Number of regions.
        outfolder (str): Path to the output folder where results will be saved.
        selectedregioncount (int): Counter for number of times regions have been quantified before.
        celldata (numpy.ndarray, optional): If quantifying object-based analysis, include array of quantified expression values and IDs for each cell in the region (Default: []).
    """

    def __init__(self, avgs, imgtype, numrows, markernames, numregions, outfolder, selectedregioncount,
                 celldata=np.array([])):
        QDialog.__init__(self)
        if imgtype == "pixel":
            self.setWindowTitle("# Pixels from each cluster in Region(s)")
        elif imgtype == "object":
            self.setWindowTitle("# Cells from each cluster in Region(s)")
        else:
            self.setWindowTitle("Marker Expression in Region(s)")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.outfolder = outfolder
        self.selectedregioncount = selectedregioncount
        self.numregions = numregions
        self.headernames = ''
        self.avgs = avgs
        self.saved = False
        self.celldata = celldata
        gridLayout = QGridLayout(self)
        self.horizontalheaders = []
        gridLayout.addWidget(QLabel(""), 0, 0)
        for j in range(len(avgs)):
            header = QLineEdit(f"Region {j + 1}")
            self.horizontalheaders.append(header)
            gridLayout.addWidget(header, 0, j + 1)
        numheaderrows = 1
        self.verticalheaders = []
        if imgtype == 'object':
            self.verticalheaders.append('# Cells')
            gridLayout.addWidget(QLabel("# Cells:   "), 1, 0)
            self.objects = "# Cells"
        else:
            self.verticalheaders.append('# Pixels')
            gridLayout.addWidget(QLabel("# Pixels:   "), 1, 0)
            self.objects = "# Pixels"
        for i in range(len(avgs)):
            gridLayout.addWidget(QLabel(str(numregions[i])), numheaderrows, i + 1)
        for i in range(numrows):
            if imgtype == "raw":
                self.verticalheaders.append(markernames[i])
                gridLayout.addWidget(QLabel(markernames[i] + ":   "), i + numheaderrows + 1, 0)
            else:
                self.verticalheaders.append(f"Cluster {i + 1}")
                gridLayout.addWidget(QLabel(f"Cluster {i + 1}:   "), i + numheaderrows + 1, 0)
            for j in range(len(avgs)):
                gridLayout.addWidget(QLabel(str(avgs[j][i])), i + numheaderrows + 1, j + 1)
        okButton = QPushButton()
        okButton.setText("Save")
        if imgtype == 'object':
            okButton.clicked.connect(self.saveobj)
        else:
            okButton.clicked.connect(self.save)
        gridLayout.addWidget(okButton, numheaderrows + numrows + 1, 1)

    def save(self):
        """
        Called when user selects to save values and is not using object-based results. Close window and store selection.
        """
        arr = np.array(self.avgs)
        arr = np.transpose(arr)
        arr = np.vstack((np.array(self.numregions), arr))
        df = pd.DataFrame(arr)
        df.columns = [h.text() for h in self.horizontalheaders]
        df.insert(0, '', self.verticalheaders)
        df.to_csv(os.path.join(self.outfolder, f"quantifiedregion{self.selectedregioncount}.csv"), index=False)
        self.headernames = df.columns
        self.saved = True
        self.close()

    def saveobj(self):
        """
        Called when user selects to save values and is using object-based results. Close window and store selection.
        """
        arr = np.array(self.avgs)
        arr = np.transpose(arr)
        arr = np.vstack((np.array(self.numregions), arr))
        df = pd.DataFrame(arr)
        df.columns = [h.text() for h in self.horizontalheaders]
        df.insert(0, '', self.verticalheaders)
        df.to_csv(os.path.join(self.outfolder, f"quantifiedregionClusters{self.selectedregioncount}.csv"), index=False)
        for i in range(len(self.celldata)):
            self.celldata[i].to_csv(os.path.join(self.outfolder, f"quantifiedregionCellIDs_Region{i}.csv"), index=False)
        self.headernames = df.columns
        self.saved = True
        self.close()


class RAPIDObjectParameters(QDialog):
    """
    Prompt user to define hyperparameters for object-based clustering.

    Args:
        nummarkers (int): Number of cell markers being used for clustering.
    """

    def __init__(self, nummarkers):
        QDialog.__init__(self)
        self.setWindowTitle("Set RAPID Parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        Labellr = QLabel("Learning Rate:")
        self.Textlr = QLineEdit("0.001")
        Labelnoc = QLabel("Number of clusters :")
        self.Textnoc = QLineEdit(str(nummarkers * 3))
        Labelnit = QLabel("Number of training iterations:")
        self.Textnit = QLineEdit("1000")
        Labelmse = QLabel("Autoencoder mode")
        self.Textmse = QComboBox()
        self.Textmse.addItem("False")
        self.Textmse.addItem("True")
        Labelbo = QLabel("Noise level to introduce (0-100):")
        self.Textbo = QLineEdit("100")
        Labelnorm = QLabel("Normalize:")
        self.Textnorm = QComboBox()
        self.Textnorm.addItem("None")
        self.Textnorm.addItem("zscore")
        self.Textnorm.addItem("log2")
        self.Textnorm.addItem("log10")
        self.Textnorm.addItem("all (PCA)")
        self.Textnorm.addItem("all (no PCA)")
        Labelbs = QLabel("Batch Size:")
        self.Textbs = QLineEdit("100")
        Labelblankpercent = QLabel("Salt & peper noise %:")
        self.Textblankpercent = QLineEdit("0.2")
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(Labellr, self.Textlr)
        formLayout.addRow(Labelnoc, self.Textnoc)
        formLayout.addRow(Labelnit, self.Textnit)
        formLayout.addRow(Labelmse, self.Textmse)
        formLayout.addRow(Labelbo, self.Textbo)
        formLayout.addRow(Labelnorm, self.Textnorm)
        formLayout.addRow(Labelblankpercent, self.Textblankpercent)
        formLayout.addRow(Labelbs, self.Textbs)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.lr = self.Textlr.text()
        self.nc = self.Textnoc.text()
        self.nit = self.Textnit.text()
        self.mse = self.Textmse.currentText()
        self.BO = self.Textbo.text()
        self.normalize = self.Textnorm.currentText()
        self.pca = False
        if self.normalize == "all (PCA)":
            self.normalize = "all"
            self.pca = True
        elif self.normalize == "all (no PCA)":
            self.normalize = "all"
        self.bs = self.Textbs.text()
        self.blankpercent = self.Textblankpercent.text()
        self.OK = True
        self.close()


class RAPIDObjectParams(QDialog):
    """
    Prompt user to select which cell markers and morphological parameters to use for object-based clustering or UMAP.

    Args:
        markernames (list): List of names of cell markers being used for analysis.
        isumap (bool, optional): True if generating UMAP plots, False if performing object-based clustering.
    """

    def __init__(self, markernames, isumap=False):
        QDialog.__init__(self)
        self.markernames = markernames
        if isumap:
            self.setWindowTitle("Parameters used for UMAP")
        else:
            self.setWindowTitle("Parameters used for clustering")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        for marker in markernames:
            box = QCheckBox(marker)
            box.setChecked(True)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        for param in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
            box = QCheckBox(param)
            box.setChecked(False)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton, okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall, selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall, deselall)
        groupbox = QGroupBox()
        groupbox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        self.markernums = []
        self.objecttrainmarkers = []
        params = ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        for i in range(len(self.buttonlist) - 4):
            if self.buttonlist[i].isChecked():
                self.objecttrainmarkers.append(self.markernames[i])
                self.markernums.append(i + 1)
        for i in range(len(self.buttonlist) - 4, len(self.buttonlist)):
            if self.buttonlist[i].isChecked():
                pos = i + 4 - len(self.buttonlist)
                self.objecttrainmarkers.append(params[pos])
                self.markernums.append(i + 1)
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)


class RAPIDObjectTrainLoadedParameters(QDialog):
    """
    Prompt user to define hyperparameters for object-based clustering when loading a previously-trained model.

    Args:
        args (Namespace): User-defined parameters used to train the model being loaded.
    """

    def __init__(self, args):
        QDialog.__init__(self)
        self.setWindowTitle("Set RAPID Parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        Labellr = QLabel("Learning Rate:")
        self.Textlr = QLineEdit(str(args.lr))
        Labelnoc = QLabel("Number of clusters :")
        self.Textnoc = QLabel(str(args.ncluster))
        Labelnit = QLabel("Number of training iterations:")
        self.Textnit = QLineEdit(str(args.nit))
        Labelmse = QLabel("Autoencoder mode")
        self.Textmse = QLabel(str(args.mse))
        Labelbs = QLabel("Batch Size:")
        self.Textbs = QLineEdit(str(args.bs))
        Labelblankpercent = QLabel("Salt & peper noise %:")
        self.Textblankpercent = QLineEdit(str(args.blankpercent))
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(Labellr, self.Textlr)
        formLayout.addRow(Labelnoc, self.Textnoc)
        formLayout.addRow(Labelnit, self.Textnit)
        formLayout.addRow(Labelmse, self.Textmse)
        formLayout.addRow(Labelblankpercent, self.Textblankpercent)
        formLayout.addRow(Labelbs, self.Textbs)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.lr = self.Textlr.text()
        self.nc = self.Textnoc.text()
        self.nit = self.Textnit.text()
        self.bs = self.Textbs.text()
        self.blankpercent = self.Textblankpercent.text()
        self.OK = True
        self.close()


class RAPIDPixelParameters(QDialog):
    """
    Prompt user to define hyperparameters for pixel-based clustering.

    Args:
        nummarkers (int): Number of cell markers being used for clustering.
        maximageshape (iterable): Shape being occupied of all the images together within the GUI.
        israndompatches (bool, optional): True if randomly selecting patches for training, otherwise False.
    """

    def __init__(self, nummarkers, maximageshape, israndompatches=True):
        QDialog.__init__(self)
        self.israndompatches = israndompatches
        area = maximageshape[1] * maximageshape[2]
        self.setWindowTitle("Set RAPID Parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        Labellr = QLabel("Learning Rate:")
        self.Textlr = QLineEdit("0.001")
        Labelnoc = QLabel("Number of clusters :")
        self.Textnoc = QLineEdit(str(int(nummarkers * 3)))
        Labelnit = QLabel("Number of training iterations:")
        self.Textnit = QLineEdit(str(int(area * 0.002)))
        Labelmse = QLabel("Autoencoder mode")
        self.Textmse = QComboBox()
        self.Textmse.addItem("False")
        self.Textmse.addItem("True")
        self.Textnl = QComboBox()
        self.Textnl.addItem("True")
        self.Textnl.addItem("False")
        Labelnorm = QLabel("Normalization:")
        self.Textnorm = QComboBox()
        self.Textnorm.addItem("None")
        self.Textnorm.addItem("zscore")
        self.Textnorm.addItem("log2")
        self.Textnorm.addItem("log10")
        self.Textnorm.addItem("square root")
        self.Textnorm.addItem("inverse")
        self.Textnorm.addItem("all (PCA)")
        self.Textnorm.addItem("all (no PCA)")
        lossfnlabel = QLabel("Loss Function:")
        self.lossfn = QComboBox()
        self.lossfn.addItem("SCAN")
        self.lossfn.addItem("IID")
        Labelrc = QLabel("Analyze at low res:")
        self.Textrc = QComboBox()
        self.Textrc.addItem("True")
        self.Textrc.addItem("False")
        labeldenoise = QLabel("Denoising:")
        self.Denoise = QComboBox()
        self.Denoise.addItem("None")
        self.Denoise.addItem("Denoise")
        self.Denoise.addItem("Binarize")
        Labelrcn = QLabel("Rescale factor(0-1):")
        self.Textrcn = QLineEdit("1")
        Labelbs = QLabel("Batch Size:")
        self.Textbs = QLineEdit("100")
        Labelps = QLabel("Patch Size:")
        self.Textps = QLineEdit("64")
        Labelnop = QLabel("Number of Patches:")
        self.Textnop = QLineEdit(str(int(area * 0.2 / 4096)))
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(Labelnoc, self.Textnoc)
        formLayout.addRow(Labelnit, self.Textnit)
        formLayout.addRow(Labelnorm, self.Textnorm)
        formLayout.addRow(lossfnlabel, self.lossfn)
        formLayout.addRow(Labellr, self.Textlr)
        formLayout.addRow(labeldenoise, self.Denoise)
        formLayout.addRow(QLabel(""), QLabel(""))
        formLayout.addRow(QLabel(""), QLabel(""))
        formLayout.addRow(Labelmse, self.Textmse)
        formLayout.addRow(Labelrc, self.Textrc)
        formLayout.addRow(Labelrcn, self.Textrcn)
        formLayout.addRow(Labelbs, self.Textbs)
        if israndompatches:
            formLayout.addRow(Labelps, self.Textps)
            formLayout.addRow(Labelnop, self.Textnop)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.lr = self.Textlr.text()
        self.denoise = self.Denoise.currentText()
        self.nc = self.Textnoc.text()
        self.nit = self.Textnit.text()
        self.normalize = self.Textnorm.currentText()
        self.SCAN = self.lossfn.currentText() == 'SCAN'
        self.RC = self.Textrc.currentText()
        self.RCN = self.Textrcn.text()
        self.bs = self.Textbs.text()
        if self.israndompatches:
            self.ps = self.Textps.text()
            self.nop = self.Textnop.text()
        self.mse = self.Textmse.currentText()
        self.OK = True
        self.close()


class RAPIDTrainLoadedParams(QDialog):
    """
    Prompt user to define hyperparameters for pixel-based clustering when loading a previously-trained model.

    Args:
        args (Namespace): User-defined parameters used to train the model being loaded.
        israndompatches (bool, optional): True if randomly selecting patches for training, otherwise False.
    """

    def __init__(self, args, israndompatches=True):
        self.israndompatches = israndompatches
        QDialog.__init__(self)
        self.setWindowTitle("Set RAPID Parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        Labelnoc = QLabel("Number of clusters :")
        self.Textnoc = QLabel(str(args.ncluster))
        Labellr = QLabel("Learning Rate:")
        self.Textlr = QLineEdit(str(args.lr))
        Labelnit = QLabel("Number of training iterations:")
        self.Textnit = QLineEdit(str(args.nit))
        Labelmse = QLabel("Autoencoder mode")
        self.Textmse = QLabel(str(args.mse))
        self.Textnl = QComboBox()
        self.Textnl.addItem("True")
        self.Textnl.addItem("False")
        lossfnlabel = QLabel("Loss Function:")
        self.lossfn = QComboBox()
        self.lossfn.addItem("SCAN")
        self.lossfn.addItem("IID")
        Labelrc = QLabel("Analyze at low res:")
        self.Textrc = QComboBox()
        self.Textrc.addItem("False")
        self.Textrc.addItem("True")
        labeldenoise = QLabel("Denoising:")
        self.Denoise = QComboBox()
        self.Denoise.addItem("None")
        self.Denoise.addItem("Denoise")
        self.Denoise.addItem("Binarize")
        Labelrcn = QLabel("Rescale factor (0-1):")
        self.Textrcn = QLineEdit("1")
        Labelbs = QLabel("Batch Size:")
        self.Textbs = QLineEdit(str(args.bs))
        Labelps = QLabel("Patch Size:")
        self.Textps = QLineEdit(str(args.patchsize))
        Labelnop = QLabel("Number of Patches:")
        self.Textnop = QLineEdit(str(args.npatches))
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(Labellr, self.Textlr)
        formLayout.addRow(Labelnoc, self.Textnoc)
        formLayout.addRow(Labelnit, self.Textnit)
        formLayout.addRow(lossfnlabel, self.lossfn)
        formLayout.addRow(labeldenoise, self.Denoise)
        formLayout.addRow(Labelmse, self.Textmse)
        formLayout.addRow(Labelrc, self.Textrc)
        formLayout.addRow(Labelrcn, self.Textrcn)
        formLayout.addRow(Labelbs, self.Textbs)
        if israndompatches:
            formLayout.addRow(Labelps, self.Textps)
            formLayout.addRow(Labelnop, self.Textnop)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.lr = self.Textlr.text()
        self.denoise = self.Denoise.currentText()
        self.nc = self.Textnoc.text()
        self.nit = self.Textnit.text()
        self.SCAN = self.lossfn.currentText() == 'SCAN'
        self.RC = self.Textrc.currentText()
        self.RCN = self.Textrcn.text()
        self.bs = self.Textbs.text()
        if self.israndompatches:
            self.ps = self.Textps.text()
            self.nop = self.Textnop.text()
        self.mse = self.Textmse.text()
        self.OK = True
        self.close()


class RemoveMarkerNames(QDialog):
    """
    Prompt user to select markers not to include after loading images into RAPID.

    Args:
        markernames (list): List of all cell marker names for the images loaded into RAPID.
    """

    def __init__(self, markernames):
        QDialog.__init__(self)
        self.setWindowTitle("Included Markers")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.markernames = markernames
        self.OK = False
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        for marker in markernames:
            box = QCheckBox(marker)
            box.setChecked(True)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall)
        groupbox = QGroupBox()
        groupbox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        markernums = []
        self.markers = []
        countincluded = 0
        for i in range(len(self.buttonlist)):
            if self.buttonlist[i].isChecked():
                markernums.append(i)
                self.markers.append(self.markernames[i])
                countincluded += 1
        if countincluded == 0:
            display_error_message("Please include at least one marker",
                                  "You cannot select all markers because you must include at least one marker when adding an image")
            return
        self.markernums = markernums
        self.nummarkers = len(markernums)
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)


class RenameClusters(QDialog):
    """
    Open a popup window to allow users to rename clusters.

    Args:
        clusternames (list): List of current cluster names.
    """

    def __init__(self, clusternames):
        QDialog.__init__(self)
        self.setWindowTitle("Rename Clusters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.clusternames = clusternames
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        self.clusternameentries = []
        for name in clusternames:
            self.clusternameentries.append(QLineEdit(name))
            formLayout.addRow(QLabel(name), self.clusternameentries[-1])
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.newclusternames = [h.text() for h in self.clusternameentries]
        if not len(self.newclusternames) == len(set(self.newclusternames)):
            display_error_message("Duplicate names entered",
                                  "Please each cluster has a unique name.")
            self.close()
            self.__init__(self.clusternames)
            self.exec()
        self.OK = True
        self.close()


class SaveData(QDialog):
    """
    Prompt user to indicate which dataset(s) they would like to save and how they would like to save them.

    Args:
        viewer (napari.Viewer): Viewer object for the RAPID GUI.
        outfolder (str): Path to the output folder where results will be saved.
        tablevals (pandas.DataFrame): Dataframe with values currently displayed in the table.
        arepixelbased (list): List accounting for which clustering rounds correspond to pixel- or object-based.
        greypixels (list): List of numpy arrays with the labeled pixel-based clustering images.
        greyobjects (list): List of numpy arrays with the labeled object-based clustering images.
        imageshapelist (list): List of shapes for each of the images loaded into RAPID.
        filenames (list): List of names of each of the images loaded into RAPID.
        flipimg (list): List of boolean values indicating which images were flipped when loaded.
    """

    def __init__(self, viewer, outfolder, tablevals, arepixelbased, greypixels, greyobjects, imageshapelist,
                 filenames, flipimg):
        QDialog.__init__(self)
        self.viewer = viewer
        self.outfolder = outfolder
        self.tablevals = tablevals
        self.arepixelbased = arepixelbased
        self.greypixels = greypixels
        self.greyobjects = greyobjects
        self.imageshapelist = imageshapelist
        self.filenames = filenames
        self.flipimg = flipimg
        self.setWindowTitle("Save RAPID Data")
        self.OK = False
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)

        savevisible = QPushButton()
        savevisible.setText("Save Visible Window")
        savevisible.clicked.connect(self.saveVisible)

        savescreenshot = QPushButton()
        savescreenshot.setText("Save Screenshot of GUI")
        savescreenshot.clicked.connect(self.saveWindow)

        saveclusters = QPushButton()
        saveclusters.setText("Save Clusters")
        saveclusters.clicked.connect(self.saveClusters)

        savetable = QPushButton()
        savetable.setText("Save Table")
        savetable.clicked.connect(self.saveTable)

        savevisiblefull = QPushButton()
        savevisiblefull.setText("Save Full Visible Images")
        savevisiblefull.clicked.connect(self.saveVisibleFull)

        formlayout = QFormLayout(self)
        formlayout.addRow(savevisible)
        formlayout.addRow(savescreenshot)
        formlayout.addRow(saveclusters)
        formlayout.addRow(savetable)
        formlayout.addRow(savevisiblefull)

    def saveVisible(self):
        """
        Called when user selects to save a screenshot of what's currently visible in the viewer. Close window.
        """
        self.viewer.window.qt_viewer._last_visited_dir = self.outfolder
        self.viewer.window.qt_viewer._screenshot_dialog()
        log_actions(self.outfolder, "Saved Visible")
        self.close()

    def saveWindow(self):
        """
        Called when user selects to save a screenshot of the entire GUI window. Close window.
        """
        filename, _ = QFileDialog.getSaveFileName(parent=self.viewer.window.qt_viewer, caption='Save GUI screenshot',
                                                  directory=self.outfolder)
        img = self.viewer.window.screenshot()
        tifffile.imwrite(filename.split(".")[0] + ".tiff", img)
        log_actions(self.outfolder, f"Saved GUI Screenshot ({filename})")
        self.close()

    def saveClusters(self):
        """
        Called when user selects to save each cluster from a selected round of clustering. Close window.
        """
        # User can only save clusters after having performed clustering.
        if len(self.arepixelbased) == 0:
            display_error_message("Clustering has not been executed",
                                  "Please run a clustering algorithm first")
            return

        # If clustering has been performed once, use that by default.
        if len(self.arepixelbased) == 1:
            ispixelcluster = self.arepixelbased[0]
            clusteringnum = 0
            overallclusterindex = 0

        # If clustering has been performed more than once, allow user to select which clustering results to use.
        else:
            selectclusteringround = SelectClusteringRound(self.arepixelbased)
            selectclusteringround.exec()
            if not selectclusteringround.OK:
                return
            ispixelcluster = selectclusteringround.ispixelcluster
            clusteringnum = selectclusteringround.clusteringnum
            overallclusterindex = selectclusteringround.overallclusterindex

        # Prompt user to choose path to output folder where clusters will be saved.
        filename, _ = QFileDialog.getSaveFileName(parent=self.viewer.window.qt_viewer, caption='Save clusters',
                                                  directory=self.outfolder)
        if not os.path.exists(filename):
            os.mkdir(filename)
        log_actions(self.outfolder, f"Saved Clusters: Iteration ({overallclusterindex}), Output folder ({filename})")

        # Retrieve the labeled clustered image the user would like to save.
        if ispixelcluster:
            grey = self.greypixels[clusteringnum]
        else:
            grey = self.greyobjects[clusteringnum]

        # Save each cluster one at a time with the corresponding colormap.
        colors = generate_colormap(int(np.max(grey)) + 1)
        for name in self.filenames:
            os.mkdir(os.path.join(filename, os.path.split(name)[-1].split(".")[0]))
        for i in range(int(np.max(grey))):
            color = colors[i]
            image = np.zeros((grey.shape[0], grey.shape[1], grey.shape[2], 3), dtype=np.uint8)
            image[:, :, :, 0][grey == i + 1] = color[0]
            image[:, :, :, 1][grey == i + 1] = color[1]
            image[:, :, :, 2][grey == i + 1] = color[2]
            for j in range(len(self.filenames)):
                img = image.astype(np.uint8)[j, :self.imageshapelist[j][0], :self.imageshapelist[j][1], :]
                if self.flipimg[j]:
                    img = np.moveaxis(img, 0, 1)
                tifffile.imwrite(
                    os.path.join(filename, os.path.split(self.filenames[j])[-1].split(".")[0], f"Cluster_{i + 1}.tif"),
                    img, metadata={'axes': 'ZXYC'})
        self.OK = True
        self.close()

    def saveTable(self):
        """
        Called when user selects to save the currently displayed table. Close window.
        """
        # User must have generated a table to save.
        if self.tablevals.empty:
            display_error_message("No table generated",
                                  "Please run segmentation or a clustering algorithm first to generate a data table.")
            return

        # Prompt user to choose path to output folder where table will be saved.
        filename, _ = QFileDialog.getSaveFileName(parent=self.viewer.window.qt_viewer, caption='Save current table',
                                                  directory=self.outfolder)

        log_actions(self.outfolder, f"Saved Table: Output folder ({filename})")

        # Save currently displayed table to csv file.
        self.tablevals.to_csv(filename.split(".")[0] + ".csv")
        self.OK = True
        self.close()

    def saveVisibleFull(self):
        """
        Called when user selects to save the full images for each currently visible image. Close window.
        """
        # Prompt user to choose path to output folder where images will be saved.
        filename, _ = QFileDialog.getSaveFileName(parent=self.viewer.window.qt_viewer, caption='Save visible layers',
                                                  directory=self.outfolder)

        # If user has loaded multiple images, prompt them to select which ones to save.
        if len(self.filenames) > 1:
            selectimgs = SelectImages(self.filenames)
            selectimgs.exec()
            if not selectimgs.OK:
                return
            imgnums = selectimgs.imgnums
        else:
            imgnums = [0]
        log_actions(self.outfolder, f"Saved Full Visible: Images ({imgnums})")

        # Loop through each image being saved.
        for imgnum in imgnums:
            # Retrieve the shape of the current image.
            shape = [self.imageshapelist[imgnum][0], self.imageshapelist[imgnum][1]]
            outputimg = np.zeros((shape[0], shape[1], 3))

            # Loop through each layer.
            for le in range(len(self.viewer.layers)):
                # Only include layers for which the image dimension is at least as large as the current image index.
                if len(self.viewer.layers[le].data.shape) == 3 or self.viewer.layers[le].data.shape[-1] == 3:
                    numimgsinlayer = self.viewer.layers[le].data.shape[0]
                else:
                    numimgsinlayer = self.viewer.layers[le].data.shape[1]
                if self.viewer.layers[le].visible and numimgsinlayer > imgnum:
                    print(self.viewer.layers[le].name)
                    # Apply the appropriate colormap to the image and convert to 8-bit.
                    color = self.viewer.layers[le].colormap.colors[-1]
                    if self.viewer.layers[le].data.shape[-1] == 3:
                        image = self.viewer.layers[le].data[imgnum, :shape[0], :shape[1], :]
                    else:
                        if len(self.viewer.layers[le].data.shape) == 4:
                            image = np.zeros((len(self.viewer.layers[le].data), shape[0], shape[1], 3))
                            for i in range(3):
                                image[:, :, :, i] = self.viewer.layers[le].data[:, imgnum, :shape[0], :shape[1]] * color[i]
                        else:
                            image = np.zeros((len(self.viewer.layers[le].data), shape[0], shape[1], 3))
                            for i in range(3):
                                image[:, :, i] = self.viewer.layers[le].data[imgnum, :shape[0], :shape[1]] * color[i]
                    lower = copy.deepcopy(self.viewer.layers[le].contrast_limits[0])
                    upper = copy.deepcopy(self.viewer.layers[le].contrast_limits[1])
                    image[image < lower] = lower
                    image[image > upper] = upper
                    image = (image - lower) / (upper - lower) * 255
                    if len(self.viewer.layers[le].data.shape) == 4 and not len(outputimg.shape) == 4:
                        outputimg = np.vstack([np.expand_dims(outputimg, 0), np.expand_dims(outputimg, 0)])
                        outputimg[:, :image.shape[1], :image.shape[2], :] += image.astype(np.uint8)
                    elif len(self.viewer.layers[le].data.shape) == 4 and len(outputimg.shape) == 4:
                        outputimg[:, :image.shape[0], :image.shape[1], :] += image.astype(np.uint8)
                    elif len(self.viewer.layers[le].data.shape) == 3 and len(outputimg.shape) == 4:
                        outputimg[0, :image.shape[0], :image.shape[1], :] += image.astype(np.uint8)
                        outputimg[1, :image.shape[0], :image.shape[1], :] += image.astype(np.uint8)
                    else:
                        outputimg[:image.shape[0], :image.shape[1], :] += image.astype(np.uint8)

            outputimg[outputimg > 255] = 255
            outputimg = outputimg.astype(np.uint8)
            # Save image to output folder.
            if self.flipimg[imgnum]:
                outputimg = np.moveaxis(outputimg, 0, 1)
            imgname = os.path.split(self.filenames[imgnum])[-1].split(".")[0]
            tifffile.imwrite(filename.split(".")[0] + "_" + imgname + ".tif", outputimg)
        self.OK = True
        self.close()


class SciPyParameters(QDialog):
    """
    Prompt user to define parameters for clustering algorithms from the SciPy package.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Set SciPy clustering parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)

        Labelscipy_algo = QLabel("Clustering algo:")
        self.Textsc_algo = QComboBox()
        self.Textsc_algo.addItem("KMeans")
        self.Textsc_algo.addItem("AffinityPropagation")
        self.Textsc_algo.addItem("SpectralClustering")
        self.Textsc_algo.addItem("AgglomerativeClustering")
        self.Textsc_algo.addItem("DBSCAN")
        self.Textsc_algo.addItem("HDBSCAN")

        Labelnorm = QLabel("Normalization:")
        self.Textnorm = QComboBox()
        self.Textnorm.addItem("None")
        self.Textnorm.addItem("zscore")
        self.Textnorm.addItem("log2")
        self.Textnorm.addItem("log10")
        self.Textnorm.addItem("all (PCA)")
        self.Textnorm.addItem("all (no PCA)")

        Labelsc_args = QLabel("args:")
        self.Textsc_args = QLineEdit("")
        Labelsc_kwarg = QLabel("kwargs dict:")
        self.Textsc_kwarg = QLineEdit("")

        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(Labelscipy_algo, self.Textsc_algo)
        formLayout.addRow(Labelsc_args, self.Textsc_args)
        formLayout.addRow(Labelsc_kwarg, self.Textsc_kwarg)
        formLayout.addRow(Labelnorm, self.Textnorm)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.scipyalgo = self.Textsc_algo.currentText()
        self.scipyargs = self.Textsc_args.text()
        self.scipykwarg = self.Textsc_kwarg.text()
        self.normalize = self.Textnorm.currentText()
        self.pca = False
        if self.normalize == "all (PCA)":
            self.normalize = "all"
            self.pca = True
        elif self.normalize == "all (no PCA)":
            self.normalize = "all"
        self.OK = True
        self.close()


class SegmentationModel(QDialog):
    """
    Prompt user to select which algorithm to use for segmentation.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Select Segmentation Model")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.modelindex = 0
        rapidbutton = QPushButton()
        rapidbutton.setText("RAPID")
        rapidbutton.clicked.connect(self.rapid_model)
        rapidplusbutton = QPushButton()
        rapidplusbutton.setText("RAPID+")
        rapidplusbutton.clicked.connect(self.rapid_plus_model)
        rapiddcbutton = QPushButton()
        rapiddcbutton.setText("RAPIDDC")
        rapiddcbutton.clicked.connect(self.rapid_dc_model)
        formLayout = QFormLayout(self)
        formLayout.addRow(rapidbutton)
        formLayout.addRow(rapidplusbutton)
        formLayout.addRow(rapiddcbutton)

    def rapid_model(self):
        """
        Called when user selects to use the RAPID segmentation model. Close window and store user selection.
        """
        self.OK = True
        self.close()

    def rapid_plus_model(self):
        """
        Called when user selects to use the RAPID+ segmentation model. Close window and store user selection.
        """
        self.modelindex = 1
        self.OK = True
        self.close()

    def rapid_dc_model(self):
        """
        Called when user selects to use the RAPID+ segmentation model. Close window and store user selection.
        """
        self.modelindex = 2
        self.OK = True
        self.close()


class SelectClusteringRound(QDialog):
    """
    Prompt user to indicate which clustering results to use.

    Args:
        arepixelbased (list): List accounting for which clustering rounds correspond to pixel- or object-based.
    """

    def __init__(self, arepixelbased):
        QDialog.__init__(self)
        self.setWindowTitle("Select round of clustering to be used")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.ispixelcluster = False
        self.pixelcount = 1
        self.objectcount = 1
        formLayout = QFormLayout(self)
        labelimage = QLabel("Clustered Image: ")
        self.clustering = QComboBox(self)
        self.OK = False
        for entry in arepixelbased:
            if entry:
                st = f"Pixel {self.pixelcount}"
                self.pixelcount += 1
            else:
                st = f"Object {self.objectcount}"
                self.objectcount += 1
            self.clustering.addItem(st)
        formLayout.addRow(labelimage, self.clustering)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user selection.
        """
        if self.clustering.currentText().startswith("Pixel"):
            self.ispixelcluster = True
        self.clusteringnum = int(self.clustering.currentText().split()[-1]) - 1
        self.overallclusterindex = self.clustering.currentIndex()
        self.name = self.clustering.currentText()
        self.OK = True
        self.close()


class SelectData(QDialog):
    """
    Prompt user to indicate whether to quantify the raw or clustered data.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Select what to quantify")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.RAPID = True
        self.rawimg = False
        rawimgbutton = QPushButton()
        rawimgbutton.setText("Raw Image (Marker expression)")
        rawimgbutton.clicked.connect(self.useRaw)
        clusteredimgbutton = QPushButton()
        clusteredimgbutton.setText("Clustered Image (Cluster expression)")
        clusteredimgbutton.clicked.connect(self.useClustered)
        formLayout = QFormLayout(self)
        formLayout.addRow(rawimgbutton)
        formLayout.addRow(clusteredimgbutton)

    def useRaw(self):
        """
        Called when user selects to quantify the raw data. Close window and store user selection.
        """
        self.OK = True
        self.rawimg = True
        self.close()

    def useClustered(self):
        """
        Called when user selects to quantify clustered data. Close window and store user selection.
        """
        self.OK = True
        self.close()


class SelectImages(QDialog):
    """
    Prompt user to select which image(s) to save results for.

    Args:
        imagenames (list): List of names of each of the images.
    """

    def __init__(self, imagenames):
        QDialog.__init__(self)
        self.setWindowTitle("Select Images to save:")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        for img in imagenames:
            imgname = os.path.split(img)[-1]
            box = QCheckBox(imgname)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton, okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall, selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall, deselall)
        groupbox = QGroupBox()
        groupbox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def add(self):
        """
        Close window and store user selections.
        """
        self.imgnums = []
        for i in range(len(self.buttonlist)):
            if self.buttonlist[i].isChecked():
                self.imgnums.append(i)
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)


class SelectImgDropdown(QDialog):
    """
    Prompt user to select which image(s) to include in the Edit Image popup.

    Args:
        imagenames (list): List of names of each of the images.
    """

    def __init__(self, imagenames):
        QDialog.__init__(self)
        self.setWindowTitle("Select Image")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formlayout = QFormLayout(self)
        imgnames = QLabel("Image to analyze: ")
        self.imgnames = QComboBox(self)
        self.OK = False
        for imgname in imagenames:
            self.imgnames.addItem(str(imgname.split("/")[-1].split(".")[0]))
        formlayout.addRow(imgnames, self.imgnames)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formlayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user selection.
        """
        self.imgindex = self.imgnames.currentIndex()
        self.OK = True
        self.close()


class SelectLoadImages(QDialog):
    """
    When loading pixel-based clustering results, if there is more than one image being loaded, prompt the user to
    indicate which images to load results and data for.

    Args:
        imagenames (list): Names of images that were used for the pixel-based clustering results being loaded.
    """

    def __init__(self, imagenames):
        QDialog.__init__(self)
        self.OK = False
        self.setWindowTitle("Select images to load")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.formLayout = QFormLayout(self)
        self.buttonlist = []
        for image in imagenames:
            box = QCheckBox(image)
            box.setChecked(True)
            self.formLayout.addRow(box)
            self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.formLayout.addRow(okButton, okButton)
        selall = QPushButton()
        selall.setText("Select All")
        selall.clicked.connect(self.selectAll)
        self.formLayout.addRow(selall, selall)
        deselall = QPushButton()
        deselall.setText("Deselect All")
        deselall.clicked.connect(self.deselectAll)
        self.formLayout.addRow(deselall, deselall)

    def add(self):
        """
        Close window and store user selection.
        """
        self.images = []
        for i in range(len(self.buttonlist)):
            if self.buttonlist[i].isChecked():
                self.images.append(i)
        self.OK = True
        self.close()

    def selectAll(self):
        """
        Check all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(True)

    def deselectAll(self):
        """
        Uncheck all boxes in the popup window.
        """
        for i in range(len(self.buttonlist)):
            self.formLayout.itemAt(i).widget().setChecked(False)


class SelectNNImgs(QDialog):
    """
    Prompt user to select which image(s) to use for Nearest Neighbour analysis.

    Args:
        imagenames (list): List of names of each of the images.
    """

    def __init__(self, imagenames):
        self.imagenames = imagenames
        QDialog.__init__(self)
        self.setWindowTitle("Select Image(s)")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formlayout = QFormLayout(self)
        image4analysis = QLabel("Image(s) to analyze: ")
        self.imgname = QComboBox(self)
        self.OK = False
        for imgname in imagenames:
            self.imgname.addItem(str(imgname.split("/")[-1].split(".")[0]))
        self.imgname.addItem("All")
        formlayout.addRow(image4analysis, self.imgname)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formlayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user selections.
        """
        self.selimg = self.imgname.currentText()
        if self.selimg == 'All':
            imgindex = len(self.imagenames)
        else:
            imgindex = self.imgname.currentIndex()
        print(imgindex)
        self.imgindex = imgindex
        self.OK = True
        self.close()


class SelectSegmentedImage(QDialog):
    """
    Prompt user to select which round of segmentation to use for downstream analysis.

    Args:
        segresultnames (list): List of names of segmentation results.
    """

    def __init__(self, segresultnames):
        QDialog.__init__(self)
        self.setWindowTitle("Select Segmentation Results")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.OK = False
        formLayout = QFormLayout(self)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        self.segresultnames = segresultnames
        labelimage = QLabel("Segmentation Results: ")
        self.images = QComboBox(self)
        for image in segresultnames:
            self.images.addItem(image)
        formLayout.addRow(labelimage, self.images)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user selections.
        """
        self.image = self.images.currentText()
        self.imageindex = self.segresultnames.index(self.image)
        self.OK = True
        self.close()


class SpatialParameters(QDialog):
    """
    Prompt user to define parameters for spatial codistribution.
    """

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Set spatial codistribution parameters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        npixlabel = QLabel("Pixels per simulation:")
        self.npixentry = QLineEdit("1000")
        nsimlabel = QLabel("Number of simulations:")
        self.nsimentry = QLineEdit("10")
        self.OK = False
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout = QFormLayout(self)
        formLayout.addRow(npixlabel, self.npixentry)
        formLayout.addRow(nsimlabel, self.nsimentry)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.npix = int(self.npixentry.text())
        self.nsim = int(self.nsimentry.text())
        self.OK = True
        self.close()


class SubCluster(QDialog):
    """
    Prompt user to indicate which cluster to subdivide.

    Args:
        clusterindices (list): List of cluster IDs to select from.
    """

    def __init__(self, clusterindices):
        QDialog.__init__(self)
        self.setWindowTitle("Select Cluster to be Divided")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formLayout = QFormLayout(self)
        labelcluster = QLabel("Cluster: ")
        self.cluster = QComboBox(self)
        self.OK = False
        for cluster in clusterindices:
            self.cluster.addItem(str(cluster))
        formLayout.addRow(labelcluster, self.cluster)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formLayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user input.
        """
        self.cluster = int(self.cluster.currentText())
        self.OK = True
        self.close()


class TableFilters(QDialog):
    """
    Prompt user to set filters for one of the columns in the table.

    Args:
        markernames (list): List of names of each of the cell markers.
    """

    def __init__(self, markernames):
        QDialog.__init__(self)
        self.setWindowTitle("Table Filters")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        self.reset = False
        formlayout = QFormLayout(self)
        labelmarkers = QLabel("Marker: ")
        label2 = QLabel("Filter Type: ")
        self.markers = QComboBox(self)
        self.bounds = QComboBox(self)
        self.OK = False
        self.dict = {}
        paramnames = markernames + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        for param in paramnames:
            self.markers.addItem(param)
            self.dict[param] = paramnames.index(param) + 1
        self.bounds.addItem("Lower Bound")
        self.bounds.addItem("Upper Bound")
        self.filterval = QLineEdit("0.0")
        filtervallabel = QLabel("Filter Value: ")
        formlayout.addRow(labelmarkers, self.markers)
        formlayout.addRow(label2, self.bounds)
        formlayout.addRow(filtervallabel, self.filterval)
        okbutton = QPushButton()
        okbutton.setText("OK")
        okbutton.clicked.connect(self.add)
        resetbutton = QPushButton()
        resetbutton.setText("Reset")
        resetbutton.clicked.connect(self.resetFilters)
        formlayout.addRow("", QLabel(""))
        formlayout.addRow(okbutton)
        formlayout.addRow(resetbutton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.marker = self.markers.currentText()
        self.bound = self.bounds.currentText()
        self.val = float(self.filterval.text())
        self.OK = True
        self.close()

    def resetFilters(self):
        """
        Called when user selects to reset all table filters. Close window and store user selection.
        """
        self.reset = True
        self.OK = True
        self.close()


class UMAPParameters(QDialog):
    """
    Prompt user to define parameters and coloring schemes for UMAP plots.

    Args:
        hasclusteredobjects (bool): True if user has performed object-based clustering, otherwise False.
        segresultnames (list): List of names of segmentation results.
        groupsnames (list): List of names of experimental conditions for UMAP coloring.
    """

    def __init__(self, hasclusteredobjects, segresultnames, groupsnames):
        QDialog.__init__(self)
        Labeldistance = QLabel("Distance:")
        self.Textdistance = QComboBox()
        self.Textdistance.addItem("cosine")
        self.Textdistance.addItem("correlation")
        self.Textdistance.addItem("euclidean")
        self.Textdistance.setFixedWidth(134)
        n_neighbors = QLabel("Neighborhood Size:")
        self.n_neighbors = QLineEdit("70")
        min_dist = QLabel("Minimum Distance:")
        self.min_dist = QLineEdit("0.03")
        self.hasclusteredobjects = hasclusteredobjects
        self.groupsnames = groupsnames
        self.OK = False
        self.oneselected = False
        self.setWindowTitle("UMAP Plots")
        w = font_width(self.font().family(), self.font().pointSize(), [self.windowTitle()])
        self.setMinimumWidth(w + 100)
        formlayout = QFormLayout(self)
        formlayout.addRow(Labeldistance, self.Textdistance)
        formlayout.addRow(n_neighbors, self.n_neighbors)
        formlayout.addRow(min_dist, self.min_dist)
        formlayout.addRow("", QLabel(""))

        self.segresultnames = segresultnames
        if len(segresultnames) > 1:
            labelimage = QLabel("Image: ")
            self.images = QComboBox(self)
            for image in segresultnames:
                self.images.addItem(image)
            formlayout.addRow(labelimage, self.images)
            formlayout.addRow("", QLabel(""))

        self.buttonlist = []
        box2 = QCheckBox("Color according to cell marker expression")
        box2.setChecked(True)
        formlayout.addRow(box2)
        self.buttonlist.append(box2)
        if hasclusteredobjects:
            box3 = QCheckBox("Color according to individual clusters")
            box3.setChecked(True)
            formlayout.addRow(box3)
            self.buttonlist.append(box3)
            box4 = QCheckBox("Color according to combined clusters")
            box4.setChecked(True)
            formlayout.addRow(box4)
            self.buttonlist.append(box4)
        if len(groupsnames) > 0:
            for i in range(len(groupsnames)):
                box = QCheckBox("Color according to group assignment: " + groupsnames[i])
                box.setChecked(True)
                formlayout.addRow(box)
                self.buttonlist.append(box)
        okButton = QPushButton()
        okButton.setText("OK")
        okButton.clicked.connect(self.add)
        formlayout.addRow(okButton, okButton)

    def add(self):
        """
        Close window and store user inputs.
        """
        self.distance = self.Textdistance.currentText()
        self.min_dist = float(self.min_dist.text())
        self.n_neighbors = int(self.n_neighbors.text())
        if len(self.segresultnames) > 1:
            self.imageindex = self.segresultnames.index(self.images.currentText())
        else:
            self.imageindex = 0
        self.colorbymarkers = self.buttonlist[0].isChecked()
        self.colorbygroups = []
        if self.hasclusteredobjects:
            self.colorbyindivclusters = self.buttonlist[1].isChecked()
            self.colorbycombclusters = self.buttonlist[2].isChecked()
            if len(self.groupsnames) > 0:
                for i in range(3, len(self.buttonlist)):
                    if self.buttonlist[i].isChecked():
                        self.colorbygroups.append(i - 3)
        elif len(self.groupsnames) > 0:
            print(len(self.buttonlist))
            for i in range(1, len(self.buttonlist)):
                if self.buttonlist[i].isChecked():
                    self.colorbygroups.append(i - 1)
        self.OK = True
        self.close()


def create_new_folder(name, outfolder):
    """
    Creates a new subfolder within the user-defined output folder. This is used to compartmentalize results, as well as
    to ensure that a unique output folder is created for each time the same functionality is run (ie, creates different
    folders for different rounds of segmentation).

    Args:
        name (str): Base name of the new folder being created.
        outfolder (str): Path to the output folder where results will be saved.
    """
    count = 1
    while True:
        dir = os.path.join(outfolder, f"{name}{count}")
        if not os.path.exists(dir):
            os.mkdir(dir)
            break
        else:
            count += 1
    return dir


def display_error_message(text, detailedtext):
    """
    Generate a popup window when the user does something they are not supposed to.

    Args:
        text (str): Brief error message.
        detailedtext (str): Detailed error message.
    """
    msg = QMessageBox()
    msg.setWindowTitle("RAPID Alert")
    msg.setText(text)
    msg.setDetailedText(detailedtext)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


def font_width(style, size, strings):
    """
    Find the maximum width, in pixels, from a list of strings in a specified font size and style.

    Args:
        style (str): The font style for the list of strings being displayed.
        size (int): The font size for the list of strings being displayed.
        strings (list): List of strings that the maximum width is to be calculated for.

    :return: width *(int)*: \n
        The pixel-width required to contain each of the input strings with the specified size and font.
    """
    width = 1
    for label in strings:
        w = QFontMetrics(QFont(style, pointSize=size)).boundingRect(label).width()
        if w > width:
            width = w
    return width


def get_nn_in_radius(data=None, clusterid1=None, clusterid2=None, radius=100, nn=0):
    """
    Find all cells in a given cluster that are within a user-defined radius or number of nearest neighbours from a cell
    in a different cluster.

    Args:
        data (pandas.Series, optional): Table containing quantified values for all cells in the image being analyzed (Default: None).
        clusterid1 (int, optional): ID for the source cluster (Default: None).
        clusterid2 (int, optional): ID for the target cluster (Default: None).
        radius (int, optional): Maximum distance from source cluster to search for cells from target cluster (Default: 100).
        nn (int, optional): Maximum number of nearest neighbours from each cell in the source cluster to search for cells from target cluster (Default: 0).

    :return: cellind *(pandas.DataFrame)*: \n
        Dataframe containing the IDs for each of the cells from the source cluster that fall within the user-defined distance or number of nearest neighbours.
    """
    data4cluster1 = data[data['Cluster'] == str(clusterid1)]
    print("CLUSTER 1:", data4cluster1.shape)
    data4cluster2 = data[data['Cluster'] == str(clusterid2)]
    print("CLUSTER 2:", data4cluster2.shape)
    ckdtree4c1 = cKDTree(data4cluster1[["X", "Y"]])
    ckdtree4c2 = cKDTree(data4cluster2[["X", "Y"]])
    if nn == 0:
        retttt = data4cluster2.iloc[np.unique(np.hstack(ckdtree4c1.query_ball_tree(ckdtree4c2, radius)))]
    else:
        retttt = data4cluster2.iloc[
            np.unique(np.hstack(ckdtree4c2.query(data4cluster1[["X", "Y"]], nn, distance_upper_bound=radius)[1]))[:-1]]
    cellind = retttt['Label']
    return cellind


def log_actions(outfolder, text):
    """
    Record all actions taken in the GUI by saving to a file within the output folder.

    Args:
        outfolder (str): Path to the output folder where results will be saved.
        text (str): Text to be added in the file indicating the exact action that was taken by the user.
    """
    logging.basicConfig(filename=os.path.join(outfolder, 'logger.log'), encoding='utf-8', level=logging.DEBUG)
    logging.info(text)


def nn_to_heatmap(data, clusterid1=None, radius=100, nn=0):
    """
    Generate a heatmap during nearest neighbour analysis illustrating the differential expression of each marker in the
    selected cells relative to overall marker expression within the source cluster.

    Args:
        data (pandas.DataFrame): Dataframe with quantified values and coordinates for each cell within the constraints of the nearest neighbour analysis.
        clusterid1 (int, optional): ID for the source cluster.
        radius (int, optional): Maximum distance from source cluster to search for cells from target cluster (Default: 100).
        nn (int, optional): Maximum number of nearest neighbours from each cell in the source cluster to search for cells from target cluster (Default: 0).

    :return: nnplot *(seaborn.matrix.ClusterGrid)*: \n
        Heatmap plot.
    """
    data['X'] = data['X'] * (data['ImgID'] + 1) + 100000
    data['Y'] = data['Y'] * (data['ImgID'] + 1) + 100000
    uniqueclusters = np.unique(data['Cluster'])
    dict = {}
    dictfulldata = {}
    if nn == 0:
        nn = 100
    for i in uniqueclusters:
        dict[i] = cKDTree(data[data['Cluster'] == str(i)][["X", "Y"]])
        dictfulldata[i] = data[data['Cluster'] == str(i)]
    FinMat2 = np.zeros((len(uniqueclusters), data.loc[:, 'Cluster':].shape[1]-1))
    NormlizationFactor = dictfulldata[clusterid1].loc[:, 'Cluster':].iloc[:,1:].mean().values
    for i in range(len(uniqueclusters)):
        uniquerowid = np.unique(np.hstack(
            dict[uniqueclusters[i]].query(dictfulldata[clusterid1][["X", "Y"]], nn, distance_upper_bound=radius)[1]))
        if len(uniquerowid) > 0:
            FinMat2[i, :] = np.log10(dictfulldata[uniqueclusters[i]].iloc[uniquerowid[:-1]].loc[:,"Cluster":].iloc[:,1:].mean().values + 1e-5) - np.log10(NormlizationFactor + 1e-5)
    FinMat2 = np.nan_to_num(FinMat2)
    DF = pd.DataFrame(FinMat2)
    DF.columns = data.loc[:, "Cluster":].columns[1:]
    DF = DF.replace(np.inf, 10)
    DF = DF.replace(-np.inf, -10)
    DF.dropna(inplace=True)
    DF.round(2)
    DF[DF < 0.000001] = 0.00001
    nnplot = sns.clustermap(DF, cmap="RdBu_r", row_cluster=False, col_cluster=False)
    return nnplot


def pixel_normtype(normtype):
    if normtype == "None":
        return False, False, "", False
    elif normtype == "zscore":
        return True, False, "zscore", False
    elif normtype == "log2":
        return True, False, "log2", False
    elif normtype == "log10":
        return True, False, "log10", False
    elif normtype == "square root":
        return True, False, "sqrt", False
    elif normtype == "inverse":
        return True, False, "inverse", False
    elif normtype == "all (no PCA)":
        return False, True, "", False
    elif normtype == "all (PCA)":
        return False, True, "", True
