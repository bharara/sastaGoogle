from nltk.corpus import wordnet 

synonyms = []

for syn in wordnet.synsets("no"):
    for l in syn.lemmas(): 
        synonyms.append(l.name())
  
print(tuple(synonyms))