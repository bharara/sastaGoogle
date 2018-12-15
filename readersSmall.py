from bs4 import BeautifulSoup
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

def runfiles(filename):
	arrayofpath = Path (filename).glob("**/*")
	files=[x for x in arrayofpath if x.is_file()]
	for i in files:
		i = str(i)
		if any(x in i[40:].lower() for x in ['talk~','user~','template~','category~','image~']):
			continue
		countWords(i)

def countWords(file):
		
		soup = BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')
		filehash = hashF(file[33:])		
		print(file[33:],filehash)

		wordMap = {} 

		for i in soup.find_all('title'):
			for j in i.get_text().split():
				incrementValue(wordMap,j,100)
		for i in soup.find_all('h1'):
			for j in i.get_text().split():
				incrementValue(wordMap,j,100)
		for i in soup.find_all('h2'):
			for j in i.get_text().split():
				incrementValue(wordMap,j,10)
		for i in soup.find_all('h3'):
			for j in i.get_text().split():
				incrementValue(wordMap,j,30)
		for i in soup.find_all('h4'):
			for j in i.get_text().split():
				incrementValue(wordMap,j,20)
		for i in soup.get_text().split():
			incrementValue(wordMap,i,1)

		for word,score in sorted(wordMap.items(), key=operator.itemgetter(1), reverse=True):
			Google.execute("""INSERT INTO wordfile (fileID, wordID, score) VALUES ("%s", "%s", "%d")""" % (filehash, hashF(word), score))
			
def incrementValue(wMap,word,score):
	word = word.lower().translate(translator)
	if word in wMap:
		wMap[word] += score
	else:
		wMap[word] = score


# Prepare Files to Be fond in directory
filename = 'D:/3- DSA/Project/simple/articles/u/n/i'

# Write files to DB
runfiles(filename)
conn.commit()

# Closes the connection
Google.close()
conn.close()