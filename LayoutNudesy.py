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
        self.setText('\n\n Drop Image Here \n\n')
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
        self.resize(400, 400)
        self.setAcceptDrops(True)

        mainLayout = QGridLayout()

        self.photoViewer = ImageLabel()
        self.button = QPushButton("Szyfruj")
        self.info = QLineEdit("")
        mainLayout.addWidget(self.photoViewer, 0, 0, 9, 1)
        mainLayout.addWidget(self.button, 11, 0, 1, 1)
        mainLayout.addWidget(self.info, 10, 0, 1, 1)

        self.setLayout(mainLayout)

        self.button.clicked.connect(self.software)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)

            event.accept()
        else:
            event.ignore()


    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))


    def generateCSV(self, file_path):
        img = cv2.imread(file_path)

        imgReshaped = img.reshape(img.shape[0], -1)
        # saving reshaped array to file.
        np.savetxt("NudeCSV.csv", imgReshaped)

    def software(self):
         nadawca = self.sender()

         if nadawca.text() == "Szyfruj":
             self.generateCSV(self.file_path)
             self.info.setText("Zrobione!")




app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
