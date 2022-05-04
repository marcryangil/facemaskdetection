import pandas as pd
import sqlite3

def converter(table_name):
    conn = sqlite3.connect('facemaskdetectionDB.db')
    df = pd.read_sql("SELECT * FROM \'"+table_name+"\'", conn)
    df.to_csv(r".\\exported\\"+table_name+".csv")
    # r"" + RESULTS_DIR + "viajes_withDIF_AUX_42.csv"
    print('EXPORTING CSV FILE '+table_name)