import pytest

from modules.commands.filter_data.filters.filter_by_language import FilterByLanguage


@pytest.fixture(scope='module')
def language_filter():
    """ Setup of language filter class """

    language_filter = FilterByLanguage()
    yield language_filter

    del language_filter


@pytest.fixture(scope='module')
def db_data():
    """ Simulate the databasse output info """

    movie = {'title': 'Something', 'language': 'English, Spanish'}
    yield movie

    del movie


def test_column_name(language_filter):
    """ Test if column name is correct """

    assert language_filter.column_name == 'language'


@pytest.mark.parametrize('args, result',
                         [
                             (['language', 'Spanish'], True),
                             (['language', 'German'], False)
                         ])
def test_filter_by_language(language_filter, args, db_data, result):
    """ Verify correctness of filtering director method """

    filter_func = language_filter.get_filter_function(*args)
    ans = filter_func(db_data)
    assert ans is result
