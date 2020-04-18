from abc import abstractmethod

from modules.commands.data_tools.common_utils import ExtractNumber


class Sorter:
    """ Sorter interface template for every sorter """

    keyword = None  # Implement keyword in proper sorter
    column_name = None  # Implement column_name in proper sorter

    @abstractmethod
    def sort_data(self, *args):
        """
        Implement specific sorting function
        :return: sorted data
        """

        raise NotImplementedError


class GenericSorter(Sorter):
    """ Sorting data which don't need parsing """

    def sort_data(self, db_results, order_factor):
        """
        Sorting database results
        :param db_results: Results from the SQL database
        :param order_factor: Ordering factor of the data
        :return: Sorted generator of dict values
        """

        ordering = (order_factor.lower() == 'desc')  # True if descending sort
        sorted_data = sorted(db_results, key=lambda x: x[self.column_name],
                             reverse=ordering)

        return sorted_data


class ParsingSorter(GenericSorter):
    """ Sorting data which needs parsing before sort """

    word_to_parse = None  # Implement word_to_parse in proper sorter

    def sort_data(self, db_results, order_factor):
        """
        Parsing db results before sorting
        :param db_results: Results from the SQL database
        :param order_factor: Ordering factor of the data
        :return: Sorted generator of dict values
        """

        parsed_data = (ExtractNumber.parse(result, self.column_name, self.word_to_parse)
                       for result in db_results)
        sorted_data = super().sort_data(parsed_data, order_factor)

        return sorted_data
