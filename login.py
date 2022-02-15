# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(942, 495)
        MainWindow.setMinimumSize(QtCore.QSize(942, 495))
        MainWindow.setMaximumSize(QtCore.QSize(942, 495))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 36))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 36))
        self.frame_3.setStyleSheet("background-color: rgb(137, 213, 194)")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(10, 5, 81, 31))
        self.label_3.setStyleSheet("background: transparent")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/newPrefix/logo.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.frame_3)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(168, 242, 223, 255), stop:1 rgba(255, 255, 255, 255))")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.loginbtn = QtWidgets.QPushButton(self.frame)
        self.loginbtn.setGeometry(QtCore.QRect(380, 340, 171, 41))
        self.loginbtn.setMinimumSize(QtCore.QSize(150, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loginbtn.setFont(font)
        self.loginbtn.setStyleSheet("QPushButton{\n"
"    background-color: rgb(33, 113, 93);\n"
"    border: none;\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(46, 159, 131);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(29, 100, 82);\n"
"}")
        self.loginbtn.setFlat(False)
        self.loginbtn.setObjectName("loginbtn")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(405, 120, 151, 71))
        self.label_2.setMinimumSize(QtCore.QSize(151, 71))
        font = QtGui.QFont()
        font.setFamily("Work Sans SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: transparent")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(360, 40, 221, 91))
        self.label.setStyleSheet("background: transparent")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.usernamefield = QtWidgets.QLineEdit(self.frame)
        self.usernamefield.setGeometry(QtCore.QRect(350, 210, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        self.usernamefield.setFont(font)
        self.usernamefield.setStyleSheet("QLineEdit{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 8px;\n"
"    border-color: rgb(140, 140, 140);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px; \n"
"}\n"
"")
        self.usernamefield.setObjectName("usernamefield")
        self.passwordfield = QtWidgets.QLineEdit(self.frame)
        self.passwordfield.setGeometry(QtCore.QRect(350, 270, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        self.passwordfield.setFont(font)
        self.passwordfield.setStyleSheet("QLineEdit{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 8px;\n"
"    border-color: rgb(140, 140, 140);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px; \n"
"}\n"
"")
        self.passwordfield.setObjectName("passwordfield")
        self.errorlabel = QtWidgets.QLabel(self.frame)
        self.errorlabel.setGeometry(QtCore.QRect(350, 316, 231, 21))
        self.errorlabel.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Work Sans Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.errorlabel.setFont(font)
        self.errorlabel.setStyleSheet("background: transparent;\n"
"color: red;")
        self.errorlabel.setText("")
        self.errorlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorlabel.setObjectName("errorlabel")
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 36))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 36))
        self.frame_2.setStyleSheet("background-color: rgb(137, 213, 194)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(340, -20, 251, 71))
        self.label_4.setMinimumSize(QtCore.QSize(151, 71))
        font = QtGui.QFont()
        font.setFamily("Work Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background: transparent")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loginbtn.setText(_translate("MainWindow", "LOG IN"))
        self.label_2.setText(_translate("MainWindow", "Mandate Safety, \n"
"Mandate Mask."))
        self.label_4.setText(_translate("MainWindow", "Powered by CloverByte, 2021"))
import resources_rc
