import sys
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QGridLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap, QAction, QGuiApplication, QIcon
from PyQt6 import QtCore
from PyQt6.QtCore import QSize
from yolo_object_detection import ObjectDetector


class ImageViewerApp(QMainWindow):
    currentImgPath = None
    obj_det = ObjectDetector(
        "yolov3_custom_best.weights", "yolov3_custom.cfg", "data/obj.names")

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
        openFileBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        openDirBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        zoomInBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        zoomOutBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        openFileBtn.clicked.connect(self.openImage)
        zoomInBtn.clicked.connect(lambda: self.zoomImage(1.1))
        zoomOutBtn.clicked.connect(lambda: self.zoomImage(0.9))

        # Image panel widgets
        self.image_label.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        image_panel_layout.addWidget(self.image_label)

        # Button to trigger YOLO model treatment
        self.compute_button = QPushButton("Compute YOLO Model Treatment")
        self.compute_button.clicked.connect(self.computeResearch)
        image_panel_layout.addWidget(self.compute_button)

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

        self.setGeometry(100, 100, 800, 600)

        self.setWindowTitle('App')
        self.show()

    def openImage(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.jpg *.bmp);;All Files (*)")

        if fileName:
            self.currentImgPath = fileName
            pixmap = QPixmap(fileName)
            self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        shutil.rmtree("tmp/", ignore_errors=True)
        event.accept()
    
    def zoomImage(self, factor):
        if self.currentImgPath != None:
            pixmap = self.image_label.pixmap()
            size = pixmap.size()
            size.setWidth(int(size.width() * factor))
            size.setHeight(int(size.height() * factor))
            pixmap = pixmap.scaled(size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
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
