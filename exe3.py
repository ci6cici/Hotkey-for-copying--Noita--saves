import os
import sys
import shutil
import keyboard
from datetime import datetime
import json
from pathlib import Path

# 全局变量，用于存储最近9次复制的目标路径
recent_backups = []


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
RESTORE_HOTKEY_BASE = config.get('restore_hotkey', 'shift+v')

if not SRC_PATH or not DST_DIR:
    print("Error: Source path or destination directory is not specified in the config file.")
    sys.exit(1)


def ensure_backup_directory_exists():
    """确保备份文件夹存在"""
    if not os.path.exists(DST_DIR):
        os.makedirs(DST_DIR)
        print(f"Backup directory created at {DST_DIR}")


def load_existing_backups():
    """加载现有的备份文件夹，并按时间排序填入 recent_backups 中"""
    global recent_backups
    backup_folders = [f for f in Path(DST_DIR).iterdir() if f.is_dir()]
    backup_folders.sort(key=lambda p: p.stat().st_mtime, reverse=True)  # 按修改时间降序排序

    recent_backups = [str(folder) for folder in backup_folders[:9]]
    print(f"Loaded {len(recent_backups)} existing backups.")


def copy_folder_with_timestamp(src, dst_dir):
    """将文件夹从 src 复制到 dst_dir，并用时间戳重命名"""
    global recent_backups
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

        # 更新最近一次复制的目标路径，并保持最多9个备份
        recent_backups.insert(0, dst)
        recent_backups = recent_backups[:9]

    except FileExistsError:
        print(f"Destination folder {dst} already exists.")
    except PermissionError as e:
        print(f"Permission denied when trying to copy the folder: {e}")
    except Exception as e:
        print(f"An error occurred while copying the folder: {e}")

def adjust_restore_path(backup_path):
    """调整恢复路径以指向 'save00' 文件夹（如果存在）"""
    save00_path = os.path.join(backup_path, 'save00')
    if os.path.isdir(save00_path):
        print(f"'save00' folder found within the backup. Adjusting restore path to: {save00_path}")
        return save00_path
    else:
        print("'save00' folder not found. Using original backup path.")
        return backup_path


def restore_backup(index):
    """将指定编号的备份文件夹复制回源文件夹的上一级目录，并替换同名文件"""
    if index < 1 or index > len(recent_backups):
        print(f"Invalid backup index: {index}. Available backups are from 1 to {len(recent_backups)}.")
        return

    src_backup = recent_backups[index - 1]
    try:
        # 调整源备份路径到 'save00' 文件夹（如果存在）
        adjusted_src_backup = adjust_restore_path(src_backup)

        # 获取源文件夹的上一级目录
        parent_dir = str(Path(SRC_PATH).parent)
        foldername = os.path.basename(os.path.normpath(SRC_PATH))
        dst_path = os.path.join(parent_dir, foldername)

        print(f"Restoring from {adjusted_src_backup} to {dst_path}")
        shutil.rmtree(dst_path, ignore_errors=True)  # 删除目标文件夹（如果有）
        shutil.copytree(adjusted_src_backup, dst_path)
        print(f"Backup restored successfully to {dst_path}")
    except Exception as e:
        print(f"An error occurred while restoring the backup: {e}")


def on_copy_hotkey():
    """当按下指定热键时调用此函数来执行文件夹复制"""
    print("Copy hotkey triggered.")
    copy_folder_with_timestamp(SRC_PATH, DST_DIR)


def on_restore_hotkey(index):
    """当按下指定热键时调用此函数来恢复指定编号的备份"""
    print(f"Restore hotkey {index} triggered.")
    restore_backup(index)


def add_restore_hotkeys():
    """为每个恢复操作添加热键监听器"""
    for i in range(1, 10):
        hotkey = f"{RESTORE_HOTKEY_BASE}+{i}"
        keyboard.add_hotkey(hotkey, lambda idx=i: on_restore_hotkey(idx), suppress=False)


def initialize_program():
    """初始化程序，确保备份文件夹存在并加载现有存档"""
    ensure_backup_directory_exists()
    load_existing_backups()


def main():
    initialize_program()
    print("Starting program...")
    try:
        print(f"Press {COPY_HOTKEY.upper()} to copy the folder.")
        print(f"Press {RESTORE_HOTKEY_BASE.upper()} + [1-9] to restore a specific backup.")
        print(f"Press {EXIT_HOTKEY.upper()} to exit.")

        keyboard.add_hotkey(COPY_HOTKEY, on_copy_hotkey, suppress=False)
        add_restore_hotkeys()
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