import pytest
import sqlite3

from modules.database.db_manager import DbManager


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


def test_insert_statement_correct(database, select_statement):
    """ Testing the db response of correct insert statement """

    statement = f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Memento');"""

    database.execute_statement(statement)
    results = database.execute_statement(select_statement)

    result = next(results)
    assert result['Title'] == 'Memento'


def test_insert_statement_duplicates(database):
    """ Testing the db response of duplicate insert statement """

    statement = f"""INSERT INTO {database.db_table_name}(TITLE) VALUES ('Memento');"""

    database.execute_statement(statement)

    with pytest.raises(sqlite3.IntegrityError):
        database.execute_statement(statement)


def test_incorrect_statement(database):
    """ Testing the db response of incorrect statement """

    statement = f"""some very incorrect statement"""

    with pytest.raises(sqlite3.OperationalError):
        database.execute_statement(statement)

