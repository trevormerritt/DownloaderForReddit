"""
Downloader for Reddit takes a list of reddit users and subreddits and downloads content posted to reddit either by the
users or on the subreddits.


Copyright (C) 2017, Kyle Hickey


This file is part of the Downloader for Reddit.

Downloader for Reddit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Downloader for Reddit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Downloader for Reddit.  If not, see <http://www.gnu.org/licenses/>.
"""


from PyQt5 import QtWidgets, QtCore, QtGui

from AboutDialog_auto import Ui_About


class AboutDialog(QtWidgets.QDialog, Ui_About):

    def __init__(self):
        """
        Opens the "about" dialog box which displays the licensing information
        """
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)

        pixmap = QtGui.QPixmap('Images/RedditDownloaderIcon.png')
        pixmap = pixmap.scaled(QtCore.QSize(183, 186), QtCore.Qt.KeepAspectRatio)
        self.logo_label.setFixedWidth(80)
        self.logo_label.setFixedHeight(82)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)

        self.info_label.setText('Version: 1.0\nAuthor: Kyle H')
        self.info_label.setScaledContents(True)

        self.license_box.setOpenExternalLinks(True)

    def accept(self):
        super().accept()




