from modules.commands.filter_data.filters.generic_filters import \
    GenericNumbersFilter


class FilterByEarnings(GenericNumbersFilter):
    """ Class which handles filtering by $100,000,000 box office earnings """

    column_name = 'box_office'

