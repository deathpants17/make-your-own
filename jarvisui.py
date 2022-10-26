from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import *
my_window = Tk()


screen_width = my_window.winfo_screenwidth()
screen_height = my_window.winfo_screenheight()


class Ui_JarvisUi(object):
    def setupUi(self, JarvisUi):
        JarvisUi.setObjectName("JarvisUi")
        JarvisUi.resize(screen_width/2, screen_height/2)
        self.centralwidget = QtWidgets.QWidget(JarvisUi)
        self.centralwidget.setObjectName("centralwidget")

        self.gif_3 = QtWidgets.QLabel(self.centralwidget)
        self.gif_3.setGeometry(QtCore.QRect(0, 0, screen_width/2, screen_height/2))
        self.gif_3.setText("")
        self.gif_3.setPixmap(QtGui.QPixmap("watch-dogs2-dedsec.gif"))
        self.gif_3.setScaledContents(True)
        self.gif_3.setObjectName("gif_3")

        self.Text_Time = QtWidgets.QTextBrowser(self.centralwidget)
        self.Text_Time.setGeometry(QtCore.QRect(0, 0, 331, 51))
        self.Text_Time.setStyleSheet("background-color: Transparent;\n"
            "border-color: rgb(47, 47, 47);\n"
            "color:rgb(0, 230, 230);\n"
            "font-size: 30px;\n")
        self.Text_Time.setObjectName("Text_Time")
        self.Text_Date = QtWidgets.QTextBrowser(self.centralwidget)
        self.Text_Date.setGeometry(QtCore.QRect(0, 100, 331, 51))
        self.Text_Date.setStyleSheet("background-color: Transparent;\n"
            "border-color: rgb(47, 47, 47);\n"
            "color:rgb(0, 230, 230);\n"
            "font-size: 30px;\n")
        self.Text_Date.setObjectName("Text_Date")
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setGeometry(QtCore.QRect((screen_width/2) - 200, (screen_height/2) - 200, 211, 61))
        self.pushButton_Start.setStyleSheet("background-color: rgb(0, 0, 0);\n"
            "font: 24pt \"PMingLiU-ExtB\";\n"
            "border-radius:None;\n"
            "color: rgb(0, 255, 255);\n"
            "\n")
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.pushButton_Exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Exit.setGeometry(QtCore.QRect((screen_width/2) - 200, (screen_height/2) - 100, 211, 61))
        self.pushButton_Exit.setStyleSheet("background-color: rgb(0, 0, 0);\n"
            "font: 24pt \"PMingLiU-ExtB\";\n"
            "border-radius:None;\n"
            "color: rgb(0, 255, 255);\n"
            "\n")
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.gif_3.raise_()
        self.Text_Time.raise_()
        self.Text_Date.raise_()
        self.pushButton_Start.raise_()
        self.pushButton_Exit.raise_()
        JarvisUi.setCentralWidget(self.centralwidget)

        self.retranslateUi(JarvisUi)
        QtCore.QMetaObject.connectSlotsByName(JarvisUi)

    def retranslateUi(self, JarvisUi):
        _translate = QtCore.QCoreApplication.translate
        JarvisUi.setWindowTitle(_translate("JarvisUi", "MainWindow"))
        self.pushButton_Start.setText(_translate("JarvisUi", "Start"))
        self.pushButton_Exit.setText(_translate("JarvisUi", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    JarvisUi = QtWidgets.QMainWindow()
    ui = Ui_JarvisUi()
    ui.setupUi(JarvisUi)
    JarvisUi.show()
    sys.exit(app.exec_())