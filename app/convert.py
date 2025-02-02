import os
import os.path
import shutil

def write_to_info_file(directory, message):
    with open(f"instance/conversions/{directory}/info.txt", "w") as info_file:
        info_file.write(message)
        info_file.flush()

def create_venv(directory):
    initial_dir = os.getcwd()
    os.chdir(f"instance/conversions/{directory}")
    if os.name == 'nt': # if running on windows
        _ = os.system(f"virtualenv venv")
        _ = os.system(f"venv\Scripts\python.exe -m pip install pyinstaller && venv\Scripts\python.exe -m pip install -r requirements.txt")
    else:
        os.environ["PATH"] = "/usr/bin"
        os.environ["WINEPREFIX"] = initial_dir+"/wine"
        os.environ["WINEPATH"] = initial_dir
        _ = os.system(f"wine {initial_dir}/wine/drive_c/python3.12/python.exe -m virtualenv venv")
        _ = os.system(f"wine venv/Scripts/python.exe -m pip install pyinstaller && wine venv/Scripts/python.exe -m pip install -r requirements.txt")
    os.chdir(initial_dir)

def run_pyinstaller(directory, filename, venv: bool=False):
    """
    run pyinstaller - if venv=True, expect virtual environment in "venv/"
    """
    initial_dir = os.getcwd()
    os.chdir(f"instance/conversions/{directory}")
    if os.name == 'nt': # if running on windows
        if venv:
            _ = os.system(f"venv\Scripts\python.exe -m pyinstaller {filename} --onedir")
        else:
            _ = os.system(f"pyinstaller {filename} --onedir")
    else:
        os.environ["PATH"] = "/usr/bin"
        os.environ["WINEPREFIX"] = initial_dir+"/wine"
        os.environ["WINEPATH"] = initial_dir
        if venv:
            _ = os.system(f"wine venv/Scripts/python.exe -m PyInstaller {filename} --onedir")
        else:
            _ = os.system(f"wine {initial_dir}/wine/drive_c/python3.12/python.exe -m PyInstaller {filename} --onedir")
    os.chdir(initial_dir)

def convert(directory):
    write_to_info_file(directory, "Analyzing file(s)\n")
    for filename in os.listdir(f"instance/conversions/{directory}"): # expects only one file in instance/conversions/{directory} (either one py script or zip)
        if filename.endswith(".py"):
            write_to_info_file(directory, "Starting conversion\n")
            run_pyinstaller(directory, filename)
            break

        if filename.endswith(".zip"):
            write_to_info_file(directory, "Unpacking zip archive\n")
            shutil.unpack_archive(f"instance/conversions/{directory}/{filename}", f"instance/conversions/{directory}", "zip")
            python_files = [f for f in os.listdir(f"instance/conversions/{directory}") if f.endswith(".py")]
            root_file = None
            if len(python_files) == 1:
                root_file = python_files[0]
            if "app.py" in python_files:
                root_file = "app.py"
            if "main.py" in python_files:
                root_file = "main.py"
            if "run.py" in python_files:
                root_file = "run.py"
            if not root_file:
                write_to_info_file(directory, f"Conversion failed: Please rename the root file of your project to main.py or run.py")
                return False
            venv = False
            if "requirements.txt" in os.listdir(f"instance/conversions/{directory}"):
                write_to_info_file(directory, "Creating virtual environment")
                create_venv(directory)
                venv = True
            write_to_info_file(directory, f"Converting - {root_file}\n")
            run_pyinstaller(directory, root_file, venv=venv)
            break

    if os.path.exists(f"instance/conversions/{directory}/dist/{filename.split(".")[0]}/{filename.split(".")[0]}.exe"):
        write_to_info_file(directory, "Finshed conversion successfully\n")
        write_to_info_file(directory, "Starting zip archive creation\n")
        shutil.make_archive(f"instance/conversions/{directory}/output", "zip", f"instance/conversions/{directory}/dist")
        write_to_info_file(directory, "Created zip archive - ready for download")
    else:
        write_to_info_file(directory, "An error occured during conversion - please check that your python files run properly on python 3.12.8 and try again")