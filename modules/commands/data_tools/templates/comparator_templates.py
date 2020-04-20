""" Templates for creating comparators """
from modules.commands.data_tools.common_utils import ExtractNumber


class GenericComparator:
    """ Generic number comparator """

    keyword = None
    column_name = None

    def compare_data(self, db_results):
        """
        Comparing data from the database
        :param db_results: Results from the database
        :return:
        """

        not_none_results = (result for result in db_results if
                            result[self.column_name] is not None)

        try:
            result = max(not_none_results, key=lambda x: x[self.column_name])
        except ValueError:
            raise ValueError(f"Given titles doesn't have data to compare: {db_results}")

        dict_result = {'title': result['title'],
                       self.keyword: result[self.column_name]}

        return dict_result


class ParsingComparator(GenericComparator):
    """ Comparing data which needs parsing """

    word_to_parse = None

    def parse_function(self, db_result):
        """
        Extracting a number from a single database record
        :param db_result: single result from SQL database
        :return:
        """

        try:
            parsed_data = ExtractNumber.extract(db_result[self.column_name],
                                                self.word_to_parse)
        except IndexError:
            parsed_data = None
        except TypeError:
            parsed_data = None

        results = {'title': db_result['title'], self.column_name: parsed_data}

        return results

    def compare_data(self, db_results):
        """
        Comparing parsed data from the database
        :param db_results: Results from the database
        :return:
        """

        parsed_db_results = (self.parse_function(result) for result in db_results)

        result = super().compare_data(db_results=parsed_db_results)

        return result
