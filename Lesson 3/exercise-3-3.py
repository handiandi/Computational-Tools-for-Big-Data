#!/usr/bin/env python3
import pandas as pd
import numpy as np

#Exercise 1
#-----------
#Use the data combining tools discussed above to combine these three objects into a single object named movie_data

print("Loading data. Please wait...\n")
#Defining column names for movies
movies_col_names = ["movie id", "title", "genre"] 
#Load the data from file, with seperator found with bash command 'head'
movies = pd.read_table("ml-1m/movies.dat", sep="::", names=movies_col_names, engine="python") 
#Defining column names for users
users_col_names = ["user id", "gender", "age", "occupation code", "zip"] 
#Load the data from file, with seperator found with bash command 'head'
users = pd.read_table("ml-1m/users.dat", sep="::", names=users_col_names, engine="python") 

ratings_col_names = ["user id", "movie id", "rating", "timestamp"] #Defining column names for ratings
#Load the data from file, with seperator found with bash command 'head'
ratings = pd.read_table("ml-1m/ratings.dat", sep="::", names=ratings_col_names, engine="python") 
#Merging data from ratings and users on column name 'user id'
movie_data = pd.merge(ratings, users, on="user id")
#Merging the already merged data with movies on column name 'movie id'
movie_data = pd.merge(movie_data, movies, on="movie id")



#Exercise 2
#-----------
#The 5 movies with the most number of ratings
most_rated_movies = movie_data.groupby("title").count()
most_rated_movies.index.name = "Movies with the most number of ratings"
print(most_rated_movies.sort("rating", ascending=False).head(5)["rating"])
print("\n")
titles = movie_data['title'].value_counts().keys()

#A new object called active_titles that is made up of movies each having at least 250 ratings
#Get the occurences of the movies (no. of ratings)
occurences =  movie_data['title'].value_counts().values
#Finding the index where the occurence is 249 (less than 250)
stop_index = np.where(occurences==249)[0][0]
#Get all data for movies with 250 or more ratings (based of the index from before)
active_titles = movie_data[movie_data.title.isin(titles[:stop_index])]

highest_average_movies_women = active_titles[active_titles["gender"] == "F"].groupby("title").mean()
highest_average_movies_women.index.name = "The 3 movies with the highest number average rating for females"
print(highest_average_movies_women.sort("rating", ascending=False).head(3)["rating"])
print("\n")

highest_average_movies_men = active_titles[active_titles["gender"] == "M"].groupby("title").mean()
highest_average_movies_men.index.name = "The 3 movies with the highest number average rating for Males"
print(highest_average_movies_men.sort("rating", ascending=False).head(3)["rating"])
print("\n")

average_difference_movies = highest_average_movies_men.subtract(highest_average_movies_women)
average_difference_movies.index.name="The 10 movies men liked much more than women"
print(average_difference_movies.sort("rating", ascending=False).head(10)["rating"])
print("\n")

average_difference_movies.index.name="The 10 movies women liked much more than men"
print(average_difference_movies.sort("rating", ascending=True).head(10)["rating"])
print("\n")

highest_std_movies = active_titles.groupby("title").std()
highest_std_movies.index.name = "Movies with the highest rating standard deviation"
print("\n")
print(highest_std_movies.sort("rating", ascending=False).head(5)["rating"])
