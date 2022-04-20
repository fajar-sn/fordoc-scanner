import json
import pytesseract
import cv2
import os
import sys
import PySide6
import glob
import csv

from PIL import Image
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import *
from fordoc_scanner.entities.custom_table_model import CustomTableModel
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
        self.item_count = 0
        self.ui.open_image_button.clicked.connect(self.open_image)
        self.ui.open_camera_button.clicked.connect(self.open_camera)
        self.ui.extract_image_button.clicked.connect(self.extract_image)
        self.ui.save_form_button.clicked.connect(self.save_form)
        self.ui.save_table_button.clicked.connect(self.save_table)

        self.init_data_table()

    def open_image(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Select File')
        self.image = cv2.imread(str(self.filename[0]))
        frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.current_image = QImage(
            frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.ui.image_label.setPixmap(QPixmap.fromImage(self.current_image))

    def open_camera(self):
        open_camera_dialog = OpenCameraDialog()
        if open_camera_dialog.ui.exec():
            print("taking picture on main window")
            # open_camera_dialog.take_picture()
            self.current_image = open_camera_dialog.image
            self.ui.image_label.setPixmap(
                QPixmap.fromImage(open_camera_dialog.image))
        else:
            print("canceled")

    def extract_image(self):
        ocr_process = OcrProcess(self.filename[0])
        ocr_result = ocr_process.result
        # json_result = ocr_process.to_json()
        # parsed_json = json.loads(json_result)

        self.ui.id_line_edit.setText(ocr_result.id)
        self.ui.name_line_edit.setText(ocr_result.name)
        self.ui.birthplace_line_edit.setText(ocr_result.birth_place)
        self.ui.birth_date_line_edit.setText(ocr_result.birth_date)
        self.ui.gender_line_edit.setText(ocr_result.gender)
        self.ui.blood_group_line_edit.setText(ocr_result.blood_group)
        self.ui.address_line_edit.setText(ocr_result.address)
        self.ui.rtrw_line_edit.setText(f"{ocr_result.rt}/{ocr_result.rw}")
        self.ui.village_line_edit.setText(ocr_result.village)
        self.ui.district_line_edit.setText(ocr_result.district)
        self.ui.religion_line_edit.setText(ocr_result.relligion)
        self.ui.marriage_status_line_edit.setText(ocr_result.marriage_status)
        self.ui.job_line_edit.setText(ocr_result.job)
        self.ui.citizenship_line_edit.setText(ocr_result.citizenship)
        self.ui.valid_until_line_edit.setText(ocr_result.valid_until)

    def init_data_table(self):
        self.table_model = CustomTableModel()
        self.ui.table_view.setModel(self.table_model)

    def save_form(self):
        id = self.ui.id_line_edit.text()
        name = self.ui.name_line_edit.text()
        birthplace = self.ui.birthplace_line_edit.text()
        birth_date = self.ui.birth_date_line_edit.text()
        gender = self.ui.gender_line_edit.text()
        blood_group = self.ui.blood_group_line_edit.text()
        address = self.ui.address_line_edit.text()
        rtrw = self.ui.rtrw_line_edit.text()
        village = self.ui.village_line_edit.text()
        district = self.ui.district_line_edit.text()
        relligion = self.ui.religion_line_edit.text()
        marriage_status = self.ui.marriage_status_line_edit.text()
        job = self.ui.job_line_edit.text()
        citizenship = self.ui.citizenship_line_edit.text()
        valid_until = self.ui.valid_until_line_edit.text()

        self.table_model.extracted_data.append([
            id, name, birthplace, birth_date, gender, blood_group, address, rtrw, village, district, relligion, marriage_status, job, citizenship, valid_until
        ])
        self.table_model.layoutChanged.emit()

        # id_item = QTableWidgetItem(id)
        # name_item = QTableWidgetItem(name)
        # birthplace_item = QTableWidgetItem(birthplace)
        # birth_date_item = QTableWidgetItem(birth_date)
        # gender_item = QTableWidgetItem(gender)
        # blood_group_item = QTableWidgetItem(blood_group)
        # address_item = QTableWidgetItem(address)
        # rtrw_item = QTableWidgetItem(rtrw)
        # village_item = QTableWidgetItem(village)
        # district_item = QTableWidgetItem(district)
        # relligion_item = QTableWidgetItem(relligion)
        # marriage_status_item = QTableWidgetItem(marriage_status)
        # job_item = QTableWidgetItem(job)
        # citizenship_item = QTableWidgetItem(citizenship)
        # valid_until_item = QTableWidgetItem(valid_until)

        # index = QModelIndex()
        # self.table_model.beginInsertRows(index, self.item_count, self.item_count + 1)
        # self.table_model.insertRow(self.item_count, index)
        # self.table_model.setData(index, 'aa')
        # self.table_model.endInsertRows()

        # self.table_model.setItem(self.item_count, 0, id_item)
        # self.table_model.setItem(self.item_count, 1, name_item)

        self.ui.id_line_edit.setText('')
        self.ui.name_line_edit.setText('')
        self.ui.birthplace_line_edit.setText('')
        self.ui.birth_date_line_edit.setText('')
        self.ui.gender_line_edit.setText('')
        self.ui.blood_group_line_edit.setText('')
        self.ui.address_line_edit.setText('')
        self.ui.rtrw_line_edit.setText('')
        self.ui.village_line_edit.setText('')
        self.ui.district_line_edit.setText('')
        self.ui.religion_line_edit.setText('')
        self.ui.marriage_status_line_edit.setText('')
        self.ui.job_line_edit.setText('')
        self.ui.citizenship_line_edit.setText('')
        self.ui.valid_until_line_edit.setText('')

        self.item_count += 1

    def save_table(self):
        outfile = open('./export-result.csv', 'w', newline='')
        writer = csv.writer(outfile)
        writer.writerow(["NIK", "Nama", "Tempat Lahir", "Tanggal Lahir", "Jenis Kelamin", "Golongan Darah", "Alamat", "RT/RW", "Kelurahan/Desa", "Kecamatan", "Agama", "Status Perkawinan", "Pekerjaan", "Kewarganegaraan", "Berlaku Hingga"])
        writer.writerows(self.table_model.extracted_data)