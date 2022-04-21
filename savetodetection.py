import sqlite3
import time
from datetime import datetime
def save(idnumber, userid):
    try:
        connection = sqlite3.connect("facemaskdetectionDB.db")
        cur = connection.cursor()

        if idnumber == 'guest':
            sqlquery = "INSERT INTO detection_logs_guest VALUES(:id, :date, :user_id)"
            cur.execute(sqlquery, {
                'id': None,
                'date': datetime.now().isoformat(' ', 'seconds'),
                'user_id': userid,
            })
        else:
            sqlquery = "INSERT INTO detection_logs VALUES(:id, :date, :employee_id, :user_id)"
            cur.execute(sqlquery, {
                                    'id': None,
                                    'date': datetime.now().isoformat(' ', 'seconds'),
                                    'employee_id': idnumber,
                                    'user_id': userid,
                                  })
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
    
    # CREATED FILE FOR db_management.py




