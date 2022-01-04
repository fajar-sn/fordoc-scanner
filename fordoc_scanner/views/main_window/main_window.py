import json
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
from fordoc_scanner.logics.ocr_process.ocr_process import OcrProcess

from fordoc_scanner.views.open_camera_dialog.open_camera_dialog import OpenCameraDialog

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        ui_file = QFile("./fordoc_scanner/views/main_window/main_window.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        self.image = None
        self.ui.open_image_button.clicked.connect(self.open_image)
        self.ui.open_camera_button.clicked.connect(self.open_camera)
        self.ui.extract_image_button.clicked.connect(self.extract_image)

    def open_image(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Select File')
        self.image = cv2.imread(str(self.filename[0]))
        frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.current_image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.ui.image_label.setPixmap(QPixmap.fromImage(self.current_image))

    def open_camera(self):
        open_camera_dialog = OpenCameraDialog()
        if open_camera_dialog.ui.exec():
            print("taking picture on main window")
            # open_camera_dialog.take_picture()
            self.current_image = open_camera_dialog.image
            self.ui.image_label.setPixmap(QPixmap.fromImage(open_camera_dialog.image))
        else:
            print("canceled")

    def extract_image(self):
        ocr_process = OcrProcess(self.filename[0])
        json_result = ocr_process.to_json()
        parsed_json = json.loads(json_result)

        self.ui.id_line_edit.setText(parsed_json['nik'])
        self.ui.name_line_edit.setText(parsed_json['nama'])
        self.ui.birthplace_line_edit.setText(parsed_json['tempat_lahir'])
        self.ui.birth_date_line_edit.setText(parsed_json['tanggal_lahir'])
        self.ui.gender_line_edit.setText(parsed_json['jenis_kelamin'])
        self.ui.blood_group_line_edit.setText(parsed_json['golongan_darah'])
        self.ui.address_line_edit.setText(parsed_json['alamat'])
        self.ui.rtrw_line_edit.setText(f"{parsed_json['rt']}/{parsed_json['rw']}")
        self.ui.village_line_edit.setText(parsed_json['kelurahan_atau_desa'])
        self.ui.district_line_edit.setText(parsed_json['kecamatan'])
        self.ui.religion_line_edit.setText(parsed_json['agama'])
        self.ui.marriage_status_line_edit.setText(parsed_json['status_perkawinan'])
        self.ui.job_line_edit.setText(parsed_json['pekerjaan'])
        self.ui.citizenship_line_edit.setText(parsed_json['kewarganegaraan'])
        self.ui.valid_until_line_edit.setText('SEUMUR HIDUP')
