import sqlite3
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QStackedWidget


app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi('register.ui')

window.show()
app.exec()