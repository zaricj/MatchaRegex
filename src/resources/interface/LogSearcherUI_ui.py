# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogSearcherUI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)

from resources.interface.qrc import LogSearcher_resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1206, 1060)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(9)
        font.setBold(False)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/images/clean-emissions-svgrepo-com.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"\n"
"    QMainWindow {\n"
"        background-color: #1e1e1e;\n"
"        color: #ffffff;\n"
"    }\n"
"    \n"
"    QLabel {\n"
"        color: #ffffff;\n"
"        font-weight: 600;\n"
"    }\n"
"    \n"
"    QLineEdit {\n"
"        border: 1px solid #404040;\n"
"        border-radius: 4px;\n"
"        padding: 6px 8px;\n"
"        background-color: #2d2d30;\n"
"        color: #ffffff;\n"
"        font-size: 9pt;\n"
"    }\n"
"    \n"
"    QLineEdit:focus {\n"
"        border-color: #0078d4;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton {\n"
"        background-color: #0078d4;\n"
"        color: white;\n"
"        border: none;\n"
"        border-radius: 4px;\n"
"        padding: 6px 12px;\n"
"        font-weight: 600;\n"
"        font-size: 9pt;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #106ebe;\n"
"    }\n"
"    \n"
"    QPushButton:pressed {\n"
"        background-color: #005a9e;\n"
"    }\n"
"    \n"
"    QPushButton#button_start_search {\n"
"       "
                        " background-color: #107c10;\n"
"        font-size: 9pt;\n"
"        padding: 8px 16px;\n"
"    }\n"
"    \n"
"    QPushButton#button_start_search:hover {\n"
"        background-color: #0e6e0e;\n"
"    }\n"
"    \n"
"    QPushButton#button_string_to_regex {\n"
"        background-color: #8a2be2;\n"
"    }\n"
"    \n"
"    QPushButton#button_string_to_regex:hover {\n"
"        background-color: #7b2bc7;\n"
"    }\n"
"    \n"
"    QListWidget {\n"
"        border: 1px solid #404040;\n"
"        border-radius: 4px;\n"
"        background-color: #2d2d30;\n"
"        color: #ffffff;\n"
"        alternate-background-color: #323233;\n"
"        selection-background-color: #0078d4;\n"
"    }\n"
"    \n"
"    QTableWidget {\n"
"        border: 1px solid #404040;\n"
"        border-radius: 4px;\n"
"        background-color: #2d2d30;\n"
"        color: #ffffff;\n"
"        alternate-background-color: #323233;\n"
"        gridline-color: #404040;\n"
"    }\n"
"    \n"
"    QTableWidget::item {\n"
"        padding: 4px;\n"
""
                        "    }\n"
"    \n"
"    QTableWidget QHeaderView::section {\n"
"        background-color: #404040;\n"
"        color: #ffffff;\n"
"        padding: 4px;\n"
"        border: 1px solid #505050;\n"
"    }\n"
"    \n"
"    QTextEdit {\n"
"        border: 1px solid #404040;\n"
"        border-radius: 4px;\n"
"        background-color: #0c0c0c;\n"
"        color: #ffffff;\n"
"        font-family: 'Consolas', 'Monaco', monospace;\n"
"        font-size: 8pt;\n"
"        padding: 6px;\n"
"    }\n"
"    \n"
"    QSpinBox {\n"
"        border: 1px solid #404040;\n"
"        border-radius: 4px;\n"
"        padding: 4px;\n"
"        background-color: #2d2d30;\n"
"        color: #ffffff;\n"
"        min-width: 50px;\n"
"    }\n"
"    \n"
"    QSpinBox:focus {\n"
"        border-color: #0078d4;\n"
"    }\n"
"    \n"
"    QSpinBox::up-button, QSpinBox::down-button {\n"
"        background-color: #404040;\n"
"        border: none;\n"
"        width: 16px;\n"
"    }\n"
"    \n"
"    QSpinBox::up-button:hover, QSpinBox::down-butt"
                        "on:hover {\n"
"        background-color: #505050;\n"
"    }\n"
"   ")
        MainWindow.setAnimated(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"\n"
"     QWidget#centralwidget {\n"
"         background-color: #1e1e1e;\n"
"     }\n"
"    ")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        font1.setWeight(QFont.DemiBold)
        self.title_label.setFont(font1)
        self.title_label.setAutoFillBackground(False)
        self.title_label.setStyleSheet(u"\n"
"        color: #ffffff;\n"
"        margin-bottom: 3px;\n"
"		background-color: rgb(37, 37, 115);\n"
"       ")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.title_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_left = QVBoxLayout()
        self.verticalLayout_left.setObjectName(u"verticalLayout_left")
        self.input_frame = QFrame(self.centralwidget)
        self.input_frame.setObjectName(u"input_frame")
        self.input_frame.setStyleSheet(u"\n"
"          QFrame#input_frame {\n"
"              background-color: #252526;\n"
"              border: 1px solid #3e3e42;\n"
"              border-radius: 6px;\n"
"          }\n"
"         ")
        self.input_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_line_edits = QVBoxLayout(self.input_frame)
        self.verticalLayout_line_edits.setSpacing(8)
        self.verticalLayout_line_edits.setObjectName(u"verticalLayout_line_edits")
        self.verticalLayout_line_edits.setContentsMargins(12, 12, 12, 12)
        self.section_label_1 = QLabel(self.input_frame)
        self.section_label_1.setObjectName(u"section_label_1")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setWeight(QFont.DemiBold)
        self.section_label_1.setFont(font2)
        self.section_label_1.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"             margin-bottom: 2px;\n"
"            ")

        self.verticalLayout_line_edits.addWidget(self.section_label_1)

        self.horizontalLayout_01 = QHBoxLayout()
        self.horizontalLayout_01.setSpacing(8)
        self.horizontalLayout_01.setObjectName(u"horizontalLayout_01")
        self.label_files_folder = QLabel(self.input_frame)
        self.label_files_folder.setObjectName(u"label_files_folder")
        self.label_files_folder.setMinimumSize(QSize(90, 0))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(9)
        font3.setWeight(QFont.DemiBold)
        self.label_files_folder.setFont(font3)

        self.horizontalLayout_01.addWidget(self.label_files_folder)

        self.line_edit_files_folder = QLineEdit(self.input_frame)
        self.line_edit_files_folder.setObjectName(u"line_edit_files_folder")
        self.line_edit_files_folder.setMinimumSize(QSize(0, 30))
        self.line_edit_files_folder.setClearButtonEnabled(True)

        self.horizontalLayout_01.addWidget(self.line_edit_files_folder)

        self.button_browse_folder = QPushButton(self.input_frame)
        self.button_browse_folder.setObjectName(u"button_browse_folder")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_browse_folder.sizePolicy().hasHeightForWidth())
        self.button_browse_folder.setSizePolicy(sizePolicy)
        self.button_browse_folder.setMinimumSize(QSize(100, 30))
        self.button_browse_folder.setFont(font3)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.button_browse_folder.setIcon(icon1)

        self.horizontalLayout_01.addWidget(self.button_browse_folder)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_01)

        self.horizontalLayout_04 = QHBoxLayout()
        self.horizontalLayout_04.setObjectName(u"horizontalLayout_04")
        self.label_file_pattern = QLabel(self.input_frame)
        self.label_file_pattern.setObjectName(u"label_file_pattern")
        self.label_file_pattern.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_04.addWidget(self.label_file_pattern)

        self.line_edit_file_pattern = QLineEdit(self.input_frame)
        self.line_edit_file_pattern.setObjectName(u"line_edit_file_pattern")
        self.line_edit_file_pattern.setMinimumSize(QSize(0, 30))
        self.line_edit_file_pattern.setClearButtonEnabled(True)

        self.horizontalLayout_04.addWidget(self.line_edit_file_pattern)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_04)

        self.section_label_2 = QLabel(self.input_frame)
        self.section_label_2.setObjectName(u"section_label_2")
        self.section_label_2.setFont(font2)
        self.section_label_2.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"             margin-top: 6px;\n"
"             margin-bottom: 2px;\n"
"            ")

        self.verticalLayout_line_edits.addWidget(self.section_label_2)

        self.horizontalLayout_03 = QHBoxLayout()
        self.horizontalLayout_03.setSpacing(8)
        self.horizontalLayout_03.setObjectName(u"horizontalLayout_03")
        self.label_string_to_regex = QLabel(self.input_frame)
        self.label_string_to_regex.setObjectName(u"label_string_to_regex")
        self.label_string_to_regex.setMinimumSize(QSize(90, 0))
        self.label_string_to_regex.setFont(font3)

        self.horizontalLayout_03.addWidget(self.label_string_to_regex)

        self.line_edit_string_to_regex = QLineEdit(self.input_frame)
        self.line_edit_string_to_regex.setObjectName(u"line_edit_string_to_regex")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_string_to_regex.sizePolicy().hasHeightForWidth())
        self.line_edit_string_to_regex.setSizePolicy(sizePolicy1)
        self.line_edit_string_to_regex.setMinimumSize(QSize(0, 30))
        self.line_edit_string_to_regex.setClearButtonEnabled(True)

        self.horizontalLayout_03.addWidget(self.line_edit_string_to_regex)

        self.button_string_to_regex = QPushButton(self.input_frame)
        self.button_string_to_regex.setObjectName(u"button_string_to_regex")
        sizePolicy.setHeightForWidth(self.button_string_to_regex.sizePolicy().hasHeightForWidth())
        self.button_string_to_regex.setSizePolicy(sizePolicy)
        self.button_string_to_regex.setMinimumSize(QSize(100, 30))
        self.button_string_to_regex.setFont(font3)

        self.horizontalLayout_03.addWidget(self.button_string_to_regex)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_03)

        self.horizontalLayout_02 = QHBoxLayout()
        self.horizontalLayout_02.setSpacing(8)
        self.horizontalLayout_02.setObjectName(u"horizontalLayout_02")
        self.label_regex = QLabel(self.input_frame)
        self.label_regex.setObjectName(u"label_regex")
        self.label_regex.setMinimumSize(QSize(90, 0))
        self.label_regex.setFont(font3)

        self.horizontalLayout_02.addWidget(self.label_regex)

        self.line_edit_regex = QLineEdit(self.input_frame)
        self.line_edit_regex.setObjectName(u"line_edit_regex")
        self.line_edit_regex.setMinimumSize(QSize(0, 30))
        self.line_edit_regex.setClearButtonEnabled(True)

        self.horizontalLayout_02.addWidget(self.line_edit_regex)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_02)

        self.button_add_regex_to_list_widget = QPushButton(self.input_frame)
        self.button_add_regex_to_list_widget.setObjectName(u"button_add_regex_to_list_widget")
        self.button_add_regex_to_list_widget.setMinimumSize(QSize(0, 28))
        self.button_add_regex_to_list_widget.setFont(font3)
        self.button_add_regex_to_list_widget.setStyleSheet(u"\n"
"             QPushButton {\n"
"                 background-color: #6f42c1;\n"
"             }\n"
"             QPushButton:hover {\n"
"                 background-color: #5a36a0;\n"
"             }\n"
"            ")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.button_add_regex_to_list_widget.setIcon(icon2)
        self.button_add_regex_to_list_widget.setIconSize(QSize(16, 16))
        self.button_add_regex_to_list_widget.setFlat(False)

        self.verticalLayout_line_edits.addWidget(self.button_add_regex_to_list_widget)


        self.verticalLayout_left.addWidget(self.input_frame)

        self.pattern_list_frame = QFrame(self.centralwidget)
        self.pattern_list_frame.setObjectName(u"pattern_list_frame")
        self.pattern_list_frame.setStyleSheet(u"\n"
"          QFrame#pattern_list_frame {\n"
"              background-color: #252526;\n"
"              border: 1px solid #3e3e42;\n"
"              border-radius: 6px;\n"
"          }\n"
"         ")
        self.pattern_list_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_item_widget = QVBoxLayout(self.pattern_list_frame)
        self.verticalLayout_item_widget.setSpacing(6)
        self.verticalLayout_item_widget.setObjectName(u"verticalLayout_item_widget")
        self.verticalLayout_item_widget.setContentsMargins(12, 12, 12, 12)
        self.section_label_3 = QLabel(self.pattern_list_frame)
        self.section_label_3.setObjectName(u"section_label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.section_label_3.sizePolicy().hasHeightForWidth())
        self.section_label_3.setSizePolicy(sizePolicy2)
        self.section_label_3.setMinimumSize(QSize(0, 0))
        self.section_label_3.setMaximumSize(QSize(16777215, 16777215))
        self.section_label_3.setFont(font2)
        self.section_label_3.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"            ")

        self.verticalLayout_item_widget.addWidget(self.section_label_3)

        self.list_widget_regex = QListWidget(self.pattern_list_frame)
        self.list_widget_regex.setObjectName(u"list_widget_regex")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.list_widget_regex.sizePolicy().hasHeightForWidth())
        self.list_widget_regex.setSizePolicy(sizePolicy3)
        self.list_widget_regex.setMinimumSize(QSize(0, 150))
        self.list_widget_regex.setMaximumSize(QSize(16777215, 16777215))
        self.list_widget_regex.setStyleSheet(u"")
        self.list_widget_regex.setResizeMode(QListView.ResizeMode.Fixed)

        self.verticalLayout_item_widget.addWidget(self.list_widget_regex)


        self.verticalLayout_left.addWidget(self.pattern_list_frame)

        self.output_frame = QFrame(self.centralwidget)
        self.output_frame.setObjectName(u"output_frame")
        self.output_frame.setStyleSheet(u"\n"
"          QFrame#output_frame {\n"
"              background-color: #252526;\n"
"              border: 1px solid #3e3e42;\n"
"              border-radius: 6px;\n"
"          }\n"
"         ")
        self.output_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_program_output = QVBoxLayout(self.output_frame)
        self.verticalLayout_program_output.setSpacing(6)
        self.verticalLayout_program_output.setObjectName(u"verticalLayout_program_output")
        self.verticalLayout_program_output.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.section_label_program_output = QLabel(self.output_frame)
        self.section_label_program_output.setObjectName(u"section_label_program_output")
        sizePolicy2.setHeightForWidth(self.section_label_program_output.sizePolicy().hasHeightForWidth())
        self.section_label_program_output.setSizePolicy(sizePolicy2)
        self.section_label_program_output.setFont(font2)
        self.section_label_program_output.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"            ")

        self.horizontalLayout_3.addWidget(self.section_label_program_output)

        self.label_font_size_program_output = QLabel(self.output_frame)
        self.label_font_size_program_output.setObjectName(u"label_font_size_program_output")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_font_size_program_output.sizePolicy().hasHeightForWidth())
        self.label_font_size_program_output.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.label_font_size_program_output)

        self.combobox_font_size_program_output = QComboBox(self.output_frame)
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.setObjectName(u"combobox_font_size_program_output")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.combobox_font_size_program_output.sizePolicy().hasHeightForWidth())
        self.combobox_font_size_program_output.setSizePolicy(sizePolicy5)
        self.combobox_font_size_program_output.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.combobox_font_size_program_output)


        self.verticalLayout_program_output.addLayout(self.horizontalLayout_3)

        self.program_output = QTextEdit(self.output_frame)
        self.program_output.setObjectName(u"program_output")
        sizePolicy3.setHeightForWidth(self.program_output.sizePolicy().hasHeightForWidth())
        self.program_output.setSizePolicy(sizePolicy3)
        self.program_output.setMinimumSize(QSize(0, 80))
        self.program_output.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setFamilies([u"Consolas"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.program_output.setFont(font4)
        self.program_output.setStyleSheet(u"font: 10pt \"Consolas\";")
        self.program_output.setReadOnly(True)

        self.verticalLayout_program_output.addWidget(self.program_output)


        self.verticalLayout_left.addWidget(self.output_frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_left)

        self.verticalLayout_right = QVBoxLayout()
        self.verticalLayout_right.setObjectName(u"verticalLayout_right")
        self.results_frame = QFrame(self.centralwidget)
        self.results_frame.setObjectName(u"results_frame")
        self.results_frame.setStyleSheet(u"\n"
"          QFrame#results_frame {\n"
"              background-color: #252526;\n"
"              border: 1px solid #3e3e42;\n"
"              border-radius: 6px;\n"
"          }\n"
"         ")
        self.results_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_table_widget = QVBoxLayout(self.results_frame)
        self.verticalLayout_table_widget.setSpacing(8)
        self.verticalLayout_table_widget.setObjectName(u"verticalLayout_table_widget")
        self.verticalLayout_table_widget.setContentsMargins(12, 12, 12, 12)
        self.section_label_4 = QLabel(self.results_frame)
        self.section_label_4.setObjectName(u"section_label_4")
        self.section_label_4.setFont(font2)
        self.section_label_4.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"            ")

        self.verticalLayout_table_widget.addWidget(self.section_label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 4)
        self.label_headers = QLabel(self.results_frame)
        self.label_headers.setObjectName(u"label_headers")
        self.label_headers.setMinimumSize(QSize(80, 0))
        self.label_headers.setFont(font3)

        self.horizontalLayout.addWidget(self.label_headers)

        self.line_edit_headers = QLineEdit(self.results_frame)
        self.line_edit_headers.setObjectName(u"line_edit_headers")
        self.line_edit_headers.setMinimumSize(QSize(0, 30))
        self.line_edit_headers.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.line_edit_headers)


        self.verticalLayout_table_widget.addLayout(self.horizontalLayout)

        self.horizontalLayout_table_settings = QHBoxLayout()
        self.horizontalLayout_table_settings.setSpacing(12)
        self.horizontalLayout_table_settings.setObjectName(u"horizontalLayout_table_settings")
        self.label_3 = QLabel(self.results_frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy6)
        self.label_3.setFont(font3)

        self.horizontalLayout_table_settings.addWidget(self.label_3)

        self.spinBox = QSpinBox(self.results_frame)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(60, 26))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setValue(100)

        self.horizontalLayout_table_settings.addWidget(self.spinBox)

        self.label_4 = QLabel(self.results_frame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy6.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy6)
        self.label_4.setFont(font3)

        self.horizontalLayout_table_settings.addWidget(self.label_4)

        self.spinBox_2 = QSpinBox(self.results_frame)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimumSize(QSize(60, 26))
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(20)
        self.spinBox_2.setValue(4)

        self.horizontalLayout_table_settings.addWidget(self.spinBox_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_table_settings.addItem(self.horizontalSpacer)


        self.verticalLayout_table_widget.addLayout(self.horizontalLayout_table_settings)

        self.button_start_search = QPushButton(self.results_frame)
        self.button_start_search.setObjectName(u"button_start_search")
        self.button_start_search.setMinimumSize(QSize(0, 30))
        self.button_start_search.setFont(font3)

        self.verticalLayout_table_widget.addWidget(self.button_start_search)

        self.table_widget_results = QTableWidget(self.results_frame)
        self.table_widget_results.setObjectName(u"table_widget_results")
        sizePolicy3.setHeightForWidth(self.table_widget_results.sizePolicy().hasHeightForWidth())
        self.table_widget_results.setSizePolicy(sizePolicy3)
        self.table_widget_results.setMinimumSize(QSize(0, 180))
        self.table_widget_results.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_table_widget.addWidget(self.table_widget_results)


        self.verticalLayout_right.addWidget(self.results_frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_right)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1206, 25))
        self.menubar.setStyleSheet(u"\n"
"     QMenuBar {\n"
"         background-color: #2d2d30;\n"
"         color: white;\n"
"         border-bottom: 1px solid #404040;\n"
"     }\n"
"     QMenuBar::item {\n"
"         padding: 4px 8px;\n"
"     }\n"
"     QMenuBar::item:selected {\n"
"         background-color: #404040;\n"
"     }\n"
"    ")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"\n"
"     QStatusBar {\n"
"         background-color: #2d2d30;\n"
"         border-top: 1px solid #404040;\n"
"         color: #cccccc;\n"
"     }\n"
"    ")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.button_add_regex_to_list_widget.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Log Searcher Pro", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"Log File Search & Analysis", None))
        self.section_label_1.setText(QCoreApplication.translate("MainWindow", u"Source Configuration", None))
        self.label_files_folder.setText(QCoreApplication.translate("MainWindow", u"Folder Path:", None))
        self.line_edit_files_folder.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select a folder containing log files to search...", None))
        self.button_browse_folder.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_file_pattern.setText(QCoreApplication.translate("MainWindow", u"File Pattern:", None))
        self.line_edit_file_pattern.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(Optional) Enter patterns to search only specific files (wildcard * accepted and comma-separated)", None))
        self.section_label_2.setText(QCoreApplication.translate("MainWindow", u"Search Pattern Setup", None))
        self.label_string_to_regex.setText(QCoreApplication.translate("MainWindow", u"Text to Convert:", None))
        self.line_edit_string_to_regex.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter plain text to convert to regex pattern...", None))
        self.button_string_to_regex.setText(QCoreApplication.translate("MainWindow", u"Convert", None))
        self.label_regex.setText(QCoreApplication.translate("MainWindow", u"Regex Pattern:", None))
        self.line_edit_regex.setText("")
        self.line_edit_regex.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter or generate regular expression pattern...", None))
        self.button_add_regex_to_list_widget.setText(QCoreApplication.translate("MainWindow", u"Add Pattern to Search List", None))
        self.section_label_3.setText(QCoreApplication.translate("MainWindow", u"Active Search Patterns", None))
        self.section_label_program_output.setText(QCoreApplication.translate("MainWindow", u"System Output", None))
        self.label_font_size_program_output.setText(QCoreApplication.translate("MainWindow", u"Font Size:", None))
        self.combobox_font_size_program_output.setItemText(0, QCoreApplication.translate("MainWindow", u"12pt", None))
        self.combobox_font_size_program_output.setItemText(1, QCoreApplication.translate("MainWindow", u"13pt", None))
        self.combobox_font_size_program_output.setItemText(2, QCoreApplication.translate("MainWindow", u"14pt", None))
        self.combobox_font_size_program_output.setItemText(3, QCoreApplication.translate("MainWindow", u"15pt", None))
        self.combobox_font_size_program_output.setItemText(4, QCoreApplication.translate("MainWindow", u"16pt", None))

        self.program_output.setPlaceholderText(QCoreApplication.translate("MainWindow", u"System output and status messages will appear here...", None))
        self.section_label_4.setText(QCoreApplication.translate("MainWindow", u"Search Results & Configuration", None))
        self.label_headers.setText(QCoreApplication.translate("MainWindow", u"Table Headers:", None))
        self.line_edit_headers.setPlaceholderText(QCoreApplication.translate("MainWindow", u"File, Line, Match, Timestamp (comma-separated headers)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Rows:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Columns:", None))
        self.button_start_search.setText(QCoreApplication.translate("MainWindow", u"Start Search", None))
    # retranslateUi

