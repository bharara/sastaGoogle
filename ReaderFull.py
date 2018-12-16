###############
##
##	This code reads the files in /u/n/i folder and store them in chotaGoogle database
##	It also read all words and store them in wordfile table
##
###############
from bs4 import BeautifulSoup
import os, os.path
from pathlib import Path
import hashlib
import pymysql
import string

# Prepare Punctuation Striper
translator = str.maketrans('', '', string.punctuation)

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

def runfiles(filename):
	arrayofpath = Path (filename).glob("**/*")
	files=[x for x in arrayofpath if x.is_file()]
	for i in files:
		i = str(i)
		if any(x in i[40:].lower() for x in ['talk~','user~','template~','category~','image~']):
			continue
		countWords(i)
		conn.commit()

def countWords(file):
		
		soup = BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')
		filehash = hashF(file[33:])		
		print(file[33:],filehash)

		wordMap = {} 

		###### THe Weighatage of different words is
		## title - 100
		## h1 - 100
		## h2 - 10
		## h3 - 30
		## h4 - 20
		## h5 - 0
		## h6 - 0
		## normal text - 1
		################
		for i in soup.find_all('title'):
			for j in i.get_text().lower().translate(translator).split():
				incrementValue(wordMap,j,100)
		for i in soup.find_all('h1'):
			for j in i.get_text().lower().translate(translator).split():
				incrementValue(wordMap,j,100)
		for i in soup.find_all('h2'):
			for j in i.get_text().lower().translate(translator).split():
				incrementValue(wordMap,j,10)
		for i in soup.find_all('h3'):
			for j in i.get_text().lower().translate(translator).split():
				incrementValue(wordMap,j,30)
		for i in soup.find_all('h4'):
			for j in i.get_text().lower().translate(translator).split():
				incrementValue(wordMap,j,20)
		for i in soup.get_text().lower().translate(translator).split():
			incrementValue(wordMap,i,1)

		for word,score in wordMap.items():
			# print(word, score)
			try:
				Google.execute("""INSERT INTO wordfile (fileID, wordID, score) VALUES ("%s", "%s", "%d")""" % (filehash, hashF(word), score))
			except:
				print (filehash, word, score)
				errorCount += 1
def incrementValue(wMap,word,score):
	if word in wMap:
		wMap[word] += score
	else:
		wMap[word] = score


# Prepare Files to Be fond in directory
filename = 'D:/3- DSA/Project/simple/articles'
errorCount = 0
# Write files to DB
runfiles(filename)
conn.commit()
print(errorCount)

# Closes the connection
Google.close()
conn.close()