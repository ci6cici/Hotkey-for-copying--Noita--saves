# Hotkey-for-copying--Noita--saves
his code implements a feature that allows copying the Noita save folder to a backup directory with a timestamp via hotkeys, and supports restoring the last 9 backups.这段代码实现了通过快捷键复制noita存档文件夹到备份目录，并以时间戳命名，支持恢复最近的9次备份。

依赖库：keyboard、pyinstaller 
main.py: 仅有备份存档功能，默认为ctrl+shift+x复制 
appcreate.py: 1.0 封装为exe，增加了json修改快捷键的功能 
exe2.py: 2.0 增加了恢复功能 
exe3.py: 3.0 最高支持9个存档，默认使用shift+v+1-9，shift+v+1 为最新存档 
exe3.py已封装为“..\noita快捷存档\存档.exe” 
现有功能： 
第一次使用在%USERPROFILE%\AppData\LocalLow\Nolla_Games_Noita\文件夹新建一个“备份”文件夹， 
ctrl+shift+x复制存档文件夹save00到这个文件夹中。 shift+v+1-9恢复存档， 
第二次及以后启动程序，会读取最多9个存档，按时间排序，允许手动复制save文件夹到备份中 
ctrl+shift+q或关掉程序框退出

Dependent Libraries: keyboard、pyinstaller main.py: Has only the backup save function, with the default shortcut of Ctrl+Shift+X for copying. appcreate.py: 1.0 Encapsulated into an exe, added the function to modify shortcuts in json. exe2.py: 2.0 Added the restore function. exe3.py: 3.0 Supports up to 9 saves, with default shortcuts of Shift+V+1-9, Shift+V+1 for the most recent save. exe3.py has been encapsulated as "..\Noita Quick Save\Save.exe". Current Features:

Upon first use, it creates a "Backup" folder in the %USERPROFILE%\AppData\LocalLow\Nolla_Games_Noita\ directory.
Copies the save folder save00 to this folder using Ctrl+Shift+X.
Restores saves using Shift+V+1-9.
On subsequent launches, it reads up to 9 saves, sorts them by time, and allows manual copying of the save folder to the backup.
Exits by pressing Ctrl+Shift+Q or closing the program window.
