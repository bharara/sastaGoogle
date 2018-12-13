## This file writes all files and there address to database

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
    db='sastaGoogle')
Google = conn.cursor()

## Hashing up the filename/word for storing
def hashF (val):
	return hashlib.md5(val.encode()).hexdigest()

def writeToDB(files):
	for i in files:
		i = str(i)
		## ALL talk pages, user pages and templates are ignored
		if any(x in  i[40:].lower() for x in ['talk~','user~','template~']):
			continue
		
		## Remaing files are categorized as
		## 1 for articles
		## 2 for Categories
		## 3 for Images
		if 'Category~' in i[40:]: cat = 2
		elif 'Image~' in i[40:]: cat = 3
		else: cat = 1

		try:
			Google.execute("""INSERT INTO files (fileID, fileAdd, category) VALUES ("%s", "%s", "%d")""" % (hashF(i), i, cat))
		except:
			print(i)


# Prepare Files to Be fond in directory
filename = 'D:/3- DSA/Project/simple/articles/'
arrayofpath = Path (filename).glob("**/*")
files=[x for x in arrayofpath if x.is_file()]

# Write files to DB
writeToDB(files)
conn.commit()

# Closes the connection
Google.close()
conn.close()
