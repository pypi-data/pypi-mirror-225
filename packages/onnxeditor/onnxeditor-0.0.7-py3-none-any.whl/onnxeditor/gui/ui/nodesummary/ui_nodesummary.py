# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nodesummary.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_NodeSummary(object):
    def setupUi(self, NodeSummary):
        if not NodeSummary.objectName():
            NodeSummary.setObjectName(u"NodeSummary")
        NodeSummary.resize(400, 300)
        self.verticalLayout = QVBoxLayout(NodeSummary)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.name_label = QLabel(NodeSummary)
        self.name_label.setObjectName(u"name_label")

        self.horizontalLayout.addWidget(self.name_label)

        self.name_edit = QLineEdit(NodeSummary)
        self.name_edit.setObjectName(u"name_edit")

        self.horizontalLayout.addWidget(self.name_edit)

        self.line = QFrame(NodeSummary)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.op_type_label = QLabel(NodeSummary)
        self.op_type_label.setObjectName(u"op_type_label")

        self.horizontalLayout.addWidget(self.op_type_label)

        self.op_type_edit = QLineEdit(NodeSummary)
        self.op_type_edit.setObjectName(u"op_type_edit")

        self.horizontalLayout.addWidget(self.op_type_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(NodeSummary)
        self.tabWidget.setObjectName(u"tabWidget")
        self.inputs_tab = QWidget()
        self.inputs_tab.setObjectName(u"inputs_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.inputs_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.inputs_list_widget = QListWidget(self.inputs_tab)
        self.inputs_list_widget.setObjectName(u"inputs_list_widget")
        self.inputs_list_widget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.inputs_list_widget.setDragEnabled(True)
        self.inputs_list_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.inputs_list_widget.setDefaultDropAction(Qt.MoveAction)
        self.inputs_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.horizontalLayout_2.addWidget(self.inputs_list_widget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.inputs_add = QPushButton(self.inputs_tab)
        self.inputs_add.setObjectName(u"inputs_add")

        self.verticalLayout_2.addWidget(self.inputs_add)

        self.inputs_del = QPushButton(self.inputs_tab)
        self.inputs_del.setObjectName(u"inputs_del")

        self.verticalLayout_2.addWidget(self.inputs_del)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.inputs_tab, "")
        self.output_tab = QWidget()
        self.output_tab.setObjectName(u"output_tab")
        self.horizontalLayout_3 = QHBoxLayout(self.output_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.outputs_list_widget = QListWidget(self.output_tab)
        self.outputs_list_widget.setObjectName(u"outputs_list_widget")
        self.outputs_list_widget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.outputs_list_widget.setDragEnabled(True)
        self.outputs_list_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.outputs_list_widget.setDefaultDropAction(Qt.MoveAction)
        self.outputs_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.horizontalLayout_3.addWidget(self.outputs_list_widget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.outputs_add = QPushButton(self.output_tab)
        self.outputs_add.setObjectName(u"outputs_add")

        self.verticalLayout_3.addWidget(self.outputs_add)

        self.outputs_del = QPushButton(self.output_tab)
        self.outputs_del.setObjectName(u"outputs_del")

        self.verticalLayout_3.addWidget(self.outputs_del)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.output_tab, "")
        self.attr_tab = QWidget()
        self.attr_tab.setObjectName(u"attr_tab")
        self.horizontalLayout_4 = QHBoxLayout(self.attr_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.attr_tabel_widget = QTableWidget(self.attr_tab)
        self.attr_tabel_widget.setObjectName(u"attr_tabel_widget")
        self.attr_tabel_widget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.attr_tabel_widget.setColumnCount(0)
        self.attr_tabel_widget.horizontalHeader().setVisible(True)
        self.attr_tabel_widget.horizontalHeader().setCascadingSectionResizes(False)

        self.horizontalLayout_4.addWidget(self.attr_tabel_widget)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.attr_add = QPushButton(self.attr_tab)
        self.attr_add.setObjectName(u"attr_add")

        self.verticalLayout_4.addWidget(self.attr_add)

        self.attr_del = QPushButton(self.attr_tab)
        self.attr_del.setObjectName(u"attr_del")

        self.verticalLayout_4.addWidget(self.attr_del)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.attr_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(NodeSummary)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NodeSummary)
        self.buttonBox.accepted.connect(NodeSummary.accept)
        self.buttonBox.rejected.connect(NodeSummary.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(NodeSummary)
    # setupUi

    def retranslateUi(self, NodeSummary):
        NodeSummary.setWindowTitle(QCoreApplication.translate("NodeSummary", u"Dialog", None))
        self.name_label.setText(QCoreApplication.translate("NodeSummary", u"Name:", None))
        self.op_type_label.setText(QCoreApplication.translate("NodeSummary", u"op_type:", None))
        self.inputs_add.setText(QCoreApplication.translate("NodeSummary", u"+", None))
        self.inputs_del.setText(QCoreApplication.translate("NodeSummary", u"-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inputs_tab), QCoreApplication.translate("NodeSummary", u"Inputs", None))
        self.outputs_add.setText(QCoreApplication.translate("NodeSummary", u"+", None))
        self.outputs_del.setText(QCoreApplication.translate("NodeSummary", u"-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.output_tab), QCoreApplication.translate("NodeSummary", u"Outputs", None))
        self.attr_add.setText(QCoreApplication.translate("NodeSummary", u"+", None))
        self.attr_del.setText(QCoreApplication.translate("NodeSummary", u"-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.attr_tab), QCoreApplication.translate("NodeSummary", u"Attrs", None))
    # retranslateUi

