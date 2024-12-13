import os
import sys
import shutil
import keyboard
from datetime import datetime
import json

# 全局变量，用于存储最近一次复制的目标路径
last_copied_dst = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
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

# 使用 os.path.expandvars 扩展环境变量
SRC_PATH = os.path.expandvars(config.get('src_path', ''))
DST_DIR = os.path.expandvars(config.get('dst_dir', ''))
COPY_HOTKEY = config.get('copy_hotkey', 'ctrl+shift+x')
EXIT_HOTKEY = config.get('exit_hotkey', 'ctrl+shift+q')
RESTORE_HOTKEY = config.get('restore_hotkey', 'ctrl+shift+v')  # 新增恢复快捷键

if not SRC_PATH or not DST_DIR:
    print("Error: Source path or destination directory is not specified in the config file.")
    sys.exit(1)

def copy_folder_with_timestamp(src, dst_dir):
    """将文件夹从 src 复制到 dst_dir，并用时间戳重命名"""
    global last_copied_dst
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

        # 更新最近一次复制的目标路径
        last_copied_dst = dst

    except FileExistsError:
        print(f"Destination folder {dst} already exists.")
    except PermissionError as e:
        print(f"Permission denied when trying to copy the folder: {e}")
    except Exception as e:
        print(f"An error occurred while copying the folder: {e}")

def restore_last_backup():
    """将最近一次备份的文件夹复制回源文件夹，并替换同名文件"""
    global last_copied_dst
    if last_copied_dst is None:
        print("No recent backup to restore.")
        return

    try:
        print(f"Restoring from {last_copied_dst} to {SRC_PATH}")
        shutil.rmtree(SRC_PATH, ignore_errors=True)  # 删除源文件夹（如果有）
        shutil.copytree(last_copied_dst, SRC_PATH)
        print(f"Backup restored successfully to {SRC_PATH}")
    except Exception as e:
        print(f"An error occurred while restoring the backup: {e}")

def on_copy_hotkey():
    """当按下指定热键时调用此函数来执行文件夹复制"""
    print("Copy hotkey triggered.")
    copy_folder_with_timestamp(SRC_PATH, DST_DIR)

def on_restore_hotkey():
    """当按下指定热键时调用此函数来恢复最近一次备份"""
    print("Restore hotkey triggered.")
    restore_last_backup()

def main():
    print("Starting program...")
    try:
        print(f"Press {COPY_HOTKEY.upper()} to copy the folder. Press {RESTORE_HOTKEY.upper()} to restore the last backup. Press {EXIT_HOTKEY.upper()} to exit.")
        keyboard.add_hotkey(COPY_HOTKEY, on_copy_hotkey, suppress=False)
        keyboard.add_hotkey(RESTORE_HOTKEY, on_restore_hotkey, suppress=False)
        print("Hotkeys added successfully.")
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