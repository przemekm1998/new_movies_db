from modules.commands.filter_data.generic_filters.generic_text_filter import \
    GenericTextFilter


class FilterByLanguage(GenericTextFilter):
    """ Class which handles filtering by language """

    def get_column_name(self):
        return 'language'
