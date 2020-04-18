""" Fetching sorted data from the database """
from modules.commands.commands_handler import CommandHandler
from modules.commands.data_tools.sorters import TitleSort, YearSort, GenreSort, \
    CastSort, WriterSort, AwardsSort, ImdbRatingSort, ImdbVotesSort, BoxOfficeSort, \
    RuntimeSort
from modules.database.db_interfaces import DbReader


class DataSorter(DbReader, CommandHandler):
    """ This class contains every method needed for sorting data """

    keyword = 'sort_by'

    sorters = (TitleSort(), YearSort(), GenreSort(), CastSort(), WriterSort(),
               AwardsSort(), ImdbRatingSort(), ImdbVotesSort(), BoxOfficeSort(),
               RuntimeSort())

    def handle(self, *args):
        """
        Handling the sorting command request
        :param args: ['requested_sorter', 'sorting_order']
        :return: Generator of sorted values from database
        """

        requested_sorter = args[0]
        for sorter in self.sorters:
            if requested_sorter == sorter.keyword:
                db_data = self.select_data_from_db(sorter.column_name)

                # Prevent None values from being sorted
                filtered_data = filter(lambda x: x[sorter.column_name], db_data)

                sort_order = args[1]
                sorted_data = sorter.sort_data(filtered_data, sort_order)

                return sorted_data
        raise ValueError(f"Given sort option doesn't exist: {requested_sorter}")
