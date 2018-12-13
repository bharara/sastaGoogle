import os, os.path
from pathlib import Path

def printInFolder(files):
	n = 1
	ignore = ['Category~','Image~','Image_talk~','Talk~','Template~','Template_talk~','User~','User_talk~','\\User_talk~']
	for i in files:
		i = str(i)
		if any(x in i[40:] for x in ignore):
			continue
		print(n,i)
		n+=1

filename = "D:/3- DSA/Project/simple/articles/u/s/a"
arrayofpath = Path (filename).glob("**/*")

files=[x for x in arrayofpath if x.is_file()]

printInFolder(files)