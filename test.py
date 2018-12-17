from bs4 import BeautifulSoup ## HTML Parser and Striper library

rootFolder = 'D:/3- DSA/Project/simple/articles/u/n/i/Category~Uniforms_d3e0.html'
soup = BeautifulSoup(open(rootFolder, encoding="utf-8"), 'html.parser')

print(soup.get_text())



