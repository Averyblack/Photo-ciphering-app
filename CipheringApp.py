import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGridLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
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
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Photo security")
        mainLayout = QGridLayout()
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.setColumnStretch(2, 1)
        mainLayout.setColumnStretch(3, 1)
        mainLayout.setColumnStretch(4, 1)
        mainLayout.setColumnStretch(5, 1)
        mainLayout.setColumnStretch(6, 1)
        self.photoViewer = ImageLabel()
        self.button = QPushButton("Encode")
        self.info = QLineEdit("")
        mainLayout.addWidget(self.photoViewer, 0, 0, 12, 7)
        mainLayout.addWidget(self.button, 11, 7, 1, 2)
        mainLayout.addWidget(self.info, 9, 7, 1, 2)
        self.keyLabel = QLabel("Key:")
        self.keyFrame = QLineEdit("1")
        self.passLabel = QLabel("Password: ")
        self.passFrame = QLineEdit("")
        mainLayout.addWidget(self.keyLabel, 6, 7, 1, 1)
        mainLayout.addWidget(self.keyFrame, 6, 8, 1, 1)
        mainLayout.addWidget(self.passLabel, 5, 7, 1, 1)
        mainLayout.addWidget(self.passFrame, 5, 8, 1, 1)
        self.button2 = QPushButton("Decode")
        self.info2 = QLineEdit("")
        self.dirButton = QPushButton("Browse")
        mainLayout.addWidget(self.button2, 10, 7, 1, 2 )
        mainLayout.addWidget(self.dirButton, 8, 7, 1, 2)
        mainLayout.addWidget(self.info2, 7, 7, 1, 2)
        self.setLayout(mainLayout)
        self.button.clicked.connect(self.software)
        self.button2.clicked.connect(self.software)
        self.dirButton.clicked.connect(self.software)

        self.password = "Password"
        self.folderName = os.getcwd()

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

    def generateCSV(self, file_path, key):
        img = cv2.imread(file_path)
        img2 = img.astype(float)
        coded_img = img2*int(key)**3
        imgReshaped = coded_img.reshape(coded_img.shape[0], -1)
        np.savetxt("CodedPhoto.csv", imgReshaped)


    def software(self):
        nadawca = self.sender()
        if nadawca.text() == "Encode":
            self.key = self.keyFrame.text()
            self.generateCSV(self.file_path, self.key)
            self.info.setText("Encoded! Key used:" + self.key)
        elif nadawca.text() == "Decode":
            self.key = self.keyFrame.text()
            self.inputPassword = self.passFrame.text()
            if self.inputPassword == self.password:
                self.retrievePhoto(self.file_path, self.key, self.folderName)
                self.info.setText("Decoded! Key used: " + self.key)
            else:
                self.info.setText("Wrong password!")
        elif nadawca.text() == "Browse":
            self.browseFiles()

    def browseFiles(self):
        self.folderName = QFileDialog.getExistingDirectory(None)
        self.info2.setText(self.folderName)

    def retrievePhoto(self, file_path, key, folderName):
        loadedArr = np.loadtxt(file_path)
        loadedOriginal = loadedArr.reshape(loadedArr.shape[0], loadedArr.shape[1] // 3, 3)
        decoded_img = loadedOriginal/int(key)**3
        os.chdir(folderName)
        img2 = cv2.imwrite("Photo.jpg", decoded_img)


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
