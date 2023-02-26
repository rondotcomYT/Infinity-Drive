import PIL
from tqdm import tqdm
from PIL import Image, ImageDraw
import cv2
import shutil
import os

cam = cv2.VideoCapture("archive.avi")
currentframe = 0
process_frame = 1

for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

while True:
    ret, frame = cam.read()
    if ret:
        name = "./temp/" + str(currentframe) + ".png"
        cv2.imwrite(name, frame)
        currentframe += 1
    else:
        break

width = cv2.imread("./temp/1.png", cv2.IMREAD_UNCHANGED).shape[1]
height = cv2.imread("./temp/1.png", cv2.IMREAD_UNCHANGED).shape[0]
print(width)
print(height)


x = 0
y = 0
coordinate = x, y
frame = 1
image = Image.open(r"./temp/" + str(frame) + ".png")
while currentframe > process_frame:
    binary = ""
    for i in range(7):
        color = image.getpixel(coordinate)
        print(color)
        if color[0] > 128:
            binary = binary + "1"
        elif color[0] < 128:
            binary = binary + "0"
