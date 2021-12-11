import pytesseract
import cv2
import os
import sys
import PySide6
import glob

from PIL import Image
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        ui_file = QFile("./fordoc_scanner/views/main_window/main_window.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        self.image = None
        self.ui.open_image_button.clicked.connect(self.open_image)

    def open_image(self):
        filename = QFileDialog.getOpenFileName(self, 'Select File')
        self.image = cv2.imread(str(filename[0]))
        frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.ui.image_label.setPixmap(QPixmap.fromImage(image))
