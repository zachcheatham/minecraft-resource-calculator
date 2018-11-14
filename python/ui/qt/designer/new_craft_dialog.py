# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_craft_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_newCraftDialog(object):
    def setupUi(self, newCraftDialog):
        newCraftDialog.setObjectName("newCraftDialog")
        newCraftDialog.setWindowModality(QtCore.Qt.WindowModal)
        newCraftDialog.resize(350, 96)
        newCraftDialog.setMinimumSize(QtCore.QSize(350, 96))
        newCraftDialog.setMaximumSize(QtCore.QSize(350, 96))
        newCraftDialog.setModal(True)
        self.formLayout = QtWidgets.QFormLayout(newCraftDialog)
        self.formLayout.setContentsMargins(-1, -1, -1, 8)
        self.formLayout.setObjectName("formLayout")
        self.itemNameLabel = QtWidgets.QLabel(newCraftDialog)
        self.itemNameLabel.setObjectName("itemNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.itemNameLabel)
        self.itemNameLineEdit = QtWidgets.QLineEdit(newCraftDialog)
        self.itemNameLineEdit.setObjectName("itemNameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.itemNameLineEdit)
        self.quantityLabel = QtWidgets.QLabel(newCraftDialog)
        self.quantityLabel.setObjectName("quantityLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.quantityLabel)
        self.quantitySpinBox = QtWidgets.QSpinBox(newCraftDialog)
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setMaximum(100000)
        self.quantitySpinBox.setObjectName("quantitySpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.quantitySpinBox)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.calculateButton = QtWidgets.QPushButton(newCraftDialog)
        self.calculateButton.setEnabled(False)
        self.calculateButton.setObjectName("calculateButton")
        self.buttonLayout.addWidget(self.calculateButton)
        self.closeButton = QtWidgets.QPushButton(newCraftDialog)
        self.closeButton.setObjectName("closeButton")
        self.buttonLayout.addWidget(self.closeButton)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.SpanningRole, self.buttonLayout)

        self.retranslateUi(newCraftDialog)
        QtCore.QMetaObject.connectSlotsByName(newCraftDialog)

    def retranslateUi(self, newCraftDialog):
        _translate = QtCore.QCoreApplication.translate
        newCraftDialog.setWindowTitle(_translate("newCraftDialog", "New Craft Calculation"))
        self.itemNameLabel.setText(_translate("newCraftDialog", "Item Name"))
        self.quantityLabel.setText(_translate("newCraftDialog", "Quantity"))
        self.calculateButton.setText(_translate("newCraftDialog", "Calculate"))
        self.closeButton.setText(_translate("newCraftDialog", "Close"))

