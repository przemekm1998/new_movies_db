""" Filtering numbers column based on value to be filtered out """
from abc import abstractmethod

from modules.commands.filter_data.generic_filters.generic_filter import GenericFilter


class GenericNumbersFilter(GenericFilter):
    """ Class containing all methods needed to filter numbers column """

    def __init__(self):
        self.operator = None
        self.value_to_filter = None
        super().__init__()

    def get_filter_function(self, *args):
        """
        Return text filter function
        :param args: ['column_name', 'operator', 'value'] -> ['box_office', 'lt', '10']
        :return: Appropriate filter function
        :raises ValueError: User passed invalid number as argument
        """

        self.operator = args[1]
        try:
            self.value_to_filter = float(args[2])  # Convert str '10' argument to int
            filter_function = self.select_function()
            return filter_function
        except ValueError:
            raise ValueError(f'Invalid arguments passed: {args}')

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
        :return parsed: Parsed db result, as default -> plain db result
        """

        parsed = database_result[self.column_name]
        return parsed

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

    @abstractmethod
    def get_column_name(self):
        """ Return column name to filter """

        raise NotImplementedError
