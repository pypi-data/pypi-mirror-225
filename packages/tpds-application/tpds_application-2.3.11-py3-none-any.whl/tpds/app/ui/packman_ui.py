import os
import sys
import socket
import random
import string

from functools import partial
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import (
    QThreadPool, QTimer, Slot, Qt, QAbstractTableModel, QProcess,
    QSettings, QDir)
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QWidget, QApplication, QLineEdit, QLabel,
    QPushButton, QFormLayout, QMessageBox, QTextEdit, QVBoxLayout,
    QSpacerItem, QSizePolicy, QFileDialog)
from packaging.version import parse
from zipfile import ZipFile

from tpds.settings import TrustPlatformSettings
from tpds.app.network import NetworkTools
from tpds.worker import Worker
from tpds.app.vars import get_setting_name
from tpds.app.processing import TpdsAppProcessing
from tpds.app.control import shutdown
from tpds.package_manager import PackageManager, prettify_channel
from tpds.helper import TableIterator

from .packman_form import Ui_Form

default_tpds_pckgs = [
    'tpds-application',
    'tpds-core',
    'tpds-helper'
]

nda_tpds_pckgs = [
    'sw-atecc608b-tcsm',
    'sw-ta100-tcsm'
]

third_party_pckgs = []

tpds_default_channel = 'microchiporg'


def run_in_thread(fn, *args, result_callback=None, **kwargs):
    """
    Run a specific function in worker thread,
    only result callback is supported
    """
    worker_obj = Worker(fn, *args, **kwargs)
    worker_obj.signals.result.connect(result_callback)
    QThreadPool.globalInstance().start(worker_obj)


def get_installed_packages(package_manager):
    return package_manager.get_installed()


def is_logged_in(package_manager):
    return package_manager.is_logged_in()


def login_package_manager(package_manager, *args):
    try:
        package_manager.login(*args)
        return 0
    except BaseException:
        return -1


def logout_package_manager(package_manager):
    return package_manager.logout()


def get_packages(package_manager):
    return package_manager.get_packages()


def refresh_package_list(package_manager, *args):
    return package_manager.refresh_package_list(*args)


def install_package(package_manager, packages, **kwargs):
    return package_manager.install(packages, refresh=False, **kwargs)


class LoginPrompt(QDialog):
    """
    Class for Login prompt
    """
    def __init__(self, parent=None):
        super(LoginPrompt, self).__init__(parent)
        # QLineEdit and QuserLabel for Username
        self.username = QLineEdit(self)
        self.QUserLabel = QLabel("Username : ")
        # QLineEdit and QuserLabel for Password
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.QPasswordLabel = QLabel("Password : ")
        # QPushbutton for Submit button
        self.btn_Submit = QPushButton(" Login ")
        # Structure/Layout UI
        layout = QFormLayout()
        layout.addRow(self.QUserLabel, self.username)
        layout.addRow(self.QPasswordLabel, self.password)
        layout.addRow(self.btn_Submit)
        # Set as form layout
        self.setLayout(layout)
        # Add callback for submit button click
        self.btn_Submit.clicked.connect(self.btn_submit_clicked)

    def btn_submit_clicked(self):
        """
        Callback for submit button
        """
        self.user = self.username.text()
        self.psswd = self.password.text()
        self.close()


class LicensePrompt(QDialog):
    """
    UI Class for license prompt
    """
    def __init__(
            self, parent=None, package_name='',
            reject_label='To install this package you must accept this agreement'):
        super(LicensePrompt, self).__init__(parent)
        # CMD list class variable copy
        self.package_name = package_name
        # Get the reject label to get context
        self.reject_label = reject_label
        # Setup the UI
        self.setup_ui()
        # Setup License terms in text window
        self.setup_license()
        # Variable to hold user button click
        self.result = None

    def setup_ui(self):
        """
        Setup UI
        """
        # Set window title
        self.setWindowTitle(f'{self.package_name.upper()} License Agreement')
        self.setMinimumHeight(800)
        self.setMinimumWidth(1300)
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # License text line edit header
        self.license_label = QLabel(self)
        self.license_label.setText(
            "Please read the following license agreement carefully")
        self.license_label.setWordWrap(True)
        # License text window and set minimumsize
        self.license_textedit = QTextEdit(self)
        self.license_textedit.setReadOnly(True)
        self.license_textedit.setMinimumHeight(600)
        self.license_textedit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        # Accept/Reject Qlabel information
        self.accept_reject_label = QLabel(self)
        self.accept_reject_label.setText(
            "If you select Reject, the prompt will close." + self.reject_label)
        self.accept_reject_label.setWordWrap(True)
        # QPushbutton for Accept button
        self.btn_accept = QPushButton(" Accept ")
        # QPushbutton for Reject button
        self.btn_reject = QPushButton(" Reject ")
        self.accept_reject_spacer = QSpacerItem(
            200, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # Structure/Layout UI
        self.layout = QFormLayout()
        self.layout.addRow(self.license_label)
        self.layout.addRow(self.license_textedit)
        self.layout.addRow(self.accept_reject_label)
        self.hbox = QHBoxLayout()
        self.hbox.addSpacerItem(self.accept_reject_spacer)
        self.hbox.addWidget(self.btn_accept)
        self.hbox.addWidget(self.btn_reject)
        self.layout.addRow(self.hbox)
        # Set as form layout
        self.setLayout(self.layout)
        # Set Slot for accept button
        self.btn_accept.clicked.connect(self.accept_callback)
        # Set Slot for reject button
        self.btn_reject.clicked.connect(self.reject_callback)

    @Slot()
    def accept_callback(self):
        # Set variable
        self.result = 'accepted'
        # Accept QDialog to close
        self.accept()

    @Slot()
    def reject_callback(self):
        # Set variable
        self.result = 'rejected'
        # Accept QDialog to close
        self.accept()

    def get_license_diectory(self):
        """
        Get package license directory
        """
        # Fetch conda_prefix
        config = TrustPlatformSettings()
        conda_path = config.settings.conda_path
        # Join with the license dir path
        license_path = os.path.join(
            conda_path, 'tpds_application', 'package_manager', 'pkg_licenses')
        return license_path

    def setup_license(self):
        """
        Fetch and display the license from file
        """
        try:
            package = PackageManager(processor=TpdsAppProcessing()).get_packages(self.package_name)[0]

            if package.license_text:
                license_text = package.license_text
            elif package.license:
                license_text = package.license
            else:
                license_text = PackageManager().get_default_license()
        except BaseException:
            license_text = PackageManager().get_default_license()

        self.license_textedit.append(license_text)
        self.license_textedit.moveCursor(QTextCursor.Start)


class PackageAction(QDialog):
    """
    QDialog class to execute install / upgrade commands with a UI window
    """
    def __init__(self, parent=None, cmd_list=None):
        """
        Init class, with cmd process
        """
        super(PackageAction, self).__init__(parent)
        # Init UI
        self.setup_UI()

        self._parent = parent

        # Connect the package manager
        self.package_manager = parent.package_manager

        # Initial Process state
        self.process_running = False

        # Running process associated with this action
        self.process = None

        # Setup signals and slots
        self.btn_close.clicked.connect(self.close_event)

    def setup_UI(self):
        # Setup widgets and layout
        self.info_label = QLabel()
        self.info_label.setText('Command Log :')
        self.cmd_log = QTextEdit()
        self.btn_close = QPushButton('Close')
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.info_label)
        vlayout.addWidget(self.cmd_log)
        vlayout.addWidget(self.btn_close)
        self.setLayout(vlayout)
        self.cmd_log.setMinimumHeight(200)
        self.cmd_log.setMinimumWidth(500)

    def install_package(self, package_name) -> None:
        if package_name is not None:
            package_name = package_name.strip()

        license_prompt = LicensePrompt(package_name=package_name)
        exec_out = license_prompt.exec_()
        if exec_out:
            if license_prompt.result == 'rejected':
                return None
            self.update_package(package_name, name='Package Installer')
        else:
            return None

    def update_package(
            self, package_name, name: str = 'Package Updater',
            final_package: bool = True) -> None:
        # Reset state
        self.process_running = False

        # We'll forward display to ourselves
        callbacks = {
            'result_callback': self.update_package_callback,
            'stdout_callback': self.cmd_text_update,
            'stderr_callback': self.cmd_error_update,
            'started_callback': self.cmd_started
        }
        if not final_package:
            # It is not the final package, keep the close button disabled
            callbacks['result_callback'] = \
                self.update_package_callback_close_disabled

        # Set Window Title based on command
        self.setWindowTitle(name)
        # Show self
        self.show()
        # Run the install package function in thread
        run_in_thread(
            install_package, self.package_manager, [package_name], **callbacks)

    def update_package_callback(self):
        self.process_running = False
        self._parent._restart_required = True
        self._parent.refresh_action(True, False)
        self.btn_close.setEnabled(True)

    def update_package_callback_close_disabled(self):
        # Retain the state of the UI close button
        self.process_running = False
        self._parent._restart_required = True
        self._parent.refresh_action(True, False)

    def closeEvent(self, event):
        # Close event from Qdialog class
        if self.process_running:
            # Kill any process before quiting
            self.process.kill()
            event.accept()
        else:
            event.accept()

    @Slot()
    def close_event(self):
        # Close signal called from close button
        self.process.kill()
        self.close()

    @Slot(str)
    def cmd_text_update(self, stdout_buffer):
        # Pipe stdout to textbox
        self.cmd_log.append(stdout_buffer.replace('\0', ''))
        self.cmd_log.verticalScrollBar().setValue(
            self.cmd_log.verticalScrollBar().maximum())

    @Slot(str)
    def cmd_error_update(self, stderr_buffer):
        # Pipe stderr to textbox
        self.cmd_log.append(stderr_buffer.replace('\0', ''))
        self.cmd_log.verticalScrollBar().setValue(
            self.cmd_log.verticalScrollBar().maximum())

    @Slot(QProcess)
    def cmd_started(self, process):
        self.process = process
        self.process_running = True
        # Command started callback
        self.cmd_log.append('Started processing command ...')
        self.btn_close.setEnabled(False)


class TableModel(QAbstractTableModel):
    """
    QAbstractTableModel model for standard tables
    """
    def __init__(self, data, columns):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = columns

    def data(self, index, role):
        """
        Function to load the given data
        """
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        """
        Overloaded rowCount function
        """
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        """
        Overloaded columnCount function
        """
        # The following takes the first sub-list, and returns the length
        return len(self.columns)

    def headerData(self, section, orientation, role):
        """
        Code to update the tabls headers
        """
        # Section is the index of the column.
        # Column names are
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.columns[section])


class PackageManagerUi(QWidget):
    """
    Package manager class, handles GUI events
    """
    def __init__(self):
        super(PackageManagerUi, self).__init__()
        # Load QT generated Qwidget class
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.tabWidget.setCurrentIndex(0)
        self.process_list = []
        self.restoreWindow()
        self.show()
        self._restart_required = False
        # Class variables
        self.package_manager = PackageManager(processor=TpdsAppProcessing())
        self.installed_packages = None
        self.package_info = None
        self.processed_table_content = None
        self.package_update_obj = PackageAction(parent=self)
        # Setup signals/slots
        self.ui.login_button.clicked.connect(self.login_button_clicked)
        self.ui.refresh_button.clicked.connect(self.refresh_action)
        self.ui.install_extn_button.clicked.connect(self.install_extn_action)
        # Update UI content
        self.refresh_action(False, False)

    def restoreWindow(self) -> None:
        geometry = QSettings().value(get_setting_name(self, 'geometry'), None)
        if geometry is not None:
            self.restoreGeometry(geometry)
        return True

    def updateStatus(self, message) -> None:
        self.ui.statusbar.showMessage(message, timeout=0)

    @Slot()
    def install_extn_action(self):
        def reset_ui_state():
            self.ui.refresh_button.setEnabled(True)
            self.ui.install_extn_button.setEnabled(True)

        zipUrl, _ = QFileDialog.getOpenFileName(
                            None,
                            dir=os.path.join(
                                str(QDir.homePath()), 'Downloads'),
                            caption='Select Extension Package to install',
                            filter="Zip Files (*.zip)")

        workingDir = os.path.join(str(
            QDir.homePath()), '.trustplatform', 'tpds_extn_install')
        os.makedirs(workingDir, exist_ok=True)
        if not zipUrl:
            return None
        with ZipFile(os.path.normpath(zipUrl), 'r') as zipObject:
            whlFiles = [zipObject.extract(fileName, workingDir) for fileName in zipObject.namelist() if fileName.endswith('.whl')]
            if len(whlFiles):
                self.ui.refresh_button.setEnabled(False)
                self.ui.install_extn_button.setEnabled(False)
                # Loop through the list and invoke license prompts
                for whlFile in whlFiles:
                    wheel_data = os.path.basename(whlFile).split('-')
                    license_prompt = LicensePrompt(
                        package_name=f'{wheel_data[0]}-{wheel_data[1]}')
                    exec_out = license_prompt.exec_()
                    if exec_out:
                        if license_prompt.result == 'rejected':
                            # License is rejected, reset the UI state
                            # and return
                            reset_ui_state()
                            return None
                # Loop through the list and install packages
                for whlFile in whlFiles:
                    # Checking for the final package to change state of UI
                    # close button in case of bundles with more than
                    # one wheel file
                    if whlFile == whlFiles[-1]:
                        self.package_update_obj.update_package(
                            whlFile,
                            name=f'Installing {os.path.basename(whlFile)}',
                            final_package=True)
                    else:
                        self.package_update_obj.update_package(
                            whlFile,
                            name=f'Installing {os.path.basename(whlFile)}',
                            final_package=False)
        reset_ui_state()
        return None

    @Slot()
    def refresh_action(self, local: bool = True, remote: bool = True):
        # Disable refresh button
        self.ui.refresh_button.setEnabled(False)
        # Also disable login while the refresh is happening
        self.ui.login_button.setEnabled(False)
        self.ui.install_extn_button.setEnabled(False)
        # Reset Table data
        self.installed_packages = None
        self.package_info = None
        # Update the package lists
        self.updateStatus('Refreshing package info...')
        run_in_thread(
            refresh_package_list, self.package_manager, local, remote,
            result_callback=self.refresh_action_callback)

    def refresh_action_callback(self):
        self.refresh_ui_content()

    def refresh_ui_content(self):
        # Setup tpds packages tab
        self.setup_tpds_packags_Tab()
        # Setup timer routine to monitor activities
        self.tpds_packages_tab_timer()
        # Check available packages that user has access to
        self.get_package_info()
        # Setup installed packages table
        self.set_installed_packages()
        # Check if logged in
        # self.ui.login_info.setText('')
        # self.check_if_logged_in()
        self.ui.refresh_button.setEnabled(True)
        self.ui.login_button.setEnabled(False)
        self.ui.install_extn_button.setEnabled(True)

    def closeEvent(self, event):
        """
        Catching close event to close gracefully
        """
        QSettings().setValue(get_setting_name(
            self, 'geometry'), self.saveGeometry())
        if self._restart_required:
            shutdown('A package was installed or updated - the application will need to be restarted', True)
        event.accept()

    def _display_version(self, version) -> str:
        return str(version) if version else ''

    def set_available_packages_table(self, data, columns):
        """
        Function to set and load data onto table
        """
        self.model = TableModel(data, columns)
        self.ui.installed_pkgs_table.setModel(self.model)
        self.ui.installed_pkgs_table.resizeColumnsToContents()

    def set_tpds_packages_table(self, data, columns):
        """
        Function to set and load data onto table
        """
        self.tpds_model = TableModel(data, columns)
        self.ui.tpds_packages_table.setModel(self.tpds_model)
        self.ui.tpds_packages_table.resizeColumnsToContents()

    def set_installed_packages(self):
        """
        Fetch conda list information in thread
        """
        # Execute the conda list in a thread
        run_in_thread(
            get_installed_packages, self.package_manager,
            result_callback=self.installed_packages_callback)

    def installed_packages_callback(self, result):
        """
        Callback which fetches result from conda list and updates GUI
        """
        if result is None:
            self.updateStatus('Error fetching installed packages')
            return None

        # Store result in class variable
        self.installed_packages = list(TableIterator(
            result, ['name', (
                'installed', self._display_version),
                ('channel', prettify_channel)]))

        # Update the table with package list
        columns = ['Package', 'Version', 'Channel']
        self.set_available_packages_table(self.installed_packages, columns)
        self.updateStatus('Done')
        self.ui.refresh_button.setEnabled(True)
        return None

    def check_if_logged_in(self):
        """
        Function to check if someone is logged in
        """
        # Info initial state
        self.ui.login_info.setText('Checking login info...')
        # Disable button till we get some info
        self.ui.login_button.setEnabled(False)
        # Execute the conda list in a thread
        run_in_thread(
            is_logged_in, self.package_manager,
            result_callback=self.check_if_logged_in_callback)

    def check_if_logged_in_callback(self, username):
        """
        Is logged in callback
        """
        if username is not None:
            # Set Info
            self.ui.login_info.setText('Logged in as \'{}\''.format(username))
            self.ui.login_button.setText('Logout')
        else:
            # Set Info
            self.ui.login_info.setText('')
            self.ui.login_button.setText('Login')
        # Enable button
        self.ui.login_button.setEnabled(True)

    @Slot()
    def login_button_clicked(self):
        """
        Callback for login button click
        """
        self.trigger_after_nw_check(self.process_login_button)

    def process_login_button(self, internet_available):
        if internet_available:
            if self.ui.login_button.text() == 'Logout':
                self.run_logout()
            elif self.ui.login_button.text() == 'Login':
                self.run_login()
        else:
            nw_message = QMessageBox()
            nw_message.setIcon(QMessageBox.Warning)
            nw_message.setWindowTitle('Network')
            nw_message.setText((
                '''
                <font color=#0000ff>
                    <b>Internet connection is down</b>
                </font><br>
                <br>Check connection and try again<br>
                '''
                ))
            nw_message.setStandardButtons(QMessageBox.Ok)
            nw_message.exec()

    def run_logout(self):
        # Set info banner
        self.ui.login_info.setText('Logging out...')
        # Disable button
        self.ui.login_button.setEnabled(False)
        # Execute the command in a thread
        run_in_thread(
            logout_package_manager, self.package_manager,
            result_callback=self.run_logout_callback)

    def run_logout_callback(self, result):
        # Set info banner
        self.ui.login_info.setText('')
        # Change button text
        self.ui.login_button.setText('Login')
        # Enable button
        self.ui.login_button.setEnabled(True)

    def run_login(self):
        # Set info banner
        self.ui.login_info.setText('Logging in...')
        # Disable button
        self.ui.login_button.setEnabled(False)
        # Get login username and password from QDialog
        prompt = LoginPrompt(parent=self)
        prompt.exec_()

        def exit_routine():
            # Set info banner
            self.ui.login_info.setText('')
            # Change button text
            self.ui.login_button.setText('Login')
            # Enable button
            self.ui.login_button.setEnabled(True)
            return None

        try:
            username = prompt.user
            password = prompt.psswd
            # Exit if username or password too small
            if (len(str(username)) < 2) or (len(str(password)) < 7):
                QMessageBox.warning(
                    self, "Invalid credentials", "Username/Password too short")
                # Call exit routine
                exit_routine()
                return None
        except Exception:
            # Window is closed, call exit routine
            exit_routine()
            return None

        # Get a custom randomized hostname
        letters = string.ascii_lowercase
        pc_hostname = socket.gethostname()
        hostname = pc_hostname + '-' + \
            ''.join(random.choice(letters) for i in range(5))

        # Push conda login credentials to background thread for processing
        run_in_thread(
            login_package_manager, self.package_manager,
            username, password, hostname,
            result_callback=self.run_login_callback)

    def run_login_callback(self, result):
        # Set info banner
        self.ui.login_info.setText('')
        if result != 0:
            print('run_login_callback: ', result)
            QMessageBox.warning(
                self, "Login falied",
                "Login failed: Please check credentials and network connection")
            # Enable login button
            self.ui.login_button.setEnabled(True)
        else:
            self.check_if_logged_in()

    def trigger_after_nw_check(self, fn):
        # Network check callback
        network_manager = NetworkTools()
        network_manager.network_check_thread(fn)

    def setup_tpds_packags_Tab(self):
        # Setup startup state of tpds_packages tab elements
        pass

    def get_package_info(self):
        # Start conda show
        self.updateStatus('Fetching available tpds packages')
        run_in_thread(
            get_packages, self.package_manager,
            result_callback=self.get_packages_callback)

    def get_packages_callback(self, result):
        # ['Package name', 'Channel', 'Installed version',
        # 'Latest version', 'Action']
        self.package_info = list(TableIterator(
            result,
            ['name', ('channel', prettify_channel),
                ('installed', self._display_version),
                ('latest', self._display_version)]))

    def tpds_packages_tab_timer(self):
        self.tpds_packages_timer = QTimer()
        self.tpds_packages_timer.timeout.connect(
            self.tpds_packages_timer_callback)
        self.tpds_packages_timer.start(1000)
        self.tpds_packages_timer_counter = 0
        self.tpds_packages_timer_timeout = 120

    def tpds_packages_timer_callback(self):
        self.tpds_packages_timer_counter += 1

        # Check for timer timeout
        if self.tpds_packages_timer_counter >= \
                self.tpds_packages_timer_timeout:
            self.ui.tpds_packages_label.setText(
                'Data fetch timeout, check network connection')
            return None

        # Set progress messages
        if self.installed_packages is None:
            self.updateStatus('Fetching available tpds packages')
            return None
        elif self.package_info is None:
            self.updateStatus('Fetching packages and available versions')
            return None

        # Check is all data needed are available
        if (self.installed_packages is not None) and \
                (self.package_info is not None):
            # Everything good, stop timer and process data
            self.tpds_packages_timer.stop()
            self.updateStatus('Done')
            self.processed_table_content = self.process_tpds_packages_data()

            self.post_process_table_data()

    def process_tpds_packages_data(self):
        """
        Process data for packages
        """
        # Package name, channel, installed version, latest version, status
        self.tpds_packages_table_content = \
            [x + [''] for x in self.package_info]

        columns = [
            'Package name', 'Channel',
            'Installed version', 'Latest version',
            'Action']
        self.set_tpds_packages_table(self.tpds_packages_table_content, columns)

        return self.tpds_packages_table_content

    def post_process_table_data(self):
        """
        Post process table content, add user access
        """
        table_data = self.processed_table_content

        for index, row in enumerate(table_data):
            package_name = row[0]
            installed_version = row[2]
            latest_version = row[3]
            action_item_column = 4

            if installed_version == '':
                btn = QPushButton(self.ui.tpds_packages_table)
                btn.setText('Install')
                btn.clicked.connect(partial(
                    self.package_update_obj.install_package, package_name))
                self.ui.tpds_packages_table.setIndexWidget(
                    self.tpds_model.index(index, action_item_column), btn)
            elif parse(installed_version) >= parse(latest_version):
                temp_label = QLabel()
                temp_label.setText('Up-to-date')
                self.ui.tpds_packages_table.setIndexWidget(
                    self.tpds_model.index(
                        index, action_item_column), temp_label)
            else:
                btn = QPushButton(self.ui.tpds_packages_table)
                btn.setText('Update')
                btn.clicked.connect(partial(
                    self.package_update_obj.update_package, package_name))
                self.ui.tpds_packages_table.setIndexWidget(
                    self.tpds_model.index(index, action_item_column), btn)

        self.ui.tpds_packages_table.resizeColumnsToContents()


def tpds_package_manager():
    app = QApplication(sys.argv)
    app.setApplicationName("TrustPlatformDesignSuite")
    app.setApplicationDisplayName("Trust Platform Design Suite")
    app.setOrganizationDomain("microchip.com")

    PackageManagerUi()
    sys.exit(app.exec_())


__all__ = ['PackageManagerUi', 'tpds_package_manager']

if __name__ == "__main__":
    tpds_package_manager()
