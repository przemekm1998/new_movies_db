import pytest

from modules.commands.data_tools.filters import OscarsNominationsFilter, AwardsWonFilter


@pytest.fixture(scope='module')
def oscars_nominated_filter():
    """ Setup of oscars nominated filter object """

    oscars_filter = OscarsNominationsFilter()
    yield oscars_filter

    del oscars_filter


@pytest.fixture(scope='module')
def awards_won_filter():
    """ Setup of awards won filter """

    awards_filter = AwardsWonFilter()
    yield awards_filter

    del awards_filter


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


def test_oscars_nominations_filter(fake_database_results, oscars_nominated_filter):
    """ Test filter by different columns and values """

    oscars_nominated_filter.column_name = 'awards'

    filter_func = oscars_nominated_filter.get_filter_function()

    assert filter_func(fake_database_results[0]) is True
    assert filter_func(fake_database_results[1]) is False
    assert filter_func(fake_database_results[2]) is False


def test_awards_won_filter_database_parse(fake_database_results, awards_won_filter):
    """ Test filter by different columns and values """

    result = awards_won_filter.database_result_parse(fake_database_results[0])
    assert result == 60.0

    result = awards_won_filter.database_result_parse(fake_database_results[1])
    assert result == 86.66666666666667

    result = awards_won_filter.database_result_parse(fake_database_results[2])
    assert result == 96.22641509433963


def test_awards_won_database_parse_not_enough_data(awards_won_filter):
    """ Verify if proper exceprion is throws """

    db_incorrect_result = {
        'title': 'something',
        "awards": "Won 2 Oscars. Another 153 wins."
    }

    with pytest.raises(IndexError):
        awards_won_filter.database_result_parse(db_incorrect_result)


def test_awards_won_database_parse_incorrect_type(awards_won_filter):
    """ Verify if proper exceprion is throws """

    db_incorrect_result = {
        'title': 'something',
        "awards": 1654
    }

    with pytest.raises(TypeError):
        awards_won_filter.database_result_parse(db_incorrect_result)
