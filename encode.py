# import libraries
import PIL
import cv2
from PIL import Image, ImageDraw
from tqdm import tqdm
import shutil
import os

# black = 0
# white = 1

# deletes files from /temp/ folder
for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

file = input("What file should I encode? (i.e input.zip): ")
file_size = os.path.getsize(file)
width = 1920
height = 1080
density = 8
w_pix = 0
h_pix = 0
frame = 0
img = PIL.Image.new('1', (width, height), "black")
d = ImageDraw.Draw(img)

if int(round(file_size / ((width / (density * 3)) * (height / (density * 3))))) < 1:
    print("Generating 1 image...")
elif int(round(file_size / ((width / (density * 3)) * (height / (density * 3))))) >= 1:
    print("Generating " + str(round(file_size / ((width / (density * 3)) * (height / (density * 3))))) + " images...")


with open(file, "rb") as f:
    while byte := f.read(1):
        binary = "{0:08b}".format(int(hex(byte[0])[2:], 16))
        for a in range(len(binary)):
            if binary[a] == "1":
                d.rectangle((w_pix, h_pix, w_pix + density, h_pix + density), fill="white", outline=None, width=1)
            w_pix += density
            if w_pix > width - 1:
                w_pix = 0
                h_pix += density
                if h_pix > height - 1:
                    w_pix = 0
                    h_pix = 0
                    img.save("./temp/" + str(frame) + ".png")
                    img = PIL.Image.new('1', (width, height), "black")
                    d = ImageDraw.Draw(img)
                    frame += 1
img.save("./temp/" + str(frame) + ".png")
frame += 1

image_folder = './temp/'
video_name = 'infinity_drive.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
img_frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = img_frame.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

i = 0
for image in tqdm(range(frame), unit=' FP'):
    video.write(cv2.imread(os.path.join(image_folder, str(i) + ".png")))
    i += 1

for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

video.release()
cv2.destroyAllWindows()
