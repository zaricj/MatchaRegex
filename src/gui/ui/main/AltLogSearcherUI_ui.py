# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AltLogSearcherUI.ui'
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
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpinBox, QSplitter,
    QStatusBar, QTableView, QTextEdit, QVBoxLayout,
    QWidget)
from gui.assets.qrc import LogSearcher_resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1358, 1055)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
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
        self.actionOpen_Input_Folder = QAction(MainWindow)
        self.actionOpen_Input_Folder.setObjectName(u"actionOpen_Input_Folder")
        self.actionOpen_Output_Folder = QAction(MainWindow)
        self.actionOpen_Output_Folder.setObjectName(u"actionOpen_Output_Folder")
        self.actionRegex_101 = QAction(MainWindow)
        self.actionRegex_101.setObjectName(u"actionRegex_101")
        self.actionRegex_Cheatsheet = QAction(MainWindow)
        self.actionRegex_Cheatsheet.setObjectName(u"actionRegex_Cheatsheet")
        self.actionOpen_Regex_Expression_Manager = QAction(MainWindow)
        self.actionOpen_Regex_Expression_Manager.setObjectName(u"actionOpen_Regex_Expression_Manager")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setWeight(QFont.DemiBold)
        self.title_label.setFont(font)
        self.title_label.setAutoFillBackground(False)
        self.title_label.setStyleSheet(u"\n"
"        color: #ffffff;\n"
"        margin-bottom: 3px;\n"
"		background-color: rgb(37, 37, 115);\n"
"       ")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.title_label)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setMinimumSize(QSize(0, 0))
        self.splitter.setSizeIncrement(QSize(0, 0))
        self.splitter.setBaseSize(QSize(0, 0))
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(5)
        self.splitter.setChildrenCollapsible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_Top = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_Top.setObjectName(u"verticalLayout_Top")
        self.verticalLayout_Top.setContentsMargins(0, 0, 0, 0)
        self.widget_top_main = QWidget(self.verticalLayoutWidget)
        self.widget_top_main.setObjectName(u"widget_top_main")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_top_main)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 4, -1, -1)
        self.input_frame = QFrame(self.widget_top_main)
        self.input_frame.setObjectName(u"input_frame")
        self.input_frame.setStyleSheet(u"\n"
"          QFrame#input_frame {\n"
"              background-color: #252526;\n"
"              border: 1px solid #3e3e42;\n"
"              border-radius: 6px;\n"
"          }\n"
"         ")
        self.input_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_line_edits_3 = QVBoxLayout(self.input_frame)
        self.verticalLayout_line_edits_3.setSpacing(8)
        self.verticalLayout_line_edits_3.setObjectName(u"verticalLayout_line_edits_3")
        self.verticalLayout_line_edits_3.setContentsMargins(6, 6, 6, 6)
        self.groupBox_source_config = QGroupBox(self.input_frame)
        self.groupBox_source_config.setObjectName(u"groupBox_source_config")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.groupBox_source_config.setFont(font1)
        self.groupBox_source_config.setFlat(True)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_source_config)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 6, 0, 2)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(8)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_files_folder = QLabel(self.groupBox_source_config)
        self.label_files_folder.setObjectName(u"label_files_folder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_files_folder.sizePolicy().hasHeightForWidth())
        self.label_files_folder.setSizePolicy(sizePolicy2)
        self.label_files_folder.setMinimumSize(QSize(90, 0))
        self.label_files_folder.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_files_folder)

        self.line_edit_files_folder = QLineEdit(self.groupBox_source_config)
        self.line_edit_files_folder.setObjectName(u"line_edit_files_folder")
        self.line_edit_files_folder.setMinimumSize(QSize(0, 0))
        self.line_edit_files_folder.setClearButtonEnabled(True)

        self.horizontalLayout_12.addWidget(self.line_edit_files_folder)

        self.button_browse_folder = QPushButton(self.groupBox_source_config)
        self.button_browse_folder.setObjectName(u"button_browse_folder")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_browse_folder.sizePolicy().hasHeightForWidth())
        self.button_browse_folder.setSizePolicy(sizePolicy3)
        self.button_browse_folder.setMinimumSize(QSize(0, 0))
        self.button_browse_folder.setFont(font1)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.button_browse_folder.setIcon(icon)

        self.horizontalLayout_12.addWidget(self.button_browse_folder)


        self.verticalLayout_8.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_file_pattern = QLabel(self.groupBox_source_config)
        self.label_file_pattern.setObjectName(u"label_file_pattern")
        self.label_file_pattern.setMinimumSize(QSize(92, 0))

        self.horizontalLayout_13.addWidget(self.label_file_pattern)

        self.line_edit_file_pattern = QLineEdit(self.groupBox_source_config)
        self.line_edit_file_pattern.setObjectName(u"line_edit_file_pattern")
        self.line_edit_file_pattern.setMinimumSize(QSize(0, 0))
        self.line_edit_file_pattern.setClearButtonEnabled(True)

        self.horizontalLayout_13.addWidget(self.line_edit_file_pattern)


        self.verticalLayout_8.addLayout(self.horizontalLayout_13)


        self.verticalLayout_line_edits_3.addWidget(self.groupBox_source_config)


        self.verticalLayout_3.addWidget(self.input_frame)

        self.output_frame = QFrame(self.widget_top_main)
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
        self.verticalLayout_program_output.setContentsMargins(6, 6, 6, 6)
        self.groupBox_system_output = QGroupBox(self.output_frame)
        self.groupBox_system_output.setObjectName(u"groupBox_system_output")
        self.groupBox_system_output.setFont(font1)
        self.groupBox_system_output.setFlat(True)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_system_output)
        self.verticalLayout_10.setSpacing(4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 6, 0, 2)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_font_size_program_output = QLabel(self.groupBox_system_output)
        self.label_font_size_program_output.setObjectName(u"label_font_size_program_output")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_font_size_program_output.sizePolicy().hasHeightForWidth())
        self.label_font_size_program_output.setSizePolicy(sizePolicy4)

        self.horizontalLayout_16.addWidget(self.label_font_size_program_output)

        self.combobox_font_size_program_output = QComboBox(self.groupBox_system_output)
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.addItem("")
        self.combobox_font_size_program_output.setObjectName(u"combobox_font_size_program_output")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.combobox_font_size_program_output.sizePolicy().hasHeightForWidth())
        self.combobox_font_size_program_output.setSizePolicy(sizePolicy5)
        self.combobox_font_size_program_output.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_16.addWidget(self.combobox_font_size_program_output)

        self.button_clear_program_output = QPushButton(self.groupBox_system_output)
        self.button_clear_program_output.setObjectName(u"button_clear_program_output")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.button_clear_program_output.sizePolicy().hasHeightForWidth())
        self.button_clear_program_output.setSizePolicy(sizePolicy6)
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        self.button_clear_program_output.setFont(font2)
        self.button_clear_program_output.setMouseTracking(True)
        self.button_clear_program_output.setFlat(True)

        self.horizontalLayout_16.addWidget(self.button_clear_program_output)


        self.verticalLayout_10.addLayout(self.horizontalLayout_16)

        self.program_output = QTextEdit(self.groupBox_system_output)
        self.program_output.setObjectName(u"program_output")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.program_output.sizePolicy().hasHeightForWidth())
        self.program_output.setSizePolicy(sizePolicy7)
        self.program_output.setMinimumSize(QSize(0, 60))
        self.program_output.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"Consolas"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.program_output.setFont(font3)
        self.program_output.setStyleSheet(u"font: 10pt \"Consolas\";background: #0c0c0c;")
        self.program_output.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.program_output)

        self.progress_bar = QProgressBar(self.groupBox_system_output)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        self.verticalLayout_10.addWidget(self.progress_bar)


        self.verticalLayout_program_output.addWidget(self.groupBox_system_output)


        self.verticalLayout_3.addWidget(self.output_frame)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 4, -1, -1)
        self.pattern_list_frame = QFrame(self.widget_top_main)
        self.pattern_list_frame.setObjectName(u"pattern_list_frame")
        self.pattern_list_frame.setStyleSheet(u"\n"
"          QFrame#pattern_list_frame {\n"
"              background-color: #252526;\n"
"              border: 1px solid #3e3e42;\n"
"              border-radius: 6px;\n"
"          }\n"
"         ")
        self.pattern_list_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_item_widget_3 = QVBoxLayout(self.pattern_list_frame)
        self.verticalLayout_item_widget_3.setSpacing(6)
        self.verticalLayout_item_widget_3.setObjectName(u"verticalLayout_item_widget_3")
        self.verticalLayout_item_widget_3.setContentsMargins(6, 6, 6, 6)
        self.groupBox_search_patterns = QGroupBox(self.pattern_list_frame)
        self.groupBox_search_patterns.setObjectName(u"groupBox_search_patterns")
        self.groupBox_search_patterns.setFont(font1)
        self.groupBox_search_patterns.setStyleSheet(u"")
        self.groupBox_search_patterns.setFlat(True)
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_search_patterns)
        self.verticalLayout_7.setSpacing(4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 6, 0, 4)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(8)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_string_to_regex = QLabel(self.groupBox_search_patterns)
        self.label_string_to_regex.setObjectName(u"label_string_to_regex")
        self.label_string_to_regex.setMinimumSize(QSize(90, 0))
        self.label_string_to_regex.setFont(font)

        self.horizontalLayout_14.addWidget(self.label_string_to_regex)

        self.line_edit_string_to_regex = QLineEdit(self.groupBox_search_patterns)
        self.line_edit_string_to_regex.setObjectName(u"line_edit_string_to_regex")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.line_edit_string_to_regex.sizePolicy().hasHeightForWidth())
        self.line_edit_string_to_regex.setSizePolicy(sizePolicy8)
        self.line_edit_string_to_regex.setMinimumSize(QSize(0, 0))
        self.line_edit_string_to_regex.setClearButtonEnabled(True)

        self.horizontalLayout_14.addWidget(self.line_edit_string_to_regex)

        self.button_string_to_regex = QPushButton(self.groupBox_search_patterns)
        self.button_string_to_regex.setObjectName(u"button_string_to_regex")
        sizePolicy5.setHeightForWidth(self.button_string_to_regex.sizePolicy().hasHeightForWidth())
        self.button_string_to_regex.setSizePolicy(sizePolicy5)
        self.button_string_to_regex.setMinimumSize(QSize(0, 0))
        self.button_string_to_regex.setMaximumSize(QSize(16777215, 16777215))
        self.button_string_to_regex.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/images/convert.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_string_to_regex.setIcon(icon1)
        self.button_string_to_regex.setIconSize(QSize(14, 14))

        self.horizontalLayout_14.addWidget(self.button_string_to_regex)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(8)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_regex = QLabel(self.groupBox_search_patterns)
        self.label_regex.setObjectName(u"label_regex")
        self.label_regex.setMinimumSize(QSize(90, 0))
        self.label_regex.setFont(font)

        self.horizontalLayout_15.addWidget(self.label_regex)

        self.line_edit_regex = QLineEdit(self.groupBox_search_patterns)
        self.line_edit_regex.setObjectName(u"line_edit_regex")
        self.line_edit_regex.setMinimumSize(QSize(0, 0))
        self.line_edit_regex.setClearButtonEnabled(True)

        self.horizontalLayout_15.addWidget(self.line_edit_regex)

        self.button_add_regex_to_list_widget = QPushButton(self.groupBox_search_patterns)
        self.button_add_regex_to_list_widget.setObjectName(u"button_add_regex_to_list_widget")
        self.button_add_regex_to_list_widget.setMinimumSize(QSize(0, 0))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(10)
        font4.setWeight(QFont.DemiBold)
        font4.setItalic(False)
        self.button_add_regex_to_list_widget.setFont(font4)
        self.button_add_regex_to_list_widget.setStyleSheet(u"")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.button_add_regex_to_list_widget.setIcon(icon2)
        self.button_add_regex_to_list_widget.setIconSize(QSize(16, 16))
        self.button_add_regex_to_list_widget.setAutoDefault(False)
        self.button_add_regex_to_list_widget.setFlat(False)

        self.horizontalLayout_15.addWidget(self.button_add_regex_to_list_widget)


        self.verticalLayout_7.addLayout(self.horizontalLayout_15)


        self.verticalLayout_item_widget_3.addWidget(self.groupBox_search_patterns)

        self.groupBox_active_patterns = QGroupBox(self.pattern_list_frame)
        self.groupBox_active_patterns.setObjectName(u"groupBox_active_patterns")
        self.groupBox_active_patterns.setFont(font1)
        self.groupBox_active_patterns.setFlat(True)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_active_patterns)
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 6, 0, 2)
        self.list_widget_regex = QListWidget(self.groupBox_active_patterns)
        self.list_widget_regex.setObjectName(u"list_widget_regex")
        sizePolicy7.setHeightForWidth(self.list_widget_regex.sizePolicy().hasHeightForWidth())
        self.list_widget_regex.setSizePolicy(sizePolicy7)
        self.list_widget_regex.setMinimumSize(QSize(0, 100))
        self.list_widget_regex.setMaximumSize(QSize(16777215, 16777215))
        self.list_widget_regex.setStyleSheet(u"")
        self.list_widget_regex.setAlternatingRowColors(True)
        self.list_widget_regex.setResizeMode(QListView.ResizeMode.Fixed)

        self.verticalLayout_9.addWidget(self.list_widget_regex)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.button_regex_pattern_remove_selected = QPushButton(self.groupBox_active_patterns)
        self.button_regex_pattern_remove_selected.setObjectName(u"button_regex_pattern_remove_selected")
        self.button_regex_pattern_remove_selected.setFont(font1)
        icon3 = QIcon()
        icon3.addFile(u":/images/remove-selected.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_regex_pattern_remove_selected.setIcon(icon3)

        self.horizontalLayout_17.addWidget(self.button_regex_pattern_remove_selected)

        self.button_regex_pattern_remove_all = QPushButton(self.groupBox_active_patterns)
        self.button_regex_pattern_remove_all.setObjectName(u"button_regex_pattern_remove_all")
        self.button_regex_pattern_remove_all.setFont(font1)
        icon4 = QIcon()
        icon4.addFile(u":/images/remove-all.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_regex_pattern_remove_all.setIcon(icon4)

        self.horizontalLayout_17.addWidget(self.button_regex_pattern_remove_all)


        self.verticalLayout_9.addLayout(self.horizontalLayout_17)


        self.verticalLayout_item_widget_3.addWidget(self.groupBox_active_patterns)


        self.verticalLayout_4.addWidget(self.pattern_list_frame)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout_Top.addWidget(self.widget_top_main)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_Bottom = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_Bottom.setObjectName(u"verticalLayout_Bottom")
        self.verticalLayout_Bottom.setContentsMargins(0, 0, 0, 0)
        self.widget_bottom_table = QWidget(self.verticalLayoutWidget_2)
        self.widget_bottom_table.setObjectName(u"widget_bottom_table")
        self.widget_bottom_table.setMinimumSize(QSize(0, 500))
        self.verticalLayout_5 = QVBoxLayout(self.widget_bottom_table)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_table = QHBoxLayout()
        self.horizontalLayout_table.setObjectName(u"horizontalLayout_table")
        self.horizontalLayout_table.setContentsMargins(-1, 4, -1, -1)
        self.results_frame = QFrame(self.widget_bottom_table)
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
        self.verticalLayout_table_widget.setContentsMargins(6, 6, 6, 6)
        self.groupBox_table = QGroupBox(self.results_frame)
        self.groupBox_table.setObjectName(u"groupBox_table")
        self.groupBox_table.setFlat(True)
        self.verticalLayout = QVBoxLayout(self.groupBox_table)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 6, 0, 2)
        self.horizontalLayout_table_settings = QHBoxLayout()
        self.horizontalLayout_table_settings.setSpacing(12)
        self.horizontalLayout_table_settings.setObjectName(u"horizontalLayout_table_settings")
        self.button_start_search = QPushButton(self.groupBox_table)
        self.button_start_search.setObjectName(u"button_start_search")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.button_start_search.sizePolicy().hasHeightForWidth())
        self.button_start_search.setSizePolicy(sizePolicy9)
        self.button_start_search.setMinimumSize(QSize(0, 0))
        self.button_start_search.setMaximumSize(QSize(16777215, 25))
        self.button_start_search.setFont(font)
        icon5 = QIcon()
        icon5.addFile(u":/images/search-file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_start_search.setIcon(icon5)
        self.button_start_search.setIconSize(QSize(24, 24))

        self.horizontalLayout_table_settings.addWidget(self.button_start_search)

        self.line = QFrame(self.groupBox_table)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_table_settings.addWidget(self.line)

        self.label_3 = QLabel(self.groupBox_table)
        self.label_3.setObjectName(u"label_3")
        sizePolicy4.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy4)
        self.label_3.setFont(font)

        self.horizontalLayout_table_settings.addWidget(self.label_3)

        self.spinbox_rows = QSpinBox(self.groupBox_table)
        self.spinbox_rows.setObjectName(u"spinbox_rows")
        self.spinbox_rows.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.spinbox_rows.sizePolicy().hasHeightForWidth())
        self.spinbox_rows.setSizePolicy(sizePolicy5)
        self.spinbox_rows.setMinimumSize(QSize(0, 0))
        self.spinbox_rows.setStyleSheet(u"")
        self.spinbox_rows.setMinimum(0)
        self.spinbox_rows.setMaximum(10000)
        self.spinbox_rows.setValue(0)
        self.spinbox_rows.setDisplayIntegerBase(10)

        self.horizontalLayout_table_settings.addWidget(self.spinbox_rows)

        self.checkbox_limit_rows = QCheckBox(self.groupBox_table)
        self.checkbox_limit_rows.setObjectName(u"checkbox_limit_rows")
        sizePolicy6.setHeightForWidth(self.checkbox_limit_rows.sizePolicy().hasHeightForWidth())
        self.checkbox_limit_rows.setSizePolicy(sizePolicy6)

        self.horizontalLayout_table_settings.addWidget(self.checkbox_limit_rows)

        self.line_2 = QFrame(self.groupBox_table)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_table_settings.addWidget(self.line_2)

        self.checkbox_multiline_search = QCheckBox(self.groupBox_table)
        self.checkbox_multiline_search.setObjectName(u"checkbox_multiline_search")
        sizePolicy6.setHeightForWidth(self.checkbox_multiline_search.sizePolicy().hasHeightForWidth())
        self.checkbox_multiline_search.setSizePolicy(sizePolicy6)

        self.horizontalLayout_table_settings.addWidget(self.checkbox_multiline_search)

        self.checkbox_enable_parallel_processing = QCheckBox(self.groupBox_table)
        self.checkbox_enable_parallel_processing.setObjectName(u"checkbox_enable_parallel_processing")
        sizePolicy6.setHeightForWidth(self.checkbox_enable_parallel_processing.sizePolicy().hasHeightForWidth())
        self.checkbox_enable_parallel_processing.setSizePolicy(sizePolicy6)

        self.horizontalLayout_table_settings.addWidget(self.checkbox_enable_parallel_processing)

        self.button_parallel_processing_info = QPushButton(self.groupBox_table)
        self.button_parallel_processing_info.setObjectName(u"button_parallel_processing_info")
        self.button_parallel_processing_info.setMaximumSize(QSize(30, 16777215))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setKerning(True)
        self.button_parallel_processing_info.setFont(font5)
        self.button_parallel_processing_info.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogInformation))
        self.button_parallel_processing_info.setIcon(icon6)
        self.button_parallel_processing_info.setAutoDefault(False)
        self.button_parallel_processing_info.setFlat(False)

        self.horizontalLayout_table_settings.addWidget(self.button_parallel_processing_info)


        self.verticalLayout.addLayout(self.horizontalLayout_table_settings)

        self.table_widget_results = QTableView(self.groupBox_table)
        self.table_widget_results.setObjectName(u"table_widget_results")
        self.table_widget_results.setEnabled(True)
        sizePolicy7.setHeightForWidth(self.table_widget_results.sizePolicy().hasHeightForWidth())
        self.table_widget_results.setSizePolicy(sizePolicy7)
        self.table_widget_results.setMinimumSize(QSize(0, 100))
        self.table_widget_results.setSortingEnabled(True)
        self.table_widget_results.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.table_widget_results)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_filter_text = QLabel(self.groupBox_table)
        self.label_filter_text.setObjectName(u"label_filter_text")

        self.horizontalLayout_21.addWidget(self.label_filter_text)

        self.line_edit_filter_table_text = QLineEdit(self.groupBox_table)
        self.line_edit_filter_table_text.setObjectName(u"line_edit_filter_table_text")

        self.horizontalLayout_21.addWidget(self.line_edit_filter_table_text)


        self.verticalLayout.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.button_search_result_export_to_csv = QPushButton(self.groupBox_table)
        self.button_search_result_export_to_csv.setObjectName(u"button_search_result_export_to_csv")
        self.button_search_result_export_to_csv.setEnabled(True)
        self.button_search_result_export_to_csv.setFont(font1)
        icon7 = QIcon()
        icon7.addFile(u":/images/export-to-file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_search_result_export_to_csv.setIcon(icon7)

        self.horizontalLayout_23.addWidget(self.button_search_result_export_to_csv)

        self.button_search_result_clear_results = QPushButton(self.groupBox_table)
        self.button_search_result_clear_results.setObjectName(u"button_search_result_clear_results")
        self.button_search_result_clear_results.setFont(font1)
        self.button_search_result_clear_results.setIcon(icon4)

        self.horizontalLayout_23.addWidget(self.button_search_result_clear_results)

        self.line_3 = QFrame(self.groupBox_table)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_23.addWidget(self.line_3)

        self.combobox_count_occurrences = QComboBox(self.groupBox_table)
        self.combobox_count_occurrences.setObjectName(u"combobox_count_occurrences")

        self.horizontalLayout_23.addWidget(self.combobox_count_occurrences)

        self.button_count_occurrences = QPushButton(self.groupBox_table)
        self.button_count_occurrences.setObjectName(u"button_count_occurrences")
        self.button_count_occurrences.setFont(font1)

        self.horizontalLayout_23.addWidget(self.button_count_occurrences)


        self.verticalLayout.addLayout(self.horizontalLayout_23)


        self.verticalLayout_table_widget.addWidget(self.groupBox_table)


        self.horizontalLayout_table.addWidget(self.results_frame)


        self.verticalLayout_5.addLayout(self.horizontalLayout_table)


        self.verticalLayout_Bottom.addWidget(self.widget_bottom_table)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_6.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1358, 33))
        self.menuOpen = QMenu(self.menubar)
        self.menuOpen.setObjectName(u"menuOpen")
        self.menuAutofill = QMenu(self.menubar)
        self.menuAutofill.setObjectName(u"menuAutofill")
        self.menuManage = QMenu(self.menubar)
        self.menuManage.setObjectName(u"menuManage")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuAutofill.menuAction())
        self.menubar.addAction(self.menuManage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuOpen.addAction(self.actionOpen_Input_Folder)
        self.menuOpen.addAction(self.actionOpen_Output_Folder)
        self.menuManage.addAction(self.actionOpen_Regex_Expression_Manager)
        self.menuHelp.addAction(self.actionRegex_101)
        self.menuHelp.addAction(self.actionRegex_Cheatsheet)

        self.retranslateUi(MainWindow)

        self.button_clear_program_output.setDefault(False)
        self.button_add_regex_to_list_widget.setDefault(False)
        self.button_parallel_processing_info.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_Input_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Input Folder", None))
        self.actionOpen_Output_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Output Folder", None))
        self.actionRegex_101.setText(QCoreApplication.translate("MainWindow", u"Regex 101", None))
        self.actionRegex_Cheatsheet.setText(QCoreApplication.translate("MainWindow", u"Regex Cheatsheet", None))
        self.actionOpen_Regex_Expression_Manager.setText(QCoreApplication.translate("MainWindow", u"Open Regex Expression Manager", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"Log File Search & Analysis", None))
        self.groupBox_source_config.setTitle(QCoreApplication.translate("MainWindow", u"Source Configuration", None))
        self.label_files_folder.setText(QCoreApplication.translate("MainWindow", u"Folder Path:", None))
        self.line_edit_files_folder.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select a folder containing log files to search...", None))
        self.button_browse_folder.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_file_pattern.setText(QCoreApplication.translate("MainWindow", u"File Pattern:", None))
        self.line_edit_file_pattern.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(Optional) Enter patterns to search only specific files (wildcard * accepted and comma-separated)", None))
        self.groupBox_system_output.setTitle(QCoreApplication.translate("MainWindow", u"System Output", None))
        self.label_font_size_program_output.setText(QCoreApplication.translate("MainWindow", u"Font Size:", None))
        self.combobox_font_size_program_output.setItemText(0, QCoreApplication.translate("MainWindow", u"10pt", None))
        self.combobox_font_size_program_output.setItemText(1, QCoreApplication.translate("MainWindow", u"11pt", None))
        self.combobox_font_size_program_output.setItemText(2, QCoreApplication.translate("MainWindow", u"12pt", None))
        self.combobox_font_size_program_output.setItemText(3, QCoreApplication.translate("MainWindow", u"13pt", None))
        self.combobox_font_size_program_output.setItemText(4, QCoreApplication.translate("MainWindow", u"14pt", None))
        self.combobox_font_size_program_output.setItemText(5, QCoreApplication.translate("MainWindow", u"15pt", None))
        self.combobox_font_size_program_output.setItemText(6, QCoreApplication.translate("MainWindow", u"16pt", None))

#if QT_CONFIG(tooltip)
        self.button_clear_program_output.setToolTip(QCoreApplication.translate("MainWindow", u"Clears the output area", None))
#endif // QT_CONFIG(tooltip)
        self.button_clear_program_output.setText(QCoreApplication.translate("MainWindow", u"Clear Output", None))
        self.program_output.setPlaceholderText(QCoreApplication.translate("MainWindow", u"System output and status messages will appear here...", None))
        self.progress_bar.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.groupBox_search_patterns.setTitle(QCoreApplication.translate("MainWindow", u"Search Pattern Setup", None))
        self.label_string_to_regex.setText(QCoreApplication.translate("MainWindow", u"Literal String:", None))
        self.line_edit_string_to_regex.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter plain text to convert to regex pattern...", None))
        self.button_string_to_regex.setText(QCoreApplication.translate("MainWindow", u"Convert", None))
        self.label_regex.setText(QCoreApplication.translate("MainWindow", u"Regex Pattern:", None))
        self.line_edit_regex.setText("")
        self.line_edit_regex.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter or generate regular expression pattern...", None))
#if QT_CONFIG(tooltip)
        self.button_add_regex_to_list_widget.setToolTip(QCoreApplication.translate("MainWindow", u"Add the entered Regex to the list.", None))
#endif // QT_CONFIG(tooltip)
        self.button_add_regex_to_list_widget.setText(QCoreApplication.translate("MainWindow", u"Add Pattern", None))
        self.groupBox_active_patterns.setTitle(QCoreApplication.translate("MainWindow", u"Active Search Patterns", None))
#if QT_CONFIG(tooltip)
        self.button_regex_pattern_remove_selected.setToolTip(QCoreApplication.translate("MainWindow", u"Remove the selected Regex from the list", None))
#endif // QT_CONFIG(tooltip)
        self.button_regex_pattern_remove_selected.setText(QCoreApplication.translate("MainWindow", u"Remove Selected", None))
#if QT_CONFIG(tooltip)
        self.button_regex_pattern_remove_all.setToolTip(QCoreApplication.translate("MainWindow", u"Remove all Regexes from list", None))
#endif // QT_CONFIG(tooltip)
        self.button_regex_pattern_remove_all.setText(QCoreApplication.translate("MainWindow", u"Remove All", None))
        self.groupBox_table.setTitle(QCoreApplication.translate("MainWindow", u"Search Results and Configuration", None))
#if QT_CONFIG(tooltip)
        self.button_start_search.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Start search with the current settings and display data into the table.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.button_start_search.setText(QCoreApplication.translate("MainWindow", u"Start Search", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Rows:", None))
        self.checkbox_limit_rows.setText(QCoreApplication.translate("MainWindow", u"Limit Rows", None))
#if QT_CONFIG(tooltip)
        self.checkbox_multiline_search.setToolTip(QCoreApplication.translate("MainWindow", u"Literal ^ matches the start of the line, and $ matches the end of the line.", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_multiline_search.setText(QCoreApplication.translate("MainWindow", u"Enable multiline regex search ", None))
#if QT_CONFIG(tooltip)
        self.checkbox_enable_parallel_processing.setToolTip(QCoreApplication.translate("MainWindow", u"Enables parallel processing, useful for big files.", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_enable_parallel_processing.setText(QCoreApplication.translate("MainWindow", u"Enable parallel processing", None))
#if QT_CONFIG(tooltip)
        self.button_parallel_processing_info.setToolTip(QCoreApplication.translate("MainWindow", u"Show parallel processing help information.", None))
#endif // QT_CONFIG(tooltip)
        self.button_parallel_processing_info.setText("")
        self.label_filter_text.setText(QCoreApplication.translate("MainWindow", u"Filter Text:", None))
#if QT_CONFIG(tooltip)
        self.button_search_result_export_to_csv.setToolTip(QCoreApplication.translate("MainWindow", u"Exports the current displayed data to Excel.\n"
"If the table is using a text filter, ONLY the filtered data will be exported!", None))
#endif // QT_CONFIG(tooltip)
        self.button_search_result_export_to_csv.setText(QCoreApplication.translate("MainWindow", u"Export to Excel", None))
#if QT_CONFIG(tooltip)
        self.button_search_result_clear_results.setToolTip(QCoreApplication.translate("MainWindow", u"Clears all data from the table", None))
#endif // QT_CONFIG(tooltip)
        self.button_search_result_clear_results.setText(QCoreApplication.translate("MainWindow", u"Clear Table", None))
        self.combobox_count_occurrences.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Choose a column to count occurrences...", None))
#if QT_CONFIG(tooltip)
        self.button_count_occurrences.setToolTip(QCoreApplication.translate("MainWindow", u"Count occurrences based on the key and display the new data into the table", None))
#endif // QT_CONFIG(tooltip)
        self.button_count_occurrences.setText(QCoreApplication.translate("MainWindow", u"Count Occurrences", None))
        self.menuOpen.setTitle(QCoreApplication.translate("MainWindow", u"Open", None))
        self.menuAutofill.setTitle(QCoreApplication.translate("MainWindow", u"Autofill", None))
        self.menuManage.setTitle(QCoreApplication.translate("MainWindow", u"Manage", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

