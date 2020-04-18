from modules.commands.data_tools.common_utils import ExtractNumber
from modules.commands.comparators.generic_comparator import GenericComparator


class ParsingComparator(GenericComparator):
    """ Comparing data which needs parsing """

    def __init__(self, keyword, column_name, word_to_parse):
        self.word_to_parse = word_to_parse
        super().__init__(keyword, column_name)

    def parse_function(self, db_result):
        """
        Extracting a number from a single database record
        :param db_result: single result from SQL database
        :return:
        """

        try:
            parsed_data = ExtractNumber.extract(db_result[self.column_name],
                                                self.word_to_parse)
        except IndexError as error:
            print(f'{error}, DB_DATA: {db_result[self.column_name]}')
            parsed_data = None
        except TypeError as error:
            print(f'{error}, DB_DATA: {db_result[self.column_name]}')
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
