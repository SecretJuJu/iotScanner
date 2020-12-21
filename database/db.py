import sqlite3
def get_macMap_Connent():
    with sqlite3.connect("macMap.db", check_same_thread=False) as conn:
        return conn
