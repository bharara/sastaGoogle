from bs4 import BeautifulSoup
import os, os.path
from pathlib import Path
import hashlib
import pymysql

# Establishes the connection to database
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='090078601',
    db='chotaGoogle')
Google = conn.cursor()

## Hashing up the filename/word for storing
def hashF (val):
	return hashlib.md5(val.encode()).hexdigest()

def countWords(file):
	

		try:
			Google.execute("""INSERT INTO files (fileID, fileAdd, category) VALUES ("%s", "%s", "%d")""" % (hashF(i), i, cat))
		except:
			print(i)

def runfiles(filename):
	arrayofpath = Path (filename).glob("**/*")
	files=[x for x in arrayofpath if x.is_file()]
	for i in files:
		countWords(i)

# Prepare Files to Be fond in directory
filename = 'D:/3- DSA/Project/simple/articles/u/n/i'

# Write files to DB
runfiles(filename)

conn.commit()

# Closes the connection
Google.close()
conn.close()