# Languages: [🇷🇺 RU](README_ru.md) | [🇺🇸 *EN*](README.md)

# Blender ACES Manager

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-31210/)
[![License](https://img.shields.io/badge/License-GPLv3-orange.svg)](./LICENSE)
[![GitHub downloads](https://img.shields.io/github/downloads/Aspirata/Blender-ACES-Manager/total)](https://github.com/Aspirata/Blender-ACES-Manager/releases)
[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label)](https://discord.gg/y4CWTzbZcv)

> [!WARNING]
> Blender 5.0+ has built-in ACES 1.3 and 2.0, you don't need an external app anymore

**Blender ACES Manager** — это лёгкая утилита для простого управления **цветовой системой ACES** в **Blender**.

---

## 🎨 Что такое ACES?

**ACES (Academy Color Encoding System)** — это промышленный стандарт управления цветом, используемый в кино и визуальных эффектах.  
Он обеспечивает единообразные, точные и естественные цвета на разных устройствах, что делает его важным инструментом для профессиональной цветокоррекции и рендеринга.

**Проще говоря:**  
ACES делает ваши рендеры более кинематографичными — как в голливудских фильмах.

---

## ⚙️ Возможности

- 🧩 Установка и удаление ACES в один клик  
- 💾 **Автоматическое резервное копирование** оригинальных файлов управления цветом Blender  
- 🧠 Полная **совместимость** с версиями Blender **3.6 и выше**  
- 🔧 Простая структура — работает "из коробки"  

## 📦 Предустановленные версии ACES
- **[PixelManager v2.0](https://github.com/Joegenco/PixelManager/releases/tag/v.2.0-RC4)**  
  Обновлённый набор файлов управления цветом с поддержкой **ACES 1.3**, **ACES 2.0** и стандартной системы управления цветом **Blender 4.4**.

Вы также можете использовать собственные версии ACES или другие цветовые менеджеры — просто поместите их в папку **`ACES`** перед сборкой.

## 🖥️ Поддержка ОС

| ОС        | Статус               | Подробности                                                                 |
|-----------|----------------------|-----------------------------------------------------------------------------|
| **Windows** | Работает лучше всего ✅ | Полная поддержка                                                            |
| **macOS**   | Работает нормально ✅  | Работает нормально, но требует тестирования                                 |
| **Linux**   | Вообще не работает ❌   | Blender ACES Manager не поддерживается и не работает на Linux               |

---

## 🛠️ Зависимости для сборки

Для самостоятельной сборки Blender ACES Manager вам понадобятся:

- **Python** = 3.12  
- **PySide6** = 6.10.2  
- **nuitka** = 4.0.1  
- **zstandard** = 0.25.0  
- **py7zr** = 1.1.0   

> 💡 Совет: используйте встроенный скрипт `build.cmd` — он установит все зависимости автоматически (кроме Python)

---

## 📄 Лицензия

Проект распространяется под лицензией **GPLv3**.  
Подробнее см. файл [LICENSE](./LICENSE).
