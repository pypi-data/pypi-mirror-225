import os
import sys
import requests
import webbrowser

from PySide6.QtCore import Slot, QSettings, QTimer, QUrl, Qt, QFileInfo, QDir
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QInputDialog)
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings, QWebEngineProfile, QWebEngineDownloadRequest

from urllib import parse
from bs4 import BeautifulSoup
from datetime import datetime

from tpds.helper import LogFacility, log, make_dir
from tpds.settings import TrustPlatformSettings
from tpds.update import get_pkg_versions, CheckUpdates
from tpds.package_manager import PackageManager

from .ui import SettingsDialog, PackageManagerUi
from .control import shutdown
from .docks import LoggerDock
from .tools import WebViewStacked
from .network import NetworkTools
from .vars import get_app_ref, get_url_base, SETTING_GEOMETRY


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QWebEnginePage.__init__(self, *args, **kwargs)
        self.profile().setHttpCacheType(QWebEngineProfile.NoCache)
        self.profile().downloadRequested.connect(self.on_downloadRequested)

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        log(
            f'''JS:{sourceID} Line#{line}: '''
            f'''{msg.encode('ascii', 'ignore')}''')

    @Slot(QWebEngineDownloadRequest)
    def on_downloadRequested(self, download):
        directory = os.path.join(
            str(QDir.homePath()),
            'Downloads',
            'TPDS_Downloads')
        make_dir(directory)
        filename = \
            QFileInfo(download.downloadFileName()).baseName() + \
            '_' + datetime.now().strftime("%m%d%H%M%S") + \
            '.' + QFileInfo(download.downloadFileName()).suffix()
        full_path = os.path.join(directory, filename)
        download.setDownloadFileName(full_path)
        download.accept()


class CustomWebView(QWebEngineView):
    def __init__(self, mainwindow, main=False, notebook=False):
        super(CustomWebView, self).__init__(None)
        self._log = LogFacility()
        self.parent = mainwindow
        self.tabIndex = -1
        self.main = main
        self._notebook = notebook
        self.setPage(WebEnginePage(self))
        self.loadedPage = None
        self.urlChanged.connect(self._handle_url_change)
        self.loadStarted.connect(self.loadingpage)
        self.loadFinished.connect(self.onpagechange)
        self._web_address = ''
        self.settings().setAttribute(
            QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(
            QWebEngineSettings.PdfViewerEnabled, True)

    @property
    def notebook(self):
        return self._notebook

    def set_jupyter_address(self, web_address):
        self._web_address = web_address

    def getPageTitle(self, url):
        reqs = requests.get(url)
        parse = BeautifulSoup(reqs.text, 'html.parser')
        title_list = parse.find_all('title')
        filename = self.url().fileName()
        if len(title_list):
            filename = title_list[0].get_text()
        return filename

    def checkInstance(self, name):
        for i in range(self.parent.viewstack.count()):
            window = self.parent.viewstack.widget(i)
            tab = window.url().toString()
            if tab.startswith('http'):
                filename = self.getPageTitle(tab)
            else:
                filename = window.url().fileName()
            if filename == name:
                self.parent.viewstack.activateWebView(
                    self.parent.viewstack.wpage.index(window), False)
                return True
        return False

    @Slot()
    def loadingpage(self):
        if get_app_ref().backend._config.settings.develop:
            # Dont load voila page from Notebook window
            for js in get_app_ref().backend._voila:
                nb_voila = f'{js._web_address}voila'
                if nb_voila in self.url().toString():
                    QTimer.singleShot(0, self.close)

        if self.url().fileName().find('ipynb') > 0:
            is_notebook = True
        else:
            is_notebook = False

        if is_notebook and not self.notebook:
            QTimer.singleShot(0, self.close)
            return

    @Slot(bool)
    def onpagechange(self, ok):
        self._log.log(
            f'onpagechange {self.url().toString()}, {self.url().host()}')
        if self.url().fileName().find('ipynb') > 0:
            is_notebook = True
        else:
            is_notebook = False

        view_title = self.title()
        if view_title is None:
            view_title, _ = os.path.splitext(self.url().fileName())

        if is_notebook:
            self.parent.viewstack.updateView(
                view_title,
                self.parent.viewstack.npage.index(self),
                is_notebook)
        else:
            self.parent.viewstack.updateView(
                view_title,
                self.parent.viewstack.wpage.index(self),
                is_notebook)

        if self.url().hasQuery() is True:
            if self.loadedPage is not None:
                self._log.log("disconnecting on close and link clicked signal")
                self.loadedPage.windowCloseRequested.disconnect(self.close)
            self.loadedPage = self.page()
            self.loadedPage.windowCloseRequested.connect(self.close)
            self.setWindowTitle(self.title())
            if not self.main:
                pass
            if not ok:
                QMessageBox.information(
                    self,
                    "Error",
                    "Error loading page!",
                    QMessageBox.Ok)

        for i in range(self.parent.viewstack.count()):
            window = self.parent.viewstack.widget(i)
            if (self == window):
                break
            elif (window.url().fileName() == self.url().fileName()):
                if self.parent.viewstack.ordPages[window]:
                    self.parent.viewstack.removeWebView(
                        self.parent.viewstack.npage.index(self), True)
                    self.parent.viewstack.activateWebView(
                        self.parent.viewstack.npage.index(window), True)
                else:
                    self._log.log(
                        f'{repr(self.parent.viewstack.wpage)} - {repr(self)}')
                    self.parent.viewstack.removeWebView(
                        self.parent.viewstack.wpage.index(self), False)
                    self.parent.viewstack.activateWebView(
                        self.parent.viewstack.wpage.index(window), False)
                QTimer.singleShot(0, self.close)
                break

    @Slot(QUrl)
    def _handle_url_change(self, url: QUrl):
        if url.scheme() != 'file':
            host = url.host()
            if host.lower() not in ['127.0.0.1', 'localhost']:
                try:
                    webbrowser.open(self.url().toString(), new=2)
                    QTimer.singleShot(0, self.close)
                except Exception as e:
                    self._log.log(str(e))

    @Slot(QUrl)
    def handlelink(self, url: QUrl):
        urlstr = url.toString()
        self._log.log("handling link : %s" % urlstr)
        # check if url is for the current page
        if url.hasQuery() is True:
            parsed_url = parse.urlparse(urlstr)
            query = parse.parse_qs(parsed_url.query)
            self._log.log('handlelink - quer: %s' % query)
        if url.matches(self.url(),
                       QUrl.FormattingOptions(QUrl.RemoveFragment)):
            # do nothing, probably a JS link
            return True
        # check other windows to see if url is loaded there
        for i in range(self.parent.viewstack.count()):
            window = self.parent.viewstack.widget(i)
            if url.matches(window.url(),
                           QUrl.FormattingOptions(QUrl.RemoveFragment)):
                # self.parent.viewstack.setCurrentIndex(i)
                # if this is a tree window and not the main one, close it
                if self.url().toString().startswith(
                    self.parent.homepage.toString() + "tree") and \
                        not self.main:
                    QTimer.singleShot(0, self.close)  # don't call self.close()
                return True

        if "/files/" in urlstr:
            # save, don't load new page
            self.parent.savefile(url)
        elif "/tree/" in urlstr or urlstr.startswith(
                self.parent.homepage.toString() + "tree"):
            # keep in same window
            self.load(url)
        elif "https" in urlstr:
            newwindow = self.parent.createBrowserTab(
                QWebEnginePage.WebBrowserWindow,
                js=False, notebook=False)
            newwindow.load(url)
        elif ".html" in urlstr:
            newwindow = self.parent.createBrowserTab(
                QWebEnginePage.WebBrowserWindow,
                js=False, notebook=False)
            newwindow.load(url)
        else:
            # open in new window
            # the link is a notebook
            newwindow = self.parent.createBrowserTab(
                QWebEnginePage.WebBrowserWindow,
                js=False, notebook=True)
            newwindow.load(url)
        # if this is a tree window and not the main one, close it

        if self.url().toString().startswith(
                self.parent.homepage.toString() + "/tree") and not self.main:
            QTimer.singleShot(0, self.close)  # calling self.close() is no good
        return True

    def createWindow(self, windowtype):
        return self.parent.createBrowserTab(windowtype, js=True)

    def closeEvent(self, event):
        if self.loadedPage is not None:
            # helper.log("disconnecting on close and linkClicked signals")
            self.loadedPage.windowCloseRequested.disconnect(self.close)

        if not self.main:
            if self in self.parent.windows:
                if self.parent.viewstack.ordPages[self]:
                    self.parent.viewstack.removeWebView(
                        self.parent.viewstack.npage.index(self), True)
                else:
                    self.parent.viewstack.removeWebView(
                        self.parent.viewstack.wpage.index(self), False)
                self.parent.viewstack.removeWebView(
                    self.parent.viewstack.indexOf(self))
                self.parent.windows.remove(self)
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self, parent=None, homepage=None, log_view=True):
        super(MainWindow, self).__init__(parent)
        self._log = LogFacility()
        self.homepage = homepage
        self.windows = []
        if log_view is True:
            self.loggerdock = LoggerDock("Log Message", self)
            self.addDockWidget(Qt.BottomDockWidgetArea, self.loggerdock)
        self.viewstack = WebViewStacked(self)
        self.settings = QSettings()
        self.network = NetworkTools()
        """ Check whether the TPDS application has valid settings
        If not prompt for fixing them.
        By the time we get here, settings must have been created and checked.
        If they are still missing, bail out..
        """
        try:
            self.tpds_settings_root = TrustPlatformSettings()
            self.tpds_settings = self.tpds_settings_root.settings
        except FileNotFoundError:
            # TODO: copy a default file into the $HOME/.trustplatform folder
            # and retry
            QMessageBox.critical(
                self,
                "Settings",
                "Configuration file missing. Please re-install the software\n")
            sys.exit()

        val = self.settings.value(SETTING_GEOMETRY, None)
        if val is not None:
            self.restoreGeometry(val)
        self.initUI()

    def initUI(self):
        self.basewebview = CustomWebView(self, main=True)
        self.windows.append(self.basewebview)
        self.setCentralWidget(self.viewstack)
        self.viewstack.addWebView(
            "Home",
            self.basewebview,
            False)
        self._web_address = ''

        # Status Bar
        self.statusbar = self.statusBar()

        # Menu Bar
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # Add File menu entry
        self.file_menu = self.menubar.addMenu("&File")
        # Add Preferences menu entry to File
        self.settings_action = QAction('&Preferences', self)
        self.settings_action.setShortcut('Ctrl+P')
        self.settings_action.triggered.connect(self.open_settings)
        self.file_menu.addAction(self.settings_action)
        # Add Quit menu entry into File
        self.exit_action = QAction('&Quit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(shutdown)
        self.file_menu.addAction(self.exit_action)

        # Add Packages menu entry
        self.packages_menu = self.menubar.addMenu("&Packages")
        # Add Check for Updates menu entry into Help
        self.package_manager = QAction('&Package Manager', self)
        self.packages_menu.addAction(self.package_manager)
        self.package_manager.triggered.connect(self.package_manager_action)
        # Add Check for Updates menu entry into Help
        self.check_updates = QAction('&Check for Updates...', self)
        self.packages_menu.addAction(self.check_updates)
        self.check_updates.triggered.connect(self.check_updates_action)

        # Add Help menu entry
        self.help_menu = self.menubar.addMenu("&Help")
        # Add help documentation though markdown docs
        self.help_doc = QAction('&Documentation', self)
        self.help_menu.addAction(self.help_doc)
        self.help_doc.triggered.connect(self.process_documentation)
        # Add api documentation
        if self.tpds_settings.develop:
            self.api_doc = QAction('&API Documentation', self)
            self.help_menu.addAction(self.api_doc)
            self.api_doc.triggered.connect(self.process_api_docs)
        # Add Release Notes
        self.release_notes = QAction('&Release Notes', self)
        self.help_menu.addAction(self.release_notes)
        self.release_notes.triggered.connect(self.open_release_notes)
        # Add Report Issue
        self.report_issue = QAction('&Report Issue', self)
        self.help_menu.addAction(self.report_issue)
        self.report_issue.triggered.connect(self.process_report_issue)
        # Add view license
        self.view_license = QAction('&View License', self)
        self.help_menu.addAction(self.view_license)
        self.view_license.triggered.connect(self.process_view_license)
        # Add About menu entry into Help
        self.about = QAction('&About', self)
        self.help_menu.addAction(self.about)
        self.about.triggered.connect(self.about_action)

        self.statusbar = self.statusBar()
        self.show()

    def open_settings(self):
        self._log.log('open settings dialog')
        self.settings_dlg = SettingsDialog(
            TrustPlatformSettings())
        self.settings_dlg.exec()

    def set_jupyter_address(self, web_address):
        self._web_address = web_address
        self.basewebview.set_jupyter_address(web_address)

    def loadmain(self, homepage):
        self.homepage = homepage
        QTimer.singleShot(0, self.initialload)

    def createBrowserTab(self, windowtype, js=True, notebook=False):
        v = CustomWebView(self, notebook=notebook)
        v.set_jupyter_address(v.url().fileName())
        self.windows.append(v)
        self.viewstack.addWebView(
            v.url().fileName(), v, notebook)
        return v

    def open_release_notes(self):
        newwindow = self.createBrowserTab(
            QWebEnginePage.WebBrowserWindow,
            js=False, notebook=False)
        newwindow.setUrl(QUrl(f'{get_url_base()}/ReleaseNotes.html'))

    def about_action(self):
        self._log.log('Open About dialog')
        pkg_versions = get_pkg_versions()
        version_info = (
            '''<font color=#0000ff><b>Trust Platform Design Suite</b></font><br>
            <br>Package versions:<br>'''
        )
        msg_box = QMessageBox()
        if pkg_versions:
            for package in pkg_versions:
                version_info += (
                    f'''&emsp;{package.name}'''
                    f'''({package.channel}): '''
                    f'''<b>{package.installed}</b><br>''')
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(version_info)
        else:
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText(
                'Fetching version details... Try after few seconds!')
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowTitle('About - Trust Platform Design Suite')
        msg_box.exec_()

    def check_updates_action(self):
        self._log.log('Open Check for Updates dialog')
        self.network.network_check_thread(self.check_updates_routine)

    def check_updates_routine(self, internet_available):
        if internet_available:
            CheckUpdates(prompt_for_no_updates=True)
        else:
            nw_message = QMessageBox()
            nw_message.setIcon(QMessageBox.Warning)
            nw_message.setWindowTitle('Network')
            nw_message.setText((
                '''<font color=#0000ff><b>Internet connection is down</b></font><br>
                <br>Check connection and try again<br>'''
            ))
            nw_message.setStandardButtons(QMessageBox.Ok)
            nw_message.exec()

    def package_manager_action(self):
        self.pkg_manager_ui = PackageManagerUi()
        self.pkg_manager_ui.show()

    def process_documentation(self):
        newwindow = self.createBrowserTab(
            QWebEnginePage.WebBrowserWindow,
            js=False, notebook=False)
        newwindow.setUrl(QUrl(f'{get_url_base()}/Documentation.html'))

    def process_api_docs(self):
        newwindow = self.createBrowserTab(
            QWebEnginePage.WebBrowserWindow,
            js=True, notebook=False)
        newwindow.setUrl(QUrl(f'{get_url_base()}/docs'))

    def process_report_issue(self):
        pkg_versions = get_pkg_versions()
        if pkg_versions:
            items = ['Bug Report', 'Feature Request']
            label_description = (
                '''<font color=#0000ff><b>Report Issue on GItHub TPDS Issue Tracker</b></font><br>
                <br>Select report type and Click OK to report issue.
                <br><br>GitHub TPDS Issue Tracker requires User to Signin to GitHub account.
                <br>If GitHub account is unavailable, Click on 'Create an account' in next step and follow instructions. <br>''')
            item, ok = QInputDialog.getItem(
                None, 'Report Issue', label_description,
                items, 0, False)
            version_info = ''
            for package in pkg_versions:
                version_info += f'#### {package.name}: {package.installed}\n'

            if ok and item:
                github_link = (
                    'https://github.com/Microchip-TrustPlatformDesignSuite/'
                    'TPDS-Issue-Tracker/issues/new?')
                custom_info = {
                    'body': (
                        f'''Issue Type: <b>{item}</b>\n'''
                        f'''{version_info}\n\n'''
                        f'''<!-- Add Issue description below -->\n'''
                    )}
                custom_link = parse.urlencode(custom_info)
                newwindow = self.createBrowserTab(
                    QWebEnginePage.WebBrowserWindow,
                    js=False, notebook=False)
                newwindow.setUrl(QUrl(f'{github_link}{custom_link}'))
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setWindowTitle('Report Issue')
            msg_box.setText(
                'Fetching version details... Try after few seconds!')
            msg_box.exec_()

    def process_view_license(self):
        import tpds
        render_path = os.path.join(tpds.__path__[0], 'licenses.txt')
        newwindow = self.createBrowserTab(
            QWebEnginePage.WebBrowserWindow,
            js=False, notebook=False)
        newwindow.setUrl(QUrl('file:///'+render_path.replace("\\", "/")))

    @Slot(int)
    def destroyBrowserTab(self, which):
        closeevent = QCloseEvent()
        win = self.tabs.widget(which)
        if win.main:
            self.close()
        else:
            win.closeEvent(closeevent)
            if closeevent.isAccepted():
                self.tabs.removeTab(which)

    @Slot()
    def initialload(self):
        if self.homepage:
            self.basewebview.load(QUrl(self.homepage))
        self.show()

    def savefile(self, url):
        pass

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue(SETTING_GEOMETRY, self.saveGeometry())
        pending_processes = 0
        try:
            process_manager = PackageManager().get_proc()
            pending_processes = len(process_manager.get_processes())
        except Exception:
            pass
        if pending_processes == 0:
            if len(self.windows) >= 1:
                if not shutdown():
                    event.ignore()
                    return
            else:
                event.accept()
        else:
            msg = QMessageBox(QMessageBox.Warning, "Package Manager",
                              "Please wait for package updates to be completed.",
                              QMessageBox.Ok)
            msg.exec()
            event.ignore()
