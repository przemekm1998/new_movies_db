import pytest

from modules.commands.filter_data.filters.filter_by_wins_and_nominations import \
    FilterByWinsAndNominations


@pytest.fixture(scope='module')
def wins_and_nominations_filter():
    """ Setup of wins and nominations filter class """

    wins_and_nominations = FilterByWinsAndNominations()
    yield wins_and_nominations

    del wins_and_nominations


def test_column_name(wins_and_nominations_filter):
    """ Test if column name is correct """

    assert wins_and_nominations_filter.get_column_name() == 'awards'


def test_keyword(wins_and_nominations_filter):
    """ Test if keyword is correct """

    assert wins_and_nominations_filter.get_keyword() == 'wins_and_nominations'


@pytest.mark.parametrize('awards, result',
                         [
                             ({
                                  'awards': 'Nominated for 3 Oscars. Another 8 wins & 10 nominations.'},
                              False),
                             ({'awards': '9 wins & 50 nominations.'}, False),
                             ({'awards': '9 wins & 0 nominations.'}, False),
                             ({'awards': ''}, False),
                             ({'awards': '19 wins & 9 nominations.'}, True),
                             ({
                                  'awards': 'Won for 3 Oscars. Another 19 wins & 9 nominations'},
                              True),
                             ({'awards': '9 nominations.'}, False),
                             ({'awards': None}, False),
                         ])
def test_filter_by_wins_and_nominations(wins_and_nominations_filter, awards, result):
    """ Verify correctness of filtering movies that won >80% of nominations """

    ans = wins_and_nominations_filter.filter_result(awards)
    assert ans is result


def test_filter_by_wins_and_nominations_win_percentage_zero_division(
        wins_and_nominations_filter):
    """ Verify if methond calc percentage throws exception """

    string_to_process = 'Nominated for 3 Oscars. Another 9 wins & 0 nominations.'

    with pytest.raises(ZeroDivisionError):
        wins_and_nominations_filter.calculate_win_percentage(string_to_process)


def test_filter_by_wins_and_nominations_calculate_win_percentage_no_awards_info(
        wins_and_nominations_filter):
    """ Verify if filter throws IndexError exception if no awards in db"""

    string_to_process = None

    with pytest.raises(TypeError):
        wins_and_nominations_filter.calculate_win_percentage(string_to_process)


def test_filter_by_wins_and_nominations_calculate_win_percentage_only_nominations(
        wins_and_nominations_filter):
    """ Verify if filter throws IndexError exception if no awards won """

    string_to_process = '9 nominations'

    result = wins_and_nominations_filter.calculate_win_percentage(string_to_process)

    assert result == 0
