## This file writes all files and there address to database
## Password at line 16 and address at root 9 are relitive to the local computer

import os, os.path
from pathlib import Path
import hashlib
import pymysql

rootFolder = 'D:/3- DSA/Project/simple/articles'

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
		i = str(i)[33:]
		## ALL talk pages, user pages and templates are ignored
		if any(x in  i.lower() for x in ['talk~','user~','template~']):
			continue
		
		## Remaing files are categorized as
		## 1 for articles
		## 2 for Categories
		## 3 for Images
		if 'Category~' in i: cat = 2
		elif 'Image~' in i: cat = 3
		else: cat = 1

		try:
			Google.execute("""INSERT INTO files (fileID, fileAdd, category) VALUES ("%s", "%s", "%d")""" % (hashF(i), i.replace("\\","/",4), cat))
			print(hashF(i), i, cat)
		except:
			print(i, cat)


# Prepare Files to Be fond in directory

filename = rootFolder+''
arrayofpath = Path (filename).glob("**/*")
files=[x for x in arrayofpath if x.is_file()]

# Write files to DB
writeToDB(files)
conn.commit()

# Closes the connection
Google.close()
conn.close()
