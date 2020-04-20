""" Available comparators to use """
from modules.commands.data_tools.templates.comparator_templates import \
    GenericComparator, ParsingComparator


class BoxOfficeCompare(GenericComparator):
    """ Compare by highest box office """

    keyword = 'box_office'
    column_name = 'box_office'


class ImdbRatingCompare(GenericComparator):
    """ Compare by highest imdb rating """

    keyword = 'imdb_rating'
    column_name = 'imdb_rating'


class RuntimeCompare(ParsingComparator):
    """ Compare by highest runtime """

    keyword = 'runtime'
    column_name = 'runtime'
    word_to_parse = 'min'


class AwardsWonCompare(ParsingComparator):
    """ Compare by won awards """

    keyword = 'awards_won'
    column_name = 'awards'
    word_to_parse = 'wins'
