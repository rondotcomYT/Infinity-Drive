import os
import shutil
import cv2
from PIL import Image
from tqdm import tqdm

cam = cv2.VideoCapture(input("What file should I decode?: "))
frames = 0

for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

while True:
    ret, frame = cam.read()
    if ret:
        name = "./temp/" + str(frames) + ".png"
        cv2.imwrite(name, frame)
        frames += 1
    else:
        break

width = cv2.imread("./temp/0.png", cv2.IMREAD_UNCHANGED).shape[1]
height = cv2.imread("./temp/0.png", cv2.IMREAD_UNCHANGED).shape[0]

x = 0
y = 0
coordinate = x, y
binary = ""
frame = 0

with open(input("What should I name the output file? (i.e output.zip): "), "wb") as file:
    for a in tqdm(range(frames), unit=' FP'):
        image = Image.open("./temp/" + str(frame) + ".png")
        for b in range(480):
            for c in range(80):
                for i in range(8):
                    coordinate = c * int(8) + i, b
                    color = image.getpixel(coordinate)
                    if color[0] > 128:
                        binary = binary + "1"
                    elif color[0] < 128:
                        binary = binary + "0"
                if len(hex(int(binary, 2))) > 3:
                    file.write(bytearray.fromhex(hex(int(binary, 2))[2:]))
                elif len(hex(int(binary, 2))) == 3:
                    file.write(bytearray.fromhex(hex(int(binary, 2)).replace("0x", "0")))
                binary = ""
        frame += 1
file.close()

for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))
