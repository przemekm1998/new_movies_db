import pytest

from modules.commands.data_sorter import DataSorter
from modules.database.db_manager import DbManager


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

    # No box office
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, awards) 
        VALUES ('Supermen', 2015, 8.6, '50 min',
        '80 wins & 10 nominations');""")

    yield database

    del database


@pytest.fixture(scope='module')
def data_sorter(database):
    """ Setup of data sorter class """

    data_sorter = DataSorter(database)
    yield data_sorter

    del data_sorter


@pytest.mark.parametrize('args, result_title, result_value',
                         [
                             (['title', 'asc'],
                              'Batman', 'Batman'),
                             (['title', 'desc'],
                              'Supermen', 'Supermen'),
                             (['box_office', 'desc'],
                              'Memento', 1000),
                             (['box_office', 'asc'],
                              'Batman', 50),
                             (['runtime', 'desc'],
                              'Memento', 220),
                             (['runtime', 'asc'],
                              'Supermen', 50),
                         ])
def test_handle(data_sorter, args, result_title, result_value):
    """ Verify if executed sorting is correct """

    keyword = args[0]
    result = data_sorter.handle(*args)

    assert result[0]['title'] == result_title
    assert result[0][keyword] == result_value


def test_handle_incorrect_keyword(data_sorter):
    """ Verify if exception is thrown when inapropriate keyword is given """

    args = ['this_keyword_doesnt_exist', 'asc']

    with pytest.raises(ValueError):
        data_sorter.handle(*args)
