import pytest

from modules.commands.data_tools.templates.filter_templates import GenericTextFilter, \
    GenericNumbersFilter


@pytest.fixture(scope='module')
def generic_text_filter():
    """ Setup of generic text filter object """

    text_filter = GenericTextFilter()
    yield text_filter

    del text_filter


@pytest.fixture(scope='module')
def generic_numbers_filter():
    """ Setup of generic numbers filter object """

    num_filter = GenericNumbersFilter()
    yield num_filter

    del num_filter


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
         "box_office": None},

        {"title": "The Godfather", "year": 1972, "runtime": "175 min",
         "genre": "Crime, Drama",
         "director": "Francis Ford Coppola",
         "writer": "Mario Puzo (screenplay by), Francis Ford Coppola (screenplay by), Mario Puzo (based on the novel by)",
         "actors": "Marlon Brando, Al Pacino, James Caan, Richard S. Castellano",
         "language": "English, Italian, Latin",
         "awards": "Won 3 Oscars. Another 26 wins & 30 nominations.",
         "imdbRating": 9.2, "imdbVotes": 1516505, "box_office": None},

        {"title": "The Dark Knight", "year": 2008, "runtime": "152 min",
         "genre": "Action, Crime, Drama, Thriller", "Director": "Christopher Nolan",
         "writer": "Jonathan Nolan (screenplay), Christopher Nolan (screenplay), "
                   "Christopher Nolan (story), David S. Goyer (story), Bob Kane (characters)",
         "actors": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine",
         "language": "English, Mandarin",
         "awards": "Won 2 Oscars. Another 153 wins & 159 nominations.",
         "imdbRating": 9.0, "imdbVotes": 2184673, "BoxOffice": 533316061}
    ]
    yield results

    del results


@pytest.mark.parametrize('column, args, results',
                         [
                             ('title', ['The'], [True, True, True]),
                             ('title', ['Shawshank'], [True, False, False]),
                             ('genre', ['Drama'], [True, True, True]),
                             ('genre', ['Crime'], [False, True, True]),
                         ])
def test_generic_text_filter(fake_database_results, generic_text_filter,
                             column, args, results):
    """ Test filter by different columns and values """

    generic_text_filter.column_name = column
    filter_func = generic_text_filter.get_filter_function(*args)

    assert results[0] == filter_func(fake_database_results[0])
    assert results[1] == filter_func(fake_database_results[1])
    assert results[2] == filter_func(fake_database_results[2])


@pytest.mark.parametrize('column, args, results',
                         [
                             ('year', ['gte', '1972'], [True, True, True]),
                             ('year', ['gt', '1972'], [True, False, True]),
                             ('year', ['e', '2008'], [False, False, True]),
                             ('year', ['lt', '1995'], [True, True, False]),
                             ('year', ['lte', '1994'], [True, True, False]),
                         ])
def test_generic_num_filter(fake_database_results, generic_numbers_filter,
                            column, args, results):
    """ Test filter by different columns and values """

    generic_numbers_filter.column_name = column
    filter_func = generic_numbers_filter.get_filter_function(*args)

    assert results[0] == filter_func(fake_database_results[0])
    assert results[1] == filter_func(fake_database_results[1])
    assert results[2] == filter_func(fake_database_results[2])
