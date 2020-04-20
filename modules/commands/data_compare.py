""" Comparing data by given parameter """

from modules.commands.commands_handler import CommandHandler
from modules.commands.data_tools.comparators import (BoxOfficeCompare,
                                                     ImdbRatingCompare,
                                                     RuntimeCompare, AwardsWonCompare)
from modules.database.db_interfaces import DbReader


class DataCompare(DbReader, CommandHandler):
    """ Class containing methods needed to compare data """

    keyword = 'compare_by'

    available_comparators = (BoxOfficeCompare(), ImdbRatingCompare(), RuntimeCompare(),
                             AwardsWonCompare())

    def handle(self, *args):
        """
        Handle compare command request
        :param args: ['comparator_keyword', 'Title1', 'Title2', ...]
        :return: Highest result of comparison
        """

        requested_comparator = args[0]

        for comparator in self.available_comparators:
            if requested_comparator == comparator.keyword:
                db_data = self.select_data_from_db(comparator.column_name)

                titles_to_compare = args[1:]  # Extract only titles
                filtered_db_data = filter(lambda x: x['title'] in titles_to_compare,
                                          db_data)

                try:
                    result = comparator.compare_data(filtered_db_data)
                except ValueError as error:
                    raise error

                return result

        raise ValueError(f'Incorrect compare option given: {requested_comparator}')
