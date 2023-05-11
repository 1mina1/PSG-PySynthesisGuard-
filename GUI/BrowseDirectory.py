from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import os


class New_Project_UI(QtWidgets.QMainWindow):
    Directory_text = QtCore.pyqtSignal(str)
    Name_text = QtCore.pyqtSignal(str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 190)
        MainWindow.setMinimumSize(QtCore.QSize(550, 100))
        MainWindow.setMaximumSize(QtCore.QSize(550, 190))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.directory_text_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.directory_text_browser.setMinimumSize(QtCore.QSize(0, 0))
        self.directory_text_browser.setMaximumSize(QtCore.QSize(16777215, 31))
        self.directory_text_browser.setObjectName("directory_text_browser")
        self.horizontalLayout.addWidget(self.directory_text_browser)
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setObjectName("browse_button")
        self.horizontalLayout.addWidget(self.browse_button)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.Projectname = QtWidgets.QTextEdit(self.centralwidget)
        self.Projectname.setMaximumSize(QtCore.QSize(16777215, 40))
        self.Projectname.setObjectName("Projectname")
        self.gridLayout.addWidget(self.Projectname, 1, 0, 1, 1)
        self.createproject = QtWidgets.QPushButton(self.centralwidget)
        self.createproject.setObjectName("createproject")
        self.gridLayout.addWidget(self.createproject, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.directory_text_browser.setPlaceholderText(_translate("MainWindow", "Working Directory"))
        self.browse_button.setText(_translate("MainWindow", "Browse Directory"))
        self.Projectname.setPlaceholderText(_translate("MainWindow", "Project name"))
        self.createproject.setText(_translate("MainWindow", "Create Project"))

    def __init__(self):
        super(New_Project_UI, self).__init__()
        self.setupUi(self)
        self.directory_path = ""
        self.project_name_Totxt = ""

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
        self.project_name_Totxt = self.Projectname.toPlainText()
        if self.directory_path == "":
            self.show_msg_box("You must insert your directory")
        elif self.project_name_Totxt == "":
            self.show_msg_box("You must inert a project name")
        else:
            self.Directory_text.emit(self.directory_path)
            self.Name_text.emit(self.project_name_Totxt)
            self.directory_text_browser.clear()
            self.Projectname.clear()
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = New_Project_UI()
    UIWindow.show()
    app.exec_()
