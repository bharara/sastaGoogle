## Writes fileID and address into file table

import fun

def getInsertables(files):
	r = []
	for filename in files:
		filename = str(filename)[64:]

		## ALL talk pages, user pages and templates are ignored
		if any(x in  filename.lower() for x in ['talk~','user~','template~','wikipedia~']):
			continue
		
		## Remaing files are categorized as
		## 1 for articles
		## 2 for Categories
		## 3 for Images
		if 'Category~' in filename: cat = 2
		elif 'Image~' in filename: cat = 3
		else: cat = 1

		r.append((fun.hashF(filename), filename.replace("\\","/",4), cat))

	return r

def writeToDB(ins):
	try:
	    Google.executemany("INSERT INTO files (fileID, fileAdd, category) VALUES (%s, %s, %s)", ins)
	    conn.commit()
	except:
		conn.rollback()

files = fun.getFiles()
conn, Google = fun.dbSetup()

ins = getInsertables(files)
writeToDB(sorted(ins))

fun.dbClose(conn, Google)