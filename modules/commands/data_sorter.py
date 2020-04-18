""" Fetching sorted data from the database """
from modules.commands.commands_handler import CommandHandler
from modules.commands.templates.sorter_templates import GenericSorter, ParsingSorter
from modules.database.db_interfaces import DbReader


class DataSorter(DbReader, CommandHandler):
    """ This class contains every method needed for sorting data """

    keyword = 'sort_by'

    sorters = (GenericSorter(keyword='title', column_name='title'),
               GenericSorter(keyword='year', column_name='year'),
               GenericSorter(keyword='genre', column_name='genre'),
               GenericSorter(keyword='cast', column_name='cast'),
               GenericSorter(keyword='writer', column_name='writer'),
               GenericSorter(keyword='director', column_name='director'),
               GenericSorter(keyword='awards', column_name='awards'),
               GenericSorter(keyword='imdb_rating', column_name='imdb_rating'),
               GenericSorter(keyword='imdb_votes', column_name='imdb_votes'),
               GenericSorter(keyword='box_office', column_name='box_office'),
               ParsingSorter(keyword='runtime', column_name='runtime',
                             word_to_parse='min'),
               )

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

                # Prevent None values from sorting
                filtered_data = filter(lambda x: x[sorter.column_name], db_data)

                sort_order = args[1]
                sorted_data = sorter.sort_data(filtered_data, sort_order)

                return sorted_data
        raise ValueError(f"Given sort option doesn't exist: {requested_sorter}")
