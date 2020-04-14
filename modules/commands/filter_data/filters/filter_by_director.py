from modules.commands.filter_data.filters.generic_filters import \
    GenericTextFilter


class FilterByDirector(GenericTextFilter):
    """ Class which handles filtering by director """

    column_name = 'director'
