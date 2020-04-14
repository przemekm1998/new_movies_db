from modules.commands.filter_data.filters.generic_filters import \
    GenericTextFilter


class FilterByLanguage(GenericTextFilter):
    """ Class which handles filtering by language """

    column_name = 'language'
