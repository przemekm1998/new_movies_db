from modules.commands.commands_handler import CommandHandler
from modules.data_download import DataDownloader
from modules.database.db_interfaces import DbUpdater, DbInsert


class AddData(DbUpdater, DbInsert, CommandHandler):
    """ Class containing methods needed to compare data """

    keyword = 'add'

    def handle(self, *args):
        """
        Insert record to the db and automatically try to update it
        :param args: Titles to insert and update ['Title1', 'Title2', ...]
        """

        titles_to_insert = args

        # Insert record
        for title in titles_to_insert:
            self.insert_title_to_db(title)

        # Try to download data for inserted titles
        data_downloader = DataDownloader()
        downloaded_data = data_downloader.download_data(titles_to_insert)

        # Update db with downloaded data
        for data in downloaded_data:
            self.update_row(data)
