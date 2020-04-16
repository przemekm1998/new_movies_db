import pytest

from modules.commands.comparators.parsing_comparator import ParsingComparator


@pytest.fixture(scope='module')
def parsing_comparator():
    """ Setup of parsing comparator object """

    parsing_comp = ParsingComparator(column_name=None, keyword=None, word_to_parse=None)
    yield parsing_comp

    del parsing_comp


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


@pytest.mark.parametrize('column, keyword, word_to_parse, result',
                         [
                             ('runtime', 'runtime', 'min', 180),
                             ('awards', 'awards_won', 'wins', 50)
                         ])
def test_parsing_comparator_compare_data(fake_database_results, parsing_comparator,
                                         column, result, word_to_parse, keyword):
    """ Test comparing by different columns """

    parsing_comparator.column_name = column
    parsing_comparator.keyword = keyword
    parsing_comparator.word_to_parse = word_to_parse
    comparator_result = parsing_comparator.compare_data(fake_database_results)

    assert comparator_result[keyword] == result


def test_parse_function_index_error(parsing_comparator):
    """ Verify if proper exception is raised """

    db_result = {'title': 'The Dark Knight', 'runtime': 'strange_word'}
    parsing_comparator.column_name = 'runtime'
    parsing_comparator.word_to_parse = 'min'

    result = parsing_comparator.parse_function(db_result)
    assert result['runtime'] is None


def test_parse_function_type_error(parsing_comparator):
    """ Verify if proper exception is raised """

    db_result = {'title': 'The Dark Knight', 'runtime': None}
    parsing_comparator.column_name = 'runtime'
    parsing_comparator.word_to_parse = 'min'

    result = parsing_comparator.parse_function(db_result)
    assert result['runtime'] is None
