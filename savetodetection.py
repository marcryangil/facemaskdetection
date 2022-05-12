import sqlite3
import time
from datetime import datetime
def save(idnumber, userid):
    try:
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()
        if idnumber == 'Guest':
            sqlquery = "INSERT INTO detectionlogguest VALUES(:id, :date, :adminid)"
            cur.execute(sqlquery, {
                'id': None,
                'date': datetime.now().strftime("%B %d, %Y %I:%M %p"),
                'adminid': userid,
            })
        else:
            sqlquery = "INSERT INTO detectionlogpersonnel VALUES(:id, :date, :personnelid, :adminid)"
            cur.execute(sqlquery, {
                                    'id': None,
                                    'date': datetime.now().strftime("%B %d, %Y %I:%M %p"),
                                    'personnelid': idnumber,
                                    'adminid': userid,
                                  })
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
    
    # CREATED FILE FOR db_management.py




