from bs4 import BeautifulSoup ## HTML Parser and Striper library
import fun

def getFileMap():
	files = fun.getFiles()

	fileMap = {}
	n = 0
	for i in files:
		i = str(i)[64:]
		if any(x in i[6:].lower() for x in ['talk~','user~','template~','wikipedia~']):
			continue
		countWords(i,fileMap)
		if n%1000 == 0:
			print(n,i)
		n += 1
	return fileMap

## Make the freqency table of words in a file
def countWords(file, fileMap):
		
		soup = BeautifulSoup(open(fun.rootFolder+file, encoding="latin-1"), 'html.parser')
		filehash = fun.hashF(file)

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
				for j in i.get_text().lower().translate(fun.translator).split():
					incrementValue(wordMap,j,tag[1])
		for i in soup.get_text().lower().translate(fun.translator).split():
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
		for word, score in fileMap[file].items():
			arr.append((fun.hashF(word), file, score))
	return sorted(arr)

## Insert into Database
def writeToDB(arr):
	Google.executemany("INSERT INTO wordfile (word, fileID, score) VALUES (%s, %s, %s)", arr)
	conn.commit()

if __name__ == "__main__":

	conn, Google = fun.dbSetup()
	fileMap = getFileMap()
	print("Got fileMap")
	arr = returnSorted(fileMap)
	print("Sorted fileMap")
	writeToDB(arr)
	fun.dbClose(conn, Google)