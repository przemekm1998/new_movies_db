import re


class ExtractNumber:
    """ Extract number connected with given word """

    @staticmethod
    def extract(string_to_process, word_connected_with_number):
        """
        Extract number-word pair i.e. '9 wins' -> 9
        :param string_to_process: the whole string to process i.e. '9 wins and ...'
        :param word_connected_with_number: '9 wins' -> wins
        :return:
        """

        try:
            string_with_number = re.findall(rf'\d+ {word_connected_with_number}',
                                            string_to_process)
        except TypeError:
            raise TypeError(f"Can't process: {string_to_process}")

        try:
            num = string_with_number[0].split()  # ['9 wins'] -> ['9', 'wins]'
            num = float(num[0])  # ['9', 'wins'] -> 9
            return num
        except IndexError:
            raise IndexError(f'No number connected with {word_connected_with_number}')
