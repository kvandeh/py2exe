import os

def convert(directory):
    for filename in os.listdir(f"instance/conversions/{directory}"):
        os.chdir(f"instance/conversions/{directory}")
        os.popen(f"pyinstaller {filename} --onedir")