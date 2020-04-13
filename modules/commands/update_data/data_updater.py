""" Filling the rows with titles with downloaded data """

import sqlite3

from modules.commands.commands_handler import CommandsHandler
from modules.db_management.db_manager import DbManager
from modules.download_data.data_download import DataDownloader


class DataUpdater(CommandsHandler):
    """ Handling updating the database data """

    def __init__(self):
        self.database = DbManager()

    @property
    def select_titles_with_no_data(self):
        """
        Select titles with empty data from db, if year is NULL than the rest of
        the data must be null
        """

        statement = f"""SELECT {self.database.db_table_name}.title 
                        FROM {self.database.db_table_name}
                        WHERE year IS NULL"""

        return statement

    @property
    def insert_data_statement(self):
        """
        Insert downloaded data to the db
        """

        statement = f"""UPDATE {self.database.db_table_name} 
                        SET year = :year, runtime = :runtime,
                        genre = :genre, director = :director, writer = :writer,
                        cast = :cast, language = :language,
                        country = :country, awards = :awards, 
                        imdb_Rating = :imdbRating, imdb_Votes = :imdbVotes,
                        box_office = :BoxOffice
                        WHERE title = :title"""

        return statement

    def handle(self, *args):
        """ Handling updating the database data """

        # Get titles with empty data
        empty_titles = self.get_empty_titles()

        # Download data with empty titles
        data_downloader = DataDownloader()
        downloaded_data = data_downloader.download_data(empty_titles)

        # Insert downloaded data to the db
        for data in downloaded_data:
            self.insert_data(data)

    def get_empty_titles(self):
        """ Creating list of results based on returned SQL object"""

        empty_titles = self.database.execute_statement(self.select_titles_with_no_data)
        results = [result['Title'] for result in empty_titles]

        return results

    def insert_data(self, downloaded_data):
        """
        Inserting downloaded data to the database
        :param downloaded_data: downloaded data using API
        :return:
        """
        try:
            with self.database.connection:
                self.database.cursor.execute(self.insert_data_statement,
                                             {'title': downloaded_data['Title'],
                                              'year': downloaded_data['Year'],
                                              'runtime': downloaded_data['Runtime'],
                                              'genre': downloaded_data['Genre'],
                                              'director': downloaded_data['Director'],
                                              'writer': downloaded_data['Writer'],
                                              'cast': downloaded_data['Cast'],
                                              'language': downloaded_data['Language'],
                                              'country': downloaded_data['Country'],
                                              'awards': downloaded_data['Awards'],
                                              'imdbRating': downloaded_data[
                                                  'imdbRating'],
                                              'imdbVotes': downloaded_data['imdbVotes'],
                                              'BoxOffice': downloaded_data['BoxOffice']
                                              })
                print(f"{downloaded_data['Title']} added to the database")
        except sqlite3.IntegrityError as error:
            raise error
        except sqlite3.OperationalError as error:
            raise error
        except KeyError:
            raise KeyError(f'Data in incorrect format! {downloaded_data}')

    def get_keyword(self):
        return 'update'
