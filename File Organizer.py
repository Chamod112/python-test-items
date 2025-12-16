import os
import shutil

path = "C:/Users/YourName/Downloads"

for file in os.listdir(path):
    if file.endswith(".jpg") or file.endswith(".png"):
        os.makedirs(path + "/Images", exist_ok=True)
        shutil.move(path + "/" + file, path + "/Images")
