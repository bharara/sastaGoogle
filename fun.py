import hashlib
import pymysql
import os, os.path
from pathlib import Path
import string

rootFolder = 'sastaGoogle/static/simple/articles'

# Prepare Punctuation Striper
translator = str.maketrans('', '', string.punctuation)

# Establishes the connection to database
def dbSetup():
	conn = pymysql.connect(
	    host='127.0.0.1',
	    port=3306,
	    user='root',
	    passwd='pword',
	    db='sastaGoogle')
	cur = conn.cursor()
	return conn, cur

# Closes the connection
def dbClose(conn, cur):
	cur.close()
	conn.close()

## Hashing up the filename for storing: 32-bit Unique
def hashF (val):
	return hashlib.md5(val.encode()).hexdigest()

def getFiles(rF = rootFolder):
	arrayofpath = Path (rF).glob("**/*")
	files = [x for x in arrayofpath if x.is_file()]
	return files