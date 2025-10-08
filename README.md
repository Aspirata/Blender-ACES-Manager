# Languages: [🇷🇺 RU](README_ru.md) | [🇺🇸 *EN*](README.md)

# Blender ACES Manager

**Blender ACES Manager** is a lightweight utility designed to easily manage **ACES color configurations** in **Blender**.

---

## 🎨 What is ACES?

**ACES (Academy Color Encoding System)** is an industry-standard color management system used in film and visual effects production.  
It provides consistent, accurate, and natural-looking colors across different devices, making it essential for professional color grading and rendering.

**In simple terms:**  
ACES makes your renders look more cinematic — like in Hollywood movies.

---

## 📦 Preinstalled ACES Versions

- **ACES 1.3 Pro**  
  A version of ACES 1.3 compatible with Blender 4.1’s default color management.  
  *Note: The source of this version is unknown, so no official download link is provided.*

- **[PixelManager v2.0](https://github.com/Joegenco/PixelManager/releases/tag/v.2.0-RC4)**  
  An updated set of color management files supporting **ACES 1.3**, **ACES 2.0**, and **Blender 4.4’s default** color management system.

You can also use your own ACES or other color management configurations — just place them inside the **`ACES`** folder before building.

---

## ⚙️ Features

- 🧩 One-click **install** and **uninstall** of ACES  
- 💾 **Automatic backup** of Blender’s original color management files  
- 🧠 Full **compatibility** with Blender **3.6 and newer**  
- 🔧 Simple structure — works out of the box  

---

## 🛠️ Build Requirements

To build Blender ACES Manager yourself, make sure you have:

- **Python** ≥ 3.8 (✅ *3.12 recommended*)  
- **PySide6** = 6.9.1  
- **Nuitka** = 2.7.12  

> 💡 Tip: You can use the included `build.cmd` script — it will install all dependencies automatically (except Python).

---

## 📄 License

This project is distributed under the **MIT License**.  
See more details in the [LICENSE](LICENSE) file.
