from PySide6.QtWidgets import QDockWidget, QPlainTextEdit
from PySide6.QtCore import Slot


class LoggerDock(QDockWidget):

    def __init__(self, *args):
        super(LoggerDock, self).__init__(*args)
        self.textview = QPlainTextEdit(self)
        self.textview.setReadOnly(True)
        self.setWidget(self.textview)

    @Slot()
    def log(self, message):
        self.textview.appendPlainText(message)
