import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QGridLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QSizePolicy, QScrollArea, QMessageBox
from PyQt6.QtGui import QPixmap, QAction, QGuiApplication, QIcon
from PyQt6 import QtCore
from PyQt6.QtCore import QSize
from yolo_object_detection import ObjectDetector


class ImageViewerApp(QMainWindow):
    currentImgPath = None
    originalImgSize = None
    original_pixmap = None
    obj_det = ObjectDetector(
        "yolov3_custom_final.weights", "yolov3_custom.cfg", "data/obj.names")

    def __init__(self):
        super().__init__()
        self.image_label = QLabel("Image Display Area")
        self.initUI()

    def initUI(self):
        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layouts
        main_layout = QHBoxLayout(central_widget)
        left_panel_layout = QVBoxLayout()
        image_panel_layout = QVBoxLayout()

        # Left panel widgets
        left_panel_label = QLabel()
        left_panel_label.setObjectName("leftPanel")
        left_panel_layout.addWidget(left_panel_label)
        button_layout = QGridLayout(left_panel_label)
        openFileBtn = QPushButton()
        openFileBtn.setIcon(QIcon("app-data/icons/file-icon.svg"))
        self.setButtonIconSize(openFileBtn)
        button_layout.addWidget(openFileBtn)
        openDirBtn = QPushButton()
        openDirBtn.setIcon(QIcon("app-data/icons/open-dir.png"))
        self.setButtonIconSize(openDirBtn)
        button_layout.addWidget(openDirBtn)
        zoomInBtn = QPushButton()
        button_layout.addWidget(zoomInBtn)
        zoomInBtn.setIcon(QIcon("app-data/icons/zoomIn.png"))
        self.setButtonIconSize(zoomInBtn)
        zoomOutBtn = QPushButton()
        zoomOutBtn.setIcon(QIcon("app-data/icons/zoomOut.png"))
        self.setButtonIconSize(zoomOutBtn)
        button_layout.addWidget(zoomOutBtn)
        openFileBtn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        openDirBtn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        zoomInBtn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        zoomOutBtn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        openFileBtn.clicked.connect(self.openImage)
        zoomInBtn.clicked.connect(lambda: self.zoomImage(1.1))
        zoomOutBtn.clicked.connect(lambda: self.zoomImage(0.9))
        openDirBtn.clicked.connect(self.openDirectory)

        # Image panel widgets
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Add scroll area to contain the image label
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)
        image_panel_layout.addWidget(scroll_area)

        # Button to trigger YOLO model treatment
        self.compute_button = QPushButton("Compute YOLO Model Treatment")
        self.compute_button.clicked.connect(self.computeResearch)
        image_panel_layout.addWidget(self.compute_button)

        self.nextImgBtn = QPushButton()
        self.nextImgBtn.clicked.connect(self.goToNextImage)
        self.nextImgBtn.setIcon(QIcon("app-data/icons/next-arrow.png"))
        self.setButtonIconSize(self.nextImgBtn)
        self.nextImgBtn.setEnabled(False)
        self.nextImgBtn.setVisible(False)

        self.backImgBtn = QPushButton()
        self.backImgBtn.clicked.connect(self.goToPrevImage)
        self.backImgBtn.setIcon(QIcon("app-data/icons/back-arrow.png"))
        self.setButtonIconSize(self.backImgBtn)
        self.backImgBtn.setEnabled(False)
        self.backImgBtn.setVisible(False)
        
        btnDirContainer = QHBoxLayout()
        btnDirContainer.addWidget(self.backImgBtn)
        btnDirContainer.addWidget(self.nextImgBtn)
        image_panel_layout.addLayout(btnDirContainer)

        # Set layouts to central widget
        # Left panel takes 1/3 of the space
        main_layout.addLayout(left_panel_layout, 1)
        # Image panel takes 2/3 of the space
        main_layout.addLayout(image_panel_layout, 2)

        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # Open action in File menu
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openImage)
        file_menu.addAction(open_action)

        # Exit action in File menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.setGeometry(100, 100, 1000, 800)

        self.setWindowTitle('App')
        self.show()

    def openImage(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.jpg *.bmp);;All Files (*)")

        if fileName:
            self.currentImgPath = fileName
            pixmap = QPixmap(fileName)
            self.image_label.setPixmap(pixmap)
            self.originalImgSize = pixmap.size()
            self.original_pixmap = pixmap
            self.nextImgBtn.setEnabled(False)
            self.nextImgBtn.setVisible(False)
            self.backImgBtn.setVisible(False)
            self.backImgBtn.setEnabled(False)

    def loadImage(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.currentImgPath = file_path
            self.image_label.setPixmap(pixmap)
            self.originalImgSize = pixmap.size()
            self.original_pixmap = pixmap
        else:
            QMessageBox.warning(self, "Error", "Failed to load image.")

    def openDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Directory")
        if directory:
            self.image_files = [file for file in os.listdir(
                directory) if file.lower().endswith(('.png', '.jpg', '.bmp'))]
            if not self.image_files:
                QMessageBox.warning(
                    self, "Warning", "No image files found in the directory.")
                return

            self.currentIndex = 0
            self.loadImage(os.path.join(
                directory, self.image_files[self.currentIndex]))
            self.nextImgBtn.setEnabled(True)
            self.nextImgBtn.setVisible(True)
            self.backImgBtn.setVisible(True)
            self.backImgBtn.setEnabled(False)

    def goToNextImage(self):
        if hasattr(self, 'image_files') and hasattr(self, 'currentIndex'):
            if self.currentIndex < len(self.image_files) - 1:
                self.currentIndex += 1
                self.loadImage(os.path.join(os.path.dirname(
                    self.currentImgPath), self.image_files[self.currentIndex]))
                self.backImgBtn.setEnabled(True)
                if self.currentIndex == len(self.image_files) - 1:
                    self.nextImgBtn.setEnabled(False)
    
    def goToPrevImage(self):
        if hasattr(self, 'image_files') and hasattr(self, 'currentIndex'):
            if self.currentIndex > 0:
                self.currentIndex -= 1
                self.loadImage(os.path.join(os.path.dirname(
                    self.currentImgPath), self.image_files[self.currentIndex]))
                if self.currentIndex == 0:
                    self.backImgBtn.setEnabled(False)
            if self.currentIndex >= 0 and self.currentIndex < len(self.image_files) - 1:
                self.nextImgBtn.setEnabled(True)

    def closeEvent(self, event):
        shutil.rmtree("tmp/", ignore_errors=True)
        event.accept()

    def zoomImage(self, factor):
        if self.currentImgPath != None and self.original_pixmap != None:
            pixmap = self.image_label.pixmap()
            size = pixmap.size()
            newWidth = int(size.width() * factor)
            newHeight = int(size.height() * factor)
            if (self.originalImgSize.width() <= newWidth and self.originalImgSize.height() <= newHeight):
                size.setWidth(newWidth)
                size.setHeight(newHeight)
                pixmap = pixmap.scaled(size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                       QtCore.Qt.TransformationMode.FastTransformation)
            else:
                pixmap = self.original_pixmap
            self.image_label.setPixmap(pixmap)

    def computeResearch(self):
        if (self.currentImgPath != None):
            self.obj_det.detect_objects_and_save(self.currentImgPath,
                                                 "tmp/currentImg.png")
            pixmap = QPixmap("tmp/currentImg.png")
            self.image_label.setPixmap(pixmap)

    def setButtonIconSize(self, button):
        icon_size = min(button.size().width(), button.size().height()) * 0.15
        button.setIconSize(QSize(int(icon_size), int(icon_size)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('style.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    viewer_app = ImageViewerApp()
    sys.exit(app.exec())
