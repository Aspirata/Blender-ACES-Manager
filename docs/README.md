# Languages: [🇷🇺 *RU*](README_ru.md) | [🇺🇸 EN](README.md)

# Blender ACES Manager

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-31210/)
[![License](https://img.shields.io/badge/License-GPLv3-orange.svg)](./LICENSE)
[![GitHub downloads](https://img.shields.io/github/downloads/Aspirata/Blender-ACES-Manager/total)](https://github.com/Aspirata/Blender-ACES-Manager/releases)
[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label)](https://discord.gg/y4CWTzbZcv)

> [!WARNING]
> Blender 5.0+ has built-in ACES 1.3 and 2.0, you don't need an external app anymore

**Blender ACES Manager** is a lightweight utility designed to easily manage **ACES color configurations** in **Blender**.

---

## 🎨 What is ACES?

**ACES (Academy Color Encoding System)** is an industry-standard color management system used in film and visual effects production.  
It provides consistent, accurate, and natural-looking colors across different devices, making it essential for professional color grading and rendering.

**In simple terms:**  
ACES makes your renders look more cinematic — like in Hollywood movies.

---

## ⚙️ Features

- 🧩 One-click **install** and **uninstall** of ACES  
- 💾 **Automatic backup** of Blender’s original color management files  
- 🧠 Full **compatibility** with Blender **3.6 and newer**  
- 🔧 Simple structure — works out of the box  

## 📦 Preinstalled ACES Versions
- **[PixelManager v2.0 RC6](https://github.com/Joegenco/PixelManager/releases/tag/v.2.0-RC6)**  
  An updated set of color management files supporting **ACES 1.3**, **ACES 2.0**, and **Blender 4.4’s default** color management system.

You can also use your own ACES or other color management configurations — just place them and archive into .7z inside the **`ACES`** folder before building.

## 🖥️ OS Support

| OS          | Status          | Details                                                                 |
|-------------|-----------------|-----------------------------------------------------------------------------|
| **Windows** | Works fine ✅     | Full support                                           |
| **macOS**   | Works best ✅      | Full support + Automatic Blender.app Detection                        |
| **Linux**   | Doesn't work ❌ | Blender ACES Manager doesn't support Linux |

---

## 🛠️ Build Requirements

To build Blender ACES Manager yourself, make sure you have:

- **Python** = 3.12  
- **PySide6** = 6.10.2  
- **nuitka** = 4.0.1  
- **zstandard** = 0.25.0  
- **py7zr** = 1.1.0

> 💡 Tip: You can use the included `build_win.cmd` or `build_mac.sh` script — it will install all dependencies automatically (except Python).

---

## 📄 License

This project is distributed under the **GPLv3** License.  
See more details in the [LICENSE](./LICENSE) file.
