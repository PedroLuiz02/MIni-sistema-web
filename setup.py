import sqlite3
import pandas

conn = sqlite3.connect('banco.bd')

data_frame = pandas.read_csv('data/pet.csv')

data_frame.to_sql("pet", conn, if_exists='replace', index=False)

conn.close()