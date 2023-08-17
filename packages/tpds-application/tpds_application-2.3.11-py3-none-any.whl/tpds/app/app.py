import os
import sys
import time

from PySide6.QtCore import QUrl, QObject, Signal
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon


from tpds.settings.tpds_settings import TrustPlatformSettings
from tpds.launcher import TpdsBackend
from tpds.helper import LogFacility
from tpds.update import CheckUpdates
from tpds.app.ui.packman_ui import LicensePrompt
from .network import NetworkTools
from .main import MainWindow
from .vars import set_app_ref, dict_pckg



class GUILogger(QObject):
    def __init__(self, parent):
        super(GUILogger, self).__init__(parent)

    log_signal = Signal(str)


class TPDSApplication(QApplication):
    """TPDSApplication Trust Platform Design Suite Application Object

    PySide6 QApplication Object

    """
    def __init__(self, app_config=None):
        """__init__ Initializes TPDSApplication Object

        Inherits from QApplication and implement the main Qt GUI
        Starts a logging facility (either in file or in the GUI) then starts
        a Jupyter Notebook server in a separate process and create an
        autobahn python based websocket server in a separate thread to
        handle Javascript Remote procedure calls (RPC).

        RPCs go through a business logic filter documented in the websocket
        server module.

        Args:
            app_config: application settings
        """
        super(TPDSApplication, self).__init__(['', '--no-sandbox'])
        self._config = TrustPlatformSettings(values=app_config)
        set_app_ref(self)
        # QApplication settings
        self.setApplicationName("TrustPlatformDesignSuite")
        self.setApplicationDisplayName("Trust Platform Design Suite")
        self.setOrganizationDomain("microchip.com")
        self._view = None
        global _core_thread
        _core_thread = QThreadPool()

        """ Setup logging
            if log_window is False log into
            $HOME/.trustplatform/trustplatform.log
            Log at DEBUG level all messages if log_level_debug is True
        """
        self._logfile = os.path.join(self._config.settings.home_path, 'trustplatform.log')
        if self._config.settings.debug is True:
            self._log = LogFacility(
                logfile=self._config.settings.log_file,
                logstream=self._config.settings.log_window)
        self._log.log('Logging started')

        # Add application icon
        if os.path.isabs(self._config.settings.icon):
            icon_path = self._config.settings.icon
        else:
            icon_path = os.path.join(os.path.dirname(__file__),
                        self._config.settings.icon)
        self.setWindowIcon(QIcon(icon_path))
        self._log.log('App icon:' + icon_path)

        # Start the license prompt
        self.license_prompt()

        # Start GUI
        self.start_gui()

        # Check for updates if internet is availables
        self.network = NetworkTools()
        self.network.network_check_thread(self.check_for_updates)

        # Launch the backend servers
        self.backend = TpdsBackend()
        self.backend.start()

        while not self.backend.is_ready():
            time.sleep(1)

        # Load main tool page
        self.load_start_up_page()
        self._log.log("Qt event loop running")

    def check_for_updates(self, network_connected):
        status = 'available' if network_connected else 'unavailable'
        self._log.log(f'Network check is completed...it is {status}.')
        if network_connected:
            if self._config.settings.update_on_startup:
                CheckUpdates()
        else:
            nw_message = QMessageBox()
            nw_message.setIcon(QMessageBox.Warning)
            nw_message.setWindowTitle('Network')
            nw_message.setText((
                '''<font color=#0000ff><b>Internet connection is down</b></font><br>'''
                '''<br>Check connection and try again. Without internet connection,'''
                '''few links and functionality will not work.<br>'''
                '''<br>Connect to internet for improved User experience.<br>'''))
            nw_message.setStandardButtons(QMessageBox.Ok)
            nw_message.exec()

    def license_prompt(self):
        # Check if the license is already agreed by the user.
        license_check_path = os.path.join(os.getcwd(), 'license_check')

        self._log.log('Checking license agreement')
        if not os.path.isfile(license_check_path):
            # Launch the TPDS license prompt 
            license_prompt = LicensePrompt(reject_label='To start the application you must accept this agreement')
            exec_out = license_prompt.exec_()
            if exec_out:
                if license_prompt.result == 'rejected':
                    # If user rejects the license, exit the application
                    sys.exit()
                elif license_prompt.result == 'accepted':
                    try:
                        # Create a empty file indicating that the license has been accepted
                        open(license_check_path, 'a').close()
                    except:
                        self._log.log('Failed to create license check file')
            else:
                # If user closes the license prompt, exit the application
                sys.exit()
        else:
            self._log.log('License already accepted')
            pass

        return None

    def start_gui(self):
        self._view = MainWindow(
                None,
                '',
                log_view=self._config.settings.log_window)
        self._view.setWindowTitle(
            "Trust Platform Design Suite")
        if self._config.settings.log_window is True:
            qtlogger = GUILogger(self._view)
            qtlogger.log_signal.connect(self._view.loggerdock.log)
            self._log.set_logger(
                lambda message: qtlogger.log_signal.emit(message))

    def load_start_up_page(self):
        port = self.backend.api_port()
        self._log.log(f'Opening startup page from http://localhost:{port}/')
        self._view.loadmain(QUrl(f'http://localhost:{port}/'))

    def stop_backend(self):
        self.backend.stop()
