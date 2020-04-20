""" Comparing data by given parameter """

from modules.commands.commands_handler import CommandHandler
from modules.commands.data_tools.comparators import BoxOfficeCompare, ImdbRatingCompare, \
    RuntimeCompare, AwardsWonCompare
from modules.database.db_interfaces import DbReader


class DataHighscores(DbReader, CommandHandler):
    """ Class containing methods needed to calculate highscores """

    keyword = 'highscores'

    available_comparators = (BoxOfficeCompare(), ImdbRatingCompare(), RuntimeCompare(),
                             AwardsWonCompare())

    def handle(self, *args):
        """
        Handle highscores command request
        :param args: no required args here
        :return:
        """

        results = list()

        for comparator in self.available_comparators:
            db_data = self.select_data_from_db(comparator.column_name)

            try:
                result = comparator.compare_data(db_data)
            except ValueError as error:
                raise error

            formatted_result = self.format_result(result, comparator.keyword)
            results.append(formatted_result)

        return results

    @staticmethod
    def format_result(comparator_result, comparator_keyword):
        """
        Formatting the full results into dict
        :param comparator_keyword: Used comparator's keyword
        :param comparator_result: Result returned by comparator
        :return: Formatted dict
        """

        final_result = {'category': comparator_keyword}
        final_result.update(comparator_result)

        return final_result
