import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar, QFileDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap, QAction

class ImageViewerApp(QMainWindow):
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

        # Set layouts to central widget
        main_layout.addLayout(left_panel_layout, 1)  # Left panel takes 1/3 of the space
        main_layout.addLayout(image_panel_layout, 2)  # Image panel takes 2/3 of the space

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
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp);;All Files (*)")

        if fileName:
            pixmap = QPixmap(fileName)
            self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('style.qss', 'r') as f:
        style = f.read()
        # Set the stylesheet of the application
        app.setStyleSheet(style)
    viewer_app = ImageViewerApp()
    sys.exit(app.exec())
