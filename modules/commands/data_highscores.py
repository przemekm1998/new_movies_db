""" Comparing data by given parameter """

from modules.commands.commands_handler import CommandsHandler
from modules.commands.comparators.generic_comparator import GenericComparator
from modules.commands.comparators.parsing_comparator import ParsingComparator
from modules.db_manager import DbManager


class DataHighscores(CommandsHandler):
    """ Class containing methods needed to calculate highscores """

    available_comparators = (GenericComparator(keyword='box_office',
                                               column_name='box_office'),
                             GenericComparator(keyword='imdb_rating',
                                               column_name='imdb_rating'),
                             ParsingComparator(keyword='runtime',
                                               column_name='runtime',
                                               word_to_parse='min'),
                             ParsingComparator(keyword='awards_won',
                                               column_name='awards',
                                               word_to_parse='wins'))

    def __init__(self, database=DbManager()):
        self.column = None
        super().__init__(database)

    @property
    def select_sql_statement(self):
        """ Select data to be compared based on given column """

        statement = f"""SELECT {self.database.db_table_name}.title, 
                    {self.database.db_table_name}.{self.column} 
                    FROM {self.database.db_table_name};"""

        return statement

    def handle(self, *args):
        """
        Handle highscores command request
        :param args: no required args here
        :return:
        """

        results = list()

        for comparator in self.available_comparators:
            # Geting the data from the database
            self.column = comparator.column_name
            db_data = self.database.execute_statement(self.select_sql_statement)

            # Select highest result from filtered data
            comparator_result = comparator.compare_data(db_data)

            formatted_result = self.format_results(comparator, comparator_result)
            results.append(formatted_result)

        return results

    @staticmethod
    def format_results(comparator, comparator_result):
        """
        Formatting the full results into dict
        :param comparator: Used comparator
        :param comparator_result: Result returned by comparator
        :return: Formatted dict
        """

        final_result = {'category': comparator.keyword}
        final_result.update(comparator_result)

        return final_result

    def get_keyword(self):
        return 'highscores'
