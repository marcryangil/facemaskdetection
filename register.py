# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
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
        self.header = QtWidgets.QFrame(self.centralwidget)
        self.header.setMinimumSize(QtCore.QSize(0, 36))
        self.header.setMaximumSize(QtCore.QSize(16777215, 36))
        self.header.setStyleSheet("background-color: rgb(137, 213, 194)")
        self.header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header.setObjectName("header")
        self.label_3 = QtWidgets.QLabel(self.header)
        self.label_3.setGeometry(QtCore.QRect(10, 5, 81, 31))
        self.label_3.setStyleSheet("background: transparent")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/newPrefix/logo.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.header)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(168, 242, 223, 255), stop:1 rgba(255, 255, 255, 255))")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(440, 50, 3, 301))
        self.widget.setMinimumSize(QtCore.QSize(3, 301))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet("background-color: rgb(137, 213, 194)")
        self.widget.setObjectName("widget")
        self.btn_save = QtWidgets.QPushButton(self.frame)
        self.btn_save.setGeometry(QtCore.QRect(610, 370, 191, 41))
        self.btn_save.setMinimumSize(QtCore.QSize(191, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_save.setFont(font)
        self.btn_save.setStyleSheet("QPushButton{\n"
"    background-color: rgb(27, 185, 146);\n"
"    border: none;\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(31, 211, 166);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(22, 154, 121)\n"
"}")
        self.btn_save.setFlat(False)
        self.btn_save.setObjectName("btn_save")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(510, 197, 389, 17))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("background-color: transparent;")
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(510, 133, 389, 17))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("background-color: transparent;")
        self.label_4.setObjectName("label_4")
        self.btn_no_mask = QtWidgets.QPushButton(self.frame)
        self.btn_no_mask.setGeometry(QtCore.QRect(720, 310, 191, 41))
        self.btn_no_mask.setMinimumSize(QtCore.QSize(191, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_no_mask.setFont(font)
        self.btn_no_mask.setStyleSheet("QPushButton{\n"
"    background-color: rgb(33, 113, 93);\n"
"    border: none;\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(31, 211, 166);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(22, 154, 121)\n"
"}")
        self.btn_no_mask.setFlat(False)
        self.btn_no_mask.setObjectName("btn_no_mask")
        self.btn_back = QtWidgets.QPushButton(self.frame)
        self.btn_back.setGeometry(QtCore.QRect(10, 10, 150, 41))
        self.btn_back.setMinimumSize(QtCore.QSize(150, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("QPushButton{\n"
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
        self.btn_back.setFlat(False)
        self.btn_back.setObjectName("btn_back")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(510, 6, 389, 17))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background-color: transparent;")
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(510, 270, 171, 17))
        self.label_6.setAutoFillBackground(False)
        self.label_6.setStyleSheet("background-color: transparent;")
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(510, 70, 389, 17))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("background-color: transparent;")
        self.label_2.setObjectName("label_2")
        self.btn_mask = QtWidgets.QPushButton(self.frame)
        self.btn_mask.setGeometry(QtCore.QRect(510, 310, 191, 41))
        self.btn_mask.setMinimumSize(QtCore.QSize(191, 41))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_mask.setFont(font)
        self.btn_mask.setAutoFillBackground(False)
        self.btn_mask.setStyleSheet("QPushButton{\n"
"    background-color: rgb(33, 113, 93);\n"
"    border: none;\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(31, 211, 166);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(22, 154, 121)\n"
"}")
        self.btn_mask.setFlat(False)
        self.btn_mask.setObjectName("btn_mask")
        self.line_id = QtWidgets.QLineEdit(self.frame)
        self.line_id.setGeometry(QtCore.QRect(510, 30, 391, 31))
        self.line_id.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_id.setObjectName("line_id")
        self.line_first_name = QtWidgets.QLineEdit(self.frame)
        self.line_first_name.setGeometry(QtCore.QRect(510, 90, 391, 31))
        self.line_first_name.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_first_name.setObjectName("line_first_name")
        self.line_last_name = QtWidgets.QLineEdit(self.frame)
        self.line_last_name.setGeometry(QtCore.QRect(510, 160, 391, 31))
        self.line_last_name.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_last_name.setObjectName("line_last_name")
        self.line_status = QtWidgets.QLineEdit(self.frame)
        self.line_status.setGeometry(QtCore.QRect(510, 220, 391, 31))
        self.line_status.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_status.setObjectName("line_status")
        self.btn_clear = QtWidgets.QPushButton(self.frame)
        self.btn_clear.setGeometry(QtCore.QRect(810, 260, 89, 25))
        self.btn_clear.setAutoDefault(True)
        self.btn_clear.setObjectName("btn_clear")
        self.verticalLayout.addWidget(self.frame)
        self.footer = QtWidgets.QFrame(self.centralwidget)
        self.footer.setMinimumSize(QtCore.QSize(0, 36))
        self.footer.setMaximumSize(QtCore.QSize(16777215, 36))
        self.footer.setStyleSheet("background-color: rgb(137, 213, 194)")
        self.footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.trademark = QtWidgets.QLabel(self.footer)
        self.trademark.setGeometry(QtCore.QRect(340, -20, 251, 71))
        self.trademark.setMinimumSize(QtCore.QSize(151, 71))
        font = QtGui.QFont()
        font.setFamily("Work Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trademark.setFont(font)
        self.trademark.setStyleSheet("background: transparent")
        self.trademark.setAlignment(QtCore.Qt.AlignCenter)
        self.trademark.setObjectName("trademark")
        self.verticalLayout.addWidget(self.footer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.label_5.setBuddy(self.line_status)
        self.label_4.setBuddy(self.line_last_name)
        self.label.setBuddy(self.line_id)
        self.label_2.setBuddy(self.line_first_name)

        self.retranslateUi(MainWindow)
        self.btn_clear.clicked.connect(self.line_id.clear) # type: ignore
        self.btn_clear.clicked.connect(self.line_first_name.clear) # type: ignore
        self.btn_clear.clicked.connect(self.line_last_name.clear) # type: ignore
        self.btn_clear.clicked.connect(self.line_status.clear) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.line_id, self.line_first_name)
        MainWindow.setTabOrder(self.line_first_name, self.line_last_name)
        MainWindow.setTabOrder(self.line_last_name, self.line_status)
        MainWindow.setTabOrder(self.line_status, self.btn_clear)
        MainWindow.setTabOrder(self.btn_clear, self.btn_mask)
        MainWindow.setTabOrder(self.btn_mask, self.btn_no_mask)
        MainWindow.setTabOrder(self.btn_no_mask, self.btn_save)
        MainWindow.setTabOrder(self.btn_save, self.btn_back)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_save.setText(_translate("MainWindow", "SAVE"))
        self.label_5.setText(_translate("MainWindow", "&Status"))
        self.label_4.setText(_translate("MainWindow", "&Last Name"))
        self.btn_no_mask.setText(_translate("MainWindow", "NO MASK"))
        self.btn_back.setText(_translate("MainWindow", "BACK"))
        self.label.setText(_translate("MainWindow", "&ID Number"))
        self.label_6.setText(_translate("MainWindow", "Select face classification"))
        self.label_2.setText(_translate("MainWindow", "&First Name"))
        self.btn_mask.setText(_translate("MainWindow", "MASK"))
        self.btn_clear.setText(_translate("MainWindow", "Clear"))
        self.trademark.setText(_translate("MainWindow", "Powered by CloverByte, 2021"))
import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
