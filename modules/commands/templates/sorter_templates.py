from modules.commands.common_utils import ExtractNumber


class GenericSorter:
    """ Sorting data which don't need parsing """

    def __init__(self, keyword, column_name):
        self.keyword = keyword
        self.column_name = column_name

    def sort_data(self, db_results, order_factor):
        """
        Sorting database results
        :param db_results: Results from the SQL database
        :param order_factor: Ordering factor of the data
        :return: Sorted generator of dict values
        """

        # Converting db data to dict to make results easier to print out
        dict_data = ({'title': result['title'],
                      self.column_name: result[self.column_name]}
                     for result in db_results)

        ordering = (order_factor.lower() == 'desc')  # True if descending sort
        sorted_data = sorted(dict_data, key=lambda x: x[self.column_name],
                             reverse=ordering)

        return sorted_data


class ParsingSorter(GenericSorter):
    """ Sorting data which needs parsing before sort """

    def __init__(self, keyword, column_name, word_to_parse):
        self.word_to_parse = word_to_parse
        super().__init__(keyword, column_name)

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
