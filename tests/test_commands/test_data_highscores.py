import pytest

from modules.commands.data_compare import DataCompare, GenericComparator
from modules.commands.data_highscores import DataHighscores
from modules.db_manager import DbManager


@pytest.fixture(scope='module')
def database():
    """ Setup of the in memory database """

    database = DbManager(db_name=':memory:')

    # Highest box office
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Gods', 2012, 6.8, '120 min', 100,
        'Nominated for 3 Oscars. Another 9 wins & 10 nominations.');""")

    # Highest runtime
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Memento', 2014, 7.7, '220 min', 1000,
        'Won 2 Oscars. Another 8 wins & 10 nominations');""")

    # Highest rating
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Batman', 2015, 8.6, '200 min', 50,
        '5 wins & 10 nominations');""")

    # Highest awards
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Supermen', 2015, 8.6, '50 min', 50,
        '80 wins & 10 nominations');""")

    yield database

    del database


@pytest.fixture(scope='module')
def data_highscores(database):
    """ Setup of data highscores object """

    highscores = DataHighscores(database)
    yield highscores

    del highscores


def test_get_keyword(data_highscores):
    """ Verify keyword of data_highscores """

    assert data_highscores.get_keyword() == 'highscores'


def test_handle(data_highscores):
    """ Verify if executed comparison is correct """

    results = data_highscores.handle()

    box_office_result = results[0]
    assert box_office_result['title'] == 'Memento'
    assert box_office_result['box_office'] == 1000
    assert box_office_result['category'] == 'box_office'

    imdb_rating_result = results[1]
    assert imdb_rating_result['title'] == 'Batman'
    assert imdb_rating_result['imdb_rating'] == 8.6
    assert imdb_rating_result['category'] == 'imdb_rating'

    runtime_result = results[2]
    assert runtime_result['title'] == 'Memento'
    assert runtime_result['runtime'] == 220
    assert runtime_result['category'] == 'runtime'

    awards_won_result = results[3]
    assert awards_won_result['title'] == 'Supermen'
    assert awards_won_result['awards_won'] == 80
    assert awards_won_result['category'] == 'awards_won'
