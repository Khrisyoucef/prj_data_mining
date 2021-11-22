#encoding=utf8
import random
import numpy as np
import math
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getfile(filename):
	f = open(filename, "r")
	L = f.readlines()
	return L

l = getfile("movies_metadata.csv")

df = pd.read_csv('movies_metadata.csv',low_memory=False)



colums = ['adult','genres','original_title','production_companies','tagline','id']

def decodegenre(elem):
	j = 5
	sp = elem.split("'")
	genre = []
	while(j<len(sp)):
		genre.append(sp[j])
		j = j+6	
	s = ''
	for x in genre:
		s = s+" "+x
	return s	

def decodeproduction(elem):
	j = 3
	sp = elem.split("'")
	prod = []
	while(j<len(sp)):
		prod.append(sp[j])
		j = j+6
	s = ''
	for x in prod:
		s = s+x
	return s

def getImportantData(data):

	List = []
	Ids = []
	for x in range(0, data.shape[0]):

		important_data = ""

		if(not isinstance(data['adult'][x],float)):
			important_data = important_data+data['adult'][x]+ " "

		if(not isinstance(data['genres'][x],float)):
			important_data = important_data + decodegenre(data['genres'][x]) + " "

		if(not isinstance(data['original_title'][x],float)):
			important_data = important_data + data['original_title'][x] + " "

		if(not isinstance(data['production_companies'][x],float)):
			important_data = important_data + decodeproduction(data['production_companies'][x]) + " "	

		if(not isinstance(data['tagline'][x],float)):
			important_data = important_data + data['tagline'][x] + " "		

		List.append(important_data)
		Ids.append(data['id'][x])

	return (List,Ids)	

l,i = getImportantData(df)


def most_similair(data, item_index, k):

	vectorizer = TfidfVectorizer()
	count_matrix = vectorizer.fit_transform(data)

	similarity_scores = cosine_similarity(count_matrix)
	index_similarity = similarity_scores[item_index]
	non = [item_index]

	print("ok")

	i = 0
	while i != k:

		Max = -1
		j = 0		

		for x in index_similarity:
			if j not in non:
				if Max == -1:
					Max = j	
				else:
					if(x > index_similarity[Max]):
						Max = j	
			j = j + 1

		if max != -1:
			i = i + 1 
			non.append(Max)		
	non.pop(0)				
	return non

similair = most_similair(l[:len(l)//10],0,5)	

print(similair)

print("i tested with : ",l[0],"\n")

print("i got : \n")
for x in similair:
	print(l[x],"\n")

