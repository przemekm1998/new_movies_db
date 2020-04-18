import pytest

from modules.commands.data_tools.templates.sorter_templates import GenericSorter, \
    ParsingSorter


@pytest.fixture(scope='module')
def generic_sorter():
    """ Setup of generic sorter object """

    generic_sort = GenericSorter()
    yield generic_sort

    del generic_sort


@pytest.fixture(scope='module')
def parsing_sorter():
    """ Setup of parsing sorter object """

    parsing_sort = ParsingSorter()
    yield parsing_sort

    del parsing_sort


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


@pytest.mark.parametrize('column, sort_order, first_result',
                         [
                             ('title', 'asc', 'The Dark Knight'),  # Alphabetical sort
                             ('title', 'desc', 'The Shawshank Redemption'),
                             ('year', 'asc', 1972),  # Numeric sort
                             ('year', 'desc', 2008),
                         ])
def test_generic_sorter_sort_data(fake_database_results, generic_sorter,
                                  column, sort_order, first_result):
    """ Test sort by different columns """

    generic_sorter.column_name = column
    sorting_results = generic_sorter.sort_data(fake_database_results, sort_order)

    assert sorting_results[0][column] == first_result


@pytest.mark.parametrize('column, sort_order, word_to_parse, first_result',
                         [
                             ('runtime', 'asc', 'min', 142),
                             ('runtime', 'desc', 'min', 175),
                         ])
def test_parsing_sorter_sort_data(fake_database_results, parsing_sorter,
                                  column, sort_order, first_result, word_to_parse):
    """ Test sort by different columns """

    parsing_sorter.column_name = column
    parsing_sorter.word_to_parse = word_to_parse
    sorting_results = parsing_sorter.sort_data(fake_database_results, sort_order)

    assert sorting_results[0][column] == first_result
