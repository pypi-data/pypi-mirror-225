
# -*- coding: utf-8 -*-
"""All rights reserved. Copyright 2019 - 2020, Microchip Technology inc

This module implements the Trust Platform Settings GUI
"""
import os
import sys

import pathlib
import threading
import platform


from PySide6.QtCore import QDir
from PySide6.QtWidgets import QMessageBox, QFileDialog, QDialog

from tpds.helper import log
from tpds.settings.tpds_settings import TrustPlatformSettings

from .settings_dialog import Ui_Dialog

class SettingsDialog(QDialog):
    def __init__(self, config: TrustPlatformSettings):
        super(SettingsDialog, self).__init__()
        self._config = config
        self._config_root = self._config.settings
        self._git_obj = None    # GitModule instance
        self._git_thread_obj = None
        # Python requirements installer instance
        self.pip_requirements = threading.Event()
        self.pip_requirements.clear()
        # Setup Git Instance
        self.git_instance = None
        # load the Qt generated Dialog class
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Connect Ui_Dialog Signals
        self.ui.tb_core_path.clicked.connect(self.select_install_path)
        self.ui.tb_mplab.clicked.connect(self.select_mplab_path)

        # Populate Ui_Dialog widgets with settings data
        self.ui.le_core_path.setText(self._config_root.local_path)
        self.ui.le_core_path.setCursorPosition(0)
        self.ui.mplab_path.setText(self._config_root.mplab_path)
        self.ui.mplab_path.setCursorPosition(0)
        self.ui.cb_minimize.setChecked(self._config_root.minimize_to_tray)
        self.ui.cb_update.setChecked(self._config_root.update_on_startup)

    def reject(self):
        if not self.check_settings():
            # settings data incomplete. warn the user that
            # the application will close

            result = QMessageBox.critical(
                self,
                'Error',
                'Settings incomplete.',
                QMessageBox.Ok | QMessageBox.Cancel)

            if result == QMessageBox.Cancel:
                return False
            else:
                self._config.save()
                self.done(QDialog.Rejected)

        self.done(QDialog.Rejected)

    def accept(self):
        # Check whether settings are complete.
        # if not, indicate that they must be complete
        # to progress to the next step.
        if self.check_settings():
            self._config.save()
            self.done(QDialog.Accepted)

    def select_install_path(self):
        core_path = QFileDialog(
            self,
            caption='Installation path', directory=QDir.homePath())
        core_path.setOptions(QFileDialog.ShowDirsOnly)
        core_path.setFileMode(QFileDialog.Directory)
        result = core_path.exec()
        if result == QFileDialog.Accepted:
            self._config_root.local_path = QDir(
                str(core_path.selectedFiles()[0])).absolutePath()
            self.ui.le_core_path.setText(self._config_root.local_path)
            self.ui.le_core_path.setCursorPosition(0)

    def check_settings(self):
        log('Check if settings are valid')
        self._config_root.local_path = self.ui.le_core_path.text()
        log('local_path = {}'.format(self._config_root.local_path))
        self._config_root.mplab_path = self.ui.mplab_path.text()
        log('mplab_path = {}'.format(self._config_root.mplab_path))
        if self._config_root.local_path == "":
            QMessageBox.critical(
                self,
                'Missing setting',
                'Missing Trust Platform Core installation path',
                QMessageBox.Ok)
            #return False
        if self._config_root.mplab_path == "":
            QMessageBox.critical(
                self,
                'Missing setting',
                'Missing MPLABX installtion path',
                QMessageBox.Ok)
            #return False
        return True

    def select_mplab_path(self):
        mplab_path = ""

        if sys.platform == 'win32':
            QMessageBox.about(self, "Select MPLAB folder", r"Example: C:/Program Files (x86)/Microchip/MPLABX/v5.50")
        elif sys.platform == 'linux':
            QMessageBox.about(self, "Select MPLAB folder", r"Example: /opt/microchip/mplabx/v5.50")
        elif sys.platform == 'darwin':
            QMessageBox.about(self, "Select MPLAB folder", r"Example: /opt/microchip/mplabx/v5.50")

        mplab_path = str(QFileDialog.getExistingDirectory(
            self,
            "Select MPLAB installation directory",
            QDir.homePath(),
            QFileDialog.ShowDirsOnly))
        if QDir(mplab_path).exists():
            check_path = os.path.join(mplab_path, 'mplab_platform', 'mplablibs')

            if os.path.exists(check_path):
                log("MPLABX Path set to: {}".format(
                    mplab_path))
                self.ui.mplab_path.setText(str(mplab_path))
                self.ui.mplab_path.setCursorPosition(0)
                self._config_root.mplab_path = QDir(
                    str(mplab_path)).absolutePath()
                QMessageBox.about(
                    self,
                    'Success',
                    "MPLABX  path is set to {}".format(str(mplab_path)))
            else:
                log("MPLABX Path set to: {}".format(mplab_path))
                QMessageBox.critical(
                    self,
                    'Filesystem Error',
                    'Invalid MPLABX path',
                    QMessageBox.Ok)

        else:
            log("Invalid MPLABX directory path: {}".format(mplab_path))
            QMessageBox.critical(
                self,
                'Filesystem Error',
                'Invalid directory path',
                QMessageBox.Ok)

    def count_valid_lines(self, file_name):
        count = 0
        with open(file_name, 'r') as f:
            sline = f.readline()
            while sline:
                if(len(sline.strip().replace("\n", "").replace("\r", "")) > 0):
                    count += 1
                else:
                    pass
                sline = f.readline()
        return count

__all__ = ['SettingsDialog']
