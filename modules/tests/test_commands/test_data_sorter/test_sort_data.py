import pytest

from modules.commands.sort_data.data_sorter import DataSorter
from modules.db_management.db_manager import DbManager


@pytest.fixture(scope='module')
def database():
    """ Setup of the in memory database """

    database = DbManager(db_name=":memory:")

    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating) VALUES (
    'Gods', 2012, 6.8);""")
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating) VALUES (
    'Memento', 2014, 7.7);""")

    yield database

    del database


@pytest.fixture(scope='module')
def data_sorter(database):
    """ Setup of data sorter class """

    data_sorter = DataSorter(database)
    yield data_sorter

    del data_sorter


def test_keyword(data_sorter):
    """ Verify data_sorter keyword """

    assert data_sorter.get_keyword() == 'sort_by'


def test_handle_sort_by_year(data_sorter):
    """ Verify if results from data sorter are correct """

    results = data_sorter.handle(*['year'])

    result = next(results)
    assert result['title'] == 'Memento'
    assert result['year'] == 2014

    second_result = next(results)
    assert second_result['title'] == 'Gods'
    assert second_result['year'] == 2012


def test_handle_sort_by_title(data_sorter):
    """ Verify if results from data sorter are correct """

    results = data_sorter.handle(*['title'])

    result = next(results)
    assert result['title'] == 'Memento'

    second_result = next(results)
    assert second_result['title'] == 'Gods'


def test_handle_sort_by_imdb_rating(data_sorter):
    """ Verify if results from data sorter are correct """

    results = data_sorter.handle(*['imdb_rating'])

    result = next(results)
    assert result['title'] == 'Memento'
    assert result['imdb_rating'] == 7.7

    second_result = next(results)
    assert second_result['title'] == 'Gods'
    assert second_result['imdb_rating'] == 6.8
