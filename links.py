import re
from collections import Counter
from enum import Enum
import urllib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import ssl

class Links:
	"""
	Analyzing data from links.csv
	"""
	def __init__(self, path_to_the_file):
		"""
		Put here any fields that you think you will need.
		"""
		data = []
		# проверка на открытие файла
		with open(path_to_the_file, 'r') as f:
			str_data = (f.read().lower())
		data = str_data.split('\n')
		next_data = []
		for i in data[1:len(data) - 1]:
			data = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", i)
			# next_data.append(movieId, imdbId, tmdbId)
			next_data.append(data)
		# print(next_data)
		self.data_file = next_data
		self.list_movies_data = []
		for i in range(0, 10):
			ssl._create_default_https_context = ssl._create_unverified_context
			url = f'https://www.imdb.com/title/tt{self.data_file[i][1]}/'
			headers = {'User-Agent': 'My User Agent 1.0',
			'From': f'https://www.imdb.com/title/tt{self.data_file[i][1]}/'
			}
			page = urllib.request.urlopen(urllib.request.Request(url=url, headers=headers)).read()
			soup = BeautifulSoup(page, 'lxml')
			tags = soup.find_all('li', role='presentation', class_='ipc-metadata-list__item')
			for tag in tags:
				if (tag.text.find('Director') != -1):
					Director = tag.text.replace('Director', '')
					break
			for tag in tags:
				if (tag.text.find('Budget') != -1):
					Budget = tag.text.replace('Budget', '')
					break
			for tag in tags:
				if (tag.text.find('Also known as') != -1):
					film = tag.text.replace('Also known as', '')
					break
			for tag in tags:
				if (tag.text.find('Gross worldwide') != -1):
					Gross = tag.text.replace('Gross worldwide', '')
					break
			for tag in tags:
				if (tag.text.find('Runtime') != -1):
					Runtime = tag.text.replace('Runtime', '')
					break
			field_data = [self.data_file[i][1], film, Director, Budget, Gross, Runtime]
			self.list_movies_data.append(field_data)

	def get_imdb(list_of_movies, list_of_fields):
		"""
		The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
		For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
		The values should be parsed from the IMDB webpages of the movies.
		Sort it by movieId descendingly.
		"""
		list_movies_data = []
		for i in list_of_movies:
			ssl._create_default_https_context = ssl._create_unverified_context
			url = f'https://www.imdb.com/title/tt{i}/'
			headers = {'User-Agent': 'My User Agent 1.0',
			'From': f'https://www.imdb.com/title/tt{i}/'
			}
			page = urllib.request.urlopen(urllib.request.Request(url=url, headers=headers)).read()
			soup = BeautifulSoup(page, 'lxml')
			tags = soup.find_all('li', role='presentation', class_='ipc-metadata-list__item')
			field_data = [i]
			for field in list_of_fields:
				for tag in tags:
					if (tag.text.find(field) != -1):
						field_value = tag.text.replace(field, '')
						break
				field_data.append(field_value)
			list_movies_data.append(field_data)
		imdb_info = list(sorted(list_movies_data, key=lambda x: (-int(x[0]))))
		return imdb_info

		
	def top_directors(self, n):
		"""
		The method returns a dict with top-n directors where the keys are directors and 
		the values are numbers of movies created by them. Sort it by numbers descendingly.
		"""
		list_movies = []
		if (n > len(self.list_movies_data) and n <= 0):
			ValueError('n > list')
		for i in range(0, n):
			list_movies.append([self.list_movies_data[i][2], self.list_movies_data[i][0]])
		a = sorted(list_movies)
		directors = dict()
		for i in a:
			directors[i[0]] = i[1]
		return directors
		
	def most_expensive(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are their budgets. Sort it by budgets descendingly.
		"""
		list_movies = []
		if (n > len(self.list_movies_data) and n <= 0):
			ValueError('n > list')
		for i in range(0, n):
			list_movies.append([self.list_movies_data[i][1], self.list_movies_data[i][3]])
		a = sorted(list_movies)
		budgets = dict()
		for i in a:
			budgets[i[0]] = i[1]
		return budgets
		
	def most_profitable(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the difference between cumulative worldwide gross and budget.
		Sort it by the difference descendingly.
		"""
		list_movies = []
		if (n > len(self.list_movies_data) and n <= 0):
			ValueError('n > list')
		for i in range(0, n):
			gross = ''.join(x for x in self.list_movies_data[i][4] if x.isdigit())
			budget = ''.join(x for x in self.list_movies_data[i][3] if x.isdigit())
			list_movies.append([self.list_movies_data[i][1], int(gross) - int(budget)])
		a = sorted(list_movies, key = lambda x: -x[1])
		profits = dict()
		for i in a:
			profits[i[0]] = i[1]
		return profits
		
	def longest(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are their runtime. If there are more than one version â€“ choose any.
		Sort it by runtime descendingly.
		"""
		list_movies = []
		if (n > len(self.list_movies_data) and n <= 0):
			ValueError('n > list')
		for i in range(0, n):
			Runtime_min = int(int(self.list_movies_data[i][5].split(' ')[0]) * 60) + int(self.list_movies_data[i][5].split(' ')[2])
			field_data = [self.list_movies_data[i][1], self.list_movies_data[i][5], Runtime_min]
			list_movies.append(field_data)
		a = sorted(list_movies, key = lambda x: -x[2])
		runtimes = dict()
		for i in a:
			runtimes[i[0]] = i[1]
		return runtimes
		
	def top_cost_per_minute(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the budgets divided by their runtime. The budgets can be in different currencies â€“ do not pay attention to it. 
		The values should be rounded to 2 decimals. Sort it by the division descendingly.
		"""
		list_movies = []
		if (n > len(self.list_movies_data) and n <= 0):
			ValueError('n > list')
		for i in range(0, n):
			Runtime_min = int(int(self.list_movies_data[i][5].split(' ')[0]) * 60) + int(self.list_movies_data[i][5].split(' ')[2])
			budget = ''.join(x for x in self.list_movies_data[i][3] if x.isdigit())
			field_data = [self.list_movies_data[i][1], round(int(budget) / Runtime_min, 2)]
			list_movies.append(field_data)
		a = sorted(list_movies, key = lambda x: -x[1])
		costs = dict()
		for i in a:
			costs[i[0]] = i[1]
		return costs

link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
# print(Links.get_imdb(['0114709'], ['Director', 'Budget', 'Gross worldwide', 'Runtime']))
# print(link.top_directors(10))
# print(link.most_expensive(10))
# print(link.most_profitable(10))
# print(link.longest(10))
# print(link.top_cost_per_minute(10))