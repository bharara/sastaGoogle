###############
##
##	This code reads the files r and store them in sastaGoogle database sorted based on wordID
##	It also read all words and store them in wordfile table
##	Line 15 root and line 22 password are relitive
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

def runfiles(filename):
	arrayofpath = Path (filename).glob("**/*")
	files = [x for x in arrayofpath if x.is_file()]
	
	fileMap = {}
	n = 1
	for i in files:
		i = str(i)
		if any(x in i[40:].lower() for x in ['talk~','user~','template~','category~','image~']):
			continue
		print(i)
		countWords(i, fileMap)
		n += 1
	return fileMap

## Make the freqency table of words in a file and commit them to database
def countWords(file, fileMap):
		
		soup = BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')
		filehash = hashF(file[33:])		
		#print(file[33:],filehash)

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

		fileMap[filehash] = wordMap

def incrementValue(wMap,word,score):
	if word in wMap:
		wMap[word] += score
	else:
		wMap[word] = score

# sort the dictionary based on wordID and store it in array(tuple)
def returnSorted(fileMap):
	arr = []
	for file in fileMap.keys():
		for word in fileMap[file].items():
			arr.append((hashF(word[0]), file, word[1]))
	return sorted(arr)


# Prepare Punctuation Striper
translator = str.maketrans('', '', string.punctuation)

################### 	MAIN #######################
fileMap = runfiles(filename)
print("In dictionary")
arr = returnSorted(fileMap)
print("sorted")

# Convert in into right order
for j in range(len(arr)):
	arr[j] = (arr[j][1],arr[j][0],arr[j][2])

print("In array")

## Insert into Database
Google.executemany("INSERT INTO wordfile (fileID, wordID, score) VALUES (%s, %s, %s)", arr)
conn.commit()
print("In database - DONEEEEEEEE")

##################################################

## Closes the connection
Google.close()
conn.close()


