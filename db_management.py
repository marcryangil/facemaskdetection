import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime

class DatabaseManager():
    
    def open_db_registeredemployee(self):
        # print("THE ACCOUNT: "+ LOGIN_USER)
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
        # print("THE ACCOUNT: "+ LOGIN_USER)
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        
        # Create table
        c.execute("""CREATE TABLE if not exists system_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                action TEXT,
                adminid TEXT
            )
            """) 

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
        
    def open_db_detection_logs(self):
        # print("THE ACCOUNT: "+ LOGIN_USER)
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        
        # Create table
        c.execute("""CREATE TABLE if not exists detectionlogpersonnel(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date: datetime.now().isoformat(' ', 'seconds'),
                personnelid TEXT,
                adminid TEXT
            )
            """) 

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
    
    
        
class InsertDatabase():
    def insert_system_logs(self, action, adminid):
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("INSERT INTO system_logs VALUES(null, :date, :action, :adminid)",
                {
                    'date': datetime.now().isoformat(' ', 'seconds'),
                    'action': action,
                    'adminid': adminid,      
                }
                )
        
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        
        
    def insert_detection_logs(self, personnelid, adminid):
        # Create a database or connect to one
        conn = sqlite3.connect('facemaskdetectionDB.db')
        # Create a cursor
        c = conn.cursor()
        c.execute("INSERT INTO detectionlogpersonnel VALUES(null, :date, :personnelid, :adminid)",
                {
                    'date': datetime.now().isoformat(' ', 'seconds'),
                    'personnelid': personnelid,
                    'adminid': adminid,      
                }
                )
        
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()