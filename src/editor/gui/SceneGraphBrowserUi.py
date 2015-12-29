# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sceneGraphWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_sceneGraphBrowser(object):
    def setupUi(self, sceneGraphBrowser):
        sceneGraphBrowser.setObjectName(_fromUtf8("sceneGraphBrowser"))
        sceneGraphBrowser.resize(454, 814)
        self.centralwidget = QtGui.QWidget(sceneGraphBrowser)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cellinfo = QtGui.QLabel(self.centralwidget)
        self.cellinfo.setObjectName(_fromUtf8("cellinfo"))
        self.verticalLayout.addWidget(self.cellinfo)
        self.tileObjects = QtGui.QListWidget(self.centralwidget)
        self.tileObjects.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tileObjects.setAlternatingRowColors(True)
        self.tileObjects.setTextElideMode(QtCore.Qt.ElideLeft)
        self.tileObjects.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.tileObjects.setResizeMode(QtGui.QListView.Fixed)
        self.tileObjects.setLayoutMode(QtGui.QListView.SinglePass)
        self.tileObjects.setUniformItemSizes(False)
        self.tileObjects.setWordWrap(False)
        self.tileObjects.setObjectName(_fromUtf8("tileObjects"))
        self.verticalLayout.addWidget(self.tileObjects)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.deleteAllTexturesButton = QtGui.QPushButton(self.centralwidget)
        self.deleteAllTexturesButton.setObjectName(_fromUtf8("deleteAllTexturesButton"))
        self.horizontalLayout.addWidget(self.deleteAllTexturesButton)
        self.moveUpButton = QtGui.QPushButton(self.centralwidget)
        self.moveUpButton.setObjectName(_fromUtf8("moveUpButton"))
        self.horizontalLayout.addWidget(self.moveUpButton)
        self.moveDownButton = QtGui.QPushButton(self.centralwidget)
        self.moveDownButton.setObjectName(_fromUtf8("moveDownButton"))
        self.horizontalLayout.addWidget(self.moveDownButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.propertiesTable = QtGui.QTableWidget(self.splitter)
        self.propertiesTable.setObjectName(_fromUtf8("propertiesTable"))
        self.propertiesTable.setColumnCount(0)
        self.propertiesTable.setRowCount(0)
        self.verticalLayout.addWidget(self.splitter)
        sceneGraphBrowser.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(sceneGraphBrowser)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 454, 42))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        sceneGraphBrowser.setMenuBar(self.menubar)

        self.retranslateUi(sceneGraphBrowser)
        QtCore.QMetaObject.connectSlotsByName(sceneGraphBrowser)

    def retranslateUi(self, sceneGraphBrowser):
        sceneGraphBrowser.setWindowTitle(_translate("sceneGraphBrowser", "Scene Graph Browser", None))
        self.cellinfo.setText(_translate("sceneGraphBrowser", "Current Tile: (0,0)", None))
        self.deleteAllTexturesButton.setText(_translate("sceneGraphBrowser", "Delete all tex", None))
        self.moveUpButton.setText(_translate("sceneGraphBrowser", "Up", None))
        self.moveDownButton.setText(_translate("sceneGraphBrowser", "Down", None))

