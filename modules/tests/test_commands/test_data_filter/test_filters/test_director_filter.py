import pytest

from modules.commands.filter_data.filters.filter_by_director import FilterByDirector


@pytest.fixture(scope='module')
def director_filter():
    """ Setup of director filter class """

    director_filter = FilterByDirector()
    yield director_filter

    del director_filter


@pytest.fixture(scope='module')
def db_data():
    """ Simulate the databasse output info """

    movie = {'title': 'Something', 'director': 'Lukasz Palkowski'}
    yield movie

    del movie


def test_column_name(director_filter):
    """ Test if column name is correct """

    assert director_filter.get_column_name() == 'director'


@pytest.mark.parametrize('args, result',
                         [
                             (['director', 'Lukasz Palkowski'], True),
                             (['director', 'Quentin Tarantino'], False)
                         ])
def test_filter_by_director(director_filter, args, db_data, result):
    """ Verify correctness of filtering director method """

    filter_func = director_filter.get_filter_function(*args)
    ans = filter_func(db_data)
    assert ans is result
