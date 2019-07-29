# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beckhoff_debug_console.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_m4_BeckHoffDebug(object):
    def setupUi(self, m4_BeckHoffDebug):
        m4_BeckHoffDebug.setObjectName("m4_BeckHoffDebug")
        m4_BeckHoffDebug.resize(817, 549)
        self.m4_FWEnableBtn = QtWidgets.QPushButton(m4_BeckHoffDebug)
        self.m4_FWEnableBtn.setGeometry(QtCore.QRect(30, 50, 93, 28))
        self.m4_FWEnableBtn.setObjectName("m4_FWEnableBtn")
        self.m4_FYEnableBtn = QtWidgets.QPushButton(m4_BeckHoffDebug)
        self.m4_FYEnableBtn.setGeometry(QtCore.QRect(30, 140, 93, 28))
        self.m4_FYEnableBtn.setObjectName("m4_FYEnableBtn")
        self.m4_FWDisenableBtn = QtWidgets.QPushButton(m4_BeckHoffDebug)
        self.m4_FWDisenableBtn.setGeometry(QtCore.QRect(30, 80, 93, 28))
        self.m4_FWDisenableBtn.setObjectName("m4_FWDisenableBtn")
        self.m4_FYDisenableBtn = QtWidgets.QPushButton(m4_BeckHoffDebug)
        self.m4_FYDisenableBtn.setGeometry(QtCore.QRect(30, 170, 93, 28))
        self.m4_FYDisenableBtn.setObjectName("m4_FYDisenableBtn")
        self.m4_FWEnableFlag_T = QtWidgets.QLineEdit(m4_BeckHoffDebug)
        self.m4_FWEnableFlag_T.setGeometry(QtCore.QRect(140, 80, 61, 21))
        self.m4_FWEnableFlag_T.setObjectName("m4_FWEnableFlag_T")
        self.label = QtWidgets.QLabel(m4_BeckHoffDebug)
        self.label.setGeometry(QtCore.QRect(140, 50, 131, 16))
        self.label.setObjectName("label")
        self.m4_FYEnableFlag_T = QtWidgets.QLineEdit(m4_BeckHoffDebug)
        self.m4_FYEnableFlag_T.setGeometry(QtCore.QRect(140, 170, 61, 21))
        self.m4_FYEnableFlag_T.setObjectName("m4_FYEnableFlag_T")
        self.label_2 = QtWidgets.QLabel(m4_BeckHoffDebug)
        self.label_2.setGeometry(QtCore.QRect(140, 140, 131, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(m4_BeckHoffDebug)
        QtCore.QMetaObject.connectSlotsByName(m4_BeckHoffDebug)

    def retranslateUi(self, m4_BeckHoffDebug):
        _translate = QtCore.QCoreApplication.translate
        m4_BeckHoffDebug.setWindowTitle(_translate("m4_BeckHoffDebug", "BeckHoff Controller Debug Console"))
        self.m4_FWEnableBtn.setText(_translate("m4_BeckHoffDebug", "方位轴上电"))
        self.m4_FYEnableBtn.setText(_translate("m4_BeckHoffDebug", "俯仰轴上电"))
        self.m4_FWDisenableBtn.setText(_translate("m4_BeckHoffDebug", "方位轴断电"))
        self.m4_FYDisenableBtn.setText(_translate("m4_BeckHoffDebug", "俯仰轴断电"))
        self.label.setText(_translate("m4_BeckHoffDebug", "方位轴使能标志位"))
        self.label_2.setText(_translate("m4_BeckHoffDebug", "俯仰轴使能标志位"))

