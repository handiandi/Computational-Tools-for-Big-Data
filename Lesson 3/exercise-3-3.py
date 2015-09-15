#!/usr/bin/env python3

import pandas as pd

pd.set_option('display.max_columns', None) #Allow pandas to print unlimmited no. of columns in the terminal
pd.set_option('display.width', None) #Allow pandas to print unlimmited no. of characters in the terminal before a new row
print("Loading data. Please wait...")

movies_col_names = ["movie id", "title", "genre"] #Defining column names for movies
movies = pd.read_table("ml-1m/movies.dat", sep="::", names=movies_col_names) #Load the data from file, with seperator found with bash command 'head'

users_col_names = ["user id", "gender", "age", "occupation code", "zip"] #Defining column names for users
users = pd.read_table("ml-1m/users.dat", sep="::", names=users_col_names) #Load the data from file, with seperator found with bash command 'head'

ratings_col_names = ["user id", "movie id", "rating", "timestamp"] #Defining column names for ratings
ratings = pd.read_table("ml-1m/ratings.dat", sep="::", names=ratings_col_names) #Load the data from file, with seperator found with bash command 'head'


movie_data = pd.merge(ratings, users, on="user id") #Merging data from ratings and users on column name 'user id'
movie_data = pd.merge(movie_data, movies, on="movie id") #Merging the already merged data with movies on column name 'movie id'
print(movie_data)