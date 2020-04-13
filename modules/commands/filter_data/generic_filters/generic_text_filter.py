""" Filtering text column based on value to be filtered out """
import re
from abc import abstractmethod

from modules.commands.filter_data.generic_filters.generic_filter import GenericFilter


class GenericTextFilter(GenericFilter):
    """ Class containing all methods needed to filter text column """

    def __init__(self):
        self.value_to_filter = None
        super().__init__()

    def get_filter_function(self, *args):
        """
        Return text filter function
        :param args: ['column_name', 'value_to_filter']
        :return:
        """

        self.value_to_filter = args[1]  # args = ['column_name', 'value_to_filter']

        return self.filter_text

    def filter_text(self, database_result):
        """
        Filter result from database based on given value
        :param database_result: Result from the database to be checked
        :return: Boolean if given result contains value to be filtered ou
        """

        found = bool(re.search(rf'{self.value_to_filter}', database_result[
            self.column_name]))
        return found

    @abstractmethod
    def get_column_name(self):
        """ Return column name to filter """

        raise NotImplementedError
