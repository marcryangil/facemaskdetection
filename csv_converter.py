import pandas as pd
import sqlite3
import os


def converter(table_name):
    newpath = r'.\\exported' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    conn = sqlite3.connect('facemaskdetectionDB.db')
    df = pd.read_sql("SELECT * FROM \'"+table_name+"\'", conn)
    
    df.to_csv(r".\\exported\\"+table_name+".csv")
    # r"" + RESULTS_DIR + "sample.csv"
    
    print('EXPORTING CSV FILE '+table_name)