import pytest

from modules.commands.filter_data.filters.filter_by_awards import FilterByAwards, \
    OscarsNominated, AwardsWonPercentage


@pytest.fixture(scope='module')
def awards_filter():
    """ Setup of awards filter class """

    awards_filter = FilterByAwards()
    yield awards_filter

    del awards_filter


@pytest.fixture(scope='module')
def oscars_filter():
    """ Setup of oscars filter class """

    oscars_filter = OscarsNominated()
    yield oscars_filter

    del oscars_filter


@pytest.fixture(scope='module')
def win_percentage_filter():
    """ Setup of percentage of nominations filter class """

    win_percentage = AwardsWonPercentage()
    yield win_percentage

    del win_percentage


@pytest.fixture(scope='module')
def database_record():
    """ Setup of a fake database record """

    record = {'title': 'something',
              'awards': 'Nominated for 3 Oscars. Another 8 wins & 10 nominations.'}

    yield record

    del record


def test_awards_filter_column_name(awards_filter):
    """ Verify column name returned by awards class """

    assert awards_filter.column_name == 'awards'


@pytest.mark.parametrize('args, result',
                         [
                             (['awards', 'oscars_nominated'], True),
                             (['awards', 'awards_won_percentage', 'gte', '80'], True)
                         ])
def test_awards_get_filter_function(awards_filter, args, result, database_record):
    """ Verify if awards filter returns correct function """

    filter_func = awards_filter.get_filter_function(*args)
    ans = filter_func(database_record)
    assert ans is result


def test_awards_get_filter_function_incorrect_keyword(awards_filter):
    """ Verify if awards filter returns correct function """

    false_args = ['awards', 'not_existing_keyword', 'gte', '80']

    with pytest.raises(ValueError):
        filter_func = awards_filter.get_filter_function(*false_args)


def test_oscars_filter_column_name(oscars_filter):
    """ Test if column name is correct """

    assert oscars_filter.column_name == 'awards'


def test_oscars_filter_keyword(oscars_filter):
    """ Test if keyword is correct """

    assert oscars_filter.get_keyword() == 'oscars_nominated'


@pytest.mark.parametrize('db_data, result',
                         [
                             ({'awards': 'Nominated for 3 Oscars.'}, True),
                             ({'awards': 'Won 3 Oscars.'}, False)
                         ])
def test_filter_by_oscars(oscars_filter, db_data, result):
    """ Verify correctness of filtering movies that didn't win oscar method """

    filter_func = oscars_filter.get_filter_function()
    ans = filter_func(db_data)
    assert ans is result


def test_awards_won_filter_column_name(win_percentage_filter):
    """ Test if column name is correct """

    assert win_percentage_filter.column_name == 'awards'


def test_awards_won_filter_keyword(win_percentage_filter):
    """ Test if keyword is correct """

    assert win_percentage_filter.get_keyword() == 'awards_won_percentage'


@pytest.mark.parametrize('args, result',
                         [
                             (['awards', 'awards_won_percentage', 'e', '80'], True),
                             (['awards', 'awards_won_percentage', 'gte', '80'], True),
                             (['awards', 'awards_won_percentage', 'gt', '80'], False),
                             (['awards', 'awards_won_percentage', 'lte', '80'], True),
                             (['awards', 'awards_won_percentage', 'lt', '80'], False),
                         ])
def test_awards_won_filter_by(win_percentage_filter, database_record, args, result):
    """ Verify correctness of filtering movies that didn't win oscar method """

    filter_func = win_percentage_filter.get_filter_function(*args)
    ans = filter_func(database_record)
    assert ans is result


def test_filter_by_wins_and_nominations_win_percentage_zero_division(
        win_percentage_filter):
    """ Verify if parsing db result throws exception """

    db_result = {'awards': 'Nominated for 3 Oscars. Another 9 wins & 0 nominations.'}

    with pytest.raises(ZeroDivisionError):
        win_percentage_filter.database_result_parse(db_result)


def test_filter_by_wins_and_nominations_calculate_win_percentage_no_awards_info(
        win_percentage_filter):
    """" Verify if parsing db result throws exception """

    db_result = {'awards': None}

    with pytest.raises(TypeError):
        win_percentage_filter.database_result_parse(db_result)


def test_filter_by_wins_and_nominations_calculate_win_percentage_only_nominations(
        win_percentage_filter):
    """" Verify if parsing db result throws exception """

    db_result = {'awards': '9 nominations'}

    with pytest.raises(IndexError):
        win_percentage_filter.database_result_parse(db_result)
