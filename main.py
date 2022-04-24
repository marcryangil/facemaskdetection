import base64
import os
import sqlite3, traceback
import sys
from datetime import datetime
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QStackedWidget, QMessageBox, QMenu, QLineEdit, \
    QTableWidgetItem, QPushButton, QHBoxLayout, QFormLayout, QLabel, QDesktopWidget
from PyQt5.QtGui import QPixmap
import resources
from db_management import DatabaseManager, InsertDatabase
import stylesheets
import real_time_face_recognition
import savetolocal
import verifylocal

LOGIN_ID = ''
LOGIN_USER = ''
LOGIN_PASS = ''
SYSTEM_LOGS = []

insert_database = InsertDatabase()
class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.Tool | Qt.CustomizeWindowHint)
        # self.setWindowFlag(Qt.FramelessWindowHint)

        # self.windowFlags.hide()
        # flags = Qt.WindowFlags()
        # self.FramelessWindowHint()
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbtn.clicked.connect(self.loginfunction)

        self._login_username = ''

        self.usernamefield.textChanged.connect(self.usernamevalue)
        self.passwordfield.textChanged.connect(self.passwordvalue)
        self.passwordfield.setEchoMode(QLineEdit.Password)

        self.pushButtonHide.clicked.connect(self.toggleVisibility)
        self.label_hide.hide()


    def toggleVisibility(self):
        if self.passwordfield.echoMode() == QLineEdit.Normal:
            self.passwordfield.setEchoMode(QLineEdit.Password)
            self.label_show.show()
            self.label_hide.hide()
            print('HIDING')
        else:
            self.passwordfield.setEchoMode(QLineEdit.Normal)
            print('SHOWING')
            self.label_hide.show()
            self.label_show.hide()

    # def toggleVisibility(self):
    #     if self.passwordfield.echoMode()==QLineEdit.Normal:
    #         self.passwordfield.setEchoMode(QLineEdit.Password)
    #     else:
    #         self.passwordfield.setEchoMode(QLineEdit.Normal)

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
                global LOGIN_ID
                global LOGIN_USER
                global LOGIN_PASS

                getId = 'SELECT * FROM users WHERE username= \'' + username + "\'"
                cur.execute(getId)

                LOGIN_ID = cur.fetchone()[0]
                LOGIN_USER = username
                LOGIN_PASS = password

                open_database = DatabaseManager()
                open_database.open_db_system_logs()
                self.errorlabel.setText("")
                self.gotoDashboard()
                insert_database.insert_system_logs('Login', LOGIN_USER)

            else:
                self.errorlabel.setText("Invalid username or password.")
                self.usernamefield.setStyleSheet(stylesheets.haserrorline)
                self.passwordfield.setStyleSheet(stylesheets.haserrorline)

            # Commit changes
            conn.commit()
            # Close connection
            conn.close()

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

        insert_database.insert_system_logs('Dashboard', LOGIN_USER)

        self.btnLogout.clicked.connect(self.gotoLogout)
        self.btnProfile.clicked.connect(self.gotoProfile)

    ################################################################
    #  BUTTON MENU FOR LOGS
    ################################################################
    def gotoLogout(self):
        qm = QMessageBox()
        ret = qm.question(self,'WARNING!', "Are you sure you want to logout?", qm.Yes | qm.No)
        if ret == qm.Yes:
            # widget.removeWidget(widget.currentWidget())
            insert_database.insert_system_logs('Logged out', LOGIN_USER)
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)

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
        insert_database.insert_system_logs('Logs - Detection', LOGIN_USER)
        logs = LogScreen()
        widget.addWidget(logs)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoRegister(self):
        insert_database.insert_system_logs('Register Face', LOGIN_USER)
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLaunch(self):
        insert_database.insert_system_logs('Launch', LOGIN_USER)
        savetolocal.save()
        verifylocal.start()
        real_time_face_recognition.start(LOGIN_USER)

    def gotoRecords(self):
        insert_database.insert_system_logs('Records', LOGIN_USER)
        records = RecordsScreen()
        widget.addWidget(records)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoProfile(self):
        insert_database.insert_system_logs('Profile', LOGIN_USER)
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @QtCore.pyqtSlot()
    def openFile(self):
        insert_database.insert_system_logs('Get Started', LOGIN_USER)
        url = QtCore.QUrl.fromLocalFile("Get Started.pdf")
        QtGui.QDesktopServices.openUrl(url)

    def gotoSystemLogs(self):
        insert_database.insert_system_logs('Logs - System', LOGIN_USER)
        system_logs = SystemLogScreen()
        widget.addWidget(system_logs)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# FOR LOGS - DETECTION
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
        sqlquery = "SELECT * FROM detection_logs WHERE NOT employee_id= \'"+'Guest'+"\'"

        counter = "SELECT COUNT(id) FROM detection_logs WHERE NOT employee_id= \'"+'Guest'+"\'"
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
        self.btnLaunch.clicked.connect(self.launch)
        self.btnshowlaunch.clicked.connect(self.showbtnlaunch)

        self.activebtn.hide()
        self.inactivebtn.hide()
        self.hidden = True
        self.launchhidden = False

        self.statusbtn.clicked.connect(self.showStatusMenu)
        self.activebtn.clicked.connect(self.changeStatusToActive)
        self.inactivebtn.clicked.connect(self.changeStatusToInactive)
        self.lineId.textChanged.connect(self.idvalue)
        self.lineFirstName.textChanged.connect(self.fnamevalue)
        self.lineLastName.textChanged.connect(self.lnamevalue)

    def showbtnlaunch(self):
        self.btnLaunch.show()
        self.launchhidden = False

    def setbtntext(self, text):
        if text:
            self.btnSave.setText(f'SAVE {text}')
        else:
            self.btnSave.setText('SAVE')

    def idvalue(self):
        if len(self.lineId.text()) != 0:
            self.lineId.setStyleSheet(stylesheets.hasnoerrorline)
        else:
            self.lineId.setStyleSheet(stylesheets.haserrorline)

    def launch(self):
        import savefaceimage
        self.testtest = savefaceimage.start()

        if self.testtest == True:
            self.btnLaunch.hide()
            self.launchhidden = True

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

    def saveIt(self, _id=None, _first=None, _last=None, _status=None):

        idnumber = self.lineId.text()

        if self.has_error_id() or self.has_error_first_name() or self.has_error_last_name() or self.has_error_status() or not self.launchhidden:
            if self.has_error_id():
                self.lineId.setStyleSheet(stylesheets.haserrorline)
            if self.has_error_first_name():
                self.lineFirstName.setStyleSheet(stylesheets.haserrorline)
            if self.has_error_last_name():
                self.lineLastName.setStyleSheet(stylesheets.haserrorline)
            if self.has_error_status():
                self.statusbtn.setStyleSheet(stylesheets.haserrorstatus)
            if not self.launchhidden:
                self.btnLaunch.setStyleSheet(stylesheets.haserrorbtnlaunch)
        else:
            self.statusbtn.setStyleSheet(stylesheets.hasnoerrorstatus)
            try:

                self.labelError.setText('')
                # Create a database or connect to one
                conn = sqlite3.connect('facemaskdetectionDB.db')
                c = conn.cursor()
                # Insert user to the database
                if self.btnSave.text() == 'SAVE' and self.launchhidden:
                    c.execute("INSERT INTO registeredemployee VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
                            {
                                'id_number': idnumber,
                                'first_name': self.lineFirstName.text(),
                                'last_name': self.lineLastName.text(),
                                'status': self.statusbtn.text(),
                                'registered_by': LOGIN_USER,
                            }
                            )
                    conn.commit()
                    self.clearDetails()

                elif self.btnSave.text() == 'UPDATE':
                    c.execute("INSERT OR REPLACE INTO registeredemployee VALUES(:id_number, :first_name, :last_name, :status, :registered_by)",
                            {
                                'id_number': idnumber,
                                'first_name': self.lineFirstName.text(),
                                'last_name': self.lineLastName.text(),
                                'status': self.statusbtn.text(),
                                'registered_by':LOGIN_USER,
                            }
                            )

                    conn.commit()

                # Close connection
                conn.close()

                conn = sqlite3.connect('facemaskdetectionDB.db')
                c = conn.cursor()

                if self.btnSave.text() == 'SAVE' and self.launchhidden:
                    file = open('img_crop.jpg', 'rb').read()
                    file = base64.b64encode(file)
                    c.execute(
                        "INSERT INTO RegisteredFaces VALUES(:id, :employee_id, :face, :added_by)",
                        {
                            'id': None,
                            'employee_id': idnumber,
                            'face': file,
                            'added_by': LOGIN_USER,
                        }
                    )
                    conn.commit()
                    conn.close()
                    self.clearDetails()
                    self.btnLaunch.show()
                    self.launchhidden = False


                # Pop up message box
                msg = QMessageBox()
                msg.setWindowTitle('Saved to the Database!')
                msg.setText('User has been saved')
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()


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
        self.label_7.setText('UPDATE')
        self.facedatalbl.hide()
        self.imagelabel.hide()
        self.btnshowlaunch.hide()
        self.btnLaunch.hide()
        self.btnSave.setGeometry(382, 280, 191, 41)

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
        self.btnRegisteredFaces.clicked.connect(self.gotoRegisteredFaces)

        
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
            c.execute("DELETE FROM registeredemployee WHERE id_number=\'"+idName+"\'")

                    
            conn.commit()
            conn.close()

        # reload the data after deletion
        self.loaddata()

    def input_delete_id(self,cell_name):
        text, result = QtWidgets.QInputDialog.getText(self, 'Delete Record', 'Enter id number: ',text=cell_name)

        if result == True:
            return text

    def search(self):
        name = self.lineSearch.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0) # id number
            
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

    def gotoRegisteredFaces(self):

        registeredfaces = RegisteredFacesScreen()
        # pass
        widget.addWidget(registeredfaces)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ProfileScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(ProfileScreen, self).__init__()
        loadUi('profile.ui', self)
        self.btnBack.clicked.connect(self.gotoDashboard)
        self.passwordfield.setEchoMode(QLineEdit.Password)
        self.pushButtonHide.clicked.connect(self.toggleVisibility)
        self.label_hide.hide()
        self.lineId.setText(LOGIN_ID)
        self.usernamefield.setText(LOGIN_USER)
        self.passwordfield.setText(LOGIN_PASS)
        self.btnUpdate.setEnabled(False)
        self.usernamefield.textChanged.connect(self.enableUpdateButton)
        self.passwordfield.textChanged.connect(self.enableUpdateButton)
        self.btnUpdate.clicked.connect(self.updateProfile)

        self.temp_user = self.usernamefield.text()
        self.temp_pass = self.passwordfield.text()

    def enableUpdateButton(self):
        self.btnUpdate.setEnabled(True)
    def toggleVisibility(self):
        if self.passwordfield.echoMode() == QLineEdit.Normal:
            self.passwordfield.setEchoMode(QLineEdit.Password)
            self.label_show.show()
            self.label_hide.hide()
            print('HIDING')
        else:
            self.passwordfield.setEchoMode(QLineEdit.Normal)
            print('SHOWING')
            self.label_hide.show()
            self.label_show.hide()
            # self.pushButtonHide.show()

    def updateProfile(self):
        if (self.temp_user == self.usernamefield.text() and self.temp_pass == self.passwordfield.text()):
            msg = QMessageBox()
            msg.setWindowTitle('NO CHANGES SAVED!')
            msg.setText('NO CHANGES COMMITTED')
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        elif (len(self.usernamefield.text().replace(' ','')) != 0 and len(self.passwordfield.text().replace(' ','')) != 0):
            conn = sqlite3.connect('facemaskdetectionDB.db')
            c = conn.cursor()
                # Insert user to the database
            c.execute("INSERT OR REPLACE INTO users VALUES(:id, :username, :password)",
                    {
                        'id': self.lineId.text(),
                        'username': self.usernamefield.text(),
                        'password': self.passwordfield.text(),
                        }
                    )
            # self.usernamefield.setText(USERNAME)
            # self.passwordfield.setText(LOGIN_PASS)
                    # Commit changes
            conn.commit()
            # Close connection
            conn.close()
            global LOGIN_ID
            global LOGIN_USER
            global LOGIN_PASS

            LOGIN_ID = self.lineId.text()
            LOGIN_USER = self.usernamefield.text()
            LOGIN_PASS = self.passwordfield.text()

            self.temp_user = self.usernamefield.text()
            self.temp_pass = self.passwordfield.text()
            insert_database.insert_system_logs('Profile - Updated', LOGIN_USER)
            msg = QMessageBox()
            msg.setWindowTitle('CHANGES SAVED!')
            msg.setText('User has been saved')
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()


    def gotoDashboard(self):
        widget.removeWidget(widget.currentWidget())


class RegisteredFacesScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(RegisteredFacesScreen, self).__init__()
        loadUi('registeredfaces.ui', self)

        db_open = DatabaseManager()
        db_open.open_db_registeredemployee()

        self.tableWidget.setHorizontalHeaderLabels(["Id", "Employee ID", "Faces",'Added by', 'Registered By'])
        self.loaddata()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Remove horizontal gridlines
        self.tableWidget.setShowGrid(False)
        #self.tableWidget.setStyleSheet('QTableView::item {border-bottom: 1px solid #000000;}')

        self.btnBack.clicked.connect(self.gotoDashboard)
        self.btnDelete.clicked.connect(self.gotoDelete)
        # reuse btnRegister and btnDelete of records
        # recordsScreen = RecordsScreen()

        self.btnRegister.clicked.connect(self.gotoRegister)

        self.lineSearch.textChanged.connect(self.search)
    def gotoRegister(self):
        recordsScreen = RecordsScreen()
        recordsScreen.gotoRegister()
        # print('I HAVE REUSED THE FUNCTION')
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
            c.execute("DELETE FROM registeredemployee WHERE id_number=\'"+idName+"\'")
            conn.commit()
            conn.close()

        # reload the data after deletion
        self.loaddata()

    def input_delete_id(self,cell_name):
        text, result = QtWidgets.QInputDialog.getText(self, 'Delete Record', 'Enter id number: ',text=cell_name)

        if result == True:
            return text
    def gotoDashboard(self):
        widget.removeWidget(widget.currentWidget())
    def loaddata(self):
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM RegisteredFaces"
        counter = "SELECT COUNT(id) FROM RegisteredFaces"
        tablerow = 0

        # to count how many rows in registered user
        registeredfaces = cur.execute(counter).fetchone()[0]
        self.tableWidget.setRowCount(registeredfaces)
        self.tableWidget.setColumnWidth(0,100)


        for row in cur.execute(sqlquery):
            # btn = QtGui.QPushButton('View')
            item0 = QTableWidgetItem(str(row[0]))
            item0.setTextAlignment(Qt.AlignCenter)
            item1 = QTableWidgetItem(row[1])
            item1.setTextAlignment(Qt.AlignCenter)
            #item2 = QTableWidgetItem(row[2])
            # item2 = QTableWidgetItem(self.btnView)
            # button = self.QPushButton('View')
            # item2 = QTableWidgetItem(button)
            #item2.setTextAlignment(Qt.AlignCenter)
            item3 = QTableWidgetItem(row[3])
            item3.setTextAlignment(Qt.AlignCenter)

            btn = QPushButton()
            btn.setText('View')
            btn.setStyleSheet(stylesheets.tablewidgetbutton)
            btn.clicked.connect(self.popupImage)
            #btn.setFixedWidth(50)

            self.tableWidget.setItem(tablerow, 0, item0) # column 1
            self.tableWidget.setItem(tablerow, 1, item1) # column 2
            self.tableWidget.setCellWidget(tablerow, 2, btn) # column 3
            #self.tableWidget.setAlignment(Qt.AlignHCenter)
            self.tableWidget.setItem(tablerow, 3, item3) # column 4

            tablerow+=1

        print(cur.execute(sqlquery).rowcount)

    def popupImage(self):
        row = self.tableWidget.currentRow()
        print(row)
        cellValue = self.tableWidget.item(row,1).text()
        facevalues = self.getFacesData(cellValue)
        recordvalues = self.getRecordsData(cellValue)
        with open("new_image.png", "wb") as new_file:
            new_file.write(base64.decodebytes(facevalues[2]))

        self.gotoLoadFace(facevalues[2], recordvalues)
        

    def getFacesData(self, id):
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("SELECT * FROM RegisteredFaces WHERE employee_id= \'"+id+ "\'")
                    
        rows = c.fetchall()[0]
        values = []
        for row in rows:
            values.append(row)
            # print(row)
    
        conn.commit()
        conn.close()

        return values
    
    def getRecordsData(self, id):
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("SELECT * FROM registeredemployee WHERE id_number= \'"+id+ "\'")
                    
        rows = c.fetchall()[0]
        values = []
        for row in rows:
            values.append(row)
            # print(row)
    
        conn.commit()
        conn.close()

        return values
    
    def gotoLoadFace(self, imagestring, values):

        self.loadface = LoadFaceScreen()
        # temporarily removed 'Face Data for '
        # self.loadface.setWindowTitle('Face Data for '+values[2]+", "+values[1])
        self.loadface.setWindowTitle(values[2]+", "+values[1],)
        self.loadface.show()
        
        # loadface.loadData(imagestring)
        # widget.addWidget(loadface)
        #widget.addWidget(loadface)
        # widget.removeWidget(widget.currentWidget())
        #widget.setCurrentIndex(widget.currentIndex() + 1)

    def search(self):
        name = self.lineSearch.text()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 1)
            # if the search is *not* in the item's text *do not hide* the row
            self.tableWidget.setRowHidden(row, name not in item.text().lower())


class LoadFaceScreen(QMainWindow):
    # loading up the register
    def __init__(self):
        super(LoadFaceScreen, self).__init__()
        loadUi('loadface.ui', self)
        self.setGeometry(500,200, 500, 500)
        self.loadData()
        # self.setWindowTitle('Face Data for, ')
        # enable custom window hint
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)

        # disable (but not hide) close button
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        
    def getDetails(self, values):
        return values
    def loadData(self, imagestring=None, values= None):
        # print(imagestring)
        self.label.setText(str(imagestring))
        pixmap = QPixmap('new_image.png')
        self.label.setPixmap(pixmap)
        
        # todo > remove the image after using the app
    


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

