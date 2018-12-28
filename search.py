import operator
from flask import Flask, render_template, request, redirect, url_for, flash
import fun
from nltk.corpus import wordnet


def fastSearch(words):

	fileMap = {}
	for i in set(words):
		Google.execute("""SELECT fileID, score FROM wordfile WHERE word = "%s";""" % (fun.hashF(i)))
		data = Google.fetchall()
		for i in data:
			if i[0] in fileMap.keys():
				fileMap[i[0]][0] += i[1]
				fileMap[i[0]][1] += 1
			else:
				fileMap[i[0]] = [i[1],1]
	for file, score in fileMap.items():
		fileMap[file] = score[0] * score[1]

	results = []
	for file in list(fileMap.keys())[:10]:
		Google.execute("""SELECT fileAdd
			FROM files
			WHERE fileID = "%s";"""
			% (file))

		data = Google.fetchall()
		results.append(["simple/articles"+data[0][0],data[0][0][7:-5].replace("_"," ").replace("~"," ")])

	return results

def search (words):

	s = """SELECT fileID FROM wordfile WHERE word in ("""
	for i in set(words):
		s = s + """"%s", """ % (fun.hashF(i))
	s = s[:-2] + """) GROUP BY fileID ORDER BY SUM(score) * COUNT(score) desc;"""

	Google.execute(s)

	data = Google.fetchall()

	results = []
	for file in data:
		Google.execute("""SELECT fileAdd
			FROM files
			WHERE fileID = "%s";"""
			% (file[0]))

		data = Google.fetchall()
		results.append(["simple/articles"+data[0][0],data[0][0][7:-5].replace("_"," ")])
	return results

def searchForSyn (words):

	synonyms = []
	for word in words:
		getSynonyms(word,synonyms)

	s = """SELECT fileID, SUM(score) * COUNT(score) FROM wordfile WHERE word in ("""
	for i in words:
		s = s + """"%s", """ % (fun.hashF(i))
	s = s[:-2] + """) GROUP BY fileID"""
	Google.execute(s)
	data = Google.fetchall()

	fileMap = {}
	for file, score in data:
		fileMap[file] = score
	

	s = """SELECT fileID, SUM(score) FROM wordfile WHERE word in ("""
	for i in set(synonyms):
		s = s + """"%s", """ % (fun.hashF(i))
	s = s[:-2] + """) GROUP BY fileID"""
	Google.execute(s)
	data2 = Google.fetchall()

	for file, score in data2:
		if file in fileMap.keys():
			fileMap[file] += score/100
		else:
			fileMap[file] = score/100

	results = []
	for file,score in sorted(fileMap.items(), key=operator.itemgetter(1), reverse=True):
		Google.execute("""SELECT fileAdd
			FROM files
			WHERE fileID = "%s";"""
			% (file))

		data = Google.fetchall()
		results.append(["simple/articles"+data[0][0],data[0][0][7:-5].replace("_"," ")])
	
	return results

def getSynonyms(word,synonyms):
	for syn in wordnet.synsets(word): 
		for l in syn.lemmas(): 
			synonyms.append(l.name())
	
	return tuple(synonyms)

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template("Homepage.html")		

@app.route('/', methods=['POST', 'GET'])
def searchResults():
	global query, res, stype
	query = request.form["query"].lower()
	stype = request.form["b"]

	words = query.lower().translate(fun.translator).split(" ")	
	
	if stype == "Fast Search":
		res = fastSearch(words)
	elif stype == "Search":
		res = search(words)
	else:
		res = searchForSyn(words)

	return render_template("aftersearch.html", results=res[:10], title=query+" - "+stype, showBar=True)

@app.route('/allResults')
def allResults():
	return render_template("aftersearch.html", results=res, title="All: "+query+" - "+stype, showBar=False)

if __name__ == "__main__":
	# Establishes the connection to database
	conn, Google = fun.dbSetup()
	res = []
	query = ''
	
	#fastSearch(['pakistan','and','india'])
	app.run(debug=True, port=4999)

	# Closes the connection
	fun.dbClose(conn, Google)