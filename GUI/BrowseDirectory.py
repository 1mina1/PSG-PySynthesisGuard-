from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import os


class New_Project_UI(QtWidgets.QMainWindow):
    Directory_text = QtCore.pyqtSignal(str)
    Name_text = QtCore.pyqtSignal(str)

    def __init__(self):
        super(New_Project_UI, self).__init__()
        self.directory_path = ""
        self.project_name_Totxt = ""
        # loading uic
        uic.loadUi("NewProject.ui", self)

        # Define the widgets
        self.directory_text_browser = self.findChild(QtWidgets.QTextBrowser, "directory_text_browser")
        self.browse_button = self.findChild(QtWidgets.QPushButton, "browse_button")
        self.Project_name = self.findChild(QtWidgets.QTextEdit, "Projectname")
        self.createproject = self.findChild(QtWidgets.QPushButton, "createproject")

        # connecting the buttons
        self.browse_button.clicked.connect(self.browse_directory)
        self.createproject.clicked.connect(self.createproject_fcn)

    def browse_directory(self) -> str:
        """This function open directory and return its path"""
        self.directory_path = QtWidgets.QFileDialog.getExistingDirectory(None)
        self.directory_text_browser.setText(self.directory_path)
        return self.directory_path

    def show_msg_box(self, msg: str):
        """This function pop up the message box"""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(msg)
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        x = msg_box.exec_()

    def createproject_fcn(self):
        self.project_name_Totxt = self.Project_name.toPlainText()
        if self.directory_path == "":
            self.show_msg_box("You must insert your directory")
        elif self.project_name_Totxt == "":
            self.show_msg_box("You must inert a project name")
        else:
            self.Directory_text.emit(self.directory_path)
            self.Name_text.emit(self.project_name_Totxt)
            self.directory_text_browser.clear()
            self.Project_name.clear()
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = New_Project_UI()
    UIWindow.show()
    app.exec_()
