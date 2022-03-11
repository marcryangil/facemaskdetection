import sqlite3, traceback
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QStackedWidget, QMessageBox
import resources

ACCOUNT_LOGIN = ''
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
                
                print("Success")
                self.errorlabel.setText("")
                self.gotoDashboard()
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
        
        
    def gotoLogs(self):
        logs = LogScreen()
        widget.addWidget(logs)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoRegister(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def gotoLaunch(self):
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
        records = RecordsScreen()
        widget.addWidget(records)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    
    @QtCore.pyqtSlot()
    def open_file(self):
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

#
# Register window
#
class RegisterScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(RegisterScreen, self).__init__()
        
        loadUi('register.ui', self)
        self.open_db()
        self.btn_back.clicked.connect(self.gotoDashboard)
        self.btn_save.clicked.connect(self.save_it)
        

    def open_db(self):
        
        # print("THE ACCOUNT: "+ ACCOUNT_LOGIN)
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        
        # Create table
        c.execute("""CREATE TABLE if not exists registered_user(
                id_number TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                status TEXT,
                registered_by TEXT
            )
            """) 

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()
    
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
        ################################################################
        # self.line_id.setCurrentIndex = 0
        # help me. How to set Select after submit
        ################################################################
    
    def save_it(self):
        
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
                # Create a cursor
                c = conn.cursor()
                # print('account login: '+ACCOUNT_LOGIN)
                
                # Insert user to the database
                c.execute("INSERT INTO registered_user VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
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
        
        # Opens database if not exists
        reg = RegisterScreen()
        reg.open_db()
        
        self.tableWidget.setHorizontalHeaderLabels(["Id", "First Name", "Last Name",'Status', 'Registered By'])
        self.loaddata()
        # self.btn_register.clicked.connect(self.gotoRegister)
        
        self.btn_back.clicked.connect(self.gotoDashboard)
        self.btn_register.clicked.connect(self.gotoRegister)
        self.btn_delete.clicked.connect(self.gotoDelete)
        
        
        
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
        # Grab the selected row and add 1 for ROWID
        clicked = self.tableWidget.currentRow() + 1
        
        print('CLICKED: '+str(clicked))
        
       
        

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

################################
# can we add primary key on registered users?
# CREATE TABLE artists_backup(
#    artistid INTEGER PRIMARY KEY AUTOINCREMENT,
#    name NVARCHAR
# );
################################