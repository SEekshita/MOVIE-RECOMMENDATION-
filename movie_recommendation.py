# -*- coding: utf-8 -*-
"""MOVIE RECOMMENDATION

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_fMPyC34Wdu2Xz0Ye8EJDK-oelJ3_1SD
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import TruncatedSVD

df = pd.read_csv('TeluguMovies_dataset.csv')

df.head()

print(df.isnull().sum())

df.dropna(subset=['Rating'], inplace=True)

user_movie_matrix = df.pivot_table(index='Movie', columns='Genre', values='Rating')

user_movie_matrix.fillna(0, inplace=True)

train_data, test_data = train_test_split(user_movie_matrix, test_size=0.2, random_state=42)

svd = TruncatedSVD(n_components=20, random_state=42)
svd.fit(train_data)

train_matrix = svd.transform(train_data)
test_matrix = svd.transform(test_data)

predicted_ratings = np.dot(train_matrix, svd.components_)

train_rmse = np.sqrt(mean_squared_error(train_data, predicted_ratings))
print(f'Train RMSE: {train_rmse}')

def recommend_movies(user_id, num_recommendations=5):
    user_index = user_movie_matrix.index.get_loc(user_id)
    user_ratings = predicted_ratings[user_index]
    top_indices = user_ratings.argsort()[-num_recommendations:][::-1]
    recommended_movies = user_movie_matrix.columns[top_indices]
    return recommended_movies

M_ovie = 'Aagadu'
recommendations = recommend_movies(M_ovie)
print(f'Recommended Movies for User {M_ovie}: {recommendations}')