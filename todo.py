
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3

# Create a database or connect to one
conn = sqlite3.connect('mylist.db')
# Create a cursor
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE if not exists todo_list(
    list_item text)
    """) # One column called list_item

# Commit changes
conn.commit()

# Close connection
conn.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 417)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # add item using lambda expression
        self.additem_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.add_it())
        self.additem_pushButton.setGeometry(QtCore.QRect(10, 70, 111, 31))
        self.additem_pushButton.setObjectName("additem_pushButton")
        # delete item using lambda expression
        self.deleteitem_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.delete_it())
        self.deleteitem_pushButton.setGeometry(QtCore.QRect(140, 70, 111, 31))
        self.deleteitem_pushButton.setObjectName("deleteitem_pushButton")
        # clear item using lambda expression
        self.clearall_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.clear_it())
        self.clearall_pushButton.setGeometry(QtCore.QRect(260, 70, 111, 31))
        self.clearall_pushButton.setObjectName("clearall_pushButton")
        self.input_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.input_lineEdit.setGeometry(QtCore.QRect(12, 20, 491, 25))
        self.input_lineEdit.setObjectName("input_lineEdit")
        self.mylist_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mylist_listWidget.setGeometry(QtCore.QRect(10, 120, 491, 261))
        self.mylist_listWidget.setObjectName("mylist_listWidget")
        # save database using lambda expression
        self.savedatabase_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda:self.save_it())
        self.savedatabase_pushButton.setGeometry(QtCore.QRect(390, 70, 111, 31))
        self.savedatabase_pushButton.setObjectName("savedatabase_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.input_lineEdit, self.additem_pushButton)
        MainWindow.setTabOrder(self.additem_pushButton, self.deleteitem_pushButton)
        MainWindow.setTabOrder(self.deleteitem_pushButton, self.clearall_pushButton)
        MainWindow.setTabOrder(self.clearall_pushButton, self.mylist_listWidget)
        # Grab all the items from the database
        self.grab_all()
    
    # Grab all the items
    def grab_all(self):
        # Create a database or connect to one
        conn = sqlite3.connect('mylist.db')
        # Create a cursor
        c = conn.cursor()

        c.execute("SELECT * FROM todo_list")
        records = c.fetchall()

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
        # Loop through the records and add to the screen
        for record in records:
            self.mylist_listWidget.addItem(str(record[0]))
        
        
    #
    # Add item
    # 
    def add_it(self):
        # grab item from input
        item = self.input_lineEdit.text()
        
        # add item to list
        self.mylist_listWidget.addItem(item)
        
        # clear the input after adding
        self.input_lineEdit.setText('')
    
    
    #
    # Delete item
    # 
    def delete_it(self):
        # Grab the selected row
        clicked = self.mylist_listWidget.currentRow()
        # self.input_lineEdit.setText(str(clicked))
        
        # Delete the selected row
        self.mylist_listWidget.takeItem(clicked)

    #
    # Clear item and lists
    # 
    def clear_it(self):
        self.mylist_listWidget.clear()

    #
    # Save to the database
    # 
    def save_it(self):
        print("hello world!")
        # Create a database or connect to one
        conn = sqlite3.connect('mylist.db')
        # Create a cursor
        c = conn.cursor()
        
        # Delete everything in the database table
        c.execute("DELETE FROM todo_list;", )
        
        # Create blank lists to hold to do items
        items = []
        # Loop through the listWidget and pull out each item
        for index in range(self.mylist_listWidget.count()):
            items.append(self.mylist_listWidget.item(index))
        
        # print(items.text())
        for item in items:
            # print(item.text())
            # Add items to the table
            c.execute("INSERT INTO todo_list VALUES (:item)",
                      {
                          'item': item.text(),
                      }
                      )
        
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
        # Pop up message box
        msg = QMessageBox()
        msg.setWindowTitle('Saved to the Database!')
        msg.setText('Your todo list has been saved')
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
        


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.additem_pushButton.setText(_translate("MainWindow", "Add item "))
        self.deleteitem_pushButton.setText(_translate("MainWindow", "Delete Item"))
        self.clearall_pushButton.setText(_translate("MainWindow", "Clear List"))
        self.savedatabase_pushButton.setText(_translate("MainWindow", "Save Database"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
