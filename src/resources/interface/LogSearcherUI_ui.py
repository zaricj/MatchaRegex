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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)
from resources.interface.qrc import LogSearcher_resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1206, 1036)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setKerning(True)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/images/matcha-latte.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"/* Main window and background */\n"
"QWidget {\n"
"    background-color: #2D2D30;\n"
"    color: #F0F0F0;\n"
"    font-family: 'Segoe UI', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"/* QMenu */\n"
"QMenu {\n"
"    background-color: #3E3E42;\n"
"    border: 1px solid #5C5C60;\n"
"    color: #F0F0F0;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    background-color: #393d81;\n"
"}\n"
"\n"
"/* Push Buttons */\n"
"QPushButton {\n"
"    background-color: #3E3E42;\n"
"    border: 1px solid #5C5C60;\n"
"    color: #F0F0F0;\n"
"    padding: 4px 8px; /* Reduced padding */\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton#button_regex_pattern_remove_selected:hover {\n"
"    background-color: #813939;\n"
"}\n"
"\n"
"QPushButton#button_regex_pattern_remove_selected:pressed {\n"
"    background-color: #612b2b;\n"
"}\n"
"\n"
"QPushButton#button_regex_pattern_remove_all:hover {\n"
"    background-color: #813939;\n"
"}\n"
"\n"
"QPushButton#button_r"
                        "egex_pattern_remove_all:pressed {\n"
"    background-color: #612b2b;\n"
"}\n"
"\n"
"QPushButton#button_search_result_clear_results:hover {\n"
"    background-color: #813939;\n"
"}\n"
"\n"
"QPushButton#button_search_result_clear_results:pressed {\n"
"    background-color: #612b2b;\n"
"}\n"
"\n"
"QPushButton#button_clear_program_output:hover {\n"
"    background-color: #813939;\n"
"}\n"
"\n"
"QPushButton#button_clear_program_output:pressed {\n"
"    background-color: #612b2b;\n"
"}\n"
"\n"
"QPushButton#button_search_result_export_to_csv:hover {\n"
"    background-color: #39814e;\n"
"}\n"
"\n"
"QPushButton#button_search_result_export_to_csv:pressed {\n"
"    background-color: #2b613a;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #393d81;\n"
"    border: 1px solid #6D6D72;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2b2f61;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #3E3E42;\n"
"    border: 1px solid #5C5C60;\n"
"    color: #999999;\n"
"}\n"
"\n"
"/* Line Ed"
                        "its (text input fields) */\n"
"QLineEdit {\n"
"    background-color: #252526;\n"
"    border: 1px solid #5C5C60;\n"
"    padding: 3px; /* Reduced padding */\n"
"    border-radius: 4px;\n"
"    selection-background-color: #0078D7;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #0078D7; /* Accent color on focus */\n"
"}\n"
"\n"
"QTextEdit#program_output {\n"
"    background-color: #0c0c0c;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* Checkboxes and Radio Buttons */\n"
"QCheckBox, QRadioButton {\n"
"    color: #F0F0F0;\n"
"}\n"
"\n"
"QCheckBox::indicator, QRadioButton::indicator {\n"
"    background-color: #3E3E42;\n"
"    border: 1px solid #5C5C60;\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #0078D7;\n"
"    border: 1px solid #0078D7;\n"
"    image: url(:/icons/checkmark.svg); /* Placeholder, replace with a path to a checkmark icon */\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    backgroun"
                        "d-color: #0078D7;\n"
"    border: 1px solid #0078D7;\n"
"}\n"
"\n"
"/* Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #5C5C60;\n"
"    height: 6px;\n"
"    background: #3E3E42;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #F0F0F0;\n"
"    border: 1px solid #5C5C60;\n"
"    width: 16px;\n"
"    margin: -5px 0;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #0078D7;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"/* Progress Bar */\n"
"QProgressBar {\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    text-align: center;\n"
"    height: 12px;\n"
"    background: #3a3a3a;\n"
"    color: #f3f3f3;\n"
"}\n"
"QProgressBar::chunk {\n"
"    border-radius: 6px;\n"
"    background-color: #0078D7;\n"
"}\n"
"\n"
"/* Scroll Bars */\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: #252526;\n"
"    width: 10px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar"
                        "::handle:vertical {\n"
"    background: #5C5C60;\n"
"    min-height: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: #5C5C60;\n"
"    min-width: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: #252526;\n"
"}\n"
"\n"
"/* Tabs */\n"
"QTabBar::tab {\n"
"    background-color: #2D2D30;\n"
"    color: #F0F0F0;\n"
"    padding: 8px 16px;\n"
"    border: none;\n"
"    border-bottom: 2px solid transparent;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #3E3E42;\n"
"    border-bottom: 2px solid #0078D7;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #5C5C60;\n"
"}\n"
"\n"
"/* List and Tree Views */\n"
"QListView, QTreeView {\n"
"    background-color: #252526;\n"
"    border: 1px solid #5C5C60;\n"
"    selection-background-color: #0078D7;\n"
"    selection-color: #F"
                        "FFFFF;\n"
"}\n"
"\n"
"    QListWidget {\n"
"        border: 1px solid #404040;\n"
"        border-radius: 4px;\n"
"        background-color: #2d2d30;\n"
"        color: #ffffff;\n"
"        alternate-background-color: #323233;\n"
"        selection-background-color: #0078d4;\n"
"    }\n"
"\n"
"/* QFrame */\n"
"QFrame#output_frame {\n"
"    background-color: #252526;\n"
"    border: 1px solid #3e3e42;\n"
"    border-radius: 6px;\n"
"}\n"
"")
        MainWindow.setAnimated(True)
        self.actionOpen_Output_Folder = QAction(MainWindow)
        self.actionOpen_Output_Folder.setObjectName(u"actionOpen_Output_Folder")
        self.actionRegex_101 = QAction(MainWindow)
        self.actionRegex_101.setObjectName(u"actionRegex_101")
        self.actionOpen_Input_Folder = QAction(MainWindow)
        self.actionOpen_Input_Folder.setObjectName(u"actionOpen_Input_Folder")
        self.actionRegex_Cheatsheet = QAction(MainWindow)
        self.actionRegex_Cheatsheet.setObjectName(u"actionRegex_Cheatsheet")
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
        self.title_label.setMinimumSize(QSize(0, 30))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
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
        self.section_label_1.setFont(font1)
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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_files_folder.sizePolicy().hasHeightForWidth())
        self.label_files_folder.setSizePolicy(sizePolicy)
        self.label_files_folder.setMinimumSize(QSize(90, 0))
        self.label_files_folder.setFont(font1)

        self.horizontalLayout_01.addWidget(self.label_files_folder)

        self.line_edit_files_folder = QLineEdit(self.input_frame)
        self.line_edit_files_folder.setObjectName(u"line_edit_files_folder")
        self.line_edit_files_folder.setMinimumSize(QSize(0, 0))
        self.line_edit_files_folder.setClearButtonEnabled(True)

        self.horizontalLayout_01.addWidget(self.line_edit_files_folder)

        self.button_browse_folder = QPushButton(self.input_frame)
        self.button_browse_folder.setObjectName(u"button_browse_folder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_browse_folder.sizePolicy().hasHeightForWidth())
        self.button_browse_folder.setSizePolicy(sizePolicy1)
        self.button_browse_folder.setMinimumSize(QSize(0, 0))
        self.button_browse_folder.setFont(font1)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.button_browse_folder.setIcon(icon1)

        self.horizontalLayout_01.addWidget(self.button_browse_folder)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_01)

        self.horizontalLayout_04 = QHBoxLayout()
        self.horizontalLayout_04.setObjectName(u"horizontalLayout_04")
        self.label_file_pattern = QLabel(self.input_frame)
        self.label_file_pattern.setObjectName(u"label_file_pattern")
        self.label_file_pattern.setMinimumSize(QSize(92, 0))

        self.horizontalLayout_04.addWidget(self.label_file_pattern)

        self.line_edit_file_pattern = QLineEdit(self.input_frame)
        self.line_edit_file_pattern.setObjectName(u"line_edit_file_pattern")
        self.line_edit_file_pattern.setMinimumSize(QSize(0, 0))
        self.line_edit_file_pattern.setClearButtonEnabled(True)

        self.horizontalLayout_04.addWidget(self.line_edit_file_pattern)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_04)

        self.section_label_2 = QLabel(self.input_frame)
        self.section_label_2.setObjectName(u"section_label_2")
        self.section_label_2.setFont(font1)
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
        self.label_string_to_regex.setFont(font1)

        self.horizontalLayout_03.addWidget(self.label_string_to_regex)

        self.line_edit_string_to_regex = QLineEdit(self.input_frame)
        self.line_edit_string_to_regex.setObjectName(u"line_edit_string_to_regex")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_edit_string_to_regex.sizePolicy().hasHeightForWidth())
        self.line_edit_string_to_regex.setSizePolicy(sizePolicy2)
        self.line_edit_string_to_regex.setMinimumSize(QSize(0, 0))
        self.line_edit_string_to_regex.setClearButtonEnabled(True)

        self.horizontalLayout_03.addWidget(self.line_edit_string_to_regex)

        self.button_string_to_regex = QPushButton(self.input_frame)
        self.button_string_to_regex.setObjectName(u"button_string_to_regex")
        sizePolicy1.setHeightForWidth(self.button_string_to_regex.sizePolicy().hasHeightForWidth())
        self.button_string_to_regex.setSizePolicy(sizePolicy1)
        self.button_string_to_regex.setMinimumSize(QSize(0, 0))
        self.button_string_to_regex.setMaximumSize(QSize(16777215, 16777215))
        self.button_string_to_regex.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u":/images/convert.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_string_to_regex.setIcon(icon2)
        self.button_string_to_regex.setIconSize(QSize(14, 14))

        self.horizontalLayout_03.addWidget(self.button_string_to_regex)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_03)

        self.horizontalLayout_02 = QHBoxLayout()
        self.horizontalLayout_02.setSpacing(8)
        self.horizontalLayout_02.setObjectName(u"horizontalLayout_02")
        self.label_regex = QLabel(self.input_frame)
        self.label_regex.setObjectName(u"label_regex")
        self.label_regex.setMinimumSize(QSize(90, 0))
        self.label_regex.setFont(font1)

        self.horizontalLayout_02.addWidget(self.label_regex)

        self.line_edit_regex = QLineEdit(self.input_frame)
        self.line_edit_regex.setObjectName(u"line_edit_regex")
        self.line_edit_regex.setMinimumSize(QSize(0, 0))
        self.line_edit_regex.setClearButtonEnabled(True)

        self.horizontalLayout_02.addWidget(self.line_edit_regex)


        self.verticalLayout_line_edits.addLayout(self.horizontalLayout_02)

        self.button_add_regex_to_list_widget = QPushButton(self.input_frame)
        self.button_add_regex_to_list_widget.setObjectName(u"button_add_regex_to_list_widget")
        self.button_add_regex_to_list_widget.setMinimumSize(QSize(0, 0))
        self.button_add_regex_to_list_widget.setFont(font1)
        self.button_add_regex_to_list_widget.setStyleSheet(u"")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.button_add_regex_to_list_widget.setIcon(icon3)
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
        sizePolicy.setHeightForWidth(self.section_label_3.sizePolicy().hasHeightForWidth())
        self.section_label_3.setSizePolicy(sizePolicy)
        self.section_label_3.setMinimumSize(QSize(0, 0))
        self.section_label_3.setMaximumSize(QSize(16777215, 16777215))
        self.section_label_3.setFont(font1)
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
        self.list_widget_regex.setMinimumSize(QSize(0, 100))
        self.list_widget_regex.setMaximumSize(QSize(16777215, 16777215))
        self.list_widget_regex.setStyleSheet(u"")
        self.list_widget_regex.setAlternatingRowColors(True)
        self.list_widget_regex.setResizeMode(QListView.ResizeMode.Fixed)

        self.verticalLayout_item_widget.addWidget(self.list_widget_regex)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_regex_pattern_remove_selected = QPushButton(self.pattern_list_frame)
        self.button_regex_pattern_remove_selected.setObjectName(u"button_regex_pattern_remove_selected")
        icon4 = QIcon()
        icon4.addFile(u":/images/remove-selected.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_regex_pattern_remove_selected.setIcon(icon4)

        self.horizontalLayout_4.addWidget(self.button_regex_pattern_remove_selected)

        self.button_regex_pattern_remove_all = QPushButton(self.pattern_list_frame)
        self.button_regex_pattern_remove_all.setObjectName(u"button_regex_pattern_remove_all")
        icon5 = QIcon()
        icon5.addFile(u":/images/remove-all.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_regex_pattern_remove_all.setIcon(icon5)

        self.horizontalLayout_4.addWidget(self.button_regex_pattern_remove_all)


        self.verticalLayout_item_widget.addLayout(self.horizontalLayout_4)


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
        sizePolicy.setHeightForWidth(self.section_label_program_output.sizePolicy().hasHeightForWidth())
        self.section_label_program_output.setSizePolicy(sizePolicy)
        self.section_label_program_output.setMaximumSize(QSize(16777215, 16777215))
        self.section_label_program_output.setFont(font1)
        self.section_label_program_output.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"            ")

        self.horizontalLayout_3.addWidget(self.section_label_program_output)

        self.button_clear_program_output = QPushButton(self.output_frame)
        self.button_clear_program_output.setObjectName(u"button_clear_program_output")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.button_clear_program_output.sizePolicy().hasHeightForWidth())
        self.button_clear_program_output.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        self.button_clear_program_output.setFont(font2)
        self.button_clear_program_output.setMouseTracking(True)
        self.button_clear_program_output.setFlat(True)

        self.horizontalLayout_3.addWidget(self.button_clear_program_output)

        self.label_font_size_program_output = QLabel(self.output_frame)
        self.label_font_size_program_output.setObjectName(u"label_font_size_program_output")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_font_size_program_output.sizePolicy().hasHeightForWidth())
        self.label_font_size_program_output.setSizePolicy(sizePolicy5)

        self.horizontalLayout_3.addWidget(self.label_font_size_program_output)

        self.combobox_font_size_program_output = QComboBox(self.output_frame)
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.setObjectName(u"combobox_font_size_program_output")
        sizePolicy4.setHeightForWidth(self.combobox_font_size_program_output.sizePolicy().hasHeightForWidth())
        self.combobox_font_size_program_output.setSizePolicy(sizePolicy4)
        self.combobox_font_size_program_output.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.combobox_font_size_program_output)


        self.verticalLayout_program_output.addLayout(self.horizontalLayout_3)

        self.program_output = QTextEdit(self.output_frame)
        self.program_output.setObjectName(u"program_output")
        sizePolicy3.setHeightForWidth(self.program_output.sizePolicy().hasHeightForWidth())
        self.program_output.setSizePolicy(sizePolicy3)
        self.program_output.setMinimumSize(QSize(0, 60))
        self.program_output.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"Consolas"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.program_output.setFont(font3)
        self.program_output.setStyleSheet(u"font: 10pt \"Consolas\";")
        self.program_output.setReadOnly(True)

        self.verticalLayout_program_output.addWidget(self.program_output)

        self.progress_bar = QProgressBar(self.output_frame)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        self.verticalLayout_program_output.addWidget(self.progress_bar)


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
        self.section_label_4.setFont(font1)
        self.section_label_4.setStyleSheet(u"\n"
"             color: #0078d4;\n"
"            ")

        self.verticalLayout_table_widget.addWidget(self.section_label_4)

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
        self.label_3.setFont(font1)

        self.horizontalLayout_table_settings.addWidget(self.label_3)

        self.spinBox = QSpinBox(self.results_frame)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(0, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setValue(100)

        self.horizontalLayout_table_settings.addWidget(self.spinBox)

        self.button_limit_rows = QPushButton(self.results_frame)
        self.button_limit_rows.setObjectName(u"button_limit_rows")
        self.button_limit_rows.setCheckable(False)
        self.button_limit_rows.setChecked(False)

        self.horizontalLayout_table_settings.addWidget(self.button_limit_rows)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_table_settings.addItem(self.horizontalSpacer)


        self.verticalLayout_table_widget.addLayout(self.horizontalLayout_table_settings)

        self.checkbox_multiline_search = QCheckBox(self.results_frame)
        self.checkbox_multiline_search.setObjectName(u"checkbox_multiline_search")

        self.verticalLayout_table_widget.addWidget(self.checkbox_multiline_search)

        self.button_start_search = QPushButton(self.results_frame)
        self.button_start_search.setObjectName(u"button_start_search")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.button_start_search.sizePolicy().hasHeightForWidth())
        self.button_start_search.setSizePolicy(sizePolicy7)
        self.button_start_search.setMinimumSize(QSize(0, 0))
        self.button_start_search.setMaximumSize(QSize(16777215, 25))
        self.button_start_search.setFont(font1)
        icon6 = QIcon()
        icon6.addFile(u":/images/search-file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_start_search.setIcon(icon6)
        self.button_start_search.setIconSize(QSize(24, 24))

        self.verticalLayout_table_widget.addWidget(self.button_start_search)

        self.table_widget_results = QTableWidget(self.results_frame)
        self.table_widget_results.setObjectName(u"table_widget_results")
        self.table_widget_results.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.table_widget_results.sizePolicy().hasHeightForWidth())
        self.table_widget_results.setSizePolicy(sizePolicy3)
        self.table_widget_results.setMinimumSize(QSize(0, 100))
        self.table_widget_results.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_table_widget.addWidget(self.table_widget_results)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_search_result_export_to_csv = QPushButton(self.results_frame)
        self.button_search_result_export_to_csv.setObjectName(u"button_search_result_export_to_csv")
        self.button_search_result_export_to_csv.setEnabled(True)
        icon7 = QIcon()
        icon7.addFile(u":/images/export-to-file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_search_result_export_to_csv.setIcon(icon7)

        self.horizontalLayout_5.addWidget(self.button_search_result_export_to_csv)

        self.button_search_result_clear_results = QPushButton(self.results_frame)
        self.button_search_result_clear_results.setObjectName(u"button_search_result_clear_results")
        self.button_search_result_clear_results.setIcon(icon5)

        self.horizontalLayout_5.addWidget(self.button_search_result_clear_results)


        self.verticalLayout_table_widget.addLayout(self.horizontalLayout_5)


        self.verticalLayout_right.addWidget(self.results_frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_right)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1206, 26))
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
        self.menuOpen = QMenu(self.menubar)
        self.menuOpen.setObjectName(u"menuOpen")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
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

        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuOpen.addAction(self.actionOpen_Input_Folder)
        self.menuOpen.addAction(self.actionOpen_Output_Folder)
        self.menuHelp.addAction(self.actionRegex_101)
        self.menuHelp.addAction(self.actionRegex_Cheatsheet)

        self.retranslateUi(MainWindow)

        self.button_add_regex_to_list_widget.setDefault(False)
        self.button_clear_program_output.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MatchaRegex", None))
        self.actionOpen_Output_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Output Folder", None))
        self.actionRegex_101.setText(QCoreApplication.translate("MainWindow", u"Regex 101", None))
        self.actionOpen_Input_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Input Folder", None))
        self.actionRegex_Cheatsheet.setText(QCoreApplication.translate("MainWindow", u"Regex Cheatsheet", None))
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
        self.button_regex_pattern_remove_selected.setText(QCoreApplication.translate("MainWindow", u"Remove Selected", None))
        self.button_regex_pattern_remove_all.setText(QCoreApplication.translate("MainWindow", u"Remove All", None))
        self.section_label_program_output.setText(QCoreApplication.translate("MainWindow", u"System Output", None))
        self.button_clear_program_output.setText(QCoreApplication.translate("MainWindow", u"Clear Output", None))
        self.label_font_size_program_output.setText(QCoreApplication.translate("MainWindow", u"Font Size:", None))
        self.combobox_font_size_program_output.setItemText(0, QCoreApplication.translate("MainWindow", u"10pt", None))
        self.combobox_font_size_program_output.setItemText(1, QCoreApplication.translate("MainWindow", u"11pt", None))
        self.combobox_font_size_program_output.setItemText(2, QCoreApplication.translate("MainWindow", u"12pt", None))
        self.combobox_font_size_program_output.setItemText(3, QCoreApplication.translate("MainWindow", u"13pt", None))
        self.combobox_font_size_program_output.setItemText(4, QCoreApplication.translate("MainWindow", u"14pt", None))
        self.combobox_font_size_program_output.setItemText(5, QCoreApplication.translate("MainWindow", u"15pt", None))
        self.combobox_font_size_program_output.setItemText(6, QCoreApplication.translate("MainWindow", u"16pt", None))

        self.program_output.setPlaceholderText(QCoreApplication.translate("MainWindow", u"System output and status messages will appear here...", None))
        self.progress_bar.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.section_label_4.setText(QCoreApplication.translate("MainWindow", u"Search Results & Configuration", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Rows:", None))
        self.button_limit_rows.setText(QCoreApplication.translate("MainWindow", u"Limit Rows", None))
        self.checkbox_multiline_search.setText(QCoreApplication.translate("MainWindow", u"Enable multiline regex search - (^ and $ match start/end of line)", None))
        self.button_start_search.setText(QCoreApplication.translate("MainWindow", u"Start Search", None))
        self.button_search_result_export_to_csv.setText(QCoreApplication.translate("MainWindow", u"Export to Excel", None))
        self.button_search_result_clear_results.setText(QCoreApplication.translate("MainWindow", u"Clear Results", None))
        self.menuOpen.setTitle(QCoreApplication.translate("MainWindow", u"Open", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

