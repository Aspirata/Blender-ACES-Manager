#!/bin/bash

python3.12 -m pip install -r requirements.txt || { echo "pip install failed. Press Enter to exit."; read; exit 1; }
python3.12 "src/blender_aces_manager.py" || { echo "Script failed. Press Enter to exit."; read; exit 1; }
