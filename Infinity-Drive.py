# Import Libraries
import os
import PIL
import cv2
import time
from PIL import Image, ImageDraw
from tqdm import tqdm

pref = input("Would you like to [1] ENCODE or [2] DECODE a file?: ")

# Encode File
if pref == "1":
    # Define Input File
    input_file = input("What file should I encode? (i.e input.zip): ")
    while str(os.path.isfile(input_file)) != "True":
        print("Oops! File does not exist.")
        input_file = input("What file should I encode?: ")
    file_size = os.path.getsize(input_file)

    # Checking if encoded file exists
    file_name = "Infinity-Drive"
    file_num = 1
    if os.path.exists(f"{file_name}.mp4") is False:
        pass
    else:
        while os.path.exists(f"{file_name}({file_num}).mp4"):
            file_num += 1
        file_name = f"{file_name}({file_num})"

    # Define Video Size
    width = 1280
    height = 720

    # Define Pixel Density
    density = 8

    # Define Remaining Variables
    w_pix = 0
    h_pix = 0
    frames = 0
    video = cv2.VideoWriter(f"{file_name}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
    img = PIL.Image.new('1', (width, height), "black")
    print("Generating frames, please be patient...")

    # Generate Density Info Frame
    if len(str(density)) == 1:
        density_binary = "".join(format(byte, '08b') for byte in str(0).encode('utf-8'))
        for a in range(len(density_binary)):
            if density_binary[a] == "1":
                ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + (width / 8) - 1, h_pix + (height / 2) - 1),
                                              fill="white", outline=None, width=1)
            w_pix += (width / 8)
        w_pix = 0
        h_pix += (height / 2)
    for a in range(len(str(density))):
        density_binary = "".join(format(byte, '08b') for byte in str(density)[a].encode('utf-8'))
        for b in range(len(density_binary)):
            if str(density_binary)[b] == "1":
                ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + (width / 8) - 1, h_pix + (height / 2) - 1),
                                              fill="white", outline=None, width=1)
            w_pix += (width / 8)
        w_pix = 0
        h_pix += (height / 2)
    img.save("cache.png")
    video.write(cv2.imread("cache.png"))
    img = PIL.Image.new('1', (width, height), "black")
    frames += 1
    w_pix = 0
    h_pix = 0

    # Generate and Write Frames
    tic = time.perf_counter()
    with open(input_file, "rb") as f:
        while byte := f.read(1):
            binary = "{0:08b}".format(int(hex(byte[0])[2:], 16))
            for a in range(len(binary)):
                if binary[a] == "1":
                    ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + density - 1, h_pix + density - 1),
                                                  fill="white",
                                                  outline=None, width=1)
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

# Decode File
elif pref == "2":
    # Define Input File
    input_file = input("What file should I decode? (i.e Infinity-Drive.mp4): ")
    while str(os.path.isfile(input_file)) != "True":
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
