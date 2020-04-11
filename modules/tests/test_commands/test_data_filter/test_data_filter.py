import pytest

from modules.commands.filter_data.data_filter import DataFilter
from modules.db_management.db_manager import DbManager


@pytest.fixture(scope='module')
def database():
    """ Setup of the in memory database """

    database = DbManager(db_name=":memory:")

    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        box_office, director, cast, language, awards) VALUES ('Gods', 2012, 6.8, 
        150, 'Lukasz Palkowski', 'Tomasz Kot, Piotr Glowacki', 'Polish',
        'Nominated for 3 Oscars. Another 9 wins & 10 nominations.');""")
    database.execute_statement(
        f"""INSERT INTO {database.db_table_name}(TITLE, year, imdb_rating, 
        director, cast, language, awards) VALUES ('Memento', 2014, 7.7, 
        'Christopher Nolan', 'Guy Pearce, Carrie-Anne Moss', 'English',
        'Won 2 Oscars. Another 8 wins & 10 nominations');""")

    yield database

    del database


@pytest.fixture(scope='module')
def data_filter(database):
    """ Setup of data sorter class """

    data_filter = DataFilter(database)
    yield data_filter

    del data_filter


def test_keyword(data_filter):
    """ Verify data_filter keyword """

    assert data_filter.get_keyword() == 'filter_by'


@pytest.mark.parametrize('column_name, result',
                         [
                             ('year', 2012),
                             ('imdb_rating', 6.8),
                             ('box_office', 150),
                             ('director', 'Lukasz Palkowski'),
                             ('cast', 'Tomasz Kot, Piotr Glowacki'),
                             ('language', 'Polish'),
                             ('awards',
                              'Nominated for 3 Oscars. Another 9 wins & 10 nominations.'
                              )
                         ])
def test_select_statement(data_filter, column_name, result):
    """ Verify correctness of sql statement """

    data_filter.column = column_name

    statement = data_filter.select_sql_statement
    results = data_filter.database.execute_statement(statement)

    db_result = next(results)
    assert db_result['Title'] == 'Gods'
    assert db_result[column_name] == result


def test_handle_filter_cast(data_filter):
    """ Verify filtering by cast """

    args = ['cast', 'Tomasz Kot']

    results = data_filter.handle(*args)
    db_result = next(results)

    assert db_result['Title'] == 'Gods'
    assert args[1] in db_result['Cast']

    with pytest.raises(StopIteration):
        next_result = next(results)


def test_handle_filter_director(data_filter):
    """ Verify filtering by director """

    args = ['director', 'Christopher Nolan']

    results = data_filter.handle(*args)
    db_result = next(results)

    assert db_result['Title'] == 'Memento'
    assert args[1] in db_result['Director']

    with pytest.raises(StopIteration):
        next_result = next(results)


def test_handle_filter_language(data_filter):
    """ Verify filtering by language """

    args = ['language', 'Polish']

    results = data_filter.handle(*args)
    db_result = next(results)

    assert db_result['Title'] == 'Gods'
    assert args[1] in db_result['language']

    with pytest.raises(StopIteration):
        next_result = next(results)


def test_handle_filter_box_office(data_filter):
    """ Verify filtering by language """

    args = ['box_office', 'gt', '100']

    results = data_filter.handle(*args)
    db_result = next(results)

    assert db_result['Title'] == 'Gods'

    with pytest.raises(StopIteration):
        next_result = next(results)


def test_handle_filter_oscars(data_filter):
    """ Verify filtering by oscars nominations """

    args = ['awards', 'oscars_nominated']

    results = data_filter.handle(*args)
    db_result = next(results)

    assert db_result['Title'] == 'Gods'

    with pytest.raises(StopIteration):
        next_result = next(results)


def test_handle_filter_awards_won(data_filter):
    """ Verify filtering by oscars nominations """

    args = ['awards', 'awards_won_percentage', 'gte', '80']

    results = data_filter.handle(*args)

    db_result = next(results)
    assert db_result['Title'] == 'Gods'

    next_result = next(results)
    assert next_result['Title'] == 'Memento'


def test_handle_invalid_filter(data_filter):
    """ Verify if method handle throws correct exception """

    args = ['something_strange']

    with pytest.raises(ValueError):
        results = data_filter.handle(*args)
