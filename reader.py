from bs4 import BeautifulSoup

file = "D:/3- DSA/Project/simple/articles/%/_/_/%.html"

soup = BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')

print(soup.get_text().split())