import string, sys, os, re, shutil, py7zr, json, tempfile, platform, locale
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QStyle
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon
from ui_blender_aces_manager import Ui_MainWindow


# ============================================
# Utils
# ============================================

def get_app_path() -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_config_path() -> str:
    temp_dir = tempfile.gettempdir()
    config_dir = os.path.join(temp_dir, "blender_aces_manager_custom_paths.json")
    return config_dir


def load_custom_paths() -> list[str]:
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        return []
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            paths = json.load(f)
        
        existing_paths = [path for path in paths if os.path.exists(path)]
        
        if len(existing_paths) != len(paths):
            save_custom_paths(existing_paths)
        
        return existing_paths
    except Exception as e:
        print(f"Cannot load config: {e}")
        return []


def save_custom_paths(paths: list[str]) -> None:
    config_path = get_config_path()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(paths, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Cannot save config: {e}")


def add_custom_path(path: str) -> None:
    custom_paths = load_custom_paths()
    
    if path not in custom_paths:
        custom_paths.append(path)
        save_custom_paths(custom_paths)

def translate_text(text: str) -> str:
    use_russian = False
    translations_dict = {
        "Blender Version:": "Версия Blender:",
        "ACES Version:": "Версия ACES:",
        "Waiting...": "Ожидание...",
        "Install ACES": "Установить ACES",
        "Uninstall ACES": "Удалить ACES",

        "Creating backup...": "Создание бэкапа...",
        "Installing ACES...": "Установка ACES...",
        "ACES installed": "ACES установлен",
        "Removing ACES...": "Удаление ACES...",
        "ACES removed": "ACES удален",
        "Unexpected error:": "Непредвиденная ошибка:",
        "Backup error:": "Ошибка бэкапа:",
        "Install error:": "Ошибка установки:",
        "Uninstall error:": "Ошибка удаления:",

        "Error": "Ошибка",
        "Not Found": "Не найдено",
        "Failed to find Blender files, manual path selection required": "Не удалось найти файлы блендера, требуется ручное указание пути",
        "colormanagement backup not found. You need to install ACES first to create a backup": "Бэкап colormanagement не найден. Необходимо сначала установить ACES для создания бэкапа",
        "Choose Blender colormanagement folder": "Выберите папку Blender colormanagement",
        "Choose Blender.app File": "Выберите файл Blender.app",
        'Please select a valid path': 'Пожалуйста, выберите правильный путь'
    }

    if platform.system() == "Windows":
        try:
            lang = locale.getlocale()[0] or locale.getdefaultlocale()[0] or ''
            use_russian = lang.lower().startswith('ru')
        except Exception:
            pass
    else:
        for var in ('LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES'):
            val = os.environ.get(var, '')
            if val.lower().startswith('ru'):
                use_russian = True
                break

    if not use_russian:
        return text

    return translations_dict.get(text, text)


# ============================================
# Blender and ACES Version Search
# ============================================

def find_blender_versions() -> list[str]:
    os_name = platform.system()
    found_versions = []
    search_paths = []
    version_pattern = re.compile(r'^\d+\.\d+(\.\d+)?$')
    
    if os_name == "Windows":
        blender_paths = ["Program Files (x86)\\Steam\\steamapps\\common\\Blender", "SteamLibrary\\steamapps\\common\\Blender"]
        for drive_letter in string.ascii_uppercase:
            for blender_path in blender_paths:
                search_paths.append(os.path.join(f"{drive_letter}:\\", blender_path))
    else:
        for entry in os.listdir("/Applications"):
            if "blender" in entry.lower() and entry.endswith(".app"):
                search_paths.append(
                    os.path.join("/Applications", entry, "Contents", "Resources")
                )

        # Steam
        search_paths.append(
            os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Blender/Blender.app/Contents/Resources")
        )

    for blender_path in search_paths:
        if not os.path.exists(blender_path):
            continue
        for entry in os.listdir(blender_path):
            colormanagement_path = os.path.join(blender_path, entry, "datafiles", "colormanagement")
            if version_pattern.match(entry) and os.path.exists(colormanagement_path):
                found_versions.append(colormanagement_path)

    return sorted(found_versions)


def find_aces_versions() -> list[str]:
    aces_path = os.path.join(get_app_path(), "ACES")

    # Get list of files and folders: remove extension from files, keep folder names as is
    aces_files = [os.path.splitext(f)[0] if os.path.isfile(os.path.join(aces_path, f)) else f for f in os.listdir(aces_path)]
    return sorted(aces_files)


def get_default_aces(aces_versions: list[str], blender_versions_default_path: str) -> str:
    default_blender_version = blender_versions_default_path.split(os.sep)[-3]
    try:
        if len(aces_versions) == 1 or "aces" not in aces_versions or "pixelmanager" not in aces_versions:
            return aces_versions[0]
        elif default_blender_version >= "4.2":
            return sorted(list(filter(lambda x: "pixelmanager" in x.lower(), aces_versions)))[-1]
        else:
            return sorted(list(filter(lambda x: "aces" in x.lower(), aces_versions)))[0]
    except Exception:
        return aces_versions[0]


# ============================================
# ACES File Operations
# ============================================

def create_colormanagement_backup(path: str) -> str:
    try:
        colormanagement_backup_path = os.path.join(os.path.dirname(path), f"{os.path.basename(path)}_backup")
        if os.path.exists(colormanagement_backup_path):
            return "Success"
        
        shutil.copytree(path, colormanagement_backup_path)
        return "Success"
    except Exception as e:
        return str(e)


def install_aces(blender_version_path: str, aces_version_path: str) -> str:
    if os.path.isdir(aces_version_path):
        return "ACES version path is a directory, expected a .7z file"
    try:
        with py7zr.SevenZipFile(aces_version_path, mode='r') as archive:
            archive.extractall(path=blender_version_path)
        return "Success"
    except Exception as e:
        return str(e)


def uninstall_aces(blender_version_path: str) -> str:
    try:
        shutil.rmtree(blender_version_path)
        shutil.copytree(os.path.join(os.path.dirname(blender_version_path), "colormanagement_backup"), blender_version_path)
        return "Success"
    except Exception as e:
        return str(e)


# ============================================
# ACES Worker Thread
# ============================================

class ACESWorker(QThread):
    progress_update = Signal(str)
    operation_finished = Signal(str)
    
    def __init__(self, operation_type: str, blender_path: str, aces_path: str = None):
        super().__init__()
        self.operation_type = operation_type
        self.blender_path = blender_path
        self.aces_path = aces_path
    
    def run(self):
        try:
            if self.operation_type == "install":
                self._install()
            elif self.operation_type == "uninstall":
                self._uninstall()
        except Exception as e:
            self.operation_finished.emit(f"{translate_text("Unexpected error:")} {str(e)}")
    
    def _install(self):
        colormanagement_backup_path = os.path.join(os.path.dirname(self.blender_path), f"{os.path.basename(self.blender_path)}_backup")
        print(colormanagement_backup_path, os.path.exists(colormanagement_backup_path))
        self.progress_update.emit(translate_text("Installing ACES..."))
        if not os.path.exists(colormanagement_backup_path):
            backup_result = create_colormanagement_backup(self.blender_path)
            if backup_result != "Success":
                self.operation_finished.emit(f"{translate_text("Backup error:")} {backup_result}")
                return

        else:
            uninstall_result = uninstall_aces(self.blender_path)
            if uninstall_result != "Success":
                self.operation_finished.emit(f"{translate_text("Uninstall error:")} {uninstall_result}")
                return
        
        install_result = install_aces(self.blender_path, self.aces_path)
        if install_result != "Success":
            self.operation_finished.emit(f"{translate_text("Install error:")} {install_result}")
            return
        
        self.progress_update.emit(translate_text("ACES installed"))
        self.operation_finished.emit("Success")
    
    def _uninstall(self):
        self.progress_update.emit(translate_text("Removing ACES..."))
        uninstall_result = uninstall_aces(self.blender_path)
        
        if uninstall_result != "Success":
            self.operation_finished.emit(f"{translate_text("Uninstall error:")} {uninstall_result}")
            return
        
        self.progress_update.emit(translate_text("ACES removed"))
        self.operation_finished.emit("Success")


# ============================================
# Main Window
# ============================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.blender_versions_browse_button.setIcon(
            QIcon.fromTheme("folder", self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        )
        
        self.worker = None
        
        self.translate_gui()
        self.init_blender_versions()
        self.init_aces_versions()
        self.connect_signals()
    
    def translate_gui(self):
        self.ui.blender_version_label.setText(translate_text("Blender Version:"))
        self.ui.aces_version_label.setText(translate_text("ACES Version:"))
        self.ui.progress_label.setText(translate_text("Waiting..."))
        self.ui.install_button.setText(translate_text("Install ACES"))
        self.ui.uninstall_button.setText(translate_text("Uninstall ACES"))
        self.ui.blender_versions_combobox.setPlaceholderText(translate_text("Not Found"))
    
    def init_blender_versions(self):
        blender_versions = find_blender_versions()
        custom_paths = load_custom_paths()
        all_paths = blender_versions + custom_paths
        
        if all_paths:
            blender_versions_default_index = all_paths.index(all_paths[-1])
            self.ui.blender_versions_combobox.addItems(all_paths)
            self.ui.blender_versions_combobox.setCurrentIndex(blender_versions_default_index)
        else:
            QMessageBox.critical(self, translate_text("Error"),
                translate_text('Failed to find Blender files, manual path selection required')
            )
    
    def init_aces_versions(self):
        aces_versions = find_aces_versions()
        self.ui.aces_versions_combobox.addItems(aces_versions)
        
        current_blender_path = self.ui.blender_versions_combobox.currentText()
        if current_blender_path:
            aces_versions_default_index = aces_versions.index(get_default_aces(aces_versions, current_blender_path))
            self.ui.aces_versions_combobox.setCurrentIndex(aces_versions_default_index)
    
    def connect_signals(self):
        self.ui.blender_versions_browse_button.clicked.connect(self.blender_versions_browse)
        self.ui.install_button.clicked.connect(lambda: self.execute_install_aces(self.ui.blender_versions_combobox.currentText(), self.ui.aces_versions_combobox.currentText()))
        self.ui.uninstall_button.clicked.connect(lambda: self.execute_uninstall_aces(self.ui.blender_versions_combobox.currentText()))
        self.ui.blender_versions_combobox.currentTextChanged.connect(self.update_uninstall_button_state)
        self.update_uninstall_button_state()
    
    def set_ui_enabled(self, enabled: bool) -> None:
        self.ui.install_button.setEnabled(enabled)
        self.ui.blender_versions_combobox.setEnabled(enabled)
        self.ui.aces_versions_combobox.setEnabled(enabled)
        self.ui.blender_versions_browse_button.setEnabled(enabled)
        if enabled:
            self.update_uninstall_button_state()
        else:
            self.ui.uninstall_button.setEnabled(False)

    def update_uninstall_button_state(self) -> None:
        current_path = self.ui.blender_versions_combobox.currentText()
        colormanagement_backup_path = os.path.join(os.path.dirname(current_path), "colormanagement_backup")
        if current_path and os.path.exists(colormanagement_backup_path):
            self.ui.uninstall_button.setEnabled(True)
            self.ui.uninstall_button.setToolTip("")
        else:
            self.ui.uninstall_button.setEnabled(False)
            self.ui.uninstall_button.setToolTip(translate_text("colormanagement backup not found. You need to install ACES first to create a backup"))
    
    def blender_versions_browse(self) -> str:
        os_name = platform.system()
        select_dialog_title = translate_text("Choose Blender colormanagement folder") if os_name == "Windows" else translate_text("Choose Blender.app File")
        guessed_colormanagement_path = ""
        colormanagement_path = QFileDialog.getExistingDirectory(self, select_dialog_title)
        if not colormanagement_path:
            return "Fail"

        if "colormanagement" not in colormanagement_path or os_name == "Darwin":
            for blender_version_folder in os.listdir(colormanagement_path):
                blender_version_folder_path = os.path.join(colormanagement_path, blender_version_folder)
                if not os.path.isdir(blender_version_folder_path) or not re.match(r'^\d+\.\d+$', blender_version_folder):
                    continue

                if os.path.exists(os.path.join(blender_version_folder_path, "datafiles", "colormanagement")) or os.path.exists(os.path.join(blender_version_folder_path, "Contents", "Resources")):
                    guessed_colormanagement_path = os.path.join(blender_version_folder_path, "datafiles", "colormanagement")
                    break

            if guessed_colormanagement_path and os.path.exists(guessed_colormanagement_path):
                colormanagement_path = guessed_colormanagement_path
            else:
                QMessageBox.critical(self, translate_text("Error"),
                    translate_text('Please select a valid path')
                )
                return "Fail"
        
        colormanagement_path = os.path.normpath(colormanagement_path)
        add_custom_path(colormanagement_path)
        
        if self.ui.blender_versions_combobox.findText(colormanagement_path) == -1:
            self.ui.blender_versions_combobox.addItem(colormanagement_path)
        
        self.ui.blender_versions_combobox.setCurrentText(colormanagement_path)
        return colormanagement_path

    def execute_install_aces(self, blender_version_path: str, aces_version_path: str) -> None:
        aces_version_path = os.path.join(get_app_path(), "ACES", f"{aces_version_path}.7z")

        self.worker = ACESWorker("install", blender_version_path, aces_version_path)
        self.worker.progress_update.connect(self.ui.progress_label.setText)
        self.worker.operation_finished.connect(self.on_install_finished)
        
        self.set_ui_enabled(False)
        self.worker.start()
    
    def execute_uninstall_aces(self, blender_version_path: str) -> None:
        self.worker = ACESWorker("uninstall", blender_version_path)
        self.worker.progress_update.connect(self.ui.progress_label.setText)
        self.worker.operation_finished.connect(self.on_uninstall_finished)
        
        self.set_ui_enabled(False)
        self.worker.start()
    
    def on_install_finished(self, result: str) -> None:
        self.set_ui_enabled(True)
        
        if result != "Success":
            print(result)
            QMessageBox.critical(self, translate_text("Error"),
                result
            )

    def on_uninstall_finished(self, result: str) -> None:
        self.set_ui_enabled(True)
        
        if result != "Success":
            print(result)
            QMessageBox.critical(self, translate_text("Error"),
                result
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    if platform.system() == "Windows":
        try:
            lang = locale.getlocale()[0] or locale.getdefaultlocale()[0] or ''
            use_russian = lang.lower().startswith('ru')
            print(f"System Language: {lang}")
        except Exception:
            pass
    else:
        for var in ('LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES'):
            val = os.environ.get(var, '')
            print(f"System Language: {val}")
            if val.lower().startswith('ru'):
                use_russian = True
                break
    
    print("Use Russian:", use_russian)

    window.show()
    sys.exit(app.exec())