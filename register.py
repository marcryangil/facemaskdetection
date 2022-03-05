#
#   UNDER CONSTRUCTION HAHAHA
#


# from main import *


# class RegisterScreen(QMainWindow):
#     # loading up the register
#     def __init__(self):
#         super(RegisterScreen, self).__init__()
        
#         loadUi('register.ui', self)
#         self.open_db()
#         self.btn_back.clicked.connect(self.gotoDashboard)
#         self.btn_save.clicked.connect(self.save_it)
        

#     def open_db(self):
#         # Create a database or connect to one
#         conn = sqlite3.connect('facemaskdetectionDB.db')
#         # Create a cursor
#         c = conn.cursor()

#         # Create table
#         c.execute("""CREATE TABLE if not exists registered_user(
#                 id_number TEXT,
#                 first_name TEXT,
#                 last_name TEXT,
#                 status TEXT
#             )
#             """) 

#         # Commit changes
#         conn.commit()

#         # Close connection
#         conn.close()
    
#     def has_error(self):
#         # added .replace(' ','') to remove whitespaces
#         id = self.line_id.text().replace(' ','')
#         first_name = self.line_first_name.text().replace(' ','')
#         last_name = self.line_last_name.text().replace(' ','')
#         return not bool(len(id) and len(first_name) and len(last_name))
    
#     def is_select(self):
#         return self.comboBox_status_1.currentText() == 'Select'
    
#     # to clear details after successful submit
#     def clear_details(self):
#         self.line_id.clear()
#         self.line_first_name.clear()
#         self.line_last_name.clear()
#         ################################################################
#         # self.line_id.setCurrentIndex = 0
#         # help me. How to set Select after submit
#         ################################################################
    
#     def save_it(self):
        
#         if self.has_error() or self.is_select():
#             self.label_error.setText('Error, please check fields')
#             if self.is_select():
#                 self.comboBox_status_1.setStyleSheet(
#                                                     "color: rgb(0,0,0);\n"
#                                     "background-color: rgb(255,255,255);\n"
#                                         "border-style: solid;\n"
#                                         "border-width: 1px;\n"
#                                         "border-radius: 8px;\n"
#                                         "border-color: rgb(140, 140, 140)\n;"
#                                         "padding-left: 10px;\n"
#                                         "padding-right: 10px;\n"
#                                         "border-color: red;\n"
#                 )
#         else:
#             self.comboBox_status_1.setStyleSheet(
#                                                  "color: rgb(0,0,0);\n"
#                                 "background-color: rgb(255,255,255);\n"
#                                     "border-style: solid;\n"
#                                     "border-width: 1px;\n"
#                                     "border-radius: 8px;\n"
#                                     "border-color: rgb(140, 140, 140)\n;"
#                                     "padding-left: 10px;\n"
#                                     "padding-right: 10px;\n"
#                 )
#             self.label_error.setText('')
#             # Create a database or connect to one
#             conn = sqlite3.connect('facemaskdetectionDB.db')
#             # Create a cursor
#             c = conn.cursor()
            
#             # Insert user to the database
#             c.execute("INSERT INTO registered_user VALUES(:id_number, :first_name, :last_name, :status)",
#                     {
#                         'id_number': self.line_id.text(),
#                         'first_name': self.line_first_name.text(),
#                         'last_name': self.line_last_name.text(),
#                         'status': self.comboBox_status_1.currentText()
#                     }
#                     )            
#             # Commit changes
#             conn.commit()
#             # Close connection
#             conn.close()
            
#             # Pop up message box
#             msg = QMessageBox()
#             msg.setWindowTitle('Saved to the Database!')
#             msg.setText('User has been saved')
#             msg.setIcon(QMessageBox.Information)
#             x = msg.exec_()
            
#             self.clear_details()
    
        
        
#     def gotoDashboard(self):
#         dashboard = DashboardScreen()
#         widget.addWidget(dashboard)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
