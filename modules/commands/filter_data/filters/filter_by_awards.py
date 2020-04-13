from modules.commands.filter_data.generic_filters.generic_filter import GenericFilter
from modules.commands.filter_data.generic_filters.generic_numbers_filter import \
    GenericNumbersFilter
from modules.commands.filter_data.generic_filters.generic_text_filter import \
    GenericTextFilter
from modules.commands.utils.common_utils import ExtractNumber


class OscarsNominated(GenericTextFilter):
    """ Filter movies which were nominated to Oscars but didn't win """

    def get_column_name(self):
        return 'awards'

    @staticmethod
    def get_keyword():
        return 'oscars_nominated'

    def get_filter_function(self, *args):
        """
        Example of movie that didn't win an oscar
        "Nominated for 3 Oscars. Another 9 wins & 50 nominations."

        Example of movie that won an oscar
        "Won 2 Oscars. Another 84 wins & 190 nominations"

        So the keyword here is /Nominated/
        """

        self.value_to_filter = 'Nominated.*Oscar'  # regex expression to search

        return self.filter_text


class AwardsWonPercentage(GenericNumbersFilter):
    """ Filter movies that has a particular awards won to nominations percentage """

    def get_filter_function(self, *args):
        """
        Return numbers filter function
        :param args: ['column_name', 'operator', 'value'] -> ['box_office', 'lt', '10']
        :return: Appropriate filter function
        :raises ValueError: User passed invalid number as argument
        """

        fitted_args = args[1:]  # ['column_name', 'keyword', 'operator', 'value']

        filter_func = super().get_filter_function(*fitted_args)

        return filter_func

    def database_result_parse(self, database_result):
        """ Parse awards string to win/nominations ratio """

        try:
            won_awards = ExtractNumber.extract(database_result[self.column_name],
                                               'wins')
            nominations = ExtractNumber.extract(database_result[self.column_name],
                                                'nominations')
        except TypeError:
            raise
        except IndexError:
            raise

        try:
            win_percentage = (won_awards / nominations) * 100  # Percentage calculation
            return win_percentage
        except ZeroDivisionError:
            raise ZeroDivisionError(f"Can't divide by 0: {nominations}")

    def get_column_name(self):
        return 'awards'

    @staticmethod
    def get_keyword():
        return 'awards_won_percentage'


class FilterByAwards(GenericFilter):
    """ Class which handles filtering by cast """

    available_filters = (OscarsNominated(), AwardsWonPercentage())

    def get_filter_function(self, *args):
        """
        Get the appropriate filter function based on user request
        :param args: ['awards', 'keyword']
        :return:
        """

        keyword = args[1]

        for available_filter in FilterByAwards.available_filters:
            if keyword == available_filter.get_keyword():
                filter_func = available_filter.get_filter_function(*args)
                return filter_func
        raise ValueError(f'Incorrect option requested: {args}')

    def get_column_name(self):
        return 'awards'
