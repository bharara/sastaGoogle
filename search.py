import os, os.path
from pathlib import Path
import hashlib
import pymysql
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
		results.append([rootFolder+data[0][0],data[0][0][7:-5].replace("_"," ")])

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


@app.route('/login', methods=['POST'])
def loginAfter():
	name = request.form["name"].lower()
	password = request.form['pword']

	if (name,password) in users:
		return redirect('/admin')
	else:
		return render_template('login.html', title = 'Admin Login - AQM', flashyMsg = 'Incorrect Username or Password')


word = "dubai cricket"
rootFolder = 'D:/3- DSA/Project/simple/articles'
#word = input("Enter search word: ")
word = word.lower().translate(translator).split()
search(word)[0:10]

if __name__ == "__main__":
    app.run(debug=True,  port=6000)

