from modules.commands.filter_data.generic_filters.generic_numbers_filter import \
    GenericNumbersFilter


class FilterByEarnings(GenericNumbersFilter):
    """ Class which handles filtering by $100,000,000 box office earnings """

    def get_column_name(self):
        return 'box_office'

