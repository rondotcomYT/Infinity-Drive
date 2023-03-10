import os
import cv2
from PIL import Image
from tqdm import tqdm

input_file = input("What file should I decode? (i.e Infinity-Drive.mp4): ")
while str(os.path.exists(input_file)) != "True":
    print("Oops! File does not exist.")
    input_file = input("What file should I decode?: ")
cap = cv2.VideoCapture(input_file)
output_file = input("What should I name the output file? (i.e output.zip): ")
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.set(1, 0)
res, frame = cap.read()
cv2.imwrite("cache.png", frame)
width = cv2.imread("cache.png", cv2.IMREAD_UNCHANGED).shape[1]
height = cv2.imread("cache.png", cv2.IMREAD_UNCHANGED).shape[0]
density = 8
coordinate = 0, 0
binary = ""

with open(output_file, "wb") as file:
    for a in tqdm(range(frames), unit=' FP'):
        cap.set(1, a)
        res, frame = cap.read()
        cv2.imwrite("cache.png", frame)
        image = Image.open("cache.png")
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
os.remove("cache.png")
file.close()
