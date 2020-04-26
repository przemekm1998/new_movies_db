import pytest

from modules.commands.data_adder import AddData
from modules.database.db_manager import DbManager


@pytest.fixture(scope='function')
def database():
    """ Setup of the in memory database """

    database = DbManager(db_name=':memory:')
    yield database

    del database


@pytest.fixture(scope='function')
def data_adder(database):
    """ Setup of data adder object """

    adder = AddData(database)
    yield adder

    del adder


def test_handle_correct_titles(database, data_adder):
    """ Verify that data was downloaded for correct titles """

    args = ['The Godfather', 'The Dark Knight']
    data_adder.handle(*args)

    results = database.execute_statement('SELECT * FROM MOVIES')

    result = next(results)
    assert result['title'] == 'The Godfather'
    assert result['director'] == 'Francis Ford Coppola'

    result = next(results)
    assert result['title'] == 'The Dark Knight'
    assert result['director'] == 'Christopher Nolan'


def test_handle_incorrect_titles(database, data_adder):
    """ Verify that data for not existing title wasn't downloaded """

    args = ['This title does not exist for sure believe me']

    data_adder.handle(*args)
    results = database.execute_statement('SELECT * FROM MOVIES')
    result = next(results)

    assert result['title'] == 'This title does not exist for sure believe me'
    assert result['director'] is None
