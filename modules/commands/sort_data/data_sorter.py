""" Fetching sorted data from the database """
from modules.commands.commands_handler import CommandsHandler


class DataSorter(CommandsHandler):
    """ This class contains every method needed for sorting data """

    def __init__(self, database):
        self.database = database  # Db instance for class to work with
        self.column = None  # Column to sort by

    @property
    def sort_by_sql_statement(self):
        """ Select sorted data based on given column """

        statement = f"""SELECT {self.database.db_table_name}.title, 
                    {self.database.db_table_name}.{self.column} 
                    FROM {self.database.db_table_name}
                    ORDER BY {self.column} DESC;"""

        return statement

    def handle(self, *args):
        """
        Handling the sorting command request
        :param args: Column names to sort by
        :return: Generator of sorted values from database
        """

        self.column = args[0]  # Setting the column to sort by

        results = self.database.execute_statement(self.sort_by_sql_statement)

        return results

    def get_keyword(self):
        return 'sort_by'
