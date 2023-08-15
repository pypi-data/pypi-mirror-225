# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'iosummary.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_IOSummary(object):
    def setupUi(self, IOSummary):
        if not IOSummary.objectName():
            IOSummary.setObjectName(u"IOSummary")
        IOSummary.resize(341, 177)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(IOSummary.sizePolicy().hasHeightForWidth())
        IOSummary.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(IOSummary)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_1 = QLabel(IOSummary)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_1)

        self.label_2 = QLabel(IOSummary)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(IOSummary)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.name_edit = QLineEdit(IOSummary)
        self.name_edit.setObjectName(u"name_edit")

        self.verticalLayout_4.addWidget(self.name_edit)

        self.dim_edit = QLineEdit(IOSummary)
        self.dim_edit.setObjectName(u"dim_edit")

        self.verticalLayout_4.addWidget(self.dim_edit)

        self.type_edit = QComboBox(IOSummary)
        self.type_edit.setObjectName(u"type_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.type_edit.sizePolicy().hasHeightForWidth())
        self.type_edit.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.type_edit)


        self.horizontalLayout.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(IOSummary)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(IOSummary)
        self.buttonBox.accepted.connect(IOSummary.accept)
        self.buttonBox.rejected.connect(IOSummary.reject)

        QMetaObject.connectSlotsByName(IOSummary)
    # setupUi

    def retranslateUi(self, IOSummary):
        IOSummary.setWindowTitle(QCoreApplication.translate("IOSummary", u"Dialog", None))
        self.label_1.setText(QCoreApplication.translate("IOSummary", u"Name:", None))
        self.label_2.setText(QCoreApplication.translate("IOSummary", u"Dim:", None))
        self.label_3.setText(QCoreApplication.translate("IOSummary", u"DataType", None))
    # retranslateUi

