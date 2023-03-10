import os
import shutil
import cv2
from PIL import Image
from tqdm import tqdm

cam = cv2.VideoCapture(input("What file should I decode? (i.e infinity_drive.mp4): "))
file_name = input("What should I name the output file? (i.e output.zip): ")
frames = 0

for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

print("Extracting frames...")

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

density = 8
coordinate = 0, 0
binary = ""
frame = 0

with open(file_name, "wb") as file:
    for a in tqdm(range(frames), unit=' FP'):
        image = Image.open("./temp/" + str(frame) + ".png")
        for b in range(int(height / density)):
            for c in range(int(width / density / 8)):
                for i in range(8):
                    coordinate = (c * int(8) * density) + (i * density) + 2, b * density + 2
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
