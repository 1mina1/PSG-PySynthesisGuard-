import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import random
import sys
import threading
import pickle
import re
import os
from pathlib import Path
import qdarktheme

from source.GUI.BrowseDirectory import New_Project_UI
from source.GUI.DeleteFiles import DeleteFiles_UI
from source.GUI.QCodeEditor import Highlighter

# from BrowseDirectory import New_Project_UI
# from DeleteFiles import DeleteFiles_UI
# from QCodeEditor import Highlighter
import time


class OpenFile(QtCore.QThread):
    Editor_text = QtCore.pyqtSignal(str)
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
                            line = re.sub("\n", "", line)
                            self.Editor_text.emit(line)
                        old_file_list = new_file_list


class MainWindow_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow_UI, self).__init__()
        self.files_button = None
        self.path = None
        self.New_Project_ui = New_Project_UI()
        self.Delete_project_ui = DeleteFiles_UI()
        self.directory_path = ""
        self.projectName = ""
        self.design_files = []
        self.openFileThread = OpenFile()

        uic.loadUi("MainWindow.ui", self)

        # Define the widgets
        self.action_new_project = self.findChild(QtWidgets.QAction, "actionNew_Project")
        self.Project_Description = self.findChild(QtWidgets.QLabel, "PD_LABEL")
        self.actionDark = self.findChild(QtWidgets.QAction, "actionDark")
        self.actionLight = self.findChild(QtWidgets.QAction, "actionLight")
        self.svCodeEDitor = self.findChild(QtWidgets.QPlainTextEdit, "SVCodeEditor")
        self.work_space_tree = self.findChild(QtWidgets.QTreeWidget, "Directory_tree")
        self.charts_pie = self.findChild(QtWidgets.QWidget, "charts")

        # connect the functions
        self.action_new_project.triggered.connect(self.new_project)
        self.New_Project_ui.Directory_text.connect(self.Project_Directory)
        self.New_Project_ui.Name_text.connect(self.project_name)
        self.Delete_project_ui.Delete_Signal.connect(self.removeItem)
        self.actionDark.triggered.connect(self.setDarkMode)
        self.actionLight.triggered.connect(self.setLightMode)
        self.openFileThread.Editor_text.connect(self.PrintCode)
        self.highlighter = Highlighter(self.svCodeEDitor.document())
        # initialize Widgets
        self.svCodeEDitor.setReadOnly(True)
        self.work_space_tree.itemDoubleClicked.connect(self.handle_double_click)
        y = [100]
        mylabels = ["All Good"]
        mycolors = ["green"]
        _, self.texts, self.autotexts = self.charts_pie.canvas.axes.pie(y, labels=mylabels, colors=mycolors,
                                                                        autopct="%.2f")

    def new_project(self):
        self.New_Project_ui.show()

    def show_msg_box(self, msg: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(msg)
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        x = msg_box.exec_()

    def handle_double_click(self, item):
        self.svCodeEDitor.clear()
        self.openFileThread.finish = 1
        self.openFileThread.exit()
        self.openFileThread.design_file = self.directory_path + "/" + item.text(0)
        self.openFileThread.finish = 0
        self.openFileThread.start()

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
            if flag == 1:
                file = self.directory_path + "/" + Item.text(0)
                print(file)
                os.remove(file.replace("/", "\\"))
            self.work_space_tree.topLevelItem(0).removeChild(Item)

    def PrintCode(self, line):
        self.svCodeEDitor.appendPlainText(line)

    def Project_Directory(self, Path: str):
        self.directory_path = Path

    def project_name(self, Name: str):
        self.Project_Description.setText(Name + "-" + str(self.directory_path))

    def setDarkMode(self):
        qdarktheme.setup_theme()
        for ins in self.autotexts:
            ins.set_color('white')
        for ins in self.texts:
            ins.set_color('white')
        self.charts_pie.canvas.axes.set_facecolor("black")
        self.charts_pie.canvas.figure.set_facecolor("black")
        self.charts_pie.canvas.draw()

    def setLightMode(self):
        qdarktheme.setup_theme("light")
        for ins in self.autotexts:
            ins.set_color('black')
        for ins in self.texts:
            ins.set_color('black')
        self.charts_pie.canvas.axes.set_facecolor("white")
        self.charts_pie.canvas.figure.set_facecolor("white")
        self.charts_pie.canvas.draw()

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
                    icon_v = QtGui.QIcon(self.cwd+"/"+"Icons/verilog.png")
                    a.setIcon(0, icon_v)
                else:
                    icon_v = QtGui.QIcon(self.cwd+"/"+"Icons/systemverilog.png")
                    a.setIcon(0, icon_v)
                icon_v = QtGui.QIcon(self.cwd+"/"+"Icons/notready.png")
                a.setIcon(1, icon_v)
                self.work_space_tree.addTopLevelItem(a)
                self.design_files.append(str(file_name + "." + extension))
                os.system("copy " + file.replace("/", "\\") + " " + self.directory_path.replace("/", "\\"))


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    UIWindow = MainWindow_UI()
    UIWindow.show()
    app.exec_()
