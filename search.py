import os, os.path
from pathlib import Path
import hashlib
import pymysql
import webbrowser
import string
import operator
from flask import Flask, render_template, request, redirect, url_for, flash

# Prepare Punctuation Striper
translator = str.maketrans('', '', string.punctuation)

## Hashing up the filename/word for storing
def hashF (val):
	return hashlib.md5(val.encode()).hexdigest()

def search (words):

	# Establishes the connection to database
	conn = pymysql.connect(
    	host='127.0.0.1',
	    port=3306,
	    user='root',
	    passwd='090078601',
	    db='sastaGoogle')
	Google = conn.cursor()

	fileMap = {}
	for word in words:
		getFile(fileMap, word, Google)

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

	# Closes the connection
	Google.close()
	conn.close()
	return results

def getFile(fileMap, word, Google):
	Google.execute("""SELECT fileID, score
		FROM wordfile
		WHERE wordID = "%s";"""
		% (hashF(word)))

	data = Google.fetchall()
	for i in data:
		if i[0] in fileMap:
			fileMap[i[0]][0] += i[1]
			fileMap[i[0]][1] += 1
		else:
			fileMap[i[0]] = [i[1],1]


app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template("Homepage.html")		

@app.route('/', methods=['POST', 'GET'])
def searchResults():
	global query, res
	query = request.form["query"].lower()
	stype = request.form["b"]
	
	words = query.lower().translate(translator).split()
	res = search(words)

	return render_template("aftersearch.html", results=res[0:10], query=query, showBar=True)

@app.route('/allResults')
def allResults():
	return render_template("aftersearch.html", results=res, query=query, showBar=False)

rootFolder = 'C:/Users/Star/Documents/GitHub/dsaProject/static/simple/articles'

if __name__ == "__main__":
   app.run(debug=True, port=4999)
