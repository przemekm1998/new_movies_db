""" Fetching filtered data from the database """
from modules.commands.commands_handler import CommandHandler
from modules.commands.data_tools.filters import CastFilter, DirectorFilter, \
    LanguageFilter, BoxOfficeFilter, OscarsNominationsFilter, AwardsWonFilter
from modules.database.db_interfaces import DbReader
from modules.database.db_manager import DbManager


class DataFilter(DbReader, CommandHandler):
    """ This class contains every method needed for filtering data """

    # Filters available to use
    filters = (CastFilter(), DirectorFilter(), LanguageFilter(), BoxOfficeFilter(),
               OscarsNominationsFilter(), AwardsWonFilter())

    def __init__(self, database=DbManager()):
        super().__init__(database)
        self.column = None  # Column to filter

    def handle(self, *args):
        """
        Handling the filtering command request
        :param args: i.e. ["language", "spanish"] Requested filter and value to
        filter out
        :return: Generator of filtered values
        """

        requested_filter = args[0]  # Get keyword of requested filter

        for data_filter in self.filters:
            if requested_filter == data_filter.keyword:
                db_data = self.select_data_from_db(data_filter.column_name)

                filter_args = args[1:]
                filter_function = data_filter.get_filter_function(*filter_args)
                filtered_results = filter(filter_function, db_data)

                return filtered_results
        raise ValueError(f"Can't filter by given parameters: {args}")
