import pytest

from modules.database_updater import DatabaseUpdater
from modules.db_manager import DbManager


@pytest.fixture(scope='function')
def database():
    """ Setup of the in memory database """

    database = DbManager(db_name=":memory:")

    yield database

    del database


@pytest.fixture(scope='function')
def select_statement(database):
    """ Setup of select sql statmenet """

    statement = f"""SELECT * FROM {database.db_table_name}"""

    yield statement


@pytest.fixture(scope='function')
def data_updater(database):
    """ Setup of data updater class """

    data_updater = DatabaseUpdater(database)
    yield data_updater

    del data_updater


@pytest.fixture(scope='module')
def data_to_insert():
    """ Setup of the downloaded from OMDB API dummy data """

    data = {'Title': 'Gods', 'Year': 2014, 'Runtime': '120 min',
            'Genre': 'Biography, Drama', 'Director': 'Lukasz Palkowski',
            'Writer': 'Krzysztof Rak',
            'Cast': 'Tomasz Kot, Piotr Glowacki, Szymon Piotr Warszawski, Magdalena Czerwinska',
            'Language': 'Polish', 'Country': 'Poland',
            'Awards': '19 wins & 9 nominations.', 'imdbRating': 7.7, 'imdbVotes': 5084,
            'BoxOffice': None}

    yield data

    del data


def test_select_titles_with_no_data(database, data_updater):
    """ Testing retrieving titles with empty data from the db """

    # Add some dummy empty titles
    data_updater.database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Memento');""")
    data_updater.database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Gods');""")

    results = data_updater.get_empty_titles()

    assert 'Memento' and 'Gods' in results


def test_insert_title_data(data_updater, data_to_insert, database, select_statement):
    """ Test inserting the downloaded data """

    data_updater.database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Gods');""")

    data_updater.insert_data(data_to_insert)

    results = data_updater.database.execute_statement(select_statement)

    result = next(results)

    assert result['Title'] == data_to_insert['Title']
    assert result['Year'] == data_to_insert['Year']
    assert result['Runtime'] == data_to_insert['Runtime']
    assert result['Genre'] == data_to_insert['Genre']
    assert result['Director'] == data_to_insert['Director']
    assert result['Cast'] == data_to_insert['Cast']
    assert result['Writer'] == data_to_insert['Writer']
    assert result['Language'] == data_to_insert['Language']
    assert result['Country'] == data_to_insert['Country']
    assert result['Awards'] == data_to_insert['Awards']
    assert result['imdb_Rating'] == data_to_insert['imdbRating']
    assert result['imdb_Votes'] == data_to_insert['imdbVotes']
    assert result['Box_Office'] == data_to_insert['BoxOffice']


def test_update(data_updater, database, select_statement):
    """ Testing if the update method works properly """

    # Add some dummy empty titles
    data_updater.database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Memento');""")
    data_updater.database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Gods');""")

    data_updater.update()

    results = data_updater.database.execute_statement(select_statement)

    for result in results:
        assert result['Title'] == 'Memento' or result['Title'] == 'Gods'
        assert result['Year'] == 2014 or result['Year'] == 2000
