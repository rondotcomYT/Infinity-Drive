# Import Libraries
import os
import cv2
from PIL import Image
from tqdm import tqdm

# Define Input File
input_file = input("What file should I decode? (i.e Infinity-Drive.mp4): ")
while str(os.path.exists(input_file)) != "True":
    print("Oops! File does not exist.")
    input_file = input("What file should I decode?: ")
cap = cv2.VideoCapture(input_file)

# Define Output File
output_file = input("What should I name the output file? (i.e output.zip): ")
while str(os.path.exists(output_file)) == "True":
    print("Oops! File already exists.")
    output_file = input("What should I name the output file?: ")

# Define Variables
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.set(1, 0)
res, frame = cap.read()
cv2.imwrite("cache.png", frame)
width = cv2.imread("cache.png", cv2.IMREAD_UNCHANGED).shape[1]
height = cv2.imread("cache.png", cv2.IMREAD_UNCHANGED).shape[0]
binary = ""

# Get Density
image = Image.open("cache.png")
for a in range(2):
    for b in range(8):
        coordinate = (width / 8) * b + 2, (height / 2) * a + 2
        color = image.getpixel(coordinate)
        if color[0] > 128:
            binary += "1"
        elif color[0] < 128:
            binary += "0"
density = int(bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8)).decode('utf-8'))
binary = ""

# Read and Decode Frames
with open(output_file, "wb") as file:
    for a in tqdm(range(frames - 1), unit=' FP'):
        cap.set(1, a + 1)
        res, frame = cap.read()
        cv2.imwrite("cache.png", frame)
        image = Image.open("cache.png")
        for b in range(int(height / density)):
            for c in range(int(width / density / 8)):
                for i in range(8):
                    coordinate = (c * 8 * density) + (i * density) + 2, b * density + 2
                    color = image.getpixel(coordinate)
                    if color[0] > 128:
                        binary += "1"
                    elif color[0] < 128:
                        binary += "0"
                if len(hex(int(binary, 2))) > 3:
                    file.write(bytearray.fromhex(hex(int(binary, 2))[2:]))
                elif len(hex(int(binary, 2))) == 3:
                    file.write(bytearray.fromhex(hex(int(binary, 2)).replace("0x", "0")))
                binary = ""
os.remove("cache.png")
file.close()
