#encoding=utf8


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
		s = s+" "+x
	return s


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


def splitList(lis):

	l  = len(lis)
	l = l//3
	return(lis[0:(2*l)],lis[(2*l):len(lis)])

def splitListList(l):

	train_finale = []
	test_finale = []

	for x in l:
		train,test = splitList(x)
		train_finale.append(train)
		test_finale.append(test)

	return (train_finale,test_finale)

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

def get_movie_index(movie_id, list_movies):
	index = 0

	for x in list_movies:
		if(movie_id == x):
			return index
		index = index + 1
	return -1

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

"""print(l[:len(l)//100])
similair = most_similair(l[:len(l)//10],2,5)
print(similair)
print("i tested with : ",l[0],"\n")
print("i got : \n")
for x in similair:
	print(l[x],"\n")"""

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

	max_elements = Imaxelements(notes_finales,5)

	flat_indexs = [item for sublist in all_similairs for item in sublist]

	final_results = []

	for x in max_elements:
		final_results.append(flat_indexs[x])

	return final_results

df = pd.read_csv('movies_metadata.csv',low_memory=False)
colums = ['adult','genres','original_title','production_companies','tagline','id']
l,i = getImportantData(df)
rt,ids = read_ratings("ratings_small.csv")

#on decoupe notre ratings de chaque utilisateur a des train data et test data
train_ratings, test_ratings = splitListList(rt)
train_ids, test_ids = splitListList(ids)

#print("data ",l[0:5],"\n")
#print("train_rating ", train_ratings[0:5],"\n")
#print("train_ids  ",train_ids[0:5],"\n")
#print ("recommande par id ",recomande(l[:len(l)//3],0,rt,ids,i[:len(i)//3],5),"\n")

def validation(data,train_ratings,train_ids,test_ids,movies_ids,k):

	count=0
	listuserxmovie=[]

	for x in range (0,len(train_ratings)):
		listuserxmovie.append(recomande(data,x,train_ratings,train_ids,movies_ids,5))
		userx = test_ids[x]
		print("user num: ",x,"\n")
		for y in listuserxmovie[x]:
			if y not in userx:
				print("count rst : ", count,"y est ",y," liste de x est : ",userx,"\n")
			else:
				count +=1
				print("count rst : ", count,"y est ",y," liste de x est : ",userx,"\n")
				continue
	return count/len(train_ratings)



validation(l[:len(l)//3],train_ratings,train_ids,test_ids,i[:len(i)//3],5)


