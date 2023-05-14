import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import random
import sys
import threading
import pickle
import re
import numpy
import matplotlib

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextFormat, QColor, QPalette, QTextBlockFormat
import os
from pathlib import Path
import qdarktheme
from PyQt5.QtWidgets import QTextEdit, QToolTip

from source.GUI.BrowseDirectory import New_Project_UI
from source.GUI.DeleteFiles import DeleteFiles_UI
from source.GUI.QCodeEditor import Highlighter
from source.GUI.QCodeEditor import CodeEditor, WaveViewer
from source.Engine.EngineChecker import *
from source.Report_Generator.ReportGenerator import *

import time


class OpenFile(QtCore.QThread):
    Editor_text = QtCore.pyqtSignal(str)
    Itsdone = QtCore.pyqtSignal(int)
    design_file = ""
    finish = 0

    def init(self):
        super(OpenFile, self).init()

    def run(self):
        old_file_list = []
        new_file_list = []
        while True:
            if self.finish:
                break
            if os.path.isfile(self.design_file):
                with open(self.design_file) as File_Read:
                    new_file_list = File_Read.readlines()
                    if not (new_file_list == old_file_list):
                        for line in new_file_list:
                            if line != "\n":
                                line = re.sub("\n", "", line)
                            else:
                                line = " "
                            self.Editor_text.emit(line)
                        old_file_list = new_file_list
                    else:
                        self.Itsdone.emit(1)
                        return


class MainWindow_UI(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1273, 882)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.PD_LABEL = QtWidgets.QLabel(self.centralwidget)
        self.PD_LABEL.setObjectName("PD_LABEL")
        self.verticalLayout_4.addWidget(self.PD_LABEL)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.work_space_tree = QtWidgets.QTreeWidget(self.centralwidget)
        self.work_space_tree.setMinimumSize(QtCore.QSize(0, 350))
        self.work_space_tree.setObjectName("work_space_tree")
        self.verticalLayout_2.addWidget(self.work_space_tree)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.charts = WaveViewer(self.centralwidget)
        self.charts.setAutoFillBackground(True)
        self.charts.setStyleSheet("")
        self.charts.setObjectName("charts")
        self.verticalLayout_2.addWidget(self.charts)
        self.verticalLayout_2.setStretch(0, 40)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 24)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.svCodeEDitor = CodeEditor(self.centralwidget)
        self.svCodeEDitor.setObjectName("svCodeEDitor")
        self.verticalLayout_3.addWidget(self.svCodeEDitor)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.terminal = QtWidgets.QTextBrowser(self.centralwidget)
        self.terminal.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.terminal.setPlaceholderText("")
        self.terminal.setObjectName("terminal")
        self.verticalLayout.addWidget(self.terminal)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.setStretch(0, 20)
        self.verticalLayout_3.setStretch(1, 13)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 6)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1273, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menusettings = QtWidgets.QMenu(self.menubar)
        self.menusettings.setObjectName("menusettings")
        self.menuthem = QtWidgets.QMenu(self.menusettings)
        self.menuthem.setObjectName("menuthem")
        self.menuSimulate = QtWidgets.QMenu(self.menubar)
        self.menuSimulate.setObjectName("menuSimulate")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHELP")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionLight = QtWidgets.QAction(MainWindow)
        self.actionLight.setObjectName("actionLight")
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.actionClose_Project = QtWidgets.QAction(MainWindow)
        self.actionClose_Project.setObjectName("actionClose_Project")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionClose_Project)
        self.menuthem.addSeparator()
        self.menuthem.addAction(self.actionLight)
        self.menuthem.addAction(self.actionDark)
        self.menusettings.addAction(self.menuthem.menuAction())
        self.menuSimulate.addAction(self.actionStart)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menusettings.menuAction())
        self.menubar.addAction(self.menuSimulate.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def __init__(self):
        super(MainWindow_UI, self).__init__()
        self.setupUi(self)
        self.current_index = None
        self.Results = None
        self.files_button = None
        self.path = None
        self.New_Project_ui = New_Project_UI()
        self.Delete_project_ui = DeleteFiles_UI()
        self.directory_path = ""
        self.projectName = ""
        self.design_files = []
        self.simulation_results = []
        self.selections = []
        self.dark = 0
        self.autotexts = None
        self.texts = None
        self.openFileThread = OpenFile()
        # connect the functions
        self.actionNew_Project.triggered.connect(self.new_project)
        self.New_Project_ui.Directory_text.connect(self.Project_Directory)
        self.New_Project_ui.Name_text.connect(self.project_name)
        self.Delete_project_ui.Delete_Signal.connect(self.removeItem)
        self.actionDark.triggered.connect(self.setDarkMode)
        self.actionLight.triggered.connect(self.setLightMode)
        self.actionStart.triggered.connect(self.start_simulation)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.openFileThread.Editor_text.connect(self.PrintCode)
        self.openFileThread.Itsdone.connect(self.Highlight_everword)
        self.highlighter = Highlighter(self.svCodeEDitor.document())
        self.actionClose_Project.triggered.connect(self.closeProject)
        self.actionAbout.triggered.connect(self.show_info)
        # initialize Widgets
        self.svCodeEDitor.setReadOnly(True)
        font = QFont('Consolas', 12)
        self.svCodeEDitor.setFont(font)
        font = QFont('Consolas', 10)
        self.terminal.setFont(font)
        self.work_space_tree.itemDoubleClicked.connect(self.handle_double_click)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PD_LABEL.setText(_translate("MainWindow", "Project Name-Directory"))
        self.work_space_tree.headerItem().setText(0, _translate("MainWindow", "Name"))
        self.work_space_tree.headerItem().setText(1, _translate("MainWindow", "Status"))
        self.label_2.setText(_translate("MainWindow", "Results Pie"))
        self.label.setText(_translate("MainWindow", "Output Console"))
        self.terminal.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menusettings.setTitle(_translate("MainWindow", "settings"))
        self.menuthem.setTitle(_translate("MainWindow", "Theme"))
        self.menuSimulate.setTitle(_translate("MainWindow", "Simulate"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.actionClose_Project.setText(_translate("MainWindow", "Close Project"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def new_project(self):
        self.New_Project_ui.show()

    def dump_data(self):
        data_to_send = [self.design_files, self.directory_path, self.projectName, self.Results]
        with open(self.directory_path + "/" + re.sub(" ", "", self.projectName) + ".PSG", 'wb') as temp_data:
            pickle.dump(data_to_send, temp_data)

    def closeProject(self):
        self.terminal.clear()
        self.svCodeEDitor.clear()
        self.design_files = []
        self.projectName = ""
        self.texts = None
        self.autotexts = None
        self.directory_path = ""
        self.work_space_tree.clear()
        self.selections = []
        self.charts.canvas.axes.clear()
        self.charts.canvas.draw()
        self.PD_LABEL.clear()
        self.openFileThread.design_file = ""
        self.svCodeEDitor.line_written = []
        self.svCodeEDitor.setExtraSelections([])
        self.Results = []

    def show_msg_box(self, msg: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(msg)
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        x = msg_box.exec_()

    def show_info(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Info")
        font = QtGui.QFont("Times New Roman", 12, QtGui.QFont.Bold)
        msg_box.setFont(font)
        msg_box.setText("PSG(Py synthesis Guard)")
        font = QtGui.QFont("Times New Roman", 10, QtGui.QFont.Bold)
        msg_box.setFont(font)
        msg_box.setInformativeText("Version: 1.00\nGitHub Repo link:https://github.com/1mina1/PSG-PySynthesisGuard-")
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        x = msg_box.exec_()

    def Highlight_everword(self, signal):
        if signal:
            self.selections = []
            if self.Results:
                results = self.Results[self.current_index]
                self.svCodeEDitor.line_written = self.Arrange_lines_errors(results)
                for lines in results["Error line"]:
                    for lines_2 in lines:
                        if isinstance(lines_2, list):
                            for lines_3 in lines_2:
                                if isinstance(lines_3, list):
                                    for lines_4 in lines_3:
                                        self.highlightLine(lines_4)
                                else:
                                    self.highlightLine(lines_3)
                        else:
                            self.highlightLine(lines_2)

    def handle_double_click(self, item):
        self.svCodeEDitor.clear()
        self.svCodeEDitor.setExtraSelections([])
        self.svCodeEDitor.line_written = []
        self.openFileThread.finish = 1
        self.openFileThread.exit()
        self.openFileThread.design_file = self.directory_path + "/" + item.text(0)
        self.openFileThread.finish = 0
        self.openFileThread.start()
        self.current_index = self.design_files.index(item.text(0))

    def start_simulation(self):
        if self.design_files:
            self.Results = []
            for design in self.design_files:
                Checker = Checks(self.directory_path + "/" + design)
                Checker.do_all_checks()
                RG = ReportGenerator(Checker.error_panel, Checker.module_name, self.directory_path)
                self.Results.append(Checker.error_panel)
                self.print_console()
            mylabels = self.Results[0]["Type"]
            mycolors = ["green", "skyblue", "orange", "red", "purple", "brown", "gray", "pink"]
            Total_errors = [0, 0, 0, 0, 0, 0, 0, 0]
            self.charts.canvas.axes.clear()
            for result in self.Results:
                for i in range(len(result["Num errors"])):
                    Total_errors[i] += result["Num errors"][i]
            if sum(Total_errors) != 0:
                wedges, self.texts, self.autotexts = self.charts.canvas.axes.pie(Total_errors, colors=mycolors,
                                                                                 autopct="%.2f",
                                                                                 textprops={'fontsize': 8})
            else:
                y = [100]
                mylabels = ["All Good"]
                mycolors = ["green"]
                wedges, self.texts, self.autotexts = self.charts.canvas.axes.pie(y, colors=mycolors,
                                                                                 autopct="%.2f",
                                                                                 textprops={'fontsize': 8})
            self.charts.canvas.axes.legend(wedges, mylabels, loc="center right", bbox_to_anchor=(0.08, 0.6),
                                           prop={'size': 6})
            self.charts.canvas.draw()
            icon_v = QtGui.QIcon(absolutePath("Icons/Ready.png"))
            for i in range(self.work_space_tree.topLevelItemCount()):
                item = self.work_space_tree.topLevelItem(i)
                item.setIcon(1, icon_v)
            if self.dark:
                self.setDarkMode()
            else:
                self.setLightMode()
            self.selections = []
            current_file = re.sub(self.directory_path + "/", "", self.openFileThread.design_file)
            if current_file in self.design_files:
                index = self.design_files.index(current_file)
                results = self.Results[index]
                self.svCodeEDitor.line_written = self.Arrange_lines_errors(results)
                for lines in results["Error line"]:
                    for lines_2 in lines:
                        if isinstance(lines_2, list):
                            for lines_3 in lines_2:
                                if isinstance(lines_3, list):
                                    for lines_4 in lines_3:
                                        self.highlightLine(lines_4)
                                else:
                                    self.highlightLine(lines_3)
                        else:
                            self.highlightLine(lines_2)
            self.dump_data()
        else:
            self.show_msg_box("you need to insert your design")

    def removeItem(self, flag):
        Item = self.work_space_tree.currentItem()
        if Item is None:
            self.show_msg_box(msg="there is no file selected")
        else:
            if self.openFileThread.design_file == self.directory_path + "/" + Item.text(0):
                self.svCodeEDitor.clear()
                self.openFileThread.finish = 1
                self.openFileThread.exit()
                self.design_files.remove(Item.text(0))
                self.openFileThread.design_file = ""
            if flag == 1:
                file = self.directory_path + "/" + Item.text(0)
                print(file)
                os.remove(file.replace("/", "\\"))
            self.work_space_tree.topLevelItem(0).removeChild(Item)

    def PrintCode(self, line):
        self.svCodeEDitor.appendPlainText(line)

    def print_console(self):
        with open(self.directory_path + "/" + "Lint_check_rpt.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            line = re.sub("\n", "", line)
            self.terminal.append(line)

    def Project_Directory(self, Path: str):
        self.directory_path = Path

    def open_project(self):
        project = QtWidgets.QFileDialog.getOpenFileNames(None)
        if not project:
            return
        for prj in project[0]:
            extension = re.sub(".+\.", "", prj)
            if not (extension == "PSG"):
                self.show_msg_box("this is not a PSG supported project")
                return
            with open(prj, 'rb') as temp_data:
                self.design_files, self.directory_path, self.projectName, self.Results = pickle.load(temp_data)
            self.PD_LABEL.setText(self.projectName + "-" + str(self.directory_path))
            for file in self.design_files:
                extension = re.sub(r".+\.", "", file)
                a = QtWidgets.QTreeWidgetItem([str(file)])
                if extension == "v":
                    icon_v = QtGui.QIcon(absolutePath("Icons/verilog.png"))
                    a.setIcon(0, icon_v)
                else:
                    icon_v = QtGui.QIcon(absolutePath("Icons/systemverilog.png"))
                    a.setIcon(0, icon_v)
                icon_v = QtGui.QIcon(absolutePath("Icons/notready.png"))
                a.setIcon(1, icon_v)
                self.work_space_tree.addTopLevelItem(a)

    def project_name(self, Name: str):
        self.PD_LABEL.setText(Name + "-" + str(self.directory_path))
        self.projectName = Name
        self.terminal.clear()
        self.svCodeEDitor.clear()
        self.design_files = []
        self.texts = None
        self.autotexts = None
        self.work_space_tree.clear()
        self.selections = []
        self.charts.canvas.axes.clear()
        self.charts.canvas.draw()
        self.svCodeEDitor.line_written = []
        self.openFileThread.design_file = ""
        self.svCodeEDitor.setExtraSelections([])
        self.svCodeEDitor.line_written = []
        self.Results = []
        self.dump_data()

    def Arrange_lines_errors(self, results):
        results_dic = {}
        # arithmetic overflow
        for i in range(len(results["Error line"][0])):
            if results["Error line"][0][i] in results_dic:
                results_dic[results["Error line"][0][i]] += "-- Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])
            else:
                results_dic[results["Error line"][0][i]] = "Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])
        for i in range(len(results["Error line"][1])):
            if results["Error line"][1][i] in results_dic:
                results_dic[results["Error line"][1][i]] += "-- unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][1][i])):
                    results_dic[results["Error line"][1][i]] += str(results["variable Impacted"][1][i][j]) + " "
            else:
                results_dic[results["Error line"][1][i]] = "unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][1][i])):
                    results_dic[results["Error line"][1][i]] += str(results["variable Impacted"][1][i][j]) + " "
        for i in range(len(results["Error line"][2])):
            if results["Error line"][2][i] in results_dic:
                results_dic[results["Error line"][2][i]] += "-- unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"
            else:
                results_dic[results["Error line"][2][i]] = "unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"
        for i in range(len(results["Error line"][3])):
            if results["Error line"][3][i] in results_dic:
                results_dic[results["Error line"][3][i]] += "-- uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])
            else:
                results_dic[results["Error line"][3][i]] = "uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])
        for i in range(len(results["variable Impacted"][4])):
            for line in results["Error line"][4][i]:
                if line in results_dic:
                    results_dic[line] += "-- multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])
                else:
                    results_dic[line] = "multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])
        print(results_dic)
        for i in range(len(results["Error line"][5])):
            if results["Error line"][5][i] in results_dic:
                results_dic[results["Error line"][5][i]] += "-- Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][5][i])):
                    results_dic[results["Error line"][5][i]] += str(results["variable Impacted"][5][i][j]) + " "
            else:
                results_dic[results["Error line"][5][i]] = "Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][5][i])):
                    results_dic[results["Error line"][5][i]] += str(results["variable Impacted"][5][i][j]) + " "
        print(results_dic)
        for i in range(len(results["Error line"][6])):
            if results["Error line"][6][i] in results_dic:
                results_dic[results["Error line"][6][i]] += "--Non parallel case statement at line " + str(
                    results["Error line"][6][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][6][i])):
                    results_dic[results["Error line"][6][i]] += str(results["variable Impacted"][6][i][j]) + " "
            else:
                results_dic[results["Error line"][6][i]] = "Non parallel case statement at line " + str(
                    results["Error line"][6][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][6][i])):
                    results_dic[results["Error line"][6][i]] += str(results["variable Impacted"][6][i][j]) + " "
        for i in range(len(results["variable Impacted"][7])):
            for line in results["Error line"][7][i]:
                if line in results_dic:
                    results_dic[line] += "-- latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][7][i])
                else:
                    results_dic[line] = "latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][7][i])
        return results_dic

    def setDarkMode(self):
        qdarktheme.setup_theme()
        self.dark = 1
        if self.autotexts:
            for ins in self.autotexts:
                ins.set_color('white')
        if self.texts:
            for ins in self.texts:
                ins.set_color('white')
        self.charts.canvas.axes.set_facecolor("black")
        self.charts.canvas.figure.set_facecolor("black")
        self.charts.canvas.draw()

    def setLightMode(self):
        qdarktheme.setup_theme("light")
        self.dark = 0
        if self.autotexts:
            for ins in self.autotexts:
                ins.set_color('white')
        if self.texts:
            for ins in self.texts:
                ins.set_color('black')
        self.charts.canvas.axes.set_facecolor("white")
        self.charts.canvas.figure.set_facecolor("white")
        self.charts.canvas.draw()

    def highlightLine(self, lineNumber):
        cursor = self.svCodeEDitor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        for i in range(lineNumber - 1):
            cursor.movePosition(QTextCursor.Down)
        cursor.select(QTextCursor.LineUnderCursor)

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground((QColor(194, 223, 255, 90)))  # Set background color
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = cursor
        self.selections.append(selection)

        self.svCodeEDitor.setExtraSelections(self.selections)

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self.work_space_tree)
        new_action = contextMenu.addAction("Add Files")
        Delete_action = contextMenu.addAction("Delete Files")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == new_action:
            self.add_files()
        elif action == Delete_action:
            self.Delete_project_ui.show()

    def add_files(self):
        if self.directory_path == "":
            self.show_msg_box("You must first Create a Project")
        else:
            self.path = self.directory_path
            self.files_button = QtWidgets.QFileDialog.getOpenFileNames(None)
            if not self.files_button:
                return
            for file in self.files_button[0]:
                extension = re.sub(".+\.", "", file)
                if not (extension == "v" or extension == "sv"):
                    self.show_msg_box("Only Verilog or SystemVerilog files are supported")
                    return
                file_name = Path(file).stem
                a = QtWidgets.QTreeWidgetItem([str(file_name + "." + extension)])
                if extension == "v":
                    icon_v = QtGui.QIcon(absolutePath("Icons/verilog.png"))
                    a.setIcon(0, icon_v)
                else:
                    icon_v = QtGui.QIcon(absolutePath("Icons/systemverilog.png"))
                    a.setIcon(0, icon_v)
                icon_v = QtGui.QIcon(absolutePath("Icons/notready.png"))
                a.setIcon(1, icon_v)
                self.work_space_tree.addTopLevelItem(a)
                self.design_files.append(str(file_name + "." + extension))
                os.system("copy " + file.replace("/", "\\") + " " + self.directory_path.replace("/", "\\"))
                self.dump_data()


def absolutePath(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    UIWindow = MainWindow_UI()
    UIWindow.show()
    app.exec_()
