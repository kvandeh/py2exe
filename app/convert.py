import os
import os.path
import shutil

def convert(directory):
    with open(f"instance/conversions/{directory}/info.txt", "w") as info_file:
        info_file.write("Starting conversion\n")
        info_file.flush()
        for filename in os.listdir(f"instance/conversions/{directory}"):
            if not filename.endswith(".py"): continue
            initial_dir = os.getcwd()
            os.chdir(f"instance/conversions/{directory}")
            _ = os.system(f"pyinstaller {filename} --onedir")
            os.chdir(initial_dir)

            print(f"instance/conversions/{directory}/dist/{filename.split(".")[0]}/{filename.split(".")[0]}.exe")

            if os.path.exists(f"instance/conversions/{directory}/dist/{filename.split(".")[0]}/{filename.split(".")[0]}.exe"):
                info_file.write("Finshed conversion successfully\n")
            
            info_file.write("Starting zip archive creation\n")
            shutil.make_archive(f"instance/conversions/{directory}/output", "zip", f"instance/conversions/{directory}/dist")
            info_file.write("Created zip archive - ready for download")