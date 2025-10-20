# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreBuiltRegexManagerWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
from resources.ui.qrc from resources.ui.qrc import LogSearcher_resource_rc

class Ui_PreBuiltRegexManagerWidget(object):
    def setupUi(self, PreBuiltRegexManagerWidget):
        if not PreBuiltRegexManagerWidget.objectName():
            PreBuiltRegexManagerWidget.setObjectName(u"PreBuiltRegexManagerWidget")
        PreBuiltRegexManagerWidget.resize(949, 675)
        icon = QIcon()
        icon.addFile(u":/images/matcha-latte.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PreBuiltRegexManagerWidget.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(PreBuiltRegexManagerWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainHorLayout = QHBoxLayout()
        self.MainHorLayout.setObjectName(u"MainHorLayout")
        self.groupBox_pre_built_xpaths_main = QGroupBox(PreBuiltRegexManagerWidget)
        self.groupBox_pre_built_xpaths_main.setObjectName(u"groupBox_pre_built_xpaths_main")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_pre_built_xpaths_main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_9 = QLabel(self.groupBox_pre_built_xpaths_main)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_2.addWidget(self.label_9)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lable_pre_built_xpaths = QLabel(self.groupBox_pre_built_xpaths_main)
        self.lable_pre_built_xpaths.setObjectName(u"lable_pre_built_xpaths")

        self.horizontalLayout.addWidget(self.lable_pre_built_xpaths)

        self.combobox_xpath_configs = QComboBox(self.groupBox_pre_built_xpaths_main)
        self.combobox_xpath_configs.setObjectName(u"combobox_xpath_configs")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combobox_xpath_configs.sizePolicy().hasHeightForWidth())
        self.combobox_xpath_configs.setSizePolicy(sizePolicy)
        self.combobox_xpath_configs.setEditable(True)

        self.horizontalLayout.addWidget(self.combobox_xpath_configs)

        self.button_load_config = QPushButton(self.groupBox_pre_built_xpaths_main)
        self.button_load_config.setObjectName(u"button_load_config")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_load_config.sizePolicy().hasHeightForWidth())
        self.button_load_config.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.button_load_config)

        self.button_delete_config = QPushButton(self.groupBox_pre_built_xpaths_main)
        self.button_delete_config.setObjectName(u"button_delete_config")
        sizePolicy1.setHeightForWidth(self.button_delete_config.sizePolicy().hasHeightForWidth())
        self.button_delete_config.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.button_delete_config)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.frame_3 = QFrame(self.groupBox_pre_built_xpaths_main)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_7 = QLabel(self.frame_3)
        self.label_7.setObjectName(u"label_7")
        font = QFont()
        font.setBold(True)
        self.label_7.setFont(font)

        self.verticalLayout_8.addWidget(self.label_7)

        self.list_widget_edit_xpath_expressions = QListWidget(self.frame_3)
        self.list_widget_edit_xpath_expressions.setObjectName(u"list_widget_edit_xpath_expressions")
        self.list_widget_edit_xpath_expressions.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.verticalLayout_8.addWidget(self.list_widget_edit_xpath_expressions)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.line_3 = QFrame(self.groupBox_pre_built_xpaths_main)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.button_save_changes = QPushButton(self.groupBox_pre_built_xpaths_main)
        self.button_save_changes.setObjectName(u"button_save_changes")
        sizePolicy1.setHeightForWidth(self.button_save_changes.sizePolicy().hasHeightForWidth())
        self.button_save_changes.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.button_save_changes)


        self.MainHorLayout.addWidget(self.groupBox_pre_built_xpaths_main)

        self.LeftSide = QVBoxLayout()
        self.LeftSide.setObjectName(u"LeftSide")

        self.MainHorLayout.addLayout(self.LeftSide)

        self.RightSide = QVBoxLayout()
        self.RightSide.setObjectName(u"RightSide")
        self.groupBox = QGroupBox(PreBuiltRegexManagerWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.line_edit_xpath_expression = QLineEdit(self.frame)
        self.line_edit_xpath_expression.setObjectName(u"line_edit_xpath_expression")

        self.horizontalLayout_3.addWidget(self.line_edit_xpath_expression)

        self.button_add_xpath_to_list = QPushButton(self.frame)
        self.button_add_xpath_to_list.setObjectName(u"button_add_xpath_to_list")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.button_add_xpath_to_list.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.button_add_xpath_to_list)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.list_widget_xpath_expressions = QListWidget(self.frame)
        self.list_widget_xpath_expressions.setObjectName(u"list_widget_xpath_expressions")
        self.list_widget_xpath_expressions.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.verticalLayout_3.addWidget(self.list_widget_xpath_expressions)


        self.verticalLayout_7.addWidget(self.frame)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.line_edit_config_name = QLineEdit(self.groupBox)
        self.line_edit_config_name.setObjectName(u"line_edit_config_name")

        self.horizontalLayout_5.addWidget(self.line_edit_config_name)

        self.button_save_config = QPushButton(self.groupBox)
        self.button_save_config.setObjectName(u"button_save_config")
        sizePolicy1.setHeightForWidth(self.button_save_config.sizePolicy().hasHeightForWidth())
        self.button_save_config.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.button_save_config)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)


        self.RightSide.addWidget(self.groupBox)


        self.MainHorLayout.addLayout(self.RightSide)


        self.verticalLayout.addLayout(self.MainHorLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_remove_selected = QPushButton(PreBuiltRegexManagerWidget)
        self.button_remove_selected.setObjectName(u"button_remove_selected")

        self.horizontalLayout_2.addWidget(self.button_remove_selected)

        self.button_remove_all = QPushButton(PreBuiltRegexManagerWidget)
        self.button_remove_all.setObjectName(u"button_remove_all")

        self.horizontalLayout_2.addWidget(self.button_remove_all)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(PreBuiltRegexManagerWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(PreBuiltRegexManagerWidget)

        QMetaObject.connectSlotsByName(PreBuiltRegexManagerWidget)
    # setupUi

    def retranslateUi(self, PreBuiltRegexManagerWidget):
        PreBuiltRegexManagerWidget.setWindowTitle(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Settings - Regex Expression Manager", None))
#if QT_CONFIG(tooltip)
        PreBuiltRegexManagerWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.groupBox_pre_built_xpaths_main.setTitle(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Edit Autofill Regex Expressions", None))
        self.label_9.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Here you can edit the custom pre-built configuration for the autofill:", None))
        self.lable_pre_built_xpaths.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Select Config:", None))
#if QT_CONFIG(tooltip)
        self.button_load_config.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Load the selected configuration.", None))
#endif // QT_CONFIG(tooltip)
        self.button_load_config.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Load", None))
#if QT_CONFIG(tooltip)
        self.button_delete_config.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Deletes the selected configurtion all it's values.", None))
#endif // QT_CONFIG(tooltip)
        self.button_delete_config.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Delete", None))
        self.label_7.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Edit Regex Expression", None))
#if QT_CONFIG(tooltip)
        self.button_save_changes.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Save changes that you made to the configuration.", None))
#endif // QT_CONFIG(tooltip)
        self.button_save_changes.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Save Changes", None))
        self.groupBox.setTitle(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Create Autofill Regex Expressions", None))
        self.label.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Here you can create your own pre-built XPath Expression and CSV Headers autofill configuration:", None))
        self.label_5.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Add Regex Expressions", None))
        self.label_2.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Enter a Regex Expression:", None))
        self.line_edit_xpath_expression.setPlaceholderText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Enter a Regex Expression...", None))
#if QT_CONFIG(tooltip)
        self.button_add_xpath_to_list.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Add entered Regex Expression to it's listbox.", None))
#endif // QT_CONFIG(tooltip)
        self.button_add_xpath_to_list.setText("")
        self.label_4.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Enter a name for the autofill config:", None))
        self.line_edit_config_name.setPlaceholderText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Enter a name for the configuration...", None))
#if QT_CONFIG(tooltip)
        self.button_save_config.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Save your configurtion with all items that are in the two listboxes.", None))
#endif // QT_CONFIG(tooltip)
        self.button_save_config.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Save Config", None))
#if QT_CONFIG(tooltip)
        self.button_remove_selected.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Removes the currently selected item in the focused listbox.", None))
#endif // QT_CONFIG(tooltip)
        self.button_remove_selected.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Remove Selected", None))
#if QT_CONFIG(tooltip)
        self.button_remove_all.setToolTip(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Removes all items in the focused listbox.", None))
#endif // QT_CONFIG(tooltip)
        self.button_remove_all.setText(QCoreApplication.translate("PreBuiltRegexManagerWidget", u"Remove All", None))
    # retranslateUi

