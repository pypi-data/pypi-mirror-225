# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'datainspector.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

class Ui_DataInspector(object):
    def setupUi(self, DataInspector):
        if not DataInspector.objectName():
            DataInspector.setObjectName(u"DataInspector")
        DataInspector.resize(400, 300)
        self.verticalLayout = QVBoxLayout(DataInspector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(DataInspector)
        self.tabWidget.setObjectName(u"tabWidget")
        self.from_file = QWidget()
        self.from_file.setObjectName(u"from_file")
        self.verticalLayout_2 = QVBoxLayout(self.from_file)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.name_label = QLabel(self.from_file)
        self.name_label.setObjectName(u"name_label")

        self.verticalLayout_3.addWidget(self.name_label)

        self.label = QLabel(self.from_file)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.var_name = QLineEdit(self.from_file)
        self.var_name.setObjectName(u"var_name")

        self.verticalLayout_4.addWidget(self.var_name)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.path_edit = QLineEdit(self.from_file)
        self.path_edit.setObjectName(u"path_edit")

        self.horizontalLayout.addWidget(self.path_edit)

        self.file_btn = QToolButton(self.from_file)
        self.file_btn.setObjectName(u"file_btn")

        self.horizontalLayout.addWidget(self.file_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.load_btn = QPushButton(self.from_file)
        self.load_btn.setObjectName(u"load_btn")

        self.horizontalLayout_3.addWidget(self.load_btn)

        self.dump_to_btn = QPushButton(self.from_file)
        self.dump_to_btn.setObjectName(u"dump_to_btn")

        self.horizontalLayout_3.addWidget(self.dump_to_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.data_info = QLabel(self.from_file)
        self.data_info.setObjectName(u"data_info")

        self.verticalLayout_2.addWidget(self.data_info)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.from_file, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(DataInspector)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DataInspector)
        self.buttonBox.accepted.connect(DataInspector.accept)
        self.buttonBox.rejected.connect(DataInspector.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DataInspector)
    # setupUi

    def retranslateUi(self, DataInspector):
        DataInspector.setWindowTitle(QCoreApplication.translate("DataInspector", u"Dialog", None))
        self.name_label.setText(QCoreApplication.translate("DataInspector", u"Name:", None))
        self.label.setText(QCoreApplication.translate("DataInspector", u"Load Path:", None))
        self.file_btn.setText(QCoreApplication.translate("DataInspector", u"...", None))
        self.load_btn.setText(QCoreApplication.translate("DataInspector", u"Load", None))
        self.dump_to_btn.setText(QCoreApplication.translate("DataInspector", u"Dump to ...", None))
        self.data_info.setText(QCoreApplication.translate("DataInspector", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.from_file), QCoreApplication.translate("DataInspector", u"From File", None))
    # retranslateUi

