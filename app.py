#encoding=utf8


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Cette fonction pour mettre les données des genres dans une liste sans les données inutiles pour la recommendation
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

#Cette fonction pour mettre les données des productions dans une liste sans les données inutiles pour la recommendation
def decodeproduction(elem):

	j = 3
	sp = elem.split("'")
	prod = []

	while(j<len(sp)):
		prod.append(sp[j])
		j = j+6
	s = ''

	for x in prod:
		s = s+" "+x
	return s


#Cette fonction pour vérivier chaque colonne de notre data en utilisant la fonction isinstance pour les types des données.
def getImportantData(data):

	List = []
	Ids = []

	for x in range(0, data.shape[0]):
		important_data = ""
		if(not isinstance(data['adult'][x],float)):
			important_data = important_data+data['adult'][x][0]+ " "

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

# cette fonction pour diviser une liste donnée
def splitList(lis):

	l  = len(lis)
	l = l//3
	return(lis[0:(2*l)],lis[(2*l):len(lis)])

# cette fonction pour diviser une liste d'une liste donnée
def splitListList(l):

	train_finale = []
	test_finale = []

	for x in l:
		train,test = splitList(x)
		train_finale.append(train)
		test_finale.append(test)

	return (train_finale,test_finale)

#Cette fonction pour donner N max d'une liste donnée
def Imaxelements(list1, N):

	final_list = []

	for i in range(0, N):
		max1 = 0
		indexMax = 0

		for j in range(len(list1)):
			if (list1[j] > max1 and (j not in final_list)) :
				max1 = list1[j]
				indexMax = j
		final_list.append(indexMax)
	return final_list

#cette fonction pour récupérer l'index d'un film
def get_movie_index(movie_id, list_movies):
	index = 0

	for x in list_movies:
		if(movie_id == x):
			return index
		index = index + 1
	return -1

#Cette fonction nous retourne une liste des utilisateurs et chaque case on a une liste des ratings
#d'un utilisateur ainsi une liste avec le meme principe mais à la aulieu des ratings y'a les ids des films évalués
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


def most_similair(similarity_scores, item_index, k):

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

def recomande(data,user_index,users_ratings,users_ids,movies_ids,k):

	vectorizer = TfidfVectorizer()
	count_matrix = vectorizer.fit_transform(data)

	simls = cosine_similarity(count_matrix)

	user_ratings = users_ratings[user_index]
	user_ids = users_ids[user_index]

	all_similairs = []
	notes_finales = []

	for i in range(0, len(user_ids)):
		movie_id = user_ids[i]
		movie_index = get_movie_index(movie_id,movies_ids)

		if(movie_index == -1):
			all_similairs.append([])
		else:
			similairs =  most_similair(simls,movie_index,k)
			all_similairs.append(similairs)

	for index in range(0, len(all_similairs)):
		movie2 = get_movie_index(user_ids[index],movies_ids)
		for elem in all_similairs[index]:
			notes_finales.append(simls[movie2][elem]*user_ratings[index])

	max_elements = Imaxelements(notes_finales,k)

	flat_indexs = [item for sublist in all_similairs for item in sublist]

	final_results = []

	for x in max_elements:
		final_results.append(flat_indexs[x])

	return final_results

#cette fonction spécialement pour les nouveaux utilisateurs, tell que il nous donne une list de les films qu'il préfères
#ensuite elle va retourner une liste des films recommendés
def coldstart(data,movies_ids,listidmovie,k):

	vectorizer = TfidfVectorizer()
	count_matrix = vectorizer.fit_transform(data)
	simls = cosine_similarity(count_matrix)

	all_similairs = []
	notes_finales = []

	for i in range(0, len(listidmovie)):
		movie_id = listidmovie[i]
		movie_index = get_movie_index(movie_id,movies_ids)

		if(movie_index == -1):
			all_similairs.append([])
		else:
			similairs =  most_similair(simls,movie_index,k)
			all_similairs.append(similairs)

	for index in range(0, len(all_similairs)):
		movie2 = get_movie_index(listidmovie[index],movies_ids)
		for elem in all_similairs[index]:
			notes_finales.append(simls[movie2][elem])

	max_elements = Imaxelements(notes_finales,k)
	flat_indexs = [item for sublist in all_similairs for item in sublist]
	final_results = []

	for x in max_elements:
		final_results.append(flat_indexs[x])

	return final_results


def validation(data,train_ratings,train_ids,test_ids,movies_ids,k):

	count=0
	listuserxmovie=[]

	for x in range (0,len(train_ratings)):
		listuserxmovie.append(recomande(data,x,train_ratings,train_ids,movies_ids,k))
		userx = test_ids[x]
		print("user num: ",x,"\n")
		for y in listuserxmovie[x]:
			if y not in userx:
				print("count rst : ", count,"y est ",y," liste de x est : ",userx,"\n")
			else:
				count +=1
				print("count rst : ", count,"y est ",y," liste de x est : ",userx,"\n")
				break
	return count/len(train_ratings)


df = pd.read_csv('movies_metadata.csv',low_memory=False)
colums = ['adult','genres','original_title','production_companies','tagline','id']
l,i = getImportantData(df)
rt,ids = read_ratings("ratings_small.csv")

#on decoupe notre ratings de chaque utilisateur a des train data et test data
train_ratings, test_ratings = splitListList(rt)
train_ids, test_ids = splitListList(ids)


#print("coldstar result : ",coldstart(l[:len(l)//3],i[:len(i)//3],[4919,14313,5749,150],5))
#print(validation(l[:len(l)//3],train_ratings,train_ids,test_ids,i[:len(i)//3],5))




# 150 (id de 48 hours-- 11595 id de l'autre 48 id pour vérifier
