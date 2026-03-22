@echo off
set APP_NAME=blender_aces_manager
set VERSION=5.1

if exist %APP_NAME%.exe del /f %APP_NAME%.exe
py -3.12 -m pip install -r requirements.txt
py -3.12 -m nuitka ^
  --standalone ^
  --onefile ^
  --enable-plugin=pyside6 ^
  --no-deployment-flag=self-execution ^
  --python-flag=no_docstrings ^
  --include-data-files=src/ACES/*.7z=ACES/ ^
  --windows-console-mode=disable ^
  --windows-uac-admin ^
  src/blender_aces_manager.py

powershell -Command "Compress-Archive -Force -Path '%APP_NAME%.exe', 'docs' -DestinationPath '%APP_NAME%_v%VERSION%.zip'"
pause