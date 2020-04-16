import pytest

from modules.commands.comparators.generic_comparator import GenericComparator


@pytest.fixture(scope='module')
def generic_comparator():
    """ Setup of generic comparator object """

    generic_comp = GenericComparator(column_name=None, keyword=None)
    yield generic_comp

    del generic_comp


@pytest.fixture(scope='module')
def fake_database_results():
    """ Setup of fake database results """

    results = [
        # Highest imdb_rating
        {'title': 'The Shawshank Redemtpion', 'imdb_rating': 9.3, 'box_office': None,
         'runtime': '120 min',
         'awards': 'Won 3 Oscars. Another 5 wins & 10 nominations.'},

        # Highest runtime
        {'title': 'The Godfather', 'imdb_rating': 9.2, 'box_office': 100,
         'runtime': '180 min',
         'awards': '40 wins & 10 nominations.'},

        # Highest box office & awards won
        {'title': 'The Dark Knight', 'imdb_rating': 9.0, 'box_office': 1000,
         'runtime': '50 min',
         'awards': 'Nominated for 3 Oscars. Another 50 wins & 10 nominations.'}
    ]
    yield results

    del results


@pytest.mark.parametrize('column, keyword, result',
                         [
                             ('imdb_rating', 'imdb_rating', 9.3),
                             ('box_office', 'box_office', 1000)
                         ])
def test_generic_comparator_compare_data(fake_database_results, generic_comparator,
                                         column, result, keyword):
    """ Test comparing by different columns """

    generic_comparator.column_name = column
    generic_comparator.keyword = keyword
    comparator_result = generic_comparator.compare_data(fake_database_results)

    assert comparator_result[keyword] == result
