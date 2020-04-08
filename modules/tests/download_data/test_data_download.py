import os

import pytest
import requests

from modules.download_data.data_download import DataDownloader


@pytest.fixture(scope='module')
def data_downloader():
    """ Setup of data downloader class before tests """

    downloader = DataDownloader()
    yield downloader

    del downloader


@pytest.fixture(scope='module')
def api_key():
    """ Setup of api key for test environment """

    api_key = '305043ae'
    yield api_key

    del api_key


@pytest.fixture(scope='module')
def correct_response_json(api_key):
    """
    Setup of correct json response
    :param api_key: api key used in GET request
    :return: json response with correct data
    """

    payload = {'t': 'Gods', 'r': 'json'}  # Payload params for url request
    response = requests.get(f'http://www.omdbapi.com/?apikey={api_key}',
                            params=payload).json()

    yield response

    del response


@pytest.fixture(scope='module')
def incorrect_response_json(api_key):
    """
    Setup of incorrect json response
    :param api_key: api key used in GET request
    :return: json response with incorrect data
    """

    payload = {'t': 'Nie ma takiego :)', 'r': 'json'}  # Payload params for url request
    response = requests.get(f'http://www.omdbapi.com/?apikey={api_key}',
                            params=payload).json()

    yield response

    del response


@pytest.fixture(scope='module')
def correct_titles():
    """ Setup of list of correct titles to download their data """

    titles = ('Gods', 'Memento', 'In Bruges')
    yield titles

    del titles


def test_env_variable_set(data_downloader):
    """ Testing env variable read if set """

    api_key = data_downloader.api_key
    assert api_key is not None


def test_env_variable_not_set(data_downloader):
    """ Testing env variable not set """

    api_key = os.environ.get('OMDB_API_KEY')
    os.environ.pop('OMDB_API_KEY')

    with pytest.raises(ValueError):
        api_key = data_downloader.api_key

    os.environ['OMDB_API_KEY'] = api_key


@pytest.mark.parametrize('title, response_value',
                         [
                             ('Gods', 'True'),
                             ('Memento', 'True'),
                             ("Doesn't exist :)", 'False')
                         ])
def test_download_title_response_code(data_downloader, title, response_value):
    """ Testing response codes from GET request to OMDB API """

    response = data_downloader.download_title(title)
    assert response_value in response['Response']


@pytest.mark.parametrize('before_conversion, after_conversion',
                         [
                             ('5,047', 5047),
                             ('$25,453', 25453),
                             ('N/A', None)
                         ])
def test_parse_json_response_leave_digits(data_downloader, before_conversion,
                                          after_conversion):
    """ Test converting number strings with special characters to integers """

    result = data_downloader.leave_digits(before_conversion)
    assert result == after_conversion


def test_parse_json_response_correct(data_downloader, correct_response_json):
    """ Testing parsing the json response """

    result = data_downloader.parse_json_response(correct_response_json)

    assert result['Title'] == 'Gods'
    assert result['Year'] == 2014
    assert result['Runtime'] == '120 min'
    assert result['Genre'] == 'Biography, Drama'
    assert result['Director'] == 'Lukasz Palkowski'
    assert 'Tomasz Kot, Piotr Glowacki, Szymon Piotr Warszawski, Magdalena Czerwinska' in \
           result['Cast']
    assert result['Writer'] == 'Krzysztof Rak'
    assert result['Language'] == 'Polish'
    assert result['Country'] == 'Poland'
    assert result['Awards'] == '19 wins & 9 nominations.'
    assert result['imdbRating'] == 7.7
    assert result['imdbVotes'] == 5084
    assert result['BoxOffice'] is None


def test_parse_json_response_incorrect(data_downloader, incorrect_response_json):
    """ Testing parsing the json incorrect response """

    result = data_downloader.parse_json_response(incorrect_response_json)
    assert result is None


def test_download_data_only_correct_titles(data_downloader, correct_titles):
    """ Testing downloading data for only correct titles """

    results = tuple(data_downloader.download_data(correct_titles))

    assert len(results) == 3
    assert results[0]['Title'] == 'Gods'
    assert results[1]['Title'] == 'Memento'
    assert results[2]['Title'] == 'In Bruges'
