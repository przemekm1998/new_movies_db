import pytest

from modules.commands.data_tools.common_utils import ExtractNumber


@pytest.fixture(scope='module')
def extract_number():
    """ Setup utils class """

    utils = ExtractNumber()
    yield utils

    del utils


@pytest.mark.parametrize('string_to_process, word, result_number',
                         [
                             ('Another 9 wins & 50 nominations.', 'wins', 9),
                             ('9 wins & 50 nominations.', 'nominations', 50)
                         ])
def test_extract_number(extract_number, string_to_process, word, result_number):
    """ Test number extraction """

    result = extract_number.extract(string_to_process, word)


def test_extract_number_not_found(extract_number):
    """ Verify if exception is thrown if number is not found """

    string_to_process = 'Another 9 wins & 50 nominations.'
    word_to_find = 'some_word'

    with pytest.raises(IndexError):
        result = extract_number.extract(string_to_process, word_to_find)


def test_extract_number_wrong_argument(extract_number):
    """ Verify if exception is thrown if number is not found """

    string_to_process = 54621
    word_to_find = 'some_word'

    with pytest.raises(TypeError):
        result = extract_number.extract(string_to_process, word_to_find)
