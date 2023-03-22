import os
import shutil
import time
from joblib import Parallel, delayed
from PIL import Image, ImageDraw
from tqdm import tqdm
import PIL

input_file = input("What file should I encode?: ")
while str(os.path.isfile(input_file)) != "True":
    print("Oops! File does not exist.")
    input_file = input("What file should I encode?: ")

output_file = 'Infinity-Drive_v2.mp4'
file_size = os.path.getsize(input_file)
estimated_frames = round(file_size / 1800)
cache_path = "cache"
logical_processors = os.cpu_count()
framerate = 30

if not os.path.exists(cache_path):
    os.makedirs(cache_path)

for filename in os.listdir(cache_path):
    file_path = os.path.join(cache_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate(cache_path, frame):
    counter = 0
    start_byte = frame * 1800
    img = PIL.Image.new('1', (1280, 720), "black")
    if start_byte + counter > file_size:
        return
    with open(input_file, "rb") as f:
        for y in range(90):
            for x in range(20):
                if start_byte + counter < file_size:
                    f.seek(start_byte + counter, 0)
                    binary = "{0:08b}".format(int(hex(f.read(1)[0])[2:], 16))
                    for digit in range(len(binary)):
                        if binary[digit] == "1":
                            ImageDraw.Draw(img).rectangle(
                                ((x * 64) + (digit * 8), y * 8, (x * 64) + (digit * 8) + 7, (y * 8) + 7), fill="white",
                                outline=None, width=1)
                    counter += 1
        img.save(f"./{cache_path}/{str(frame + 1)}.png")
        # .zfill(len(str(estimated_frames)))


one = Parallel(n_jobs=logical_processors)(
    delayed(generate)(cache_path, range(estimated_frames)[i]) for i in tqdm(range(estimated_frames), unit=' FP'))

ffmpeg_cmd = f'ffmpeg -an -sn -framerate {framerate} -i {cache_path}/%d.png -c:v libx264 -pix_fmt yuv420p -r 30 -preset fast -threads {logical_processors} {output_file} -hide_banner -loglevel error'
image_files = sorted([os.path.join(cache_path, f) for f in os.listdir(cache_path) if f.endswith('.png')])
tic = time.perf_counter()
print("Generating frames...")
os.system(ffmpeg_cmd)
toc = time.perf_counter()
print(f"Completed in {toc - tic:0.4f} seconds.")

shutil.rmtree(cache_path)
