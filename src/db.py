import json
import sqlite3
from os import environ as env

def connect(database=None):
    if not database:
        raise Exception("Mete una base de datos")

    return sqlite3.connect( database )

def get_db_data(conn, query: str, json_str = False, json_dict = False ):
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    rows = db.execute(query).fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps( [dict(ix) for ix in rows] )
    
    if json_dict:
        return [dict(ix) for ix in rows]

    return rows

def execute_db(conn, query):
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    rows = db.execute(query)

    conn.commit()
    conn.close()
