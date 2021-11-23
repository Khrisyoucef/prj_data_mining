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

		movie_id = data['id'][x]
		try:
			Ids.append(int(movie_id))	    		
		except ValueError:
			Ids.append(-1)

		List.append(important_data)	
			
	return (List,Ids)	

l,i = getImportantData(df)
#print(l)
#print(i)



def most_similair(data, item_index, k):

	vectorizer = TfidfVectorizer()
	count_matrix = vectorizer.fit_transform(data)

	similarity_scores = cosine_similarity(count_matrix)
	index_similarity = similarity_scores[item_index]
	non = [item_index]


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

#similair = most_similair(l[:len(l)//10],0,5)	

#print("i tested with : ",l[0],"\n")

#print("i got : \n")
#for x in similair:
#	print(l[x],"\n")


def read_ratings(filename):

	Ratings = []
	ids = []
	user_ids = []
	user_ratings = []
    
	df = pd.read_csv(filename,low_memory=False)	

	user_index = df['userId'][0]

	for i in range(0, df.shape[0]):
		this_index = df['userId'][i]
		if(this_index != user_index):
			ids.append(user_ids)
			Ratings.append(user_ratings)
			user_index = this_index
			user_ids = [df['movieId'][i]]
			user_ratings = [df['rating'][i]]
			
		else:
			user_ids.append(df['movieId'][i])    	
			user_ratings.append(df['rating'][i])

	return (Ratings,ids)	

rt,ids = read_ratings("ratings_small.csv") 	

#print(rt[2],"\n")
#print(ids[2],"\n")

def get_movie_index(movie_id, list_movies):
	index = 0
	for x in list_movies:
		if(movie_id.item() == x):
			return index
		index = index + 1 
	
	return -1		


def get_nmax(l,n):
	i = 0
	maxs = []

	while i != n:
		Max = -1 
		j = 0
		for x in l:
			if j not in maxs:
				if Max == -1:
					Max = j
				else:
					if(x > l[Max]):
						Max = j	
			j = j + 1

		if Max != -1 :
			maxs.append(Max)
		i = i +1

	for u in range(len(maxs)):
		maxs[u] = maxs[u] + maxs[u] + 1
		u = u+1				
	return maxs	



def recomande(data,user_index,users_ratings,users_ids,movies_ids,simls,k):
	user_ratings = users_ratings[user_index]
	user_ids = users_ids[user_index]
	all_similairs = []
	notes_finales = []


	for i in range(0, len(user_ids)):
		movie_id = user_ids[i]
		movie_index = get_movie_index(movie_id,movies_ids)
		print(movie_id)
		print(movie_index)
		similairs =  most_similair(data,movie_index,k)
		all_similairs.append(similairs)

	print(all_similairs)	

	for index in range(0, len(user_ids)):
		movie = get_movie_index(user_ids[index],movies_ids)
		note =[]
		for j in range(0,len(all_similairs[index])):
			note.append(simls[movie][j]*user_ratings[index])
		notes_finales.append[note]	 

	print(notes_finales)	

			

vectorizer = TfidfVectorizer()
count_matrix = vectorizer.fit_transform(df)

similarity_scores = cosine_similarity(count_matrix)


recomande(df,0,rt,ids,i,similarity_scores,5)