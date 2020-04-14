from modules.commands.filter_data.filters.generic_filters import \
    GenericTextFilter


class FilterByCast(GenericTextFilter):
    """ Class which handles filtering by cast """

    column_name = 'cast'
