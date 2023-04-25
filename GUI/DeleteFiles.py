from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os


class DeleteFiles_UI(QtWidgets.QMainWindow):
    Delete_Signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(DeleteFiles_UI, self).__init__()

        # loading uic
        cwd = os.getcwd() +"/" +"source" "/" +"GUI"
        uic.loadUi("DeleteFiles.ui", self)

        # Define the widgets
        self.ok_button = self.findChild(QtWidgets.QPushButton, "ok_button")
        self.cancel_button = self.findChild(QtWidgets.QPushButton, "cancel_button")
        self.chkbox = self.findChild(QtWidgets.QCheckBox, "checkBox")

        # connect the buttons
        self.ok_button.clicked.connect(self.ok_func)
        self.cancel_button.clicked.connect(self.close)

    def ok_func(self):
        if self.chkbox.isChecked():
            self.Delete_Signal.emit(1)
        else:
            self.Delete_Signal.emit(2)
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = DeleteFiles_UI()
    UIWindow.show()
    app.exec_()
