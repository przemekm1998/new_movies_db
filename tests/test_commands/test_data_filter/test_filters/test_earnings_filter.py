import pytest

from modules.commands.filter_data.filters.filter_by_earnings import FilterByEarnings


@pytest.fixture(scope='module')
def earnings_filter():
    """ Setup of box office filter class """

    earnings_filter = FilterByEarnings()
    yield earnings_filter

    del earnings_filter


def test_column_name(earnings_filter):
    """ Test if column name is correct """

    assert earnings_filter.column_name == 'box_office'


@pytest.fixture(scope='module')
def db_data():
    """ Simulate the database output info """

    movie = {'title': 'Something', 'box_office': 10}
    yield movie

    del movie


@pytest.mark.parametrize('args, result',
                         [
                             (['box_office', 'gte', '10'], True),  # 10 >= 10
                             (['box_office', 'gt', '10'], False),  # 10 !> 10
                             (['box_office', 'gt', '9'], True),  # 10 > 9
                             (['box_office', 'lte', '10'], True),  # 10 <= 10
                             (['box_office', 'lt', '10'], False),  # 10 !<10
                             (['box_office', 'lt', '11'], True),  # 10 < 11
                             (['box_office', 'e', '10'], True),  # 10 == 10
                             (['box_office', 'e', '11'], False),  # 10 != 11
                         ])
def test_filter_by_earnings(earnings_filter, args, result, db_data):
    """ Verify correctness of filtering box office number filter"""

    filter_func = earnings_filter.get_filter_function(*args)
    ans = filter_func(db_data)
    assert ans is result


def test_filter_by_earnings_incorrect_operator(earnings_filter):
    """ Verify if proper exception is raised when incorrect operator is given """

    args = ['box_office', 'sdadsa', '15']

    with pytest.raises(ValueError):
        filter_func = earnings_filter.get_filter_function(*args)


def test_filter_by_earnings_incorrect_number_to_filter(earnings_filter):
    """ Verify if proper exception is raised when incorrect number is given """

    args = ['box_office', 'e', '15qeas']

    with pytest.raises(ValueError):
        filter_func = earnings_filter.get_filter_function(*args)
