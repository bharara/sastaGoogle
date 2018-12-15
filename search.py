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
	for word in words.split():
		getFile(fileMap, word)

	for file,score in sorted(fileMap.items(), key=operator.itemgetter(1), reverse=True):
		Google.execute("""SELECT fileAdd, category
		FROM files
		WHERE fileID = "%s";"""
		% (file))

		data = Google.fetchall()
		for i in data:
			print(score, i[0], i[1])

def getFile(fileMap, word):
	Google.execute("""SELECT fileID, score
		FROM wordfile
		WHERE wordID = "%s";"""
		% (hashF(word)))

	data = Google.fetchall()
	for i in data:
		if i[0] in fileMap:
			fileMap[i[0]] += i[1]
		else:
			fileMap[i[0]] = i[1]

word = input("Enter search word: ")
word = word.lower().translate(translator)
search(word)

# Closes the connection
Google.close()
conn.close()
