from modules.commands.filter_data.generic_filters.generic_text_filter import \
    GenericTextFilter


class FilterByDirector(GenericTextFilter):
    """ Class which handles filtering by director """

    def get_column_name(self):
        return 'director'
