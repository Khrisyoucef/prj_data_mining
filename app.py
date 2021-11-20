#encoding=utf8
import random
import numpy as np
import math
import pandas as pd

def getfile(filename):
	f = open(filename, "r")
	L = f.readlines()
	return L

l = getfile("movies_metadata.csv")

df = pd.read_csv('movies_metadata.csv',low_memory=False)



colums = ['adult','genres','original_title','production_companies','tagline']

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
	return List	

l = getImportantData(df)
print(l)	

