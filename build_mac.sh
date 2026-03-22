#!/bin/bash
set -e

python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

APP_NAME="blender_aces_manager"
APP_DISPLAY_NAME="Blender ACES Manager"
VERSION="5.1"
SRC="src/blender_aces_manager.py"

echo "Cleaning up previous build artifacts..."
[ -d "${APP_DISPLAY_NAME}.app" ] && rm -rf "${APP_DISPLAY_NAME}.app"
[ -d "${APP_NAME}.app" ] && rm -rf "${APP_NAME}.app"
rm -f "${APP_NAME}"_v*.dmg
rm -rf dmg_staging

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

mv "${APP_NAME}.app" "${APP_DISPLAY_NAME}.app"

mkdir -p dmg_staging
cp -R "${APP_DISPLAY_NAME}.app" dmg_staging/
cp -R docs dmg_staging/
ln -s /Applications dmg_staging/Applications

hdiutil create \
  -volname "$APP_DISPLAY_NAME" \
  -srcfolder dmg_staging \
  -ov \
  -format UDZO \
  "${APP_NAME}_v${VERSION}.dmg"

rm -rf dmg_staging

echo "Press Enter to exit."
read