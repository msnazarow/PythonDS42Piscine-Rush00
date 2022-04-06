import re
from collections import Counter
from enum import Enum

# class Genre(Enum):
#     action = 'Action'
#     adventure = 'Adventure'
#     animation = 'Animation'
#     children = "Children"
#     comedy = 'Comedy'
#     crime = 'Crime'
#     documentary = 'Documentary'
#     drama = 'Drama'
#     fantasy = 'Fantasy'
#     filmNoir = 'Film-Noir'
#     horror = 'Horror'
#     musical = 'Musical'
#     mystery = 'Mystery'
#     romance = 'Romance'
#     sciFi = 'Sci-Fi'
#     thriller = 'Thriller'
#     war = 'War'
#     Western = 'Western'
from functools import reduce
from typing import List


class Movie:
    def __init__(self, id, title, genres):
        self.id = id
        self.title = title
        try:
            self.year = int(re.sub('.*\(([0-9]{4})\).*', r'\1', title))
        except:
            self.year = 2000
        self.genres = genres.split('|')


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        with open(path_to_the_file) as file:
            self.movies: List[Movie] = []
            next(file)
            for line in file:
                movieId, title, genres = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line.strip())
                self.movies.append(Movie(movieId, title, genres))

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        return dict(Counter(map(lambda x: x.year, self.movies)))

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        return dict(Counter(reduce(lambda a, b: a + b, map(lambda x: x.genres, self.movies))))

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        # return movies


movies = Movies("ml-latest-small/movies.csv")
print(movies.dist_by_genres(), movies.dist_by_release())
