# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(403, 405)
        About.setMinimumSize(QtCore.QSize(403, 405))
        About.setMaximumSize(QtCore.QSize(403, 405))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/RedditDownloaderIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(About)
        self.buttonBox.setGeometry(QtCore.QRect(320, 370, 71, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.logo_label = QtWidgets.QLabel(About)
        self.logo_label.setGeometry(QtCore.QRect(10, 10, 80, 82))
        self.logo_label.setObjectName("logo_label")
        self.license_box = QtWidgets.QTextBrowser(About)
        self.license_box.setGeometry(QtCore.QRect(10, 120, 381, 231))
        self.license_box.setObjectName("license_box")
        self.info_label = QtWidgets.QLabel(About)
        self.info_label.setGeometry(QtCore.QRect(110, 40, 281, 61))
        self.info_label.setObjectName("info_label")
        self.label = QtWidgets.QLabel(About)
        self.label.setGeometry(QtCore.QRect(110, 10, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(About)
        self.buttonBox.accepted.connect(About.accept)
        self.buttonBox.rejected.connect(About.reject)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About"))
        self.logo_label.setText(_translate("About", "TextLabel"))
        self.license_box.setHtml(_translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:8pt;\">Downloader For Reddit is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Courier New\'; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:8pt;\">Downloader For Reddit is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Courier New\'; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:8pt;\">You should have received a copy of the GNU General Public License along with Downloader For Reddit.  If not, see: </span><a href=\"http://www.gnu.org/licenses/\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">http://www.gnu.org/licenses/</span></a></p></body></html>"))
        self.info_label.setText(_translate("About", "TextLabel"))
        self.label.setText(_translate("About", "Downloader For Reddit"))

