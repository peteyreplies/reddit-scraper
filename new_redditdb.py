#import libraries
import sqlite3

conn = None
db = None

def connect():
	'''
	open and create the database if it doesn't exist
	'''
	global conn, db
	conn = sqlite3.connect("picsdb.db")
	db = conn.cursor()
	db.execute('''CREATE TABLE IF NOT EXISTS new_pics (author_name TEXT, created_time INT, 
			reddit_id TEXT UNIQUE, title TEXT, submitted_url TEXT, domain TEXT, 
			reddit_shortlink TEXT, imgur TEXT)''')

def insert(info):
	'''
	if it is a new record, insert it to the database
	'''
	global conn,db
	sql = ""
	sql += 'INSERT OR IGNORE INTO new_pics ('
	sql += ', '.join(info.keys())
	sql += ')'
	sql += ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
	db.execute(sql, info.values())
	conn.commit()
	
	
def close():
	global conn
	conn.close()
