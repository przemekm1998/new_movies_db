from modules.cli_interface import CLI
from modules.commands.data_adder import AddData
from modules.commands.data_compare import DataCompare
from modules.commands.data_filter import DataFilter
from modules.commands.data_highscores import DataHighscores
from modules.commands.data_sorter import DataSorter
from modules.database.db_updater import DatabaseUpdater


class Main:
    """ Main program execution class """

    @staticmethod
    def main():
        """ Main program function """

        # Available handlers of commands
        handlers = (DataSorter(), DataFilter(), DataCompare(), DataHighscores(),
                    AddData())

        # Database check
        updater = DatabaseUpdater()
        updater.update()

        Main.handle_commands(handlers)

    @staticmethod
    def handle_commands(handlers):
        """
        Handling every commands request within a loop
        :param handlers: List of available handling commands classes
        :return:
        """

        commands = CLI.get_args()  # Get parsed user args

        for key in commands.keys():
            if commands[key]:
                for handler in handlers:
                    if key == handler.keyword:
                        parameters = commands[key] if type(commands[key]) is list \
                            else list()  # If command stores boolean pass empty list as parameters 
                        results = handler.handle(*parameters)
                        Main.print_results(results)

    @staticmethod
    def print_results(results):
        """
        Pretty printing results
        :param results: results generator
        :return:
        """

        if type(results) is dict:
            print(results)
        else:
            for result in results:
                print(result)


if __name__ == '__main__':
    Main.main()
