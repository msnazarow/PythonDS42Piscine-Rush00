import re
import pytest
from movielens_analysis import Ratings, Movies, Tags, Links

class Test:
	class TestRatings:
		class TestUsers:
			class TestTop_controversial:
				@pytest.fixture()
				def total_revenue(self):
					ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
					return ratings.users.top_controversial(5)

				def test_return_type(self, total_revenue):
					assert isinstance(total_revenue, dict)

				def test_return_len(self, total_revenue):
					assert len(total_revenue) == 5

				def test_returns_raiting(self, total_revenue):
					assert total_revenue['259'] == 2.94

			class TestDist_by_rating:
				@pytest.fixture()
				def total_revenue(self):
					ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
					return ratings.users.dist_by_rating()

				def test_return_type(self, total_revenue):
					assert isinstance(total_revenue, dict)

				def test_return_len(self, total_revenue):
					assert len(total_revenue) == 610

				def test_returns_raiting(self, total_revenue):
					assert total_revenue['442'] == 1.27

			class TestDist_by_num_of_ratings:
				@pytest.fixture()
				def total_revenue(self):
					ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
					return ratings.users.dist_by_num_of_ratings()

				def test_return_type(self, total_revenue):
					assert isinstance(total_revenue, dict)

				def test_return_len(self, total_revenue):
					assert len(total_revenue) == 610

				def test_returns_raiting(self, total_revenue):
					assert total_revenue['610'] == 1302
		class TestTop_by_ratings:
			@pytest.fixture()
			def total_revenue(self):
				ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
				return ratings.top_by_ratings(5)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 5

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Lesson Faust (1994)'] == 5

		class TestDist_by_rating:
			@pytest.fixture()
			def total_revenue(self):
				ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
				return ratings.dist_by_rating()

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue[0.5] == 1370

		class TestTop_controversial:
			@pytest.fixture()
			def total_revenue(self):
				ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
				return ratings.top_controversial(5)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 5

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Zed & Two Noughts, A (1985)'] == 4.0
			
		class TestTop_by_num_of_ratings:
			@pytest.fixture()
			def total_revenue(self):
				ratings = Ratings("/goinfre/dmadelei/ml-latest-small/ratings.csv", "/goinfre/dmadelei/ml-latest-small/movies.csv")
				return ratings.top_by_num_of_ratings(5)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 5

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Forrest Gump (1994)'] == 329
				
	class TestMovies:
		class TestMost_genres:
			@pytest.fixture
			def total_revenue(self):
				movie = Movies("/goinfre/dmadelei/ml-latest-small/movies.csv")
				return movie.most_genres(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Rubber (2010)'] == 10
		class TestDist_by_genres:
			@pytest.fixture
			def total_revenue(self):
				movie = Movies("/goinfre/dmadelei/ml-latest-small/movies.csv")
				return movie.dist_by_genres()

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 19

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Horror'] == 978
		class TestDist_by_release:
			@pytest.fixture
			def total_revenue(self):
				movie = Movies("/goinfre/dmadelei/ml-latest-small/movies.csv")
				return movie.dist_by_release()

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 106

			def test_returns_raiting(self, total_revenue):
				assert total_revenue[1997] == 260
			
	class TestTags:
		class TestMost_words:
			@pytest.fixture
			def total_revenue(self):
				tags = Tags("/goinfre/dmadelei/ml-latest-small/tags.csv")
				return tags.most_words(100)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 100

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Academy award (Best Supporting Actress)'] == 5
		class Testlongest:
			@pytest.fixture
			def total_revenue(self):
				tags = Tags("/goinfre/dmadelei/ml-latest-small/tags.csv")
				return tags.longest(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Something for everyone in this one... saw it without and plan on seeing it with kids!'] == 85
		class TestMost_popular:
			@pytest.fixture
			def total_revenue(self):
				tags = Tags("/goinfre/dmadelei/ml-latest-small/tags.csv")
				return tags.most_popular(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['atmospheric'] == 36
	class TestLinks:
		class TestTop_directors:
			@pytest.fixture
			def total_revenue(self):
				link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
				return link.top_directors(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['Charles Shyer'] == '0113041'
		class TestMost_expensive:
			@pytest.fixture
			def total_revenue(self):
				link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
				return link.most_expensive(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['GoldenEye'] == '$60,000,000 (estimated)'
		class TestMost_profitable:
			@pytest.fixture
			def total_revenue(self):
				link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
				return link.most_profitable(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['GoldenEye'] == 292194034

		class Testlongest:
			@pytest.fixture
			def total_revenue(self):
				link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
				return link.longest(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['GoldenEye'] == '2 hours 10 minutes'

		class TestTop_cost_per_minute:
			@pytest.fixture
			def total_revenue(self):
				link = Links("/goinfre/dmadelei/ml-latest-small/links.csv")
				return link.top_cost_per_minute(10)

			def test_return_type(self, total_revenue):
				assert isinstance(total_revenue, dict)

			def test_return_len(self, total_revenue):
				assert len(total_revenue) == 10

			def test_returns_raiting(self, total_revenue):
				assert total_revenue['GoldenEye'] == 461538.46