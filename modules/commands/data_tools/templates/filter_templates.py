""" Generic filters to use """

from abc import abstractmethod
import re


class GenericFilter:
    """ FilterTemplate interface for every filter """

    keyword = None
    column_name = None

    @abstractmethod
    def get_filter_function(self, *args):
        """
        Implement specific filtering function
        :return: function that returns true if filtering conditions are met
        """

        raise NotImplementedError


class GenericNumbersFilter(GenericFilter):
    """ Class containing all methods needed to filter numbers column """

    def __init__(self):
        self.operator = None
        self.value_to_filter = None

    def get_filter_function(self, *args):
        """
        Return text filter function
        :param args: ['column_name', 'operator', 'value'] -> ['box_office', 'lt', '10']
        :return: Appropriate filter function
        :raises ValueError: User passed invalid number as argument
        """

        self.operator = args[0]

        try:
            self.value_to_filter = float(args[1])  # Convert str '10' argument to float
        except ValueError:
            raise ValueError(f'Value to filter must be a number: {args[1]}')

        filter_function = self.select_function()
        return filter_function

    def select_function(self):
        """
        Compare database_result with filtering result by operator
        :return: proper filtering function
        :raises ValueError: incorrect operator given by the user
        """

        if self.operator == 'gte':
            return self.gte
        elif self.operator == 'gt':
            return self.gt
        elif self.operator == 'lte':
            return self.lte
        elif self.operator == 'lt':
            return self.lt
        elif self.operator == 'e':
            return self.e
        else:
            raise ValueError(f'Invalid operator: {self.operator}')

    def database_result_parse(self, database_result):
        """
        Parse the result from the database if needed, as default this function
        returns plaint result from the db
        :param database_result: SQL row object from database
        :return: Parsed db result, as default plain db result
        """

        return database_result[self.column_name]

    def gte(self, database_result):
        """
        Check if result from database >= value_to_filter
        :param database_result: Result from the database to be checked
        :return: Boolean result from database >= value_to_filter
        """

        try:
            db_result = self.database_result_parse(database_result)
            return db_result >= self.value_to_filter
        except TypeError:
            return False
        except IndexError:
            return False

    def gt(self, database_result):
        """
        Check if result from database > value_to_filter
        :param database_result: Result from the database to be checked
        :return: Boolean result from database > value_to_filter
        """

        try:
            db_result = self.database_result_parse(database_result)
            return db_result > self.value_to_filter
        except TypeError:
            return False
        except IndexError:
            return False

    def lte(self, database_result):
        """
        Check if result from database <= value_to_filter
        :param database_result: Result from the database to be checked
        :return: Boolean result from database <= value_to_filter
        """

        try:
            db_result = self.database_result_parse(database_result)
            return db_result <= self.value_to_filter
        except TypeError:
            return False
        except IndexError:
            return False

    def lt(self, database_result):
        """
        Check if result from database < value_to_filter
        :param database_result: Result from the database to be checked
        :return: Boolean result from database < value_to_filter
        """

        try:
            db_result = self.database_result_parse(database_result)
            return db_result < self.value_to_filter
        except TypeError:
            return False
        except IndexError:
            return False

    def e(self, database_result):
        """
        Check if result from database == value_to_filter
        :param database_result: Result from the database to be checked
        :return: Boolean result from database == value_to_filter
        """

        try:
            db_result = self.database_result_parse(database_result)
            return db_result == self.value_to_filter
        except TypeError:
            return False
        except IndexError:
            return False


class GenericTextFilter(GenericFilter):
    """ Class containing all methods needed to filter text column """

    def __init__(self):
        self.value_to_filter = None

    def get_filter_function(self, *args):
        """
        Return text filter function
        :param args: ['column_name', 'value_to_filter']
        :return:
        """

        self.value_to_filter = args[0]  # args = ['value_to_filter']

        return self.filter_text

    def filter_text(self, database_result):
        """
        Filter result from database based on given value
        :param database_result: Result from the database to be checked
        :return: Boolean if given result contains value to be filtered ou
        """

        found = bool(
            re.search(rf'{self.value_to_filter}', database_result[self.column_name]))

        return found
