import pytest

from modules.commands.data_tools.templates.comparator_templates import \
    GenericComparator, ParsingComparator


@pytest.fixture(scope='module')
def generic_comparator():
    """ Setup of generic comparator object """

    generic_comp = GenericComparator()
    yield generic_comp

    del generic_comp


@pytest.fixture(scope='module')
def parsing_comparator():
    """ Setup of parsing comparator object """

    parsing_comp = ParsingComparator()
    yield parsing_comp

    del parsing_comp


@pytest.fixture(scope='module')
def fake_database_results():
    """ Setup of fake database results """

    results = [

        {"title": "The Shawshank Redemption", "year": 1994, "runtime": "142 min",
         "genre": "Drama",
         "director": "Frank Darabont",
         "writer": "Stephen King (short story \"Rita Hayworth and Shawshank "
                   "Redemption\"), Frank Darabont (screenplay)",
         "actors": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler",
         "language": "English",
         "awards": "Nominated for 7 Oscars. Another 21 wins & 35 nominations.",
         "imdbRating": 9.3, "imdbVotes": 2217195,
         "BoxOffice": None},

        {"title": "The Godfather", "year": 1972, "runtime": "175 min",
         "genre": "Crime, Drama",
         "director": "Francis Ford Coppola",
         "writer": "Mario Puzo (screenplay by), Francis Ford Coppola (screenplay by), Mario Puzo (based on the novel by)",
         "actors": "Marlon Brando, Al Pacino, James Caan, Richard S. Castellano",
         "language": "English, Italian, Latin",
         "awards": "Won 3 Oscars. Another 26 wins & 30 nominations.",
         "imdbRating": 9.2, "imdbVotes": 1516505, "BoxOffice": None},

        {"title": "The Dark Knight", "year": 2008, "runtime": "152 min",
         "genre": "Action, Crime, Drama, Thriller", "director": "Christopher Nolan",
         "writer": "Jonathan Nolan (screenplay), Christopher Nolan (screenplay), "
                   "Christopher Nolan (story), David S. Goyer (story), Bob Kane (characters)",
         "actors": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine",
         "language": "English, Mandarin",
         "awards": "Won 2 Oscars. Another 153 wins & 159 nominations.",
         "imdbRating": 9.0, "imdbVotes": 2184673, "BoxOffice": 533316061}
    ]
    yield results

    del results


@pytest.mark.parametrize('column, keyword, result_title, result_value',
                         [
                             ('imdbRating', 'imdb_rating', 'The Shawshank Redemption',
                              9.3),
                             ('BoxOffice', 'box_office', 'The Dark Knight',
                              533316061),
                             ('year', 'year', 'The Dark Knight',
                              2008),
                         ])
def test_generic_comparator(fake_database_results, generic_comparator,
                            column, result_title, result_value, keyword):
    """ Test filter by different columns and values """

    generic_comparator.column_name = column
    generic_comparator.keyword = keyword

    result = generic_comparator.compare_data(fake_database_results)
    assert result['title'] == result_title
    assert result[keyword] == result_value


def test_generic_comparator_compare_empty_sequence_of_data(generic_comparator):
    """ Verify if proper exception is thrown when titles have no data """

    incorrect_data = [{'title': 'something', 'box_office': None},
                      {'title': 'something2', 'box_office': None}]

    generic_comparator.column_name = 'box_office'
    generic_comparator.keyword = 'box_office'

    with pytest.raises(ValueError):
        generic_comparator.compare_data(incorrect_data)


@pytest.mark.parametrize('column, keyword, word_to_parse, result_title, result_value',
                         [
                             ('runtime', 'runtime', 'min', 'The Godfather', 175),
                             ('awards', 'awards_won', 'wins', 'The Dark Knight', 153),
                         ])
def test_parsing_comparator(fake_database_results, parsing_comparator,
                            column, result_title, result_value, keyword, word_to_parse):
    """ Test filter by different columns and values """

    parsing_comparator.column_name = column
    parsing_comparator.keyword = keyword
    parsing_comparator.word_to_parse = word_to_parse

    result = parsing_comparator.compare_data(fake_database_results)
    assert result['title'] == result_title
    assert result[keyword] == result_value


def test_parsing_comparator_incorrect_data_to_parse(parsing_comparator):
    """ Verify if proper exception is thrown when incorrect data is given to parse """

    wrong_db_result = {'title': 'something', 'runtime': '235 hours'}

    parsing_comparator.column_name = 'runtime'
    parsing_comparator.keyword = 'runtime'
    parsing_comparator.word_to_parse = 'min'

    result = parsing_comparator.parse_function(wrong_db_result)
    assert result['runtime'] is None


def test_parsing_comparator_incorrect_type_data_to_parse(parsing_comparator):
    """ Verify if proper exception is thrown when incorrect data is given to parse """

    wrong_db_result = {'title': 'something', 'runtime': 548741}

    parsing_comparator.column_name = 'runtime'
    parsing_comparator.keyword = 'runtime'
    parsing_comparator.word_to_parse = 'min'

    result = parsing_comparator.parse_function(wrong_db_result)
    assert result['runtime'] is None
