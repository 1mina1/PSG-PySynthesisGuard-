from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os


class DeleteFiles_UI(QtWidgets.QMainWindow):
    Delete_Signal = QtCore.pyqtSignal(int)

    def setupUi(self, DeleteFiles):
        DeleteFiles.setObjectName("DeleteFiles")
        DeleteFiles.resize(310, 150)
        DeleteFiles.setMaximumSize(QtCore.QSize(310, 150))
        self.centralwidget = QtWidgets.QWidget(DeleteFiles)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.verticalLayout.setStretch(0, 40)
        self.verticalLayout.setStretch(1, 100)
        self.verticalLayout.setStretch(2, 5)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        DeleteFiles.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DeleteFiles)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 310, 26))
        self.menubar.setObjectName("menubar")
        DeleteFiles.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DeleteFiles)
        self.statusbar.setObjectName("statusbar")
        DeleteFiles.setStatusBar(self.statusbar)

        self.retranslateUi(DeleteFiles)
        QtCore.QMetaObject.connectSlotsByName(DeleteFiles)

    def retranslateUi(self, DeleteFiles):
        _translate = QtCore.QCoreApplication.translate
        DeleteFiles.setWindowTitle(_translate("DeleteFiles", "MainWindow"))
        self.label.setText(_translate("DeleteFiles", "  Are you sure you want to remove the selected files  "))
        self.ok_button.setText(_translate("DeleteFiles", "Ok"))
        self.cancel_button.setText(_translate("DeleteFiles", "Cancel"))
        self.checkBox.setText(_translate("DeleteFiles", "Delete from Disk as well"))

    def __init__(self):
        super(DeleteFiles_UI, self).__init__()

        self.setupUi(self)

        # connect the buttons
        self.ok_button.clicked.connect(self.ok_func)
        self.cancel_button.clicked.connect(self.close)

    def ok_func(self):
        if self.checkBox.isChecked():
            self.Delete_Signal.emit(1)
        else:
            self.Delete_Signal.emit(2)
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = DeleteFiles_UI()
    UIWindow.show()
    app.exec_()
