import pytest

from modules.commands.data_compare import DataCompare
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
def data_comparator(database):
    """ Setup of data compare class """

    data_comp = DataCompare(database)
    yield data_comp

    del data_comp


@pytest.mark.parametrize('args, result_title, result_value',
                         [
                             (['imdb_rating', 'The Shawshank Redemption',
                               'The Godfather', 'The Dark Knight'],
                              'The Shawshank Redemption', 9.3),
                             (['box_office', 'The Godfather', 'The Dark Knight'],
                              'The Dark Knight', 533316061),
                             (['awards_won', 'The Godfather',
                               'The Shawshank Redemption'],
                              'The Godfather', 26),
                             (['runtime', 'The Godfather', 'The Dark Knight',
                               'The Shawshank Redemption'],
                              'The Godfather', 175),
                         ])
def test_handle(data_comparator, args, result_title, result_value):
    """ Verify if executed sorting is correct """

    result = data_comparator.handle(*args)
    keys = list(result.keys())

    assert result[keys[0]] == result_title
    assert result[keys[1]] == result_value


def test_handle_incorrect_keyword(data_comparator):
    """ Verify if exception is thrown when inapropriate keyword is given """

    args = ['this_keyword_doesnt_exist', 'asc']

    with pytest.raises(ValueError):
        data_comparator.handle(*args)
