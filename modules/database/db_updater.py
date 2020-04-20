""" Filling the rows with titles with downloaded data """
from modules.database.db_interfaces import DbUpdater, DbReader
from modules.data_download import DataDownloader
from modules.database.db_manager import DbManager


class DatabaseUpdater(DbUpdater, DbReader):
    """ Handling updating the database data """

    def __init__(self, database=DbManager()):
        super().__init__(database)

    def update(self):
        """ Handling updating the database data """

        # Get titles with empty data
        titles_with_no_data = self.get_titles_with_no_data()

        # Download data with empty titles
        data_downloader = DataDownloader()
        downloaded_data = data_downloader.download_data(titles_with_no_data)

        # Update db with downloaded data
        for data in downloaded_data:
            self.update_row(data)

    def get_titles_with_no_data(self):
        """ Creating generator of results based on returned SQL object"""

        titles_with_no_data = self.select_data_from_db(column_name='year')
        results = (result['title'] for result in titles_with_no_data
                   if not result['year'])

        return results
