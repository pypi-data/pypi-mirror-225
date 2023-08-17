import os
import sys
from packaging.version import Version
from tpds.package_manager.pip_client import PipPackageClient
from tpds.settings import TrustPlatformSettings


def print_banner(message: str) -> None:
    print("\n-----------------------------------------------------------------------------")
    print("\n".join([l.strip() for l in message.split("\n")]))
    print("-----------------------------------------------------------------------------\n")


def check_and_update_core_packages():
    core_packages = {
        "PySide6": "6.5.0",
        "pip": True,
        "azure-iot-hub": False,
        "azure-identity": False,
        "azure-mgmt-iothub": False,
        "azure-iot-device": False,
        "azure-iothub-provisioningserviceclient": False,
        "azure-mgmt-iothubprovisioningservices": False,
        "azure-mgmt-resource": False,
    }
    updates = {}
    manager = PipPackageClient(core_packages, index=TrustPlatformSettings().settings.pip_index, preview=False)
    # Updating the remote first only pulls information for the above packages rather
    # than all installed tpds packages which will be updated later
    manager.update_remote()
    manager.update_local()

    for name, version in core_packages.items():
        installed = manager._installed.get(name, manager._installed.get(name.lower(), None))
        available = manager._available.get(name, manager._available.get(name.lower(), None))
        if installed:
            if isinstance(version, str):
                if installed.installed < Version(version):
                    updates[name] = (installed.installed, available.latest if available else version)
            elif available and version:
                if installed.installed < available.latest:
                    updates[name] = (installed.installed, available.latest)
        else:
            updates[name] = ("", available.latest)

    if updates:
        if sys.platform == 'darwin':
            # Force the install on mac because tpds doesn't have a console window to accept input
            pass
        else:
            # Prompt for install because we don't know if this is a safe environment to update
            print_banner(
                """
                In order to properly run TPDS some packages need to be updated
                Not updating the environment may result in unexpected behavior
                """
            )
            print("\nPackage(s) that will be updated:")
            for k,(i,l) in updates.items():
                print(f"{k}: {i} -> {l}")
            print("\n")
            response = input("Install these updates (Y/y) or continue (C/c)? ")
            if response in ["C", "c"]:
                # Continue executing the application with no updates
                updates = None
            elif response not in ["Y", "y"]:
                print_banner("Exiting without performing any updates")
                sys.exit(-1)
   

    if updates:
        manager.upgrade([x.lower() for x in updates.keys()])

        if sys.argv[0].endswith(".py"):
            entrypoint = sys.executable
            args = sys.argv
        else:
            entrypoint = sys.argv[0]
            args = sys.argv[1:]

        os.execl(entrypoint, entrypoint, *args)


def launch_app():
    from PySide6.QtCore import QDir, QLockFile
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtGui import QIcon

    from .app import TPDSApplication
    from .control import shutdown

    def run_app():
        # Configuration system
        # A default configuraiton is built here.
        # Upon start, the user is prompted with a Settings window to override
        # and complete the data set.
        # it is then saved into $HOME/.trustplatform/TPDS_config.json
        config = TrustPlatformSettings()

        if os.getenv('CONDA_PREFIX') is not None:
            # Find and add conda path
            config.settings.conda_path = os.getenv('CONDA_PREFIX')
            # Find and add tpds_core path
    #        config.settings.local_path = os.path.join(os.getenv(
    #                                            'CONDA_PREFIX'), 'tpds_core')
        # Define a default log file if there is none
        config.settings.log_file = os.path.join(
            QDir.homePath(),
            '.trustplatform',
            'trustplatform.log')
        # Write the above default configuration locally
        config.save()

        # Mainl
        if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
            # This silences the warning locally in ubuntu and seems to resolve some issues
            os.environ['XDG_SESSION_TYPE'] = 'xcb'
            # This uses the qtwayland5 wayland extension which improve performance in wayland based
            # environments - it still throws the warning however
    #        os.environ['QT_QPA_PLATFORM'] = 'wayland'

        if sys.platform == 'darwin':
            os.environ['QT_MAC_WANTS_LAYER'] = '1'
            import site
            sitePackagesPath = site.getsitepackages()
            if len(sitePackagesPath) == 1:
                os.environ['DYLD_LIBRARY_PATH'] = os.path.join(sitePackagesPath[0], 'libusb_package')

        # Clean up old instances if they exist
        if QApplication.instance():
            shutdown()

        # Start the Qt application
        _app = TPDSApplication()
        sys.exit(_app.exec_())

    try:
        lock_file = QLockFile(QDir.tempPath() + '/tpds.lock')
        if lock_file.tryLock():
            run_app()
        else:
            exit_app = QApplication(sys.argv)
            config = TrustPlatformSettings()
            # Add application icon
            icon_path = os.path.join(
                os.path.dirname(__file__), 'assets', 'app.ico')
            exit_app.setWindowIcon(QIcon(icon_path))
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Information)
            error_message.setWindowTitle('Duplicate')
            error_message.setText((
                '''<font color=#0000ff><b>Application is already running</b></font><br>
                <br>Only one instance is allowed. Click OK to close this<br>'''))
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec()
    finally:
        lock_file.unlock()


def tpds_app_launch():
    print_banner("This prompt runs Trust Platform GUI, Do NOT close this window.")

    # Check if the QT environment is correct
    check_and_update_core_packages()

    # Then we can launch the app
    launch_app()


if __name__ == '__main__':
    tpds_app_launch()
