import pytest

from modules.commands.filter_data.filters.filter_by_cast import FilterByCast


@pytest.fixture(scope='module')
def actor_filter():
    """ Setup of actor filter class """

    actor_filter = FilterByCast()
    yield actor_filter

    del actor_filter


@pytest.fixture(scope='module')
def db_data():
    """ Simulate the databasse output info """

    movie = {'title': 'Something', 'cast': 'Brad Pitt, Tomasz Kot'}
    yield movie

    del movie


def test_column_name(actor_filter):
    """ Test if column name is correct """

    assert actor_filter.column_name == 'cast'


@pytest.mark.parametrize('args, result',
                         [
                             (['cast', 'Tomasz Kot'], True),
                             (['cast', 'Jan Nowak'], False)
                         ])
def test_filter_by_actor(actor_filter, args, db_data, result):
    """ Verify correctness of filtering director method """

    filter_func = actor_filter.get_filter_function(*args)
    ans = filter_func(db_data)
    assert ans is result
