# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sceneGraphWindow.ui'
#
# Created: Thu Apr 11 16:28:10 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_sceneGraphBrowser(object):
    def setupUi(self, sceneGraphBrowser):
        sceneGraphBrowser.setObjectName(_fromUtf8("sceneGraphBrowser"))
        sceneGraphBrowser.resize(234, 511)
        self.centralwidget = QtGui.QWidget(sceneGraphBrowser)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.sgTree = QtGui.QTreeWidget(self.splitter)
        self.sgTree.setObjectName(_fromUtf8("sgTree"))
        self.propertiesTable = QtGui.QTableWidget(self.splitter)
        self.propertiesTable.setObjectName(_fromUtf8("propertiesTable"))
        self.propertiesTable.setColumnCount(0)
        self.propertiesTable.setRowCount(0)
        self.verticalLayout.addWidget(self.splitter)
        sceneGraphBrowser.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(sceneGraphBrowser)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 234, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        sceneGraphBrowser.setMenuBar(self.menubar)

        self.retranslateUi(sceneGraphBrowser)
        QtCore.QMetaObject.connectSlotsByName(sceneGraphBrowser)

    def retranslateUi(self, sceneGraphBrowser):
        sceneGraphBrowser.setWindowTitle(QtGui.QApplication.translate("sceneGraphBrowser", "Scene Graph Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.sgTree.headerItem().setText(0, QtGui.QApplication.translate("sceneGraphBrowser", "Current Scene", None, QtGui.QApplication.UnicodeUTF8))

