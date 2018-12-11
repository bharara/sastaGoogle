import os, os.path
from pathlib import Path

def printInFolder(files):
	n = 1
	igone = ('Category~','Image~','Talk~','Template~','Template_talk~','User~','User_talk~')
	for i in files:
		i = str(i)[40:]
		if i.startswith(igone):
			continue
		print(n,i)
		n+=1

filename = "D:/3- DSA/Project/simple//articles/u/n/i/"
arrayofpath = Path (filename).glob("**/*")

files=[x for x in arrayofpath if x.is_file()]
#print(len(filename))
printInFolder(files)
