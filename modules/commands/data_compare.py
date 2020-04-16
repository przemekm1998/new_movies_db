""" Comparing data by given parameter """

from modules.commands.commands_handler import CommandHandler
from modules.commands.comparators.generic_comparator import GenericComparator
from modules.commands.comparators.parsing_comparator import ParsingComparator
from modules.database.db_manager import DbManager


class DataCompare(CommandHandler):
    """ Class containing methods needed to compare data """

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
        Handle compare command request
        :param args: ['comparator_keyword', 'Title1', 'Title2']
        :return:
        """

        requested_comparator = args[0]

        for comparator in self.available_comparators:
            if requested_comparator == comparator.keyword:
                titles_to_compare = args[1:]  # Extract titles
                highest_result = self.execute_comparison(comparator, *titles_to_compare)

                return highest_result

        raise ValueError(f'Incorrect compare option given: {requested_comparator}')

    def execute_comparison(self, comparator, *titles_to_compare):
        """
        Execute single data comparison
        :param comparator: Selected comparator
        :param titles_to_compare: Titles given by user
        :return:
        """

        # Geting the data from the database
        self.column = comparator.column_name
        db_data = self.database.execute_statement(self.select_sql_statement)

        # Filter db results with particular titles to compare
        filtered_db_data = filter(lambda x: x['Title'] in titles_to_compare,
                                  db_data)

        # Select max from filtered data
        result = comparator.compare_data(filtered_db_data)

        return result

    def get_keyword(self):
        return 'compare_by'
