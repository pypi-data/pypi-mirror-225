
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox

from tpds.settings.tpds_settings import reset_runtime_settings
from .vars import get_app_ref
from tpds.helper import log


@Slot()
def shutdown(message: str = 'Do you want to exit?', force: bool = False):
    app_ref = get_app_ref()
    if app_ref._view is not None:
        if force:
            reply = QMessageBox.critical(
                app_ref._view,
                'Exit',
                message,
                QMessageBox.Ok,
                QMessageBox.Ok
            )
        else:
            reply = QMessageBox.question(
                app_ref._view,
                'Exit',
                message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)

        if reply in (QMessageBox.Yes, QMessageBox.Ok):
            log('shutdown')
            reset_runtime_settings()
            app_ref.stop_backend()
            log('quitting')
            app_ref.quit()
    else:
        return False
