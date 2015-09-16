#!/usr/bin/env python3
from __future__ import print_function #Used to use print function in list comprehension (line 26)
import pandas as pd
import numpy as np

"""
Exercise 1
-----------
Use the data combining tools discussed above to combine these three objects into a single object named movie_data
"""
pd.set_option('display.max_columns', None) #Allow pandas to print unlimmited no. of columns in the terminal
pd.set_option('display.width', 100) #Allow pandas to print unlimmited no. of characters in the terminal before a new row
print("Loading data. Please wait...")

movies_col_names = ["movie id", "title", "genre"] #Defining column names for movies
movies = pd.read_table("ml-1m/movies.dat", sep="::", names=movies_col_names) #Load the data from file, with seperator found with bash command 'head'

users_col_names = ["user id", "gender", "age", "occupation code", "zip"] #Defining column names for users
users = pd.read_table("ml-1m/users.dat", sep="::", names=users_col_names) #Load the data from file, with seperator found with bash command 'head'

ratings_col_names = ["user id", "movie id", "rating", "timestamp"] #Defining column names for ratings
ratings = pd.read_table("ml-1m/ratings.dat", sep="::", names=ratings_col_names) #Load the data from file, with seperator found with bash command 'head'


movie_data = pd.merge(ratings, users, on="user id") #Merging data from ratings and users on column name 'user id'
movie_data = pd.merge(movie_data, movies, on="movie id") #Merging the already merged data with movies on column name 'movie id'


"""
Exercise 2
-----------
The 5 movies with the most number of ratings
"""
#Gets the top 5 movie title:
#   (1) Use the value_counts() on dataframe to get the titles and no. of occurences
#   (2) Use keys() to get only titles (not occurences)
titles = movie_data['title'].value_counts().keys()
print("\nThe 5 movies with the most number of ratings:\n------------------------------------")
[print(title) for title in titles[:5]] #Printing the first 5 titles

"""
A new object called active_titles that is made up of movies each having at least 250 ratings
"""
occurences =  movie_data['title'].value_counts().values #Get the occurences of the movies (no. of ratings)
stop_index = np.where(occurences==249)[0][0] #Finding the index where the occurence is 249 (less than 250)
active_titles = movie_data[movie_data.title.isin(titles[:stop_index])] #Get all data for movies with 250 or more ratings (based of the index from before)
print("\n'active_titles' created\n------------------------------------")

""" 
The 3 movies with the highest average rating for females.
"""
print(len(active_titles))
movie_titles = pd.unique(movie_data['title'])

print(len(movie_titles)) #test
print(movie_titles[2]) #test
print(movie_titles[3]) #test
avg = []
i = 0
print(movie_data.info())
for movie in movie_titles: 
	temp = movie_data[(movie_data.title == movie) & (movie_data.gender == 'F')]['rating'].astype('int64').mean(axis=1) #beregner mean hvor title==?? og gender=='F'
	#avg.append(temp['rating'].astype('float64').mean(axis=1))
	if(i%100 == 0):
		print(i)
	i = i+1

avg_sorted, m_titles_sorted = (list(x) for x in zip(*sorted(zip(avg, movie_titles))))


