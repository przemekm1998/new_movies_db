import sqlite3

from modules.database.db_manager import DbManager


class DbConnector:
    """ Class managing database connection """

    def __init__(self, database=DbManager()):
        self.database = database


class DbUpdater(DbConnector):
    """ Class which allows database updating """

    @property
    def update_statement(self):
        """ SQL statement to update database row """

        statement = f"""UPDATE {self.database.db_table_name} 
                        SET year = :year, runtime = :runtime,
                        genre = :genre, director = :director, writer = :writer,
                        cast = :cast, language = :language,
                        country = :country, awards = :awards, 
                        imdb_Rating = :imdbRating, imdb_Votes = :imdbVotes,
                        box_office = :BoxOffice
                        WHERE title = :title"""

        return statement

    def update_row(self, data):
        """
        Updating database row
        :param data: data to update the database
        :return:
        """

        try:
            with self.database.connection:
                self.database.cursor.execute(self.update_statement,
                                             {'title': data['Title'],
                                              'year': data['Year'],
                                              'runtime': data['Runtime'],
                                              'genre': data['Genre'],
                                              'director': data['Director'],
                                              'writer': data['Writer'],
                                              'cast': data['Cast'],
                                              'language': data['Language'],
                                              'country': data['Country'],
                                              'awards': data['Awards'],
                                              'imdbRating': data['imdbRating'],
                                              'imdbVotes': data['imdbVotes'],
                                              'BoxOffice': data['BoxOffice']
                                              })
        except sqlite3.IntegrityError as error:
            raise error
        except sqlite3.OperationalError as error:
            raise error
        except KeyError:
            raise KeyError(f'Data in incorrect format! {data}')


class DbReader(DbConnector):
    """ Class allowing to read data from database """

    def __init__(self, database=DbManager()):
        self.column_name = None
        super().__init__(database)

    @property
    def select_sql_statement(self):
        """ SQL statement to select data from database """

        statement = f"""SELECT {self.column_name} FROM {self.database.db_table_name};"""

        return statement

    def select_data_from_db(self, column_name):
        """ Executing SQL statement to fetch data from db """

        self.column_name = column_name
        if self.column_name.lower() != 'title':
            self.column_name = 'title, ' + self.column_name
        data = self.database.execute_statement(self.select_sql_statement)

        return data
