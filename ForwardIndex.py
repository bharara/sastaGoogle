###############
##
##	This code reads the files in folder and store them in chotaGoogle database
##	It also read all words and store them in wordfile table
##	It is relative to the root folder given at line 16
##	Password at line 23 is also relative to the database of this computer
##
###############
from bs4 import BeautifulSoup ## HTML Parser and Striper library
import os, os.path
from pathlib import Path ## Access folders
import hashlib ## Hashing Library
import pymysql ## Database library
import string

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

## Send File by File to next functions
def runfiles(filename):
	arrayofpath = Path (filename).glob("**/*")
	files=[x for x in arrayofpath if x.is_file()]
	for i in files:
		i = str(i)
		if any(x in i[40:].lower() for x in ['talk~','user~','template~','category~','image~']): # Only take articles
			continue
		countWords(i)
		conn.commit()

## Make the freqency table of words in a file and commit them to database
def countWords(file):
		
		soup = BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')
		filehash = hashF(file[33:])		## Prepare fileID (hash)
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
		for tag in [['title',100], ['h1',100], ['h2',10], ['h3',30], ['h4',20]]:
			for i in soup.find_all(tag[0]):
				for j in i.get_text().lower().translate(translator).split():
					incrementValue(wordMap,j,tag[1])
		for i in soup.get_text().lower().translate(translator).split():
			incrementValue(wordMap,i,1)

		for word,score in wordMap.items():
			# print(word, score)
			try:
				Google.execute("""INSERT INTO wordfile (fileID, wordID, score) VALUES ("%s", "%s", "%d")""" % (filehash, hashF(word), score))
			except:
				print (filehash, word, score)
				errorCount += 1

# Store value in file dictionary				
def incrementValue(wMap,word,score):
	if word in wMap:
		wMap[word] += score
	else:
		wMap[word] = score


errorCount = 0 ## Count the number of times the exception is thrown

############ MAIN ################

## Prepare Punctuation Striper
translator = str.maketrans('', '', string.punctuation) ## This will strip all punctuation from string


runfiles(rootFolder) ## Main function
conn.commit() ## Final commit (just in case)
print(errorCount) 

## Closes the connection
Google.close()
conn.close()     