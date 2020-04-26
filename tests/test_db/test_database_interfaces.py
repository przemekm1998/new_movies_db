import sqlite3

import pytest

from modules.database.db_interfaces import DbInsert, DbUpdater
from modules.database.db_manager import DbManager


@pytest.fixture(scope='function')
def database():
    """ Fake databse fixture """

    database = DbManager(db_name=':memory:')
    yield database

    del database


@pytest.fixture(scope='function')
def db_insert(database):
    """ Setup of data insert object """

    db_ins = DbInsert(database)
    yield db_ins

    del db_ins


@pytest.fixture(scope='function')
def db_update(database):
    """ Setup of data updater object """

    db_upd = DbUpdater(database)
    yield db_upd

    del db_upd


def test_db_insert(database, db_insert):
    """ Verify if title is added to the database """

    title_to_insert = 'Some Title'

    db_insert.insert_title_to_db(title_to_insert)

    results = database.execute_statement('SELECT * FROM MOVIES')
    result = next(results)

    assert result['title'] == 'Some Title'


def test_db_insert_duplicate(db_insert):
    """ Verify if proper exception is thrown when adding duplicate value """

    title_to_insert = 'title'

    db_insert.insert_title_to_db(title_to_insert)

    with pytest.raises(sqlite3.IntegrityError):
        db_insert.insert_title_to_db(title_to_insert)


def test_db_update(database, db_update):
    """ Verify if data is updated correctly """

    title_to_add = 'The Dark Knight'
    database.execute_statement(f'INSERT INTO MOVIES (title) VALUES ({title_to_add})')


