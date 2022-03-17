import sqlite3, traceback
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QStackedWidget, QMessageBox
import resources
from db_management import DatabaseManager, InsertDatabase

ACCOUNT_LOGIN = ''
SYSTEM_LOGS = []
insert_database = InsertDatabase()
class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        # self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbtn.clicked.connect(self.loginfunction)
        
        self._login_username = ''

    def loginfunction(self):
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username) == 0 or len(password) == 0:
            self.errorlabel.setText("Please input all fields.")
        else:
            conn = sqlite3.connect("facemaskdetectionDB.db")
            cur = conn.cursor()
            query = 'SELECT password FROM users WHERE username = \'' + username + "\'"
            cur.execute(query)
            result_pass = cur.fetchone()

            if result_pass is not None:
                result_pass = result_pass[0]

            if result_pass == password:
                global ACCOUNT_LOGIN
                ACCOUNT_LOGIN = username
                open_database = DatabaseManager()
                open_database.open_db_system_logs()
                self.errorlabel.setText("")
                self.gotoDashboard()
                insert_database.insert_system_logs('Login', ACCOUNT_LOGIN)
                
            else:
                self.errorlabel.setText("Invalid username or password.")
                
    
    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class DashboardScreen(QMainWindow):
    def __init__(self):
        super(DashboardScreen, self).__init__()
        loadUi("dashboard.ui", self)
        self.launchbtn.clicked.connect(self.gotoLaunch)
        self.getstartedbtn.clicked.connect(self.open_file)
        self.logsbtn.clicked.connect(self.gotoLogs)
        self.registerbtn.clicked.connect(self.gotoRegister)
        self.recordsbtn.clicked.connect(self.gotoRecords)
        self.systemlogsbtn.clicked.connect(self.gotoSystemLogs)
        insert_database.insert_system_logs('Dashboard', ACCOUNT_LOGIN)
        
    def gotoLogs(self):
        insert_database.insert_system_logs('Logs', ACCOUNT_LOGIN)
        logs = LogScreen()
        widget.addWidget(logs)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoRegister(self):
        insert_database.insert_system_logs('Register Face', ACCOUNT_LOGIN)
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def gotoLaunch(self):
        insert_database.insert_system_logs('Launch', ACCOUNT_LOGIN)
        ######################################################
        # Temporarily unavailable
        msg = QMessageBox()
        msg.setWindowTitle('UNDER CONSTRUCTION')
        msg.setText('Temporarily Unavailable')
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()
        ######################################################
        
        import os
        os.system('python detect/mask.py')

    def gotoRecords(self):
        insert_database.insert_system_logs('Records', ACCOUNT_LOGIN)
        records = RecordsScreen()
        widget.addWidget(records)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    
    @QtCore.pyqtSlot()
    def open_file(self):
        insert_database.insert_system_logs('Get Started', ACCOUNT_LOGIN)
        ######################################################
        # Temporarily unavailable
        msg = QMessageBox()
        msg.setWindowTitle('UNDER CONSTRUCTION')
        msg.setText('Temporarily Unavailable')
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()
        ######################################################
        url = QtCore.QUrl.fromLocalFile("Get Started.pdf")
        QtGui.QDesktopServices.openUrl(url)
        
    def gotoSystemLogs(self):
        insert_database.insert_system_logs('Logs - System', ACCOUNT_LOGIN)
        system_logs = SystemLogScreen()
        widget.addWidget(system_logs)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LogScreen(QMainWindow):
    def __init__(self):
        super(LogScreen, self).__init__()
        loadUi("log.ui", self)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Username", "Password"])
        self.loaddata()
        self.gobackbtn.clicked.connect(self.gotoDashboard)

    def loaddata(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM users"
        tablerow = 0

        self.tableWidget.setRowCount(3)

        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0])) # column 1
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1])) # column 2
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2])) # column 3
            tablerow+=1

        print(cur.execute(sqlquery).rowcount)

    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class SystemLogScreen(QMainWindow):
    def __init__(self):
        super(SystemLogScreen, self).__init__()
        loadUi("system_log.ui", self)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Username", "Password"])
        self.loaddata()
        self.btn_back.clicked.connect(self.gotoDashboard)
        
    def loaddata(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM system_logs"
        counter = "SELECT COUNT(id) FROM system_logs"
        tablerow = 0
        
        # To count how many rows in registered user
        system_logs_qty = cur.execute(counter).fetchone()[0]
        self.tableWidget.setRowCount(system_logs_qty)
        # To stretch the item lists on tableWidget
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0]))) # column 1
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1])) # column 2
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2])) # column 3
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3])) # column 3
            tablerow+=1

        print(cur.execute(sqlquery).rowcount)

    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#
# Register window
#
class RegisterScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(RegisterScreen, self).__init__()
        
        loadUi('register.ui', self)
        
        db_open = DatabaseManager()
        db_open.open_db_registered_user()
        self.btn_back.clicked.connect(self.gotoDashboard)
        self.btn_save.clicked.connect(self.save_it)

    
    def has_error(self):
        # added .replace(' ','') to remove whitespaces
        id = self.line_id.text().replace(' ','')
        first_name = self.line_first_name.text().replace(' ','')
        last_name = self.line_last_name.text().replace(' ','')
        return not bool(len(id) and len(first_name) and len(last_name))
    
    def is_select(self):
        return self.comboBox_status_1.currentText() == 'Select'
    
    # to clear details after successful submit
    def clear_details(self):
        self.line_id.clear()
        self.line_first_name.clear()
        self.line_last_name.clear()
    
    def save_it(self, _id= None, _first=None, _last=None, _status=None):
        
        if self.has_error() or self.is_select():
            self.label_error.setText('Error, please check fields')
            if self.is_select():
                self.comboBox_status_1.setStyleSheet(
                                                    "color: rgb(0,0,0);\n"
                                    "background-color: rgb(255,255,255);\n"
                                        "border-style: solid;\n"
                                        "border-width: 1px;\n"
                                        "border-radius: 8px;\n"
                                        "border-color: rgb(140, 140, 140)\n;"
                                        "padding-left: 10px;\n"
                                        "padding-right: 10px;\n"
                                        "border-color: red;\n"
                )
        else:
            self.comboBox_status_1.setStyleSheet(
                                                 "color: rgb(0,0,0);\n"
                                "background-color: rgb(255,255,255);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;\n"
                                    "border-radius: 8px;\n"
                                    "border-color: rgb(140, 140, 140)\n;"
                                    "padding-left: 10px;\n"
                                    "padding-right: 10px;\n"
                )
            try:
                self.label_error.setText('')
                # Create a database or connect to one
                conn = sqlite3.connect('facemaskdetectionDB.db')
                c = conn.cursor()
                # Insert user to the database
                if self.btn_save.text() == 'SAVE':
                    c.execute("INSERT INTO registered_user VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
                            {
                                'id_number': self.line_id.text(),
                                'first_name': self.line_first_name.text(),
                                'last_name': self.line_last_name.text(),
                                'status': self.comboBox_status_1.currentText(),
                                'registered_by':ACCOUNT_LOGIN,
                            }
                            )
                elif self.btn_save.text() == 'UPDATE':
                    c.execute("INSERT OR REPLACE INTO registered_user VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
                            {
                                'id_number': self.line_id.text(),
                                'first_name': self.line_first_name.text(),
                                'last_name': self.line_last_name.text(),
                                'status': self.comboBox_status_1.currentText(),
                                'registered_by':ACCOUNT_LOGIN,
                            }
                            )
                # Commit changes
                conn.commit()
                # Close connection
                conn.close()
                
                # Pop up message box
                msg = QMessageBox()
                msg.setWindowTitle('Saved to the Database!')
                msg.setText('User has been saved')
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()
                
                self.clear_details()
            except sqlite3.Error as er:
                msg = QMessageBox()
                msg.setWindowTitle('ERROR!')
                msg.setText('Id number must be unique')
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()
                # print('SQLite error: %s' % (' '.join(er.args)))
                # print("Exception class is: ", er.__class__)
                # print('SQLite traceback: ')
                # exc_type, exc_value, exc_tb = sys.exc_info()
                # print(traceback.format_exception(exc_type, exc_value, exc_tb))   
    
    ################################################################
    # To update details 
    ################################################################
    def loadDetails(self, _id= None, _first=None, _last=None, _status=None):
        self.line_id.setText(_id)
        self.line_id.setDisabled(True)
        self.line_first_name.setText(_first)
        self.line_last_name.setText(_last)
        self.comboBox_status_1.setCurrentText(_status)
        self.btn_save.setText('UPDATE')
        
    
    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
        

#
# Records window
#
class RecordsScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(RecordsScreen, self).__init__()
        loadUi('records.ui', self)
        
        db_open = DatabaseManager()
        db_open.open_db_registered_user()
        
        self.tableWidget.setHorizontalHeaderLabels(["Id", "First Name", "Last Name",'Status', 'Registered By'])
        self.loaddata()
        # self.btn_register.clicked.connect(self.gotoRegister)
        
        self.btn_back.clicked.connect(self.gotoDashboard)
        self.btn_register.clicked.connect(self.gotoRegister)
        self.btn_delete.clicked.connect(self.gotoDelete)
        self.line_search.textChanged.connect(self.search)
        self.btn_edit.clicked.connect(self.edit)
        
    def loaddata(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM registered_user"
        counter = "SELECT COUNT(id_number) FROM registered_user"
        tablerow = 0

        # to count how many rows in registered user
        registered_users = cur.execute(counter).fetchone()[0]
        self.tableWidget.setRowCount(registered_users)

        self.tableWidget.setColumnWidth(0,100)
        
        
        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0])) # column 1
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1])) # column 2
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2])) # column 3
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3])) # column 3
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4])) # column 3
            tablerow+=1

        print(cur.execute(sqlquery).rowcount)
    
    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def gotoRegister(self):
        self.gotoDashboard()
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def gotoDelete(self):
        # set current row on table
        row = self.tableWidget.currentRow()
        # set current column on table
        # col = self.tableWidget.currentColumn() 
        
        cell_value = self.tableWidget.item(row,0).text()
        print('ROW: '+str(row))
        
        id_name = str(self.input_delete_id(cell_value))
        print("id name: "+id_name)
        
        if id_name:
            conn = sqlite3.connect('facemaskdetectionDB.db')
            # Create a cursor
            c = conn.cursor()
            c.execute("DELETE FROM registered_user WHERE id_number=(:id_number)",
                    {
                        'id_number':id_name,
                    }
                    )
            conn.commit()
            conn.close()
        
        # reload the data after deletion
        self.loaddata()
    
    def input_delete_id(self,cell_name):
        text, result = QtWidgets.QInputDialog.getText(self, 'Delete Record', 'Enter id number: ',text=cell_name)

        if result == True:
            return text
    
    def search(self):
        name = self.line_search.text()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            # if the search is *not* in the item's text *do not hide* the row
            self.tableWidget.setRowHidden(row, name not in item.text().lower())    
    
    def edit(self):
        register = RegisterScreen()
        
        row = self.tableWidget.currentRow()
        
        cell_value = self.tableWidget.item(row,0).text()
        
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("SELECT * FROM registered_user WHERE id_number=(:id_number)",
                    {
                        'id_number':cell_value,
                    }
                    )
        rows = c.fetchall()[0]
        values = [] 
        for row in rows:
            values.append(row)

        
        conn.commit()
        conn.close()

        register.loadDetails(_id=values[0], _first=values[1], _last=values[2], _status=values[3])
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
# main
app = QApplication(sys.argv)
login = LoginScreen()
widget = QStackedWidget()
widget.addWidget(login)
widget.setFixedSize(942, 495)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")