# 实现将文件从路径 a 复制到路径 b 并以时间命名的功能，并设置快捷键后台启动。
import os
import shutil
import keyboard
from datetime import datetime

# 定义源路径和目标路径
SRC_PATH = r'C:\Users\？\AppData\LocalLow\Nolla_Games_Noita\save00'
DST_DIR = r'C:\Users\？\AppData\LocalLow\Nolla_Games_Noita\备份'  # 替换为你的目标文件夹路径


def copy_folder_with_timestamp(src, dst_dir):
    """将文件夹从 src 复制到 dst_dir，并用时间戳重命名"""
    try:
        if not os.path.exists(src) or not os.access(src, os.R_OK):
            print(f"Error: No read access to {src}")
            return

        if not os.path.isdir(dst_dir) or not os.access(dst_dir, os.W_OK):
            print(f"Error: No write access to {dst_dir}")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        foldername = os.path.basename(os.path.normpath(src))
        dst = os.path.join(dst_dir, f'{foldername}_{timestamp}')

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
    copy_folder_with_timestamp(SRC_PATH, DST_DIR)


def main():
    print("Press Ctrl+Shift+x to copy the folder. Press Ctrl+Shift+Q to exit.")

    # 设置热键监听器
    keyboard.add_hotkey('ctrl+shift+x', on_copy_hotkey, suppress=False)
    keyboard.wait('ctrl+shift+q')  # 等待退出热键被按下


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")