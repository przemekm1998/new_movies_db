from modules.commands.filter_data.generic_filters.generic_filter import FilterTemplate

import re


class FilterByWinsAndNominations(FilterTemplate):
    """ Class which handles filtering by 80% of won nominations """

    WIN_PERCENTAGE = 0.8

    def get_column_name(self):
        return 'awards'

    def get_keyword(self):
        return 'wins_and_nominations'

    def filter_result(self, result, *args):
        """
        Example of movie with Oscar nominations
        "Nominated for 3 Oscars. Another 9 wins & 50 nominations."

        Example of movie with no Oscar nominations
        "19 wins & 9 nominations."

        So the keyword here is /wins/ and /nominations/
        """

        column_name = self.get_column_name()
        string_to_parse = result[column_name]

        try:
            wins_to_nominations = self.calculate_win_percentage(string_to_parse)
        except IndexError:
            return False
        except ZeroDivisionError:
            return False
        except TypeError:
            return False

        return wins_to_nominations > self.WIN_PERCENTAGE

    @staticmethod
    def calculate_win_percentage(string_to_parse):
        """
        Calculate float value of (wins / nominations)
        :param string_to_parse: String containing info about all awards
        :return result: Calculated float(wins / nominations)
        """

        try:
            wins_string = re.findall(r'\d+ wins', string_to_parse)
            nominations_string = re.findall(r'\d+ nominations', string_to_parse)
        except TypeError:
            raise TypeError("Can't process result from database")

        try:
            wins = wins_string[0].split()  # ['9 wins'] -> ['9', 'wins]'
            wins = int(wins[0])  # ['9', 'wins'] -> 9
        except IndexError:
            wins = 0  # If no wins found in string then assume it's 0

        try:
            nominations = nominations_string[0].split()  # The same as above
            nominations = int(nominations[0])  # The same as above
        except IndexError:
            raise IndexError("No data about wins and nominations")

        try:
            result = float(wins / nominations)
            return result
        except ZeroDivisionError:
            raise ZeroDivisionError(f"Can't divide by zero: {nominations_string}")
