from modules.commands.filter_data.generic_filters.generic_filter import FilterTemplate


class FilterByOscarsNominations(FilterTemplate):
    """ Class which handles filtering by Oscars nominations """

    def get_column_name(self):
        return 'awards'

    def get_keyword(self):
        return 'oscars_nominations'

    def filter_result(self, result, *args):
        """
        Example of movie that didn't win an oscar
        "Nominated for 3 Oscars. Another 9 wins & 50 nominations."

        Example of movie that won an oscar
        "Won 2 Oscars. Another 84 wins & 190 nominations"

        So the keyword here is /Nominated/
        """
        column_name = self.get_column_name()
        return 'Nominated' in result[column_name]
