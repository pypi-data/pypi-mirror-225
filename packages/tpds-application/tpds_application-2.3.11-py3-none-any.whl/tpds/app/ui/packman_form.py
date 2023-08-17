# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'packman_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(701, 499)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.refresh_button = QPushButton(self.frame)
        self.refresh_button.setObjectName(u"refresh_button")
        self.horizontalLayout.addWidget(self.refresh_button)
        
        self.install_extn_button = QPushButton(self.frame)
        self.install_extn_button.setObjectName(u"install_extn_button")
        self.horizontalLayout.addWidget(self.install_extn_button)

        self.horizontalSpacer = QSpacerItem(268, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.login_info = QLabel(self.frame)
        self.login_info.setObjectName(u"login_info")
        self.login_info.setMinimumSize(QSize(180, 0))
        self.login_info.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.login_info)

        self.login_button = QPushButton(self.frame)
        self.login_button.setObjectName(u"login_button")

        self.horizontalLayout.addWidget(self.login_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(650, 400))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.installed_pkgs_table = QTableView(self.tab)
        self.installed_pkgs_table.setObjectName(u"installed_pkgs_table")

        self.verticalLayout_2.addWidget(self.installed_pkgs_table)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_4 = QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tpds_packages_table = QTableView(self.tab_2)
        self.tpds_packages_table.setObjectName(u"tpds_packages_table")

        self.verticalLayout_3.addWidget(self.tpds_packages_table)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.gridLayout_4.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.statusbar = QStatusBar(Form)
        self.statusbar.setObjectName(u"statusbar")

        self.gridLayout_3.addWidget(self.statusbar, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Package Manager", None))
        self.refresh_button.setText(QCoreApplication.translate("Form", u"Refresh", None))
        self.login_info.setText(QCoreApplication.translate("Form", u"", None))
        self.login_button.setText(QCoreApplication.translate("Form", u"Login", None))
        self.install_extn_button.setText(QCoreApplication.translate("Form", u"Install TPDS Extension", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Installed Packages", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"TPDS Packages", None))
    # retranslateUi
