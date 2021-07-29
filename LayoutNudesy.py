import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
import pandas as pd


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image or CSV file here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)


class AppDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1600, 800)
        self.setAcceptDrops(True)

        mainLayout = QGridLayout()

        self.photoViewer = ImageLabel()
        self.button = QPushButton("Szyfruj")
        self.info = QLineEdit("")
        mainLayout.addWidget(self.photoViewer, 0, 0, 9, 2)
        mainLayout.addWidget(self.button, 11, 0, 1, 1)
        mainLayout.addWidget(self.info, 10, 0, 1, 1)

        self.button2 = QPushButton("Odzyskaj zdjęcie")
        self.info2 = QLineEdit("")
        mainLayout.addWidget(self.button2, 11, 1, 1, 1)
        mainLayout.addWidget(self.info2, 10, 1, 1, 1)

        self.setLayout(mainLayout)

        self.button.clicked.connect(self.software)
        self.button2.clicked.connect(self.software)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        elif event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        elif event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)
            event.accept()
        elif event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

    def generateCSV(self, file_path):
        img = cv2.imread(file_path)

        imgReshaped = img.reshape(img.shape[0], -1)
        np.savetxt("NudeCSV.csv", imgReshaped)

    def software(self):
        nadawca = self.sender()

        if nadawca.text() == "Szyfruj":
            self.generateCSV(self.file_path)
            self.info.setText("Zrobione!")
        elif nadawca.text() == "Odzyskaj zdjęcie":
            self.retrievePhoto(self.file_path)
            self.info2.setText("Zrobione!")

    def retrievePhoto(self, file_path):
        loadedArr = np.loadtxt(file_path)
        loadedOriginal = loadedArr.reshape(loadedArr.shape[0], loadedArr.shape[1] // 3, 3)
        img2 = cv2.imwrite("nude2.jpg",loadedOriginal)

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
