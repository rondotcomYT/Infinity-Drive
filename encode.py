# Import Libraries
import PIL
import cv2
from PIL import Image, ImageDraw
import time
import os

# Define Variables
input_file = input("What file should I encode? (i.e input.zip): ")
while str(os.path.exists(input_file)) != "True":
    print("Oops! File does not exist.")
    input_file = input("What file should I encode?: ")
file_size = os.path.getsize(input_file)
# Video Size
width = 1280
height = 720
# Pixel Density
density = 8
w_pix = 0
h_pix = 0
frames = 0
video = cv2.VideoWriter("Infinity-Drive.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
img = PIL.Image.new('1', (width, height), "black")
print("Generating " + str(round(file_size / (height * width / density / density / 8)) + 1) + " frames...")

tic = time.perf_counter()
with open(input_file, "rb") as f:
    while byte := f.read(1):
        binary = "{0:08b}".format(int(hex(byte[0])[2:], 16))
        for a in range(len(binary)):
            if binary[a] == "1":
                ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + density - 1, h_pix + density - 1), fill="white", outline=None, width=1)
            w_pix += density
            if w_pix > width - 1:
                w_pix = 0
                h_pix += density
                if h_pix > height - 1:
                    w_pix = 0
                    h_pix = 0
                    img.save("cache.png")
                    video.write(cv2.imread("cache.png"))
                    img = PIL.Image.new('1', (width, height), "black")
                    frames += 1
    img.save("cache.png")
    video.write(cv2.imread("cache.png"))
    toc = time.perf_counter()
    os.remove("cache.png")
    video.release()
    frames += 1

print("Generated " + str(frames) + f" frames in {toc - tic:0.4f} seconds.")

cv2.destroyAllWindows()
