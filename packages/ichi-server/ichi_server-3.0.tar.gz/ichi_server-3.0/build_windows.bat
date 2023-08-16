@echo off
python -m nuitka --standalone --onefile -o ichiserver_win32_x86-64.exe --windows-icon-from-ico=logo.ico --enable-console ichi
pause
