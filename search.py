import pymysql
import webbrowser
import operator
from flask import Flask, render_template, request, redirect, url_for, flash
import fun

def search (words):

	fileMap = {}
	for word in words:
		getFile(fileMap, word)

	for key, val in fileMap.items():
		fileMap[key] = val[0] * val[1]

	results = []
	for file,score in sorted(fileMap.items(), key=operator.itemgetter(1), reverse=True):
		Google.execute("""SELECT fileAdd
		FROM files
		WHERE fileID = "%s";"""
		% (file))

		data = Google.fetchall()
		results.append(["simple/articles"+data[0][0],data[0][0][7:-5].replace("_"," ")])

	return results

def search2 (words):

	fileMap = {}
	t = ()
	for word in words:
		t = t + (fun.hashF(word),)

	return t

	# Google.execute("""SELECT fileID, score
	# 	FROM wordfile
	# 	WHERE wordID = "%s";"""
	# 	% (fun.hashF(word)))

	# data = Google.fetchall()
	# for i in data:
	# 	if i[0] in fileMap:
	# 		fileMap[i[0]][0] += i[1]
	# 		fileMap[i[0]][1] += 1
	# 	else:
	# 		fileMap[i[0]] = [i[1],1]


	# for word in words:
	# 	getFile(fileMap, word)

	# for key, val in fileMap.items():
	# 	fileMap[key] = val[0] * val[1]

	# results = []
	# for file,score in sorted(fileMap.items(), key=operator.itemgetter(1), reverse=True):
	# 	Google.execute("""SELECT fileAdd
	# 	FROM files
	# 	WHERE fileID = "%s";"""
	# 	% (file))

	# 	data = Google.fetchall()
	# 	results.append(["simple/articles"+data[0][0],data[0][0][7:-5].replace("_"," ")])

	return results

def getFile(fileMap, words):

	s = """SELECT fileID, SUM(score) FROM wordfile WHERE wordID in ("""
	for i in words:
		s = s + """"%s", """ % (i)
	s = s[:-2] + """) GROUP BY fileID"""

	print(s)
	Google.execute(s)

	data = Google.fetchall()
	print(data)
	# for i in data:
	# 	if i[0] in fileMap:
	# 		fileMap[i[0]][0] += i[1]
	# 		fileMap[i[0]][1] += 1
	# 	else:
	# 		fileMap[i[0]] = [i[1],1]


app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template("Homepage.html")		

@app.route('/', methods=['POST', 'GET'])
def searchResults():
	global query, res
	query = request.form["query"].lower()
	stype = request.form["b"]

	words = query.lower().translate(fun.translator).split()	
	
	if stype == "Button 3":
		res = search(words)
	elif stype == "Button 2":
		res = search2(words)
	else:
		res = search(words)
		res.append(["link.html","Haha"])

	return render_template("aftersearch.html", results=res[:9], query=query, showBar=True)

@app.route('/allResults')
def allResults():
	return render_template("aftersearch.html", results=res, query=query, showBar=False)

if __name__ == "__main__":
	# Establishes the connection to database
	conn, Google = fun.dbSetup()

	
	#app.run(debug=True, port=4999)
	query = ('My Khan')
	words = tuple(query.lower().translate(fun.translator).split())
	getFile(0,words)
	#print(search2(words))
	
	# Closes the connection
	fun.dbClose(conn, Google)
