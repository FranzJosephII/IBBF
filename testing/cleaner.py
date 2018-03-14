import glob
import shutil
import os

my_path = "C:/Users/AGANDO/PycharmProjects"

dirs = glob.glob(my_path + '/**/__pycache__', recursive=True)
for dir in dirs:
    shutil.rmtree(dir)
    print("Deleted " + dir)

files = glob.glob(my_path + '/**/*.pyc', recursive=True)
for file in files:
    os.remove(file)
    print("Deleted " + file)
