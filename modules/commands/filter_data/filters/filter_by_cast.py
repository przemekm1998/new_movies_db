from modules.commands.filter_data.generic_filters.generic_text_filter import \
    GenericTextFilter


class FilterByCast(GenericTextFilter):
    """ Class which handles filtering by cast """

    def get_column_name(self):
        return 'cast'
