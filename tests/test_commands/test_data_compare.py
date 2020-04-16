import pytest

from modules.commands.data_compare import DataCompare
from modules.database.db_manager import DbManager


@pytest.fixture(scope='module')
def database():
    """ Setup of the in memory database """

    database = DbManager(db_name=":memory:")

    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Gods', 2012, 6.8, '120 min', 100,
        'Nominated for 3 Oscars. Another 9 wins & 10 nominations.');""")

    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Memento', 2014, 7.7, '180 min', 1000,
        'Won 2 Oscars. Another 8 wins & 10 nominations');""")

    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        runtime, box_office, awards) 
        VALUES ('Batman', 2015, 8.6, '200 min', 50,
        '5 wins & 10 nominations');""")

    yield database

    del database


@pytest.fixture(scope='module')
def data_comparator(database):
    """ Setup of data comparator object """

    comparator = DataCompare(database)
    yield comparator

    del comparator


def test_get_keyword(data_comparator):
    """ Verify keyword of data_comparator """

    assert data_comparator.get_keyword() == 'compare_by'


@pytest.mark.parametrize('args, result_title, result_value',
                         [
                             (['runtime', 'Gods', 'Batman'],
                              'Batman', 200),
                             (['box_office', 'Gods', 'Memento'],
                              'Memento', 1000),
                             (['imdb_rating', 'Gods', 'Memento'],
                              'Memento', 7.7),
                             (['awards_won', 'Batman', 'Memento'],
                              'Memento', 8),
                         ])
def test_handle(data_comparator, args, result_title, result_value):
    """ Verify if executed comparison is correct """

    keyword = args[0]
    result = data_comparator.handle(*args)

    assert result['title'] == result_title
    assert result[keyword] == result_value


def test_handle_incorrect_keyword(data_comparator):
    """ Verify if exception is thrown when inapropriate keyword is given """

    args = ['this_keyword_doesnt_exist', 'Gods', 'Memento']

    with pytest.raises(ValueError):
        data_comparator.handle(*args)
