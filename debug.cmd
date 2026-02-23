@echo off
py -3.12 -m pip install -r requirements.txt || pause
py -3.12 "src/blender_aces_manager.py" || pause