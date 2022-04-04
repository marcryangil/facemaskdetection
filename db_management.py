import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime

class DatabaseManager():
    
    def open_db_registeredemployee(self):
        # print("THE ACCOUNT: "+ ACCOUNT_LOGIN)
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        
        # Create table
        c.execute("""CREATE TABLE if not exists registeredemployee(
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
    
    def open_db_system_logs(self):
        # print("THE ACCOUNT: "+ ACCOUNT_LOGIN)
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        
        # Create table
        c.execute("""CREATE TABLE if not exists system_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                action TEXT,
                user_id TEXT
            )
            """) 

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
        
    def open_db_detection_logs(self):
        # print("THE ACCOUNT: "+ ACCOUNT_LOGIN)
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        
        # Create table
        c.execute("""CREATE TABLE if not exists detection_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                employee_id TEXT,
                user_id TEXT
            )
            """) 

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
class InsertDatabase():
    def insert_system_logs(self, action, user_id):
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("INSERT INTO system_logs VALUES(null, :date, :action, :user_id)",
                {
                    'date': datetime.now().isoformat(' ', 'seconds'),
                    'action': action,
                    'user_id': user_id,      
                }
                )
        
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
        
    def insert_detection_logs(self, employee_id, user_id):
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("INSERT INTO detection_logs VALUES(null, :date, :employee_id, :user_id)",
                {
                    'date': datetime.now().isoformat(' ', 'seconds'),
                    'employee_id': employee_id,
                    'user_id': user_id,      
                }
                )
        
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()