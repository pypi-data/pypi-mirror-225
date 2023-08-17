import os
from PySide6.QtWidgets import (
    QStackedWidget, QDockWidget, QPushButton, QWidget, QGridLayout,
    QGroupBox, QVBoxLayout, QButtonGroup, QToolButton)
from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtGui import QIcon
from collections import OrderedDict

from tpds.helper import log
from .control import shutdown
from .vars import get_app_ref


class WebViewStacked(QStackedWidget):
    def __init__(self, parent):
        super(WebViewStacked, self).__init__(parent)
        self.main_window = parent

        # Tool palette located in the left docking area
        self.tooldock = QDockWidget('Tools', parent)
        self.tooldock.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.main_window.addDockWidget(Qt.LeftDockWidgetArea, self.tooldock)

        # Top Tools widget
        self.tools = QWidget()
        self.tools_layout = QVBoxLayout()
        self.tools.setLayout(self.tools_layout)
        self.tooldock.setWidget(self.tools)  # add the top tools to the dock

        # Build the grid organizing the child widgets within viewbutton
        self.webviews_widgets = ViewButtons(
            'Webviews', self.main_window, self)
        self.tools_layout.addWidget(self.webviews_widgets)

        # Create the main widget containing all the notebook view buttons
        self.notebook_widgets = ViewButtons(
            'Usecases', self.main_window, self)
        self.tools_layout.addWidget(self.notebook_widgets)
        self.ordPages = OrderedDict()   # To maintain all the wigets
        self.wpage = list()  # webpages widgets
        self.npage = list()  # notebook widgets

    def addWebView(self, title, webview, notebook=False):
        self.addWidget(webview)  # get the webview tab index

        # Add the control widgets to the tool palette.
        self.ordPages.update({webview: notebook})

        if notebook:
            self.npage.append(webview)
            dev_mode = True if get_app_ref().backend._config.settings.develop else False
            self.notebook_widgets.add_view_controls(
                                        title, self.npage.index(webview),
                                        develop=dev_mode, new_target=False,
                                        nb=notebook)
            self.notebook_widgets.check_button(self.npage.index(webview))
        else:
            self.wpage.append(webview)
            self.webviews_widgets.add_view_controls(
                                        title, self.wpage.index(webview))
            self.activateWebView(self.wpage.index(webview), False)

    def updateView(self, title, index, notebook):
        updated_index = index
        if notebook:
            self.notebook_widgets.update_view_controls(title, updated_index)
        else:
            self.webviews_widgets.update_view_controls(title, updated_index)

    def removeWebView(self, index, notebook=None):
        if notebook:
            webview = self.npage[index]
            resp = self.ordPages.pop(webview, None)
            self.npage.remove(webview)
            if resp is not None:
                self.notebook_widgets.remove_view_controls(index)
                webview.deleteLater()
        elif index > 0 and index < len(self.wpage):
            webview = self.wpage[index]
            resp = self.ordPages.pop(webview, None)
            self.wpage.remove(webview)
            if resp is not None:
                self.webviews_widgets.remove_view_controls(index)
                webview.deleteLater()
        elif len(self.wpage) == 0:
            shutdown()

    def activateWebView(self, index, notebook):
        if notebook:
            resp = self.npage[index]
            self.notebook_widgets.check_button(index)
        else:
            resp = self.wpage[index]
            self.webviews_widgets.check_button(index)
        self.setCurrentWidget(resp)

    def windows(self):
        return len(self.pages)

    def changeDevelopView(self, index, nb):
        # This is applicable only for Notebooks
        if get_app_ref().backend._config.settings.develop:
            nb.setText('Loading...')
            webview = self.npage[index]
            nb_url = webview.url().toString()
            log(f'{nb_url}')
            for jupyter_inst in get_app_ref().backend._voila:
                if jupyter_inst._web_address in nb_url:
                    if 'voila/render' in nb_url:
                        nb_path = "/".join(nb_url.strip("/").split('/')[5:])
                        nb_url = (
                            f'{jupyter_inst._web_address}'
                            f'notebooks/{nb_path}'
                        )
                    else:
                        nb_path = "/".join(nb_url.strip("/").split('/')[4:])
                        nb_url = (
                            f'{jupyter_inst._web_address}'
                            f'voila/render/{nb_path}'
                        )
                    webview.page().setUrl(QUrl(nb_url))


class ViewButtons(QGroupBox):
    def __init__(self, title, parent, stacked_widget):
        super(ViewButtons, self).__init__(title, parent)
        self.stacked_widget = stacked_widget
        self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 1)
        self.setCheckable(False)
        self.gb = QButtonGroup(self)
        self.controls = dict()
        self.tabControl = list()
        self.notebook: bool = False

    def update_view_controls(self, title, index):
        resp = self.tabControl[index]
        if resp is not None:
            (btn, quit_btn, dev_btn) = resp
            btn.setText(title[0:40])
            log(title)
            btn.setToolTip(title)

    def add_view_controls(
                        self, title, index, develop=False,
                        new_target=True, nb=False):
        self.notebook = nb
        row = len(self.tabControl)
        while self.grid.itemAtPosition(row, 0) is not None:
            row += 1
        new_quit_btn = QToolButton()
        close_path = os.path.join(os.path.dirname(__file__),
                    'assets', 'icons8-close_window.png')
        develop_btn = None
        if develop:
            develop_path = os.path.join(os.path.dirname(__file__),
                        'assets', 'icons8-dev.png')
            develop_btn = QToolButton()
            develop_btn.setCheckable(True)
            develop_btn.setChecked(True)
            develop_btn.setIcon(QIcon(develop_path))
            develop_btn.setToolTip('Toggle View')
            self.grid.addWidget(develop_btn, row, 2)
        new_quit_btn.setIcon(QIcon(close_path))
        new_quit_btn.setToolTip('Close View')
        new_btn = QPushButton(title, parent=self)
        new_btn.setCheckable(True)
        new_btn.setStyleSheet("QPushButton { text-align: left; }")
        new_btn.setText('Loading...')
        if(new_target):
            new_btn.setChecked(True)
        self.gb.addButton(new_btn)
        self.grid.addWidget(new_quit_btn, row, 0)
        self.grid.addWidget(new_btn, row, 1, 1, 1, Qt.AlignLeft)
        self.grid.setRowStretch(row, 0)
        self.grid.setRowStretch(row+1, 2)
        self.tabControl.append((new_btn, new_quit_btn, develop_btn))
        new_btn.clicked.connect(self.handle_selection)
        new_quit_btn.clicked.connect(self.handle_remove)
        if develop:
            develop_btn.clicked.connect(self.handle_dev_view)

    def _find_index(self, obj) -> int:
        for i, o in enumerate(self.tabControl):
            if obj in o:
                return i

    @Slot()
    def handle_selection(self):
        self.stacked_widget.activateWebView(self._find_index(self.sender()), self.notebook)

    @Slot()
    def handle_remove(self):
        self.stacked_widget.removeWebView(self._find_index(self.sender()), self.notebook)

    @Slot()
    def handle_dev_view(self):
        idx = self._find_index(self.sender())
        self.stacked_widget.changeDevelopView(idx, self.tabControl[idx][0])


    def remove_view_controls(self, index):
        resp1 = self.tabControl[index]
        self.tabControl.pop(index)
        if resp1 is not None:
            (btn_to_remove, quit_btn_to_remove, develop_btn) = resp1
            self.grid.removeWidget(btn_to_remove)
            self.grid.removeWidget(quit_btn_to_remove)
            self.grid.removeWidget(develop_btn)
            self.grid.setRowStretch(index, 0)
            self.gb.removeButton(btn_to_remove)
            btn_to_remove.deleteLater()
            quit_btn_to_remove.deleteLater()
            if develop_btn:
                develop_btn.deleteLater()
            try:
                active_btn = self.tabControl[
                    self.stacked_widget.currentIndex()]
                active_btn.click()
                btn_to_remove.disconnect()
                quit_btn_to_remove.disconnect()
            except Exception:
                # will complain with the button was not connected
                pass  # Just ignore it

    def check_button(self, index):
        (new_btn, new_quit_btn, develop_btn) = self.tabControl[index]
        new_btn.setChecked(True)
