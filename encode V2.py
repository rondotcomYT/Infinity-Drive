import PIL
import cv2
from PIL import Image, ImageDraw
from tqdm import tqdm
import shutil
import os

# black = 0
# white = 1

for root, dirs, files in os.walk('./temp/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

file = "Comp 1.mp4"
width = 640
height = 480
w_pix = 0
h_pix = 0
frame = 1
img = PIL.Image.new('1', (width, height), "black")
d = ImageDraw.Draw(img)

with open(file, "rb") as f:
    while byte := f.read(1):
        byte = ' '.join(format(ord(x), 'b') for x in str(byte)[2:-1]).replace(" ", "")
        for i in range(len(byte)):
            if byte[i] == "1":
                d.point((w_pix, h_pix), fill="white")
            w_pix += 1
            if w_pix > width - 1:
                h_pix += 1
                w_pix = 0
                if h_pix > height - 1:
                    h_pix = 0
                    w_pix = 0
                    img.save("./temp/" + str(frame) + ".png")
                    img = PIL.Image.new('RGB', (width, height), "black")
                    d = ImageDraw.Draw(img)
                    frame += 1

img.save("./temp/" + str(frame) + ".png")

image_folder = './temp/'
video_name = 'archive.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 30, (width, height))

# fix this, inefficient
i = 0
for image in tqdm(images):
    i += 1
    video.write(cv2.imread(os.path.join(image_folder, str(i) + ".png")))

video.release()
cv2.destroyAllWindows()
