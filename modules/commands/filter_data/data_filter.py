""" Fetching filtered data from the database """
from modules.commands.commands_handler import CommandsHandler
from modules.commands.filter_data.filters.filter_by_awards import FilterByAwards
from modules.commands.filter_data.filters.filter_by_cast import FilterByCast
from modules.commands.filter_data.filters.filter_by_director import FilterByDirector
from modules.commands.filter_data.filters.filter_by_earnings import FilterByEarnings
from modules.commands.filter_data.filters.filter_by_language import FilterByLanguage
from modules.db_manager import DbManager


class DataFilter(CommandsHandler):
    """ This class contains every method needed for filtering data """

    def __init__(self, database=DbManager()):
        super().__init__(database)
        self.column = None  # Column to filter

        # Available filters to use
        self.handlers = (FilterByEarnings(), FilterByLanguage(),
                         FilterByCast(), FilterByDirector(),
                         FilterByAwards())

    @property
    def select_sql_statement(self):
        """ Select data to be filtered based on given column """

        statement = f"""SELECT {self.database.db_table_name}.title, 
                    {self.database.db_table_name}.{self.column} 
                    FROM {self.database.db_table_name};"""

        return statement

    def handle(self, *args):
        """
        Handling the filtering command request
        :param args: i.e. ["language", "spanish"] Column name to filter and value to
        filter by
        :return: Generator of filtered values
        """

        self.column = args[0]  # column name is always the first argument

        for handler in self.handlers:
            if self.column == handler.column_name:
                db_data = self.database.execute_statement(self.select_sql_statement)
                filter_function = handler.get_filter_function(*args)
                filtered_results = filter(filter_function, db_data)

                return filtered_results
        raise ValueError(f"Can't filter by given parameters: {args}")

    def get_keyword(self):
        return 'filter_by'
