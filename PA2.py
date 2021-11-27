"""
    title: PA2: Movie Recommendations Using Item-to-Item Collaborative Filtering
    author: Sydney Yeargers
    date created: 10/13/21
    date last modified: 10/17/21
    python version: 2.7
    description: This application generates movie recommendations for users based off of their previous ratings, and
     estimates the user's ratings for movies they did not rate. See 'ReadMe.txt' for more information on how estimates
     were calculated.
"""

import time
import pandas as pd

movies = pd.read_csv('movie-lens-data/movies.csv')
ratings = pd.read_csv('movie-lens-data/ratings.csv')
# a) Construct the profile of each item
df = pd.merge(ratings, movies, on="movieId")  # create a DataFrame of ratings and movies
movie_matrix = df.pivot_table(index='userId', columns='movieId', values='rating')  # create a pivot table with index userId
# b) Compute similarity score
corr_matrix = movie_matrix.corr(method='pearson', min_periods=5)
N = {}  # create dictionary to store neighborhood set
recommend_list = {}  # create dictionary to store movie recommendations for each user
to_write = ""  # create string to store output
estimates_matrix = movie_matrix.copy(deep=True)  # create copy of pivot table to store estimated ratings
col_list = movie_matrix.columns.values.tolist()  # store list of movieIds
num_users = len(movie_matrix)  # store number of users

# c) Compute neighborhood set
# for each movie, find 5 most similar movies
for m in range(len(movie_matrix.columns)):
    similar = corr_matrix.loc[:, col_list[m]].dropna()  # retrieve correlated movies
    similar.sort_values(inplace=True, ascending=False)  # sort by correlation
    similar_df = similar.reset_index(drop=False, name="similarity", inplace=False)  # convert Series to DataFrame
    similar_df.sort_values(by=['similarity', 'movieId'], ascending=[False, True], inplace=True)  # sort by correlation and movieId
    similar_df = similar_df[similar_df.movieId != col_list[m]]  # ensure a movie is not 'similar' to itself
    similar_five = similar_df.iloc[0:5, 0:2]  # retrieve five most similar movies
    N[col_list[m]] = pd.Series(similar_five.similarity.values, similar_five.movieId)  # add movie's neighborhood set to dictionary

t0 = time.time()  # begin timer for individual recommendation and estimation runtime
# for each user, determine estimations and recommendations
for i in range(num_users):
    to_write += str(movie_matrix.index[i])  # write userId to output string
    to_write += ". "  # format output string
    user_ratings = movie_matrix.iloc[i].dropna()  # store movies user rated
    not_rated = pd.Series(0, movie_matrix.columns[movie_matrix.iloc[i].isna()])  # store movies user did not rate
    recommend = pd.Series()  # create list of recommended movies for each user

# d) Estimate user rating for movies the user did not rate
    # for each movie user did not rate, determine estimated user rating
    for k in range(0, len(not_rated)):
        rate = 0  # set rating to zero
        sim = corr_matrix.loc[:, not_rated.index[k]].dropna()  # retrieve correlated movies
        share = sim[sim.index.isin(user_ratings.index)]  # retrieve correlated movies that have been rated by user
        most_sim_val = share.max()  # find movie with the highest correlation
        # if at least one of the correlated movies has been rated by the user, calculate estimated rating
        if len(share) != 0:
            rate = (most_sim_val * corr_matrix.at[share.idxmax(), not_rated.index[k]])  # calculate estimated rating
        estimates_matrix[not_rated.index[k]][movie_matrix.index[i]] = rate  # store estimated rating

# e) Compute top five recommended movies for each user
    # for each movie rated by user, determine movies to be recommended to user
    for j in range(0, len(user_ratings)):
        sim_mov = N.get(user_ratings.index[j])  # retrieve neighborhood set for movie
        scaled = sim_mov.map(lambda x: x * user_ratings.values[j])  # estimate user ratings for recommended movies
        recommend = recommend.append(scaled)  # add recommended movies with scaled ratings to user's recommended list
    recommend.sort_values(inplace=True, ascending=False)  # sort recommended movies by correlation values
    x = pd.DataFrame(recommend)  # convert to DataFrame
    recommend_filter = x[~x.index.isin(user_ratings.index)]  # filter out recommended movies that user has already rated
    recommend_list[i] = recommend_filter.index[0:5]  # add user and top five recommendations to recommendations dictionary
    movies_str = ""  # create string to store recommended movies for output
    # for each top five recommended movies, add movieId to string for output
    for q in range(len(recommend_list[i].values)):
        movies_str += str(recommend_list[i].values[q])  # add movieId for recommended movie
        movies_str += " "  # format output
    to_write += movies_str + '\n'  # add recommended movie string to output string
    print("****Calculating estimated ratings and generating recommendations for user ", i + 1, " ****")  # print userId to console
    print("Runtime (sec): ", time.time() - t0)  # print runtime for each user to console
    t0 = time.time()  # restart timer for next user
with open('output.txt', 'w+') as output:
    output.writelines(to_write)  # create output file

print("For the direct answer to (a), please view the DataFrame 'movie_matrix'.")
print("For the direct answer to (b), please view the DataFrame 'corr_matrix'.")
print("For the direct answer to (c), please view the dictionary 'N'.")
print("For the direct answer to (d), please view the DataFrame 'estimates_matrix'.")
print("For the direct answer to (e), please view the file 'output.txt'.")
