""" Available sorters to use """
from modules.commands.data_tools.templates.sorter_templates import GenericSorter, \
    ParsingSorter


class TitleSort(GenericSorter):
    """ Sort by titles """

    column_name = 'title'
    keyword = 'title'


class YearSort(GenericSorter):
    """ Sort by year """

    column_name = 'year'
    keyword = 'year'


class GenreSort(GenericSorter):
    """ Sort by genre """

    column_name = 'genre'
    keyword = 'genre'


class CastSort(GenericSorter):
    """ Sort by cast """

    column_name = 'cast'
    keyword = 'cast'


class WriterSort(GenericSorter):
    """ Sort by writer """

    column_name = 'writer'
    keyword = 'writer'


class AwardsSort(GenericSorter):
    """ Sort by awards """

    column_name = 'awards'
    keyword = 'awards'


class ImdbRatingSort(GenericSorter):
    """ Sort by imdb rating """

    column_name = 'imdb_rating'
    keyword = 'imdb_rating'


class ImdbVotesSort(GenericSorter):
    """ Sort by imdb votes """

    column_name = 'imdb_votes'
    keyword = 'imdb_votes'


class BoxOfficeSort(GenericSorter):
    """ Sort by box office """

    column_name = 'box_office'
    keyword = 'box_office'


class RuntimeSort(ParsingSorter):
    """ Sort by runtime """

    column_name = 'runtime'
    keyword = 'runtime'
    word_to_parse = 'min'
