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
        c.execute("""CREATE TABLE if not exists personnel(
                id TEXT UNIQUE,
                firstname TEXT,
                lastname TEXT,
                status TEXT,
                registeredby TEXT,
                registereddate TEXT
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
        c.execute("""CREATE TABLE if not exists systemlog(
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
                date: datetime.now().strftime("%B %d, %Y %I:%M %p"),
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
        c.execute("INSERT INTO systemlog VALUES(null, :date, :action, :adminid)",
                {
                    'date': datetime.now().strftime("%B %d, %Y %I:%M %p"),
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
                    'date': datetime.now().strftime("%B %d, %Y %I:%M %p"),
                    'personnelid': personnelid,
                    'adminid': adminid,      
                }
                )
        
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()