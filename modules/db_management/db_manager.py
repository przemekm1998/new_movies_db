""" SQLite database operations management """
import sqlite3


class DbManager:
    """ Managing the db """

    def __init__(self, db_name='movies.sqlite'):
        self.db_name = db_name
        self.db_table_name = 'MOVIES'

        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # Assuring the table exists in the database
        with self.connection:
            self.connection.execute(self.create_table_statement)

    @property
    def create_table_statement(self):
        """ SQL statement to create table """
        statement = f"""create table if not exists {self.db_table_name} (
                        ID INTEGER PRIMARY KEY,
                        TITLE text UNIQUE, 
                        YEAR integer, 
                        RUNTIME text, 
                        GENRE text, 
                        DIRECTOR text, 
                        CAST text, 
                        WRITER text, 
                        LANGUAGE text, 
                        COUNTRY text, 
                        AWARDS text, 
                        IMDb_Rating float,
                        IMDb_votes integer, 
                        BOX_OFFICE integer );"""

        return statement

    def execute_statement(self, statement):
        """
        Executing the given SQL statement
        :param statement: SQL statement to execute within the db
        :raises IntegrityError: i.e. insert statement violating UNIQUE constraint
        """

        try:
            with self.connection:
                results = self.cursor.execute(statement)
                return results
        except sqlite3.IntegrityError as error:
            raise error
        except sqlite3.OperationalError as error:
            raise error
