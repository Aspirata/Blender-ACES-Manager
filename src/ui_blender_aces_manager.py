# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'blender_aces_managermigShC.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(553, 138)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(138)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(132)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.blender_version_ver = QVBoxLayout()
        self.blender_version_ver.setObjectName(u"blender_version_ver")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.blender_version_label = QLabel(self.centralwidget)
        self.blender_version_label.setObjectName(u"blender_version_label")

        self.horizontalLayout.addWidget(self.blender_version_label)

        self.blender_versions_combobox = QComboBox(self.centralwidget)
        self.blender_versions_combobox.setObjectName(u"blender_versions_combobox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.blender_versions_combobox.sizePolicy().hasHeightForWidth())
        self.blender_versions_combobox.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.blender_versions_combobox)

        self.blender_versions_browse_button = QPushButton(self.centralwidget)
        self.blender_versions_browse_button.setObjectName(u"blender_versions_browse_button")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.blender_versions_browse_button.setIcon(icon)
        self.blender_versions_browse_button.setIconSize(QSize(16, 16))
        self.blender_versions_browse_button.setCheckable(False)

        self.horizontalLayout.addWidget(self.blender_versions_browse_button)


        self.blender_version_ver.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.blender_version_ver)

        self.aces_version_hor = QHBoxLayout()
        self.aces_version_hor.setObjectName(u"aces_version_hor")
        self.aces_version_label = QLabel(self.centralwidget)
        self.aces_version_label.setObjectName(u"aces_version_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.aces_version_label.sizePolicy().hasHeightForWidth())
        self.aces_version_label.setSizePolicy(sizePolicy3)

        self.aces_version_hor.addWidget(self.aces_version_label)

        self.aces_versions_combobox = QComboBox(self.centralwidget)
        self.aces_versions_combobox.setObjectName(u"aces_versions_combobox")
        sizePolicy2.setHeightForWidth(self.aces_versions_combobox.sizePolicy().hasHeightForWidth())
        self.aces_versions_combobox.setSizePolicy(sizePolicy2)

        self.aces_version_hor.addWidget(self.aces_versions_combobox)


        self.verticalLayout.addLayout(self.aces_version_hor)

        self.progress_label = QLabel(self.centralwidget)
        self.progress_label.setObjectName(u"progress_label")

        self.verticalLayout.addWidget(self.progress_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.install_button = QPushButton(self.centralwidget)
        self.install_button.setObjectName(u"install_button")
        self.install_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_2.addWidget(self.install_button)

        self.uninstall_button = QPushButton(self.centralwidget)
        self.uninstall_button.setObjectName(u"uninstall_button")

        self.horizontalLayout_2.addWidget(self.uninstall_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Blender ACES Installer", None))
#if QT_CONFIG(whatsthis)
        self.centralwidget.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.blender_version_label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u0441\u0438\u044f \u0411\u043b\u0435\u043d\u0434\u0435\u0440\u0430:", None))
        self.blender_versions_combobox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Not Found", None))
        self.blender_versions_browse_button.setText("")
        self.aces_version_label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u0441\u0438\u044f ACES:", None))
        self.aces_versions_combobox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Aboba", None))
        self.progress_label.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0436\u0438\u0434\u0430\u043d\u0438\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439...", None))
        self.install_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c ACES", None))
        self.uninstall_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c ACES", None))
    # retranslateUi

