import sys

from PySide6.QtCore import QCoreApplication, Slot
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QMessageBox, QSizePolicy

from tpds.worker import Worker
from tpds.settings.tpds_settings import TrustPlatformSettings
from tpds.helper.logger import LogFacility
from tpds.package_manager import PackageManager
from tpds.app.processing import TpdsAppProcessing
from tpds.app.control import shutdown


class UpdateMessageBox(QMessageBox):
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setFixedWidth(1000)


class CheckUpdates():
    def __init__(self, prompt_for_no_updates=False):
        self.config = TrustPlatformSettings()
        self.logger = LogFacility()
        self.manager = PackageManager(processor=TpdsAppProcessing())
        self.prompt_for_no_updates = prompt_for_no_updates

        callbacks = {
            'stdout_callback': self.log_progress,
            'stderr_callback': self.log_errors,
        }

        self.worker = Worker(self.execute_fetch_versions, **callbacks)
        self.worker.signals.result.connect(self.result_fetch_versions)
        self.worker.signals.finished.connect(self.finish_fetch_versions)
        QThreadPool.globalInstance().start(self.worker)

    @Slot()
    def log_progress(self, buffer):
        self.logger.log(f'Processing {len(buffer)} bytes')

    @Slot()
    def log_errors(self, buffer):
        self.logger.log(buffer)

    @Slot()
    def execute_fetch_versions(self, **kwargs):
        self.logger.log('Check for Package updates started...')
        self.manager.refresh_package_list(**kwargs)
        return self.manager.get_upgradable()

    @Slot()
    def finish_fetch_versions(self):
        self.logger.log('Check for Package updates finished.')

    @Slot()
    def result_fetch_versions(self, packages_list):
        detailed_text = 'Updates available for the following packages:\n'

        for pkg in packages_list:
            self.logger.log(f'Update available for {pkg.name}')
            detailed_text += (
                f'\n{pkg.channel}::{pkg.name} ({pkg.installed})'
                f' --> {pkg.latest}'
            )

        if packages_list:
            message_box = UpdateMessageBox()
            message_box.setWindowTitle("Updates")
            message_box.setText(
                'Package updates are found. Would you like to update now?')
            message_box.setDetailedText(detailed_text)
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)
            message_box.setEscapeButton(QMessageBox.No)
            message_box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

            user_resp = message_box.exec_()
            if user_resp == QMessageBox.Yes:
                self.worker = Worker(self.execute_package_update, [p.name for p in packages_list])
                self.worker.signals.finished.connect(self.finish_package_update)
                QThreadPool.globalInstance().start(self.worker)
            elif user_resp == QMessageBox.No:
                self.logger.log('User event: Dont Update packages')
        else:
            msg = 'There are currently no updates available'
            self.logger.log(msg)
            if self.prompt_for_no_updates is True:
                message_box = QMessageBox()
                message_box.setWindowTitle("Updates")
                message_box.setText(msg)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.setDefaultButton(QMessageBox.Ok)
                message_box.setEscapeButton(QMessageBox.Ok)
                message_box.exec_()

    @Slot()
    def execute_package_update(self, packages):
        self.logger.log('User event: Update packages')
        self.manager.install(packages)

    @Slot()
    def finish_package_update(self):
        self.logger.log('User event: Completed updating packages')
        shutdown('A package was installed or updated - the application will need to be restarted', True)

def get_pkg_versions():
    return PackageManager(processor=TpdsAppProcessing()).get_installed()

__all__ = ['CheckUpdates', 'get_pkg_versions']

if __name__ == '__main__':
    pass
