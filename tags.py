import re
from collections import Counter
from enum import Enum

class Tags:
	def __init__(self, path_to_the_file):
		data = []
		# проверка на открытие файла
		with open(path_to_the_file, 'r') as f:
			str_data = (f.read().lower())
		data = str_data.split('\n')
		next_data = []
		for i in data[1:len(data) - 1]:
			userId, movieId, tag, timestamp = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", i)
			next_data.append(tag)
		# print(next_data)
		self.data_teg= next_data
		# tag = Counter(next_data)
		
	
	def most_words(self, n):
		"""
		The method returns top-n tags with most words inside. It is a dict 
 		where the keys are tags and the values are the number of words inside the tag.
		Drop the duplicates. Sort it by numbers descendingly.
        """
		big_tags = dict()
		if (len(self.data_teg) < n or n <= 0):
			raise ValueError('n > count teg or n <= 0')
		else:
			no_sorted_tuple = dict(zip(self.data_teg, (map(lambda x: len(x.split(' ')), self.data_teg))))
			sorted_tuple = dict(sorted(no_sorted_tuple.items(), key=lambda x: -x[1]))
			count = 0
			for key, value in sorted_tuple.items():
				if (count != n):
					big_tags[key] = value
					count +=1
		return big_tags

	def longest(self, n):
		"""
		The method returns top-n longest tags in terms of the number of characters.
		It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
		"""
		if (len(self.data_teg) < n or n <= 0):
			raise ValueError('n > count teg or n <= 0')
		else:
			sorted_tuple = dict(zip(self.data_teg, (map(lambda x: len(x), self.data_teg))))
			big_tags = dict(sorted(sorted_tuple.items(), key=lambda x: -x[1]))
			count = 0
			for key, value in sorted_tuple.items():
				if (count != n):
					big_tags[key] = value
					count +=1
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
		if (len(self.data_teg) < n or n <= 0):
			raise ValueError('n > count teg or n <= 0')
		else:
			popular_tags = Counter(self.data_teg).most_common(n)
		return popular_tags
        
	def tags_with(self, word):
		"""
		The method returns all unique tags that include the word given as the argument.
		Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
		"""
		tags_with_word = set(filter(lambda x: x.find(word) != -1, self.data_teg))
		return tags_with_word

tags = Tags("/goinfre/dmadelei/ml-latest-small/tags.csv")
# print(tags.most_words(10))
# print(tags.longest(10))
# # print(tags.most_words_and_longest(10))
print(tags.most_popular(10))
# print(tags.tags_with('a'))