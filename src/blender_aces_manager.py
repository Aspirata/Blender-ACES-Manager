import string, sys, os, re, shutil, py7zr, json, tempfile
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QTimer
from ui_blender_aces_manager import *


def get_app_path() -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS # internal .exe path
    else:
        return os.path.dirname(os.path.abspath(__file__)) # usual .py path


def get_config_path() -> str:
    temp_dir = tempfile.gettempdir()
    config_dir = os.path.join(temp_dir, "blender_aces_manager")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    return os.path.join(config_dir, "custom_paths.json")


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


def find_blender_versions() -> list[str]:
    blender_paths = ["Program Files (x86)\\Steam\\steamapps\\common\\Blender", "SteamLibrary\\steamapps\\common\\Blender"]
    found_versions = []
    version_pattern = re.compile(r'^\d+\.\d+(\.\d+)?$')
    
    for drive_letter in string.ascii_uppercase:
        for blender_path in blender_paths:
            full_blender_path = os.path.join(f"{drive_letter}:\\", blender_path)
            if not os.path.exists(full_blender_path):
                continue

            for entry in os.listdir(full_blender_path):
                entry_path = os.path.join(full_blender_path, entry)
                if not os.path.isdir(entry_path):
                    continue
                
                colormanagement_path = os.path.join(entry_path, "datafiles", "colormanagement")
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

def create_colormanagement_backup(path: str) -> str:
    try:
        colormanagement_backup_path = os.path.join(os.path.dirname(path), f"{os.path.basename(path)}_backup")
        if os.path.exists(colormanagement_backup_path):
            return "Success"
        
        window.start_progress_animation("Создание бэкапа")
        shutil.copytree(path, colormanagement_backup_path)
        window.change_progress_status("Бэкап создан")
        return "Success"
    except Exception as e:
        return str(e)


def install_aces(blender_version_path: str, aces_version_path: str) -> str:
    try:
        window.start_progress_animation("Установка ACES")
        
        with py7zr.SevenZipFile(aces_version_path, mode='r') as archive:
            archive.extractall(path=blender_version_path)

        window.change_progress_status("ACES установлен")
        return "Success"
    except Exception as e:
        return str(e)


def uninstall_aces(blender_version_path: str) -> str:
    try:
        window.start_progress_animation("Удаление ACES")
        shutil.rmtree(blender_version_path)
        shutil.copytree(os.path.join(os.path.dirname(blender_version_path), "colormanagement_backup"), blender_version_path)
        window.change_progress_status("ACES удален")
        return "Success"
    except Exception as e:
        return str(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        global main_window
        main_window = self
        
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._animate_dots)
        self.progress_text = ""
        self.dot_count = 0
        
        blender_versions = find_blender_versions()
        custom_paths = load_custom_paths()
        all_paths = blender_versions + custom_paths
        
        if all_paths:
            blender_versions_default_index = all_paths.index(all_paths[-1])
            self.ui.blender_versions_combobox.addItems(all_paths)
            self.ui.blender_versions_combobox.setCurrentIndex(blender_versions_default_index)
        else:
            QMessageBox.critical(self, "Ошибка",
                f'Неудалось найти файлы блендера, требуется ручное указание пути"'
            )
            
        self.ui.blender_versions_browse_button.clicked.connect(self.blender_versions_browse)

        aces_versions = find_aces_versions()
        self.ui.aces_versions_combobox.addItems(aces_versions)
        if blender_versions_default_index:
            aces_versions_default_index = aces_versions.index(get_default_aces(aces_versions, self.ui.blender_versions_combobox.currentText()))
            self.ui.aces_versions_combobox.setCurrentIndex(aces_versions_default_index)

        self.ui.install_button.clicked.connect(lambda: self.execute_install_aces(self.ui.blender_versions_combobox.currentText(), self.ui.aces_versions_combobox.currentText()))
        self.ui.uninstall_button.clicked.connect(lambda: self.execute_uninstall_aces(self.ui.blender_versions_combobox.currentText()))
        self.ui.blender_versions_combobox.currentTextChanged.connect(self.update_uninstall_button_state)
        self.update_uninstall_button_state()

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
        
        elif "colormanagement" not in colormanagement_path:
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

    def execute_install_aces(self, blender_version_path: str, aces_version_path: str) -> str:
        aces_version_path = os.path.join(get_app_path(), "ACES", f"{aces_version_path}.7z")
        create_colormanagement_backup_result = create_colormanagement_backup(blender_version_path)
        if create_colormanagement_backup_result != "Success":
            QMessageBox.critical(self, "Ошибка",
                f'Неудалось создать бэкап: {create_colormanagement_backup_result}'
            )
            return "Fail"
        
        install_aces_result = install_aces(blender_version_path, aces_version_path)
        if install_aces_result != "Success":
            QMessageBox.critical(self, "Ошибка",
                f'Неудалось установить ACES: {install_aces_result}'
            )
            return "Fail"
        
        self.update_uninstall_button_state()
        
        return "Success"
    
    def execute_uninstall_aces(self, blender_version_path: str) -> str:
        uninstall_aces_result = uninstall_aces(blender_version_path)
        if uninstall_aces_result != "Success":
            QMessageBox.critical(self, "Ошибка",
                f'Неудалось удалить ACES: {uninstall_aces_result}'
            )
            return "Fail"
        
        return "Success"

    def start_progress_animation(self, text: str) -> None:
        self.progress_text = text
        self.dot_count = 0
        self.progress_timer.start(500)
    
    def _animate_dots(self):
        self.dot_count = self.dot_count % 3 + 1
        self.ui.progress_label.setText(f"{self.progress_text}{'.' * self.dot_count}")
    
    def stop_progress_animation(self) -> None:
        self.progress_timer.stop()
        self.ui.progress_label.setText("")
    
    def change_progress_status(self, status: str) -> None:
        self.progress_timer.stop()
        self.ui.progress_label.setText(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())