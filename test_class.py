import re
import pytest
from movielens_analysis import Ratings, Movies, Tags, Links

@pytest.fixture
def total_revenue():
	ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
	return ratings.users.top_controversial(5)

def test_return_type(total_revenue):
	assert isinstance(total_revenue, dict)

def test_return_len(total_revenue):
	assert len(total_revenue) == 5

def test_returns_raiting(total_revenue):
	assert total_revenue['259'] == 2.94

@pytest.fixture
def total_revenue():
	movie = Movies("/goinfre/dmadelei/ml-latest-small/movies.csv")
	return movie.most_genres(10)

def test_return_type(total_revenue):
	assert isinstance(total_revenue, dict)

def test_return_len(total_revenue):
	assert len(total_revenue) == 10

def test_returns_raiting(total_revenue):
	assert total_revenue['Rubber (2010)'] == 10

@pytest.fixture
def total_revenue():
	tags = Tags("/goinfre/dmadelei/ml-latest-small/tags.csv")
	return tags.most_words(100)

def test_return_type(total_revenue):
	assert isinstance(total_revenue, dict)

def test_return_len(total_revenue):
	assert len(total_revenue) == 100

def test_returns_raiting(total_revenue):
	assert total_revenue['Academy award (Best Supporting Actress)'] == 5

@pytest.fixture
def total_revenue():
	link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
	return link.top_directors(10)

def test_return_type(total_revenue):
	assert isinstance(total_revenue, dict)

def test_return_len(total_revenue):
	assert len(total_revenue) == 10

def test_returns_raiting(total_revenue):
	assert total_revenue['Charles Shyer'] == '0113041'