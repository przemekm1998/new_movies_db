import pytest

from modules.commands.filter_data.filters.filter_by_oscars_nominations import \
    FilterByOscarsNominations


@pytest.fixture(scope='module')
def oscars_filter():
    """ Setup of oscars filter class """

    oscars_filter = FilterByOscarsNominations()
    yield oscars_filter

    del oscars_filter


def test_column_name(oscars_filter):
    """ Test if column name is correct """

    assert oscars_filter.get_column_name() == 'awards'


def test_keyword(oscars_filter):
    """ Test if keyword is correct """

    assert oscars_filter.get_keyword() == 'oscars_nominations'



