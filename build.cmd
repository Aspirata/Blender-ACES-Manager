@echo off
py -3.12 -m pip install -r requirements.txt
py -3.12 -m nuitka ^
  --standalone ^
  --onefile ^
  --enable-plugin=pyside6 ^
  --include-data-files=src/ACES/*.7z=ACES/ ^
  --windows-console-mode=disable ^
  src/blender_aces_manager.py
pause