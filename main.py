import sqlite3, traceback
import sys

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QStackedWidget, QMessageBox, QMenu, QLineEdit, QTableWidgetItem
import resources
from db_management import DatabaseManager, InsertDatabase
import stylesheets

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
        
        self.usernamefield.textChanged.connect(self.usernamevalue)
        self.passwordfield.textChanged.connect(self.passwordvalue)
        
    
    def usernamevalue(self):
        if len(self.usernamefield.text()) != 0:
            self.usernamefield.setStyleSheet(stylesheets.hasnoerrorline)
        else:
            self.usernamefield.setStyleSheet(stylesheets.haserrorline)
    def passwordvalue(self):
        if len(self.passwordfield.text()) != 0:
            self.passwordfield.setStyleSheet(stylesheets.hasnoerrorline)
        else:
            self.passwordfield.setStyleSheet(stylesheets.haserrorline)

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
                self.usernamefield.setStyleSheet(stylesheets.haserrorline)
                self.passwordfield.setStyleSheet(stylesheets.haserrorline)
                
    
    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class DashboardScreen(QMainWindow):
    def __init__(self):
        super(DashboardScreen, self).__init__()
        loadUi("dashboard.ui", self)
        self.launchbtn.clicked.connect(self.gotoLaunch)
        self.getstartedbtn.clicked.connect(self.openFile)

        self.detectionbtn.hide()
        self.systembtn.hide()
        self.hidden = True
        self.systembtn.clicked.connect(self.gotoSystemLogs)
        self.detectionbtn.clicked.connect(self.gotoLogs)
        
        self.logsbtn.clicked.connect(self.showLogsMenu)
        self.registerbtn.clicked.connect(self.gotoRegister)
        self.recordsbtn.clicked.connect(self.gotoRecords)
        
        insert_database.insert_system_logs('Dashboard', ACCOUNT_LOGIN)
        
        self.btnLogout.clicked.connect(self.gotoLogout)
        self.btnProfile.clicked.connect(self.gotoProfile)
    ################################################################
    #  BUTTON MENU FOR LOGS
    ################################################################
    def gotoLogout(self):
        qm = QMessageBox()
        ret = qm.question(self,'WARNING!', "Are you sure you want to exit?", qm.Yes | qm.No)
        if ret == qm.Yes:
            sys.exit(app.exec_())
        
    def showLogsMenu(self):
        if self.hidden:
            self.detectionbtn.show()
            self.systembtn.show()
            self.hidden = False
        else:
            self.detectionbtn.hide()
            self.systembtn.hide()
            self.hidden = True

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
    
    def gotoProfile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    @QtCore.pyqtSlot()
    def openFile(self):
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

        self.whiteemp.hide()
        #self.whiteguest.hide()
        #self.blackemp.hide()
        self.blackguest.hide()
        self.hidden = True;

        self.guestbtn.clicked.connect(self.changeiconguesttrigger)
        self.empbtn.clicked.connect(self.changeiconemptrigger)

        # self.tableWidget.setHorizontalHeaderLabels(["ID", "DATE", "EMPLOYEE ID", 'USER ID'])
        self.loaddata()
        self.gobackbtn.clicked.connect(self.gotoDashboard)
        # To stretch the item lists on tableWidget
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.loaddataguest()

    def changeiconguesttrigger(self):
        self.whiteguest.hide()
        self.blackemp.hide()
        self.whiteemp.show()
        self.blackguest.show()

        self.guestbtn.setStyleSheet(stylesheets.activatedstyle)
        self.empbtn.setStyleSheet(stylesheets.inactivestyle)
        
        self.label_27.hide()
        self.tableWidget.hide()
        self.tableWidgetGuest.show()

    def changeiconemptrigger(self):
        self.whiteguest.show()
        self.blackemp.show()
        self.whiteemp.hide()
        self.blackguest.hide()

        self.empbtn.setStyleSheet(stylesheets.activatedstyle)
        self.guestbtn.setStyleSheet(stylesheets.inactivestyle)
        
        self.label_27.show()
        self.tableWidget.show()
        self.tableWidgetGuest.hide()

    def loaddata(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM detection_logs"
        
        counter = "SELECT COUNT(id) FROM detection_logs"
        tablerow = 0

        # to count how many rows in registered user
        detectionlogs = cur.execute(counter).fetchone()[0]
        self.tableWidget.setRowCount(detectionlogs)



        for row in cur.execute(sqlquery):

            item0 = QTableWidgetItem(str(row[0]))
            item0.setTextAlignment(Qt.AlignCenter)
            item1 = QTableWidgetItem(row[1])
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QTableWidgetItem(row[2])
            item2.setTextAlignment(Qt.AlignCenter)
            item3 = QTableWidgetItem(row[3])
            item3.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(tablerow, 0, item0)  # column 1
            self.tableWidget.setItem(tablerow, 1, item1)  # column 2
            self.tableWidget.setItem(tablerow, 2, item2)  # column 3
            self.tableWidget.setItem(tablerow, 3, item3)  # column 3
            tablerow+=1

        print(cur.execute(sqlquery).rowcount)
    
    def loaddataguest(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM detection_logs_guest"
        
        counter = "SELECT COUNT(id) FROM detection_logs_guest"
        tablerow = 0

         # To stretch the item lists on tableWidget
        self.tableWidgetGuest.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # to count how many rows in registered user
        detectionlogsguest = cur.execute(counter).fetchone()[0]
        self.tableWidgetGuest.setRowCount(detectionlogsguest)

        for row in cur.execute(sqlquery):

            item0 = QTableWidgetItem(str(row[0]))
            item0.setTextAlignment(Qt.AlignCenter)
            item1 = QTableWidgetItem(row[1])
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QTableWidgetItem(row[2])
            item2.setTextAlignment(Qt.AlignCenter)

            self.tableWidgetGuest.setItem(tablerow, 0, item0) # column 1
            self.tableWidgetGuest.setItem(tablerow, 1, item1) # column 2
            self.tableWidgetGuest.setItem(tablerow, 2, item2) # column 3
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
        self.btnBack.clicked.connect(self.gotoDashboard)
        
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

        # Remove horizontal gridlines
        self.tableWidget.setShowGrid(False)
        #self.tableWidget.setStyleSheet('QTableView::item {border-bottom: 1px solid #000000;}')
        
        # self.tableWidget.setTextAlignment()

        for row in cur.execute(sqlquery):

            item0 = QTableWidgetItem(str(row[0]))
            item0.setTextAlignment(Qt.AlignCenter)
            item1 = QTableWidgetItem(row[1])
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QTableWidgetItem(row[2])
            item2.setTextAlignment(Qt.AlignCenter)
            item3 = QTableWidgetItem(row[3])
            item3.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(tablerow, 0, item0) # column 1
            self.tableWidget.setItem(tablerow, 1, item1) # column 2
            self.tableWidget.setItem(tablerow, 2, item2) # column 3
            self.tableWidget.setItem(tablerow, 3, item3) # column 3
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
        db_open.open_db_registeredemployee()
        self.btnBack.clicked.connect(self.gotoDashboard)
        self.btnSave.clicked.connect(self.saveIt)

        self.activebtn.hide()
        self.inactivebtn.hide()
        self.hidden = True
        self.statusbtn.clicked.connect(self.showStatusMenu)
        self.activebtn.clicked.connect(self.changeStatusToActive)
        self.inactivebtn.clicked.connect(self.changeStatusToInactive)
        self.lineId.textChanged.connect(self.idvalue)
        self.lineFirstName.textChanged.connect(self.fnamevalue)
        self.lineLastName.textChanged.connect(self.lnamevalue)
    
    def idvalue(self):
        if len(self.lineId.text()) != 0:
            self.lineId.setStyleSheet(stylesheets.hasnoerrorline)
        else:
            self.lineId.setStyleSheet(stylesheets.haserrorline)
            
    def fnamevalue(self):
        if len(self.lineFirstName.text()) != 0:
            self.lineFirstName.setStyleSheet(stylesheets.hasnoerrorline)
        else:
            self.lineFirstName.setStyleSheet(stylesheets.haserrorline)
        
    def lnamevalue(self):
        if len(self.lineLastName.text()) != 0:
            self.lineLastName.setStyleSheet(stylesheets.hasnoerrorline)
        else:
            self.lineLastName.setStyleSheet(stylesheets.haserrorline)
    
    def showStatusMenu(self):
        if self.hidden:
            self.activebtn.show()
            self.inactivebtn.show()
            self.hidden = False
        else:
            self.activebtn.hide()
            self.inactivebtn.hide()
            self.hidden = True

    def changeStatusToActive(self):
        self.statusbtn.setText(self.activebtn.text())
        self.statusbtn.setStyleSheet(stylesheets.hasnoerrorstatus);
        self.activebtn.hide()
        self.inactivebtn.hide()
        self.hidden = True

    def changeStatusToInactive(self):
        self.statusbtn.setText(self.inactivebtn.text())
        self.activebtn.hide()
        self.inactivebtn.hide()
        self.hidden = True
    
    def has_error_id(self): 
        id = self.lineId.text().replace(' ','')
        # IF id has value then is a valid id
        return not bool(id)
    
    def has_error_first_name(self): 
        id = self.lineFirstName.text().replace(' ','')
        # IF id has value then is a valid first name
        return not bool(id)
    
    def has_error_last_name(self): 
        id = self.lineLastName.text().replace(' ','')
        # IF id has value then is a valid last name
        return not bool(id)
    
    def has_error_status(self):
        check_status = self.statusbtn.text() == 'active' or self.statusbtn.text() == 'inactive'
        return not check_status
    
    # to clear details after successful submit
    def clearDetails(self):
        self.lineId.clear()
        self.lineFirstName.clear()
        self.lineLastName.clear()
        # CLEARING ERROR COLORS
        self.lineId.setStyleSheet(stylesheets.hasnoerrorline)
        self.lineFirstName.setStyleSheet(stylesheets.hasnoerrorline)
        self.lineLastName.setStyleSheet(stylesheets.hasnoerrorline)
        self.statusbtn.setStyleSheet(stylesheets.hasnoerrorstatus)
    
    def saveIt(self, _id= None, _first=None, _last=None, _status=None):
        if self.has_error_id() or self.has_error_first_name() and self.has_error_last_name() or self.has_error_status():
            if self.has_error_id():
                self.lineId.setStyleSheet(stylesheets.haserrorline)
            if self.has_error_first_name():
                self.lineFirstName.setStyleSheet(stylesheets.haserrorline)
            if self.has_error_last_name():
                self.lineLastName.setStyleSheet(stylesheets.haserrorline)
            if self.has_error_status():
                self.statusbtn.setStyleSheet(stylesheets.haserrorstatus)
        else:
            self.statusbtn.setStyleSheet(stylesheets.hasnoerrorstatus)
            try:
                self.labelError.setText('')
                # Create a database or connect to one
                conn = sqlite3.connect('facemaskdetectionDB.db')
                c = conn.cursor()
                # Insert user to the database
                if self.btnSave.text() == 'SAVE':
                    c.execute("INSERT INTO registeredemployee VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
                            {
                                'id_number': self.lineId.text(),
                                'first_name': self.lineFirstName.text(),
                                'last_name': self.lineLastName.text(),
                                'status': self.statusbtn.text(),
                                'registered_by':ACCOUNT_LOGIN,
                            }
                            )
                elif self.btnSave.text() == 'UPDATE':
                    c.execute("INSERT OR REPLACE INTO registeredemployee VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
                            {
                                'id_number': self.lineId.text(),
                                'first_name': self.lineFirstName.text(),
                                'last_name': self.lineLastName.text(),
                                'status': self.statusbtn.text(),
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
                
                self.clearDetails()
            except sqlite3.Error as er:
                self.lineId.setStyleSheet(stylesheets.haserrorline)
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
        self.lineId.setText(_id)
        self.lineId.setDisabled(True)
        self.lineFirstName.setText(_first)
        self.lineLastName.setText(_last)
        self.statusbtn.setText(_status)
        self.btnSave.setText('UPDATE')
        
    
    def gotoDashboard(self):
        #register = RegisterScreen()
        widget.removeWidget(widget.currentWidget())
        #widget.setCurrentIndex(widget.currentIndex() - 1)
        
        

#
# Records window
#
class RecordsScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(RecordsScreen, self).__init__()
        loadUi('records.ui', self)
        
        db_open = DatabaseManager()
        db_open.open_db_registeredemployee()
        
        self.tableWidget.setHorizontalHeaderLabels(["Id", "First Name", "Last Name",'Status', 'Registered By'])
        self.loaddata()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Remove horizontal gridlines
        self.tableWidget.setShowGrid(False)
        #self.tableWidget.setStyleSheet('QTableView::item {border-bottom: 1px solid #000000;}')
        
        self.btnBack.clicked.connect(self.gotoDashboard)
        self.btnRegister.clicked.connect(self.gotoRegister)
        self.btnDelete.clicked.connect(self.gotoDelete)
        self.lineSearch.textChanged.connect(self.search)
        self.btnEdit.clicked.connect(self.edit)
        
        # self.tableWidget.setItem(0,0, QTableWidgetItem.setTextAlignment(4))
        # item = QTableWidgetItem(scraped_age) # create the item
        # item.setTextAlignment(Qt.AlignHCenter) # change the alignment
        
    def loaddata(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM registeredemployee"
        counter = "SELECT COUNT(id_number) FROM registeredemployee"
        tablerow = 0

        # to count how many rows in registered user
        registeredemployees = cur.execute(counter).fetchone()[0]
        self.tableWidget.setRowCount(registeredemployees)
        self.tableWidget.setColumnWidth(0,100)

        for row in cur.execute(sqlquery):

            item0 = QTableWidgetItem(row[0])
            item0.setTextAlignment(Qt.AlignCenter)
            item1 = QTableWidgetItem(row[1])
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QTableWidgetItem(row[2])
            item2.setTextAlignment(Qt.AlignCenter)
            item3 = QTableWidgetItem(row[3])
            item3.setTextAlignment(Qt.AlignCenter)
            item4 = QTableWidgetItem(row[4])
            item4.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(tablerow, 0, item0) # column 1
            self.tableWidget.setItem(tablerow, 1, item1) # column 2
            self.tableWidget.setItem(tablerow, 2, item2) # column 3
            self.tableWidget.setItem(tablerow, 3, item3) # column 4
            self.tableWidget.setItem(tablerow, 4, item4) # column 5
            tablerow+=1

        print(cur.execute(sqlquery).rowcount)
    
    def gotoDashboard(self):
        widget.removeWidget(widget.currentWidget())
        
    def gotoRegister(self):
        #self.gotoDashboard()
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def gotoDelete(self):
        # set current row on table
        row = self.tableWidget.currentRow()
        # set current column on table
        # col = self.tableWidget.currentColumn() 
        
        cellValue = self.tableWidget.item(row,0).text()
        print('ROW: '+str(row))
        
        idName = str(self.input_delete_id(cellValue))
        print("id name: "+idName)
        
        if idName:
            conn = sqlite3.connect('facemaskdetectionDB.db')
            # Create a cursor
            c = conn.cursor()
            c.execute("DELETE FROM registeredemployee WHERE id_number=(:id_number)",
                    {
                        'id_number':idName,
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
        name = self.lineSearch.text()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            # if the search is *not* in the item's text *do not hide* the row
            self.tableWidget.setRowHidden(row, name not in item.text().lower())    
    
    def edit(self):
        register = RegisterScreen()
        
        row = self.tableWidget.currentRow()
        
        cellValue = self.tableWidget.item(row,0).text()
        
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("SELECT * FROM registeredemployee WHERE id_number=(:id_number)",
                    {
                        'id_number':cellValue,
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
    
class ProfileScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(ProfileScreen, self).__init__()
        loadUi('profile.ui', self)
        self.btnBack.clicked.connect(self.gotoDashboard)
        
        self.linePassword.setEchoMode(QLineEdit.Password)

    # def on_btn_show_pwd_toggled(self, checked):
    #     if checked:
    #         self.linePassword.setEchoMode(QLineEdit.Password)
    #     else:
    #         self.linePassword.setEchoMode(QLineEdit.Normal)
        
    def gotoDashboard(self):
        widget.removeWidget(widget.currentWidget())
      
    
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