import numpy as np
import sqlite3 as sql

conn = sql.connect(".\rl.db")

cursor = conn.cursor()

# cursor.execute("CREATE TABLE experiment (id integer, name text)")
cursor.execute("INSERT INTO experiment VALUES (1, 'test_exp')")
cursor.execute("INSERT INTO experiment VALUES (2, 'test_exp')")

conn.commit()
