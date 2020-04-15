""" Comparing data by given parameter """

from modules.commands.commands_handler import CommandsHandler
from modules.commands.comparators.generic_comparator import GenericComparator
from modules.commands.comparators.parsing_comparator import ParsingComparator
from modules.db_manager import DbManager


class DataCompare(CommandsHandler):
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

        comparator_keyword = args[0]

        for comparator in self.available_comparators:
            if comparator_keyword == comparator.keyword:
                # Geting the data from the database
                self.column = comparator.column_name
                db_data = self.database.execute_statement(self.select_sql_statement)

                # Filter db results with particular titles to compare
                titles_to_compare = args[1:]  # Comparator keyword not needed anymore
                filtered_db_data = filter(lambda x: x['Title'] in titles_to_compare,
                                          db_data)

                # Select max from filtered data
                results = comparator.compare_data(filtered_db_data)

                return results

        raise ValueError(f'Incorrect compare option given: {comparator_keyword}')

    def execute_comparison(self, selected_comparator, *args):
        """
        Executing the whole process of comparing
        :param selected_comparator: comparator which matched user selected
        :param args: Titles to compare ['Title 1', 'Title 2']
        :return:
        """

    def get_keyword(self):
        return 'compare_by'
