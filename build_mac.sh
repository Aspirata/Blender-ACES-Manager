#!/bin/bash
set -e

python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

APP_NAME="Blender ACES Manager"
VERSION="5.02"
SRC="src/blender_aces_manager.py"

python3.12 -m nuitka \
  --standalone \
  --macos-create-app-bundle \
  --macos-app-name="$APP_NAME" \
  --macos-app-version="$VERSION" \
  --no-deployment-flag=self-execution \
  --python-flag=no_docstrings \
  --enable-plugin=pyside6 \
  --include-data-files=src/ACES/*.7z=ACES/ \
  --output-filename="$APP_NAME" \
  "$SRC"

echo "Press Enter to exit."
read