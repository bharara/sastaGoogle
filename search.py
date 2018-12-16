import os, os.path
from pathlib import Path
import hashlib
import pymysql
import string
import operator

# Prepare Punctuation Striper
translator = str.maketrans('', '', string.punctuation)

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

def search (words):

	fileMap = {}
	for word in words:
		getFile(fileMap, word)

	for key, val in fileMap.items():
		fileMap[key] = val[0] * val[1]

	for file,score in sorted(fileMap.items(), key=operator.itemgetter(1), reverse=True):
		Google.execute("""SELECT fileAdd
		FROM files
		WHERE fileID = "%s";"""
		% (file))

		data = Google.fetchall()
		print(score, data[0][0][7:-5].replace('_',' '))

def getFile(fileMap, word):
	Google.execute("""SELECT fileID, score
		FROM wordfile
		WHERE wordID = "%s"
		LIMIT 10;"""
		% (hashF(word)))

	data = Google.fetchall()
	for i in data:
		if i[0] in fileMap:
			fileMap[i[0]][0] += i[1]
			fileMap[i[0]][1] += 1
		else:
			fileMap[i[0]] = [i[1],1]


word = "dubai india"
#word = input("Enter search word: ")
word = word.lower().translate(translator).split()
search(word)

# Closes the connection
Google.close()
conn.close()
