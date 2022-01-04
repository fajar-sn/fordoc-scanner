from PySide6.QtCore import QFile, QDate, QStandardPaths, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QImage
from PySide6.QtMultimedia import (QCamera, QImageCapture,
                                  QMediaCaptureSession,
                                  QMediaDevices)
from PySide6.QtMultimediaWidgets import QVideoWidget

from fordoc_scanner import views

import os
import sys

class OpenCameraDialog(QDialog):
    def __init__(self):
        super().__init__()
        ui_file = QFile(views.views_file_location +
                        "/open_camera_dialog/open_camera_dialog.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        self.test = "tes gambar"

        self.image = None
        self._capture_session = None
        self._camera = None
        self._camera_info = None
        self._image_capture = None

        self.available_cameras = QMediaDevices.videoInputs()

        if self.available_cameras:
            self.ui.cameras_combo_box.addItems([camera.description() for camera in self.available_cameras])
            self.ui.cameras_combo_box.currentIndexChanged.connect(self.select_camera)
            self.select_camera(0)
            self.ui.button_box.accepted.connect(self.take_picture())


    def show_status_message(self, message):
        self.ui.status_label.setText(message)

    # def closeEvent(self, event):
    #     if self._camera and self._camera.isActive():
    #         self._camera.stop()
    #     event.accept()

    def next_image_file_name(self):
        print("getting file name")
        pictures_location = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        date_string = QDate.currentDate().toString("yyyyMMdd")
        pattern = f"{pictures_location}/pyside6_camera_{date_string}_{{:03d}}.jpg"
        n = 1
        while True:
            result = pattern.format(n)
            if not os.path.exists(result):
                return result
            n = n + 1
        # pictures_location = QStandardPaths.writableLocation(
        #     QStandardPaths.PicturesLocation)
        # print(f"location {pictures_location}")
        # date_string = QDate.currentDate().toString("yyyyMMdd")
        # pattern = f"{pictures_location}/pyside6_camera_{date_string}_{{:03d}}.jpg"
        # print(f"pattern {pattern}")
        # n = 1
        # while True:
        #     result = pattern.format(n)
        #     if not os.path.exists(result):
        #         print(f"result {result}")
        #         return result
        #     n = n + 1
        # return None

    @Slot()
    def take_picture(self):
        print("taking picture on dialog")
        # self._camera.start()
        print("starting camera")
        self._current_preview = QImage()
        result = self._image_capture.captureToFile(self.next_image_file_name())
        print(f"capture status {result}")
        # print(self._image_capture.capture())
        
        # self._camera.stop()

    @Slot(int, QImage)
    def image_captured(self, id, previewImage):
        self._current_preview = previewImage
        print(f"image captured id {id} {previewImage}")
        self.image = previewImage

    @Slot(int, str)
    def image_saved(self, id, fileName):
        print(f"image saved id {id} name {fileName}")
        # index = self._tab_widget.count()
        # image_view = ImageView(self._current_preview, fileName)
        # self._tab_widget.addTab(image_view, f"Capture #{index}")
        # self._tab_widget.setCurrentIndex(index)

    @Slot(int, QImageCapture.Error, str)
    def _capture_error(self, id, error, error_string):
        print("capture error")
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    @Slot(QCamera.Error, str)
    def _camera_error(self, error, error_string):
        print("camera error")
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    def select_camera(self, index):
        self._camera_info = self.available_cameras[index]
        self._camera = QCamera(self._camera_info)
        self._camera.errorOccurred.connect(self._camera_error)
        self._image_capture = QImageCapture(self._camera)
        self._image_capture.imageCaptured.connect(self.image_captured)
        self._image_capture.imageSaved.connect(self.image_saved)
        self._image_capture.errorOccurred.connect(self._capture_error)
        self._capture_session = QMediaCaptureSession()
        self._capture_session.setCamera(self._camera)
        self._capture_session.setImageCapture(self._image_capture)
        
        current_widget = self.ui.stacked_widget.currentWidget()
        self.ui.stacked_widget.removeWidget(current_widget)
        camera_view_finder = QVideoWidget()
        self.ui.stacked_widget.addWidget(camera_view_finder)

        if self._camera and self._camera.error() == QCamera.NoError:
            name = self._camera_info.description()
            self.show_status_message(f"Starting: '{name}'")
            self._capture_session.setVideoOutput(camera_view_finder)
            # self._take_picture_action.setEnabled(self._image_capture.isReadyForCapture())
            # self._image_capture.readyForCaptureChanged.connect(self._take_picture_action.setEnabled)
            self._camera.start()
        else:
            # self._take_picture_action.setEnabled(False)
            self.show_status_message("Camera unavailable")
