import os
import sys
import shutil
import keyboard
from datetime import datetime
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 加载配置文件
config_file_path = resource_path('config.json')
try:
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print(f"Error: Config file not found at {config_file_path}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse config file: {e}")
    sys.exit(1)

SRC_PATH = config.get('src_path', '')
DST_DIR = config.get('dst_dir', '')
COPY_HOTKEY = config.get('copy_hotkey', 'ctrl+shift+x')
EXIT_HOTKEY = config.get('exit_hotkey', 'ctrl+shift+q')

if not SRC_PATH or not DST_DIR:
    print("Error: Source path or destination directory is not specified in the config file.")
    sys.exit(1)

def copy_folder_with_timestamp(src, dst_dir):
    """将文件夹从 src 复制到 dst_dir，并用时间戳重命名"""
    try:
        print(f"Checking source path: {src}")
        if not os.path.exists(src) or not os.access(src, os.R_OK):
            print(f"Error: No read access to {src}")
            return

        print(f"Checking destination directory: {dst_dir}")
        if not os.path.isdir(dst_dir) or not os.access(dst_dir, os.W_OK):
            print(f"Error: No write access to {dst_dir}")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        foldername = os.path.basename(os.path.normpath(src))
        dst = os.path.join(dst_dir, f'{foldername}_{timestamp}')

        print(f"Copying folder from {src} to {dst}")
        shutil.copytree(src, dst)
        print(f"Folder copied successfully to {dst}")

    except FileExistsError:
        print(f"Destination folder {dst} already exists.")
    except PermissionError as e:
        print(f"Permission denied when trying to copy the folder: {e}")
    except Exception as e:
        print(f"An error occurred while copying the folder: {e}")

def on_copy_hotkey():
    """当按下指定热键时调用此函数来执行文件夹复制"""
    print("Copy hotkey triggered.")
    copy_folder_with_timestamp(SRC_PATH, DST_DIR)

def main():
    print("Starting program...")
    try:
        print(f"Press {COPY_HOTKEY.upper()} to copy the folder. Press {EXIT_HOTKEY.upper()} to exit.")
        keyboard.add_hotkey(COPY_HOTKEY, on_copy_hotkey, suppress=False)
        print("Hotkey added successfully.")
        keyboard.wait(EXIT_HOTKEY)
        print("Exit hotkey pressed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()