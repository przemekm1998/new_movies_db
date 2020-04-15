class GenericComparator:
    """ Generic number comparator """

    def __init__(self, keyword, column_name):
        """
        GenericComparator constructor
        :param column_name: column to compare
        """

        self.keyword = keyword
        self.column_name = column_name

    def compare_data(self, db_results):
        """
        Comparing data from the database
        :param db_results: Results from the database
        :return:
        """

        not_none_results = (result for result in db_results if
                            result[self.column_name] is not None)

        result = max(not_none_results, key=lambda x: x[self.column_name])

        return result
