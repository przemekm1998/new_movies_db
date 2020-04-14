from modules.cli_interface import CLI
from modules.commands.filter_data.data_filter import DataFilter
from modules.commands.data_sorter import DataSorter
from modules.database_updater import DatabaseUpdater
from pprint import pprint


class Main:
    """ Main program execution class """

    @staticmethod
    def main():
        """ Main program function """

        commands = CLI.get_args()  # Get parsed user args

        # Available handlers of commands
        handlers = (DataSorter(), DataFilter())

        updater = DatabaseUpdater()
        updater.update()

        Main.handle_commands(commands, handlers)

    @staticmethod
    def handle_commands(commands, handlers):
        """
        Handling every commands request within a loop
        :param commands: Commands requested by user
        :param handlers: List of available handling commands classes
        :return:
        """

        for key in commands.keys():
            if commands[key]:
                for handler in handlers:
                    if key == handler.get_keyword():
                        parameters = commands[key]
                        results = handler.handle(*parameters)
                        Main.print_results(results)

    @staticmethod
    def print_results(results):
        """
        Pretty printing results
        :param results: results generator
        :return:
        """

        for result in results:
            pprint(result[0] + ' | ' + str(result[1]))


if __name__ == '__main__':
    Main.main()
