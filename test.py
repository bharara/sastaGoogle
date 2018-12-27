li = ['a','b','b']


s = """SELECT fileID, score
	FROM wordfile
	WHERE word in ("""
for i in li:
	s = s + """"%s", """ % (i)
s = s[:-2] +")"
print(s)
