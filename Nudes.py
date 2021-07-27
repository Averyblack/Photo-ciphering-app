import cv2
import os
import numpy as np
import pandas as pd

directory = r'C:\Users\Jaskka8\Pictures\gify'
img = cv2.imread(r"C:\Users\Jaskka8\Desktop\Szyfrator\nude.jpg")

imgReshaped = img.reshape(img.shape[0], -1)
# saving reshaped array to file.
np.savetxt("NudeCSV.csv", imgReshaped)



# retrieving data from file.
loadedArr = np.loadtxt("NudeCSV.csv")
# This loadedArr is a 2D array, therefore we need to convert it to the original array shape.
# reshaping to get original matrice with original shape.
loadedOriginal = loadedArr.reshape(loadedArr.shape[0], loadedArr.shape[1] // img.shape[2], img.shape[2])


os.chdir(directory)
print(loadedOriginal)
img2 = cv2.imwrite("nude2.jpg",loadedOriginal)

print ("succesfully saved")
