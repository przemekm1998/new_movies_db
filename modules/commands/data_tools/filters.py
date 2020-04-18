""" Available filters to use """
from modules.commands.data_tools.common_utils import ExtractNumber
from modules.commands.data_tools.templates.filter_templates import GenericTextFilter, \
    GenericNumbersFilter


class CastFilter(GenericTextFilter):
    """ Filter by cast """

    keyword = 'cast'
    column_name = 'cast'


class DirectorFilter(GenericTextFilter):
    """ Filter by director """

    keyword = 'director'
    column_name = 'director'


class LanguageFilter(GenericTextFilter):
    """ Filter by language """

    keyword = 'language'
    column_name = 'language'


class BoxOfficeFilter(GenericNumbersFilter):
    """ Filter by box office """

    keyword = 'box_office'
    column_name = 'box_office'


class OscarsNominationsFilter(GenericTextFilter):
    """ Filter movies which were nominated to Oscars but didn't win any """

    keyword = 'oscars_nominated'
    column_name = 'awards'

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


class AwardsWonFilter(GenericNumbersFilter):
    """ Filter movies that has a particular awards won to nominations percentage """

    keyword = 'awards_won'
    column_name = 'awards'

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
        """
        Parse awards string to win/nominations ratio
        :param database_result: result from database to parse
        :return:
        """

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
