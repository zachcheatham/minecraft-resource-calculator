# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(476, 362)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stepsTreeView = QtWidgets.QTreeView(self.centralwidget)
        self.stepsTreeView.setObjectName("stepsTreeView")
        self.verticalLayout_2.addWidget(self.stepsTreeView)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 476, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionNew_Craft = QtWidgets.QAction(mainWindow)
        self.actionNew_Craft.setObjectName("actionNew_Craft")
        self.actionQuit = QtWidgets.QAction(mainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionEditRecipe = QtWidgets.QAction(mainWindow)
        self.actionEditRecipe.setObjectName("actionEditRecipe")
        self.actionAbout = QtWidgets.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExpand_All = QtWidgets.QAction(mainWindow)
        self.actionExpand_All.setObjectName("actionExpand_All")
        self.actionNew_Craft_New_Window = QtWidgets.QAction(mainWindow)
        self.actionNew_Craft_New_Window.setObjectName("actionNew_Craft_New_Window")
        self.menuFile.addAction(self.actionNew_Craft)
        self.menuFile.addAction(self.actionNew_Craft_New_Window)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionEditRecipe)
        self.menuHelp.addAction(self.actionAbout)
        self.menuView.addAction(self.actionExpand_All)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Minecraft Resource Calculator"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuEdit.setTitle(_translate("mainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.menuView.setTitle(_translate("mainWindow", "View"))
        self.actionNew_Craft.setText(_translate("mainWindow", "New Craft..."))
        self.actionQuit.setText(_translate("mainWindow", "Quit"))
        self.actionEditRecipe.setText(_translate("mainWindow", "Recipe..."))
        self.actionEditRecipe.setToolTip(_translate("mainWindow", "Edit Recipe"))
        self.actionAbout.setText(_translate("mainWindow", "About"))
        self.actionExpand_All.setText(_translate("mainWindow", "Expand All"))
        self.actionNew_Craft_New_Window.setText(_translate("mainWindow", "New Craft (New Window)..."))

