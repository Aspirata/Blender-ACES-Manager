import string, sys, os, re, shutil, py7zr, json, tempfile, platform
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QThread, Signal
from ui_blender_aces_manager import Ui_MainWindow


# ============================================
# Path and Config Utils
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


# ============================================
# Blender and ACES Version Search
# ============================================

def find_blender_versions() -> list[str]:
    os_name = platform.system()
    found_versions = []
    version_pattern = re.compile(r'^\d+\.\d+(\.\d+)?$')
    
    if os_name == "Windows":
        search_paths = []
        blender_paths = ["Program Files (x86)\\Steam\\steamapps\\common\\Blender", "SteamLibrary\\steamapps\\common\\Blender"]
        for drive_letter in string.ascii_uppercase:
            for blender_path in blender_paths:
                search_paths.append(os.path.join(f"{drive_letter}:\\", blender_path))
    else:
        search_paths = [
            os.path.expanduser("~/Applications/Blender.app/Contents/Resources"),
            os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Blender")
        ]

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
    aces_files = [f[:-3] for f in os.listdir(aces_path)]
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
            self.operation_finished.emit(f"Unexpected error: {str(e)}")
    
    def _install(self):
        self.progress_update.emit("Создание бэкапа...")
        backup_result = create_colormanagement_backup(self.blender_path)
        
        if backup_result != "Success":
            self.operation_finished.emit(f"Backup error: {backup_result}")
            return
        
        self.progress_update.emit("Установка ACES...")
        install_result = install_aces(self.blender_path, self.aces_path)
        
        if install_result != "Success":
            self.operation_finished.emit(f"Install error: {install_result}")
            return
        
        self.progress_update.emit("ACES установлен")
        self.operation_finished.emit("Success")
    
    def _uninstall(self):
        self.progress_update.emit("Удаление ACES...")
        uninstall_result = uninstall_aces(self.blender_path)
        
        if uninstall_result != "Success":
            self.operation_finished.emit(f"Uninstall error: {uninstall_result}")
            return
        
        self.progress_update.emit("ACES удален")
        self.operation_finished.emit("Success")


# ============================================
# Main Window
# ============================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.worker = None
        
        self.init_blender_versions()
        self.init_aces_versions()
        self.connect_signals()
    
    def init_blender_versions(self):
        blender_versions = find_blender_versions()
        custom_paths = load_custom_paths()
        all_paths = blender_versions + custom_paths
        
        if all_paths:
            blender_versions_default_index = all_paths.index(all_paths[-1])
            self.ui.blender_versions_combobox.addItems(all_paths)
            self.ui.blender_versions_combobox.setCurrentIndex(blender_versions_default_index)
        else:
            QMessageBox.critical(self, "Ошибка",
                f'Не удалось найти файлы блендера, требуется ручное указание пути'
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
            self.ui.uninstall_button.setToolTip("Бэкап colormanagement не найден. Необходимо сначала установить ACES для создания бэкапа.")
    
    def blender_versions_browse(self) -> str:
        colormanagement_path = QFileDialog.getExistingDirectory(self, "Выберите папку Blender Colormanagement")
        if not colormanagement_path:
            return "Fail"
        
        if "colormanagement" not in colormanagement_path:
            QMessageBox.critical(self, "Ошибка",
                f'Необходимо выбрать папку colormanagement, например "Blender\\5.0\\datafiles\\colormanagement"'
            )
            return "Fail"
        
        colormanagement_path = colormanagement_path.replace("/", "\\")
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
            QMessageBox.critical(self, "Ошибка",
                f'Не удалось установить ACES:\n{result}'
            )

    def on_uninstall_finished(self, result: str) -> None:
        self.set_ui_enabled(True)
        
        if result != "Success":
            QMessageBox.critical(self, "Ошибка",
                f'Не удалось удалить ACES:\n{result}'
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())