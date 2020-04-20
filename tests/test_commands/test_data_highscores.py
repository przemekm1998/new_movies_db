import pytest

from modules.commands.data_highscores import DataHighscores
from modules.database.db_manager import DbManager


@pytest.fixture(scope='module')
def insert_statement():
    """ Setup of SQL insert statement """

    statement = f"""INSERT INTO MOVIES(title, year, runtime, genre, 
    director, writer, cast, language, awards, imdb_rating, imdb_votes, box_office) 
    VALUES (:title, :year, :runtime, :genre, :director, :writer, :actors, 
    :language, :awards, :imdbRating, :imdbVotes, :box_office);"""

    yield statement

    del statement


@pytest.fixture(scope='module')
def database(insert_statement):
    """ Setup of the in memory database """

    database = DbManager(db_name=':memory:')

    data_to_insert = [

        {"title": "The Shawshank Redemption", "year": 1994, "runtime": "142 min",
         "genre": "Drama",
         "director": "Frank Darabont",
         "writer": "Stephen King (short story \"Rita Hayworth and Shawshank "
                   "Redemption\"), Frank Darabont (screenplay)",
         "actors": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler",
         "language": "English",
         "awards": "Nominated for 7 Oscars. Another 21 wins & 35 nominations.",
         "imdbRating": 9.3, "imdbVotes": 2217195,
         "box_office": None},

        {"title": "The Godfather", "year": 1972, "runtime": "175 min",
         "genre": "Crime, Drama",
         "director": "Francis Ford Coppola",
         "writer": "Mario Puzo (screenplay by), Francis Ford Coppola (screenplay by), Mario Puzo (based on the novel by)",
         "actors": "Marlon Brando, Al Pacino, James Caan, Richard S. Castellano",
         "language": "English, Italian, Latin",
         "awards": "Won 3 Oscars. Another 26 wins & 30 nominations.",
         "imdbRating": 9.2, "imdbVotes": 1516505, "box_office": None},

        {"title": "The Dark Knight", "year": 2008, "runtime": "152 min",
         "genre": "Action, Crime, Drama, Thriller", "director": "Christopher Nolan",
         "writer": "Jonathan Nolan (screenplay), Christopher Nolan (screenplay), "
                   "Christopher Nolan (story), David S. Goyer (story), Bob Kane (characters)",
         "actors": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine",
         "language": "English, Mandarin",
         "awards": "Won 2 Oscars. Another 153 wins & 159 nominations.",
         "imdbRating": 9.0, "imdbVotes": 2184673, "box_office": 533316061}
    ]

    for data in data_to_insert:
        database.cursor.execute(insert_statement, data)

    yield database

    del database


@pytest.fixture(scope='module')
def data_highscores(database):
    """ Setup of data compare class """

    highscores = DataHighscores(database)
    yield highscores

    del highscores


def test_format_result(data_highscores):
    """ Verify if final result is formatted correctly """

    comparator_result = {'title': 'something', 'runtime': 125}
    comparator_keyword = 'runtime_extra'

    formatted_result = data_highscores.format_result(comparator_result,
                                                     comparator_keyword)

    assert formatted_result['title'] == 'something'
    assert formatted_result['runtime'] == 125
    assert formatted_result['category'] == 'runtime_extra'


def test_handle(data_highscores):
    """ Verify if handle method works properly """

    results = data_highscores.handle()

    assert results[0]['category'] == 'box_office'
    assert results[0]['title'] == 'The Dark Knight'
    assert results[0]['box_office'] == 533316061

    assert results[1]['category'] == 'imdb_rating'
    assert results[1]['title'] == 'The Shawshank Redemption'
    assert results[1]['imdb_rating'] == 9.3

    assert results[2]['category'] == 'runtime'
    assert results[2]['title'] == 'The Godfather'
    assert results[2]['runtime'] == 175

    assert results[3]['category'] == 'awards_won'
    assert results[3]['title'] == 'The Dark Knight'
    assert results[3]['awards_won'] == 153
