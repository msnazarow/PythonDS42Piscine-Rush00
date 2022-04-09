import re
from functools import reduce
from typing import List, Dict
from collections import Counter, OrderedDict
from datetime import date


def mean(seq):
	if len(seq) == 0:
		return float('nan')
	return sum(seq) / len(seq)


def median(seq):
	if len(seq) == 0:
		return float('nan')
	seq = sorted(seq)
	return seq[len(seq) // 2] if len(seq) % 2 == 1 else (seq[len(seq) // 2 - 1] + seq[len(seq) // 2]) / 2


def variance(seq):
	if len(seq) == 0:
		return float('nan')
	return sum([(x - mean(seq)) ** 2 for x in seq]) / len(seq)


class Movie:
	def __init__(self, id, title, genres):
		self.id = id
		self.title = title
		try:
			self.year = int(re.sub('.*\(([0-9]{4})\).*', r'\1', title))
		except:
			self.year = 2000
		self.genres = [] if genres == '(no genres listed)' else genres.split('|')


class Movies:
	"""
    Analyzing data from movies.csv
    """

	def __init__(self, path_to_the_file: str):
		"""
        Put here any fields that you think you will need.
        """
		with open(path_to_the_file) as file:
			self.__movies: Dict[Movie] = {}
			next(file)
			for line in file:
				movieId, title, genres = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line.strip())
				title = re.sub("\"(.*)\"", r"\1", title)
				self.__movies[movieId] = (Movie(movieId, title, genres))

	def dist_by_release(self):
		"""
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
		return dict(Counter(map(lambda x: x.year, self.__movies)).most_common())

	def dist_by_genres(self):
		"""
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
		return dict(Counter(reduce(lambda a, b: a + b, map(lambda x: x.genres, self.__movies))).most_common())

	def most_genres(self, n):
		"""
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
		return dict(Counter({x.title: len(x.genres) for x in self.__movies}).most_common(n))

	def __getitem__(self, item):
		return self.__movies[item]


# movies = Movies("ml-latest-small/movies.csv")
# print(movies.most_genres(10))
# exit(0)


class Rating:
	def __init__(self, userId, movieId, rating, timestamp):
		self.userId = userId
		self.movieId = movieId
		self.userId = userId
		self.rating = float(rating)
		self.year = date.fromtimestamp(int(timestamp))


class Ratings:
	"""
    Analyzing data from ratings.csv
    """

	def __init__(self, path_to_the_ratings, path_to_movies):
		"""
        Put here any fields that you think you will need.
        """
		self.__ratings = Ratings.Movies(path_to_the_ratings, Movies(path_to_movies))
		self.__users = Ratings.Users(path_to_the_ratings, Movies(path_to_movies))

	@property
	def ratings(self):
		return self.__ratings

	@property
	def users(self):
		return self.__users

	def dist_by_year(self):
		"""
        The method returns a dict where the keys are years and the values are counts.
        Sort it by years ascendingly. You need to extract years from timestamps.
        """
		return self.__ratings.dist_by_year()

	def dist_by_rating(self):
		"""
        The method returns a dict where the keys are ratings and the values are counts.
     Sort it by ratings ascendingly.
        """
		return self.__ratings.dist_by_rating()

	def top_by_num_of_ratings(self, n):
		"""
        The method returns top-n movies by the number of ratings.
        It is a dict where the keys are movie titles and the values are numbers.
        Sort it by numbers descendingly.
        """
		return self.__ratings.top_by_num_of_ratings(n)

	def top_by_ratings(self, n, metric='average'):
		"""
        The method returns top-n movies by the average or median of the ratings.
        It is a dict where the keys are movie titles and the values are metric values.
        Sort it by metric descendingly.
        The values should be rounded to 2 decimals.
        """
		return self.__ratings.top_by_ratings(n, metric)

	#
	def top_controversial(self, n):
		"""
        The method returns top-n movies by the variance of the ratings.
        It is a dict where the keys are movie titles and the values are the variances.
      Sort it by variance descendingly.
        The values should be rounded to 2 decimals.
        """
		return self.__ratings.top_controversial(n)

	class Movies:
		def __init__(self, path_to_the_file, movies: Movies):
			self._movies = movies
			with open(path_to_the_file) as file:
				self._ratings: List[Rating] = []
				next(file)
				for line in file:
					userId, movieId, rating, timestamp = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line.strip())
					self._ratings.append(Rating(userId, movieId, rating, timestamp))

		def dist_by_year(self):
			"""
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
			return dict(Counter(map(lambda x: x.year, self._ratings)).most_common()[::-1])

		def dist_by_rating(self):
			"""
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
			return dict(Counter(map(lambda x: x.rating, self._ratings)).most_common()[::-1])

		def top_by_num_of_ratings(self, n):
			"""
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
			return {self._movies[x[0]].title: x[1] for x in
			        Counter(map(lambda x: x.movieId, self._ratings)).most_common(n)}

		def top_by_ratings(self, n, metric="average"):
			"""
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
			output = {}
			for elem in self._ratings:
				if elem.movieId not in output:
					output[elem.movieId] = []
				output[elem.movieId].append(elem.rating)
			if metric == "average":
				for movieId in output:
					output[movieId] = round(mean(output[movieId]), 2)
			elif metric == "median":
				for movieId in output:
					output[movieId] = round(median(output[movieId]), 2)
			else:
				return []
			return {self._movies[elem[0]].title: elem[1] for elem in sorted(output.items(), key=lambda x: -x[1])[:n]}

		def top_controversial(self, n):
			"""
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
			output = {}
			for elem in self._ratings:
				if elem.movieId not in output:
					output[elem.movieId] = []
				output[elem.movieId].append(elem.rating)
			for movieId in output:
				output[movieId] = round(variance(output[movieId]), 2)
			return {self._movies[elem[0]].title: elem[1] for elem in sorted(output.items(), key=lambda x: -x[1])[:n]}

	class Users(Movies):
		"""
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

		def dist_by_num_of_ratings(self):
			return dict(Counter(map(lambda x: x.userId, self._ratings)).most_common())

		def dist_by_ratings(self, metric="average"):
			output = {}
			for elem in self._ratings:
				if elem.userId not in output:
					output[elem.userId] = []
				output[elem.userId].append(elem.rating)
			if metric == "average":
				for userId in output:
					output[userId] = round(mean(output[userId]), 2)
			elif metric == "median":
				for userId in output:
					output[userId] = round(median(output[userId]), 2)
			else:
				return []
			return {self._movies[elem[0]].title: elem[1] for elem in sorted(output.items(), key=lambda x: -x[1])}

		def top_controversial(self, n):
			output = {}
			for elem in self._ratings:
				if elem.userId not in output:
					output[elem.userId] = []
				output[elem.userId].append(elem.rating)
			for userId in output:
				output[userId] = round(variance(output[userId]), 2)
			return dict(sorted(output.items(), key=lambda x: -x[1])[:n])


# ratings = Ratings("ml-latest-small/ratings.csv", "ml-latest-small/movies.csv")
# print(ratings.users.top_controversial(10))
# exit(0)


class Tags:
	"""
    Analyzing data from tags.csv
    """

	def __init__(self, path_to_the_file):
		"""
        Put here any fields that you think you will need.
        """
		with open(path_to_the_file) as file:
			self.__tags: List[str] = []
			next(file)
			for line in file:
				_, _, tag, _ = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line.strip())
				self.__tags.append(tag)

	def most_words(self, n):
		"""
		The method returns top-n tags with most words inside. It is a dict
		 where the keys are tags and the values are the number of words inside the tag.
		Drop the duplicates. Sort it by numbers descendingly.
		"""
		{len(x.split()) for x in self.__tags}






		big_tags = dict()
		if (len(self.__tags) < n or n <= 0):
			raise ValueError('n > count teg or n <= 0')
		else:
			no_sorted_tuple = dict(zip(self.__tags, (map(lambda x: len(x.split(' ')), self.__tags))))
			sorted_tuple = dict(sorted(no_sorted_tuple.items(), key=lambda x: -x[1]))
			count = 0
			for key, value in sorted_tuple.items():
				if (count != n):
					big_tags[key] = value
					count += 1
		return big_tags

	def longest(self, n):
		"""
		The method returns top-n longest tags in terms of the number of characters.
		It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
		"""
		# return set(self.)
		if (len(self.__tags) < n or n <= 0):
			raise ValueError('n > count teg or n <= 0')
		else:
			sorted_tuple = dict(zip(self.__tags, (map(lambda x: len(x), self.__tags))))
			big_tags = dict(sorted(sorted_tuple.items(), key=lambda x: -x[1]))
			count = 0
			for key, value in sorted_tuple.items():
				if (count != n):
					big_tags[key] = value
					count += 1
		return big_tags

	def most_words_and_longest(self, n):
		"""
		The method returns the intersection between top-n tags with most words inside and
		top-n longest tags in terms of the number of characters.
		Drop the duplicates. It is a list of the tags.
		"""

		return big_tags

	def most_popular(self, n):
		"""
		The method returns the most popular tags.
		It is a dict where the keys are tags and the values are the counts.
		Drop the duplicates. Sort it by counts descendingly.
		"""
		return dict(Counter(self.__tags).most_common(n))

	def tags_with(self, word) -> List[str]:
		"""
		The method returns all unique tags that include the word given as the argument.
		Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
		"""

		return sorted((filter(lambda x: re.search(r'\b{}\b'.format(word), x), set(self.__tags))))


tags = Tags("ml-latest-small/tags.csv")
# print(tags.most_words(10))
# print(tags.longest(10))
# # print(tags.most_words_and_longest(10))
print(tags.most_popular(10))
print(tags.tags_with("Pacino"))


# print(tags.tags_with('a'))

class Links:
	"""
    Analyzing data from links.csv
    """

	def __init__(self, path_to_the_file):
		"""
        Put here any fields that you think you will need.
        """

	def get_imdb(list_of_movies, list_of_fields):
		"""
The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
     Sort it by movieId descendingly.
        """
		return imdb_info

	def top_directors(self, n):
		"""
        The method returns a dict with top-n directors where the keys are directors and
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
		return directors

	def most_expensive(self, n):
		"""
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
		return budgets

	def most_profitable(self, n):
		"""
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
     Sort it by the difference descendingly.
        """
		return profits

	def longest(self, n):
		"""
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version â€“ choose any.
     Sort it by runtime descendingly.
        """
		return runtimes

	def top_cost_per_minute(self, n):
		"""
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies â€“ do not pay attention to it.
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
		return costs
