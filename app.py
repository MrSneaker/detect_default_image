import sys
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap, QAction
from yolo_object_detection import ObjectDetector


class ImageViewerApp(QMainWindow):
    currentImgPath = None
    obj_det = ObjectDetector(
        "yolov3_custom_final.weights", "yolov3_custom.cfg", "data/obj.names")

    def __init__(self):
        super().__init__()

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
        left_panel_label = QLabel("Left Panel")
        left_panel_layout.addWidget(left_panel_label)

        # Image panel widgets
        self.image_label = QLabel("Image Display Area")
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

    def computeResearch(self):
        if (self.currentImgPath != None):
            self.obj_det.detect_objects_and_save(self.currentImgPath,
                                                 "tmp/currentImg.png")
            pixmap = QPixmap("tmp/currentImg.png")
            self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('style.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    viewer_app = ImageViewerApp()
    sys.exit(app.exec())
