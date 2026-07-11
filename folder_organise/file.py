import os 
import shutil

# folder path 
folder_path=input("enter your path:")

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
}

files=os.listdir(folder_path)

for file in files :
  print(file)



