import sys
from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("register.ui")

window.show()
app.exec()

'''
 Created register form with proper tab construction/order.
 Created clear button.
 Created shortcut using alt
'''