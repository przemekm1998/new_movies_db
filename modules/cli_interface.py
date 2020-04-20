import argparse


class CLI:
    """ Command Line Interface """

    @staticmethod
    def get_args():
        """ Loading arguments given by user """

        # Creating parser
        parser = argparse.ArgumentParser(prog='my_program',
                                         description='Working with movies DB.')
        parser.add_argument('--version', action='version', version='1.0.0')

        # Sorting records
        parser.add_argument('--sort_by', help='sort records', action='store', nargs=2,
                            type=str)

        # Filtering records
        parser.add_argument('--filter_by', help='filter records', action='store',
                            nargs='+', type=str,
                            metavar=('column', 'value'))

        # Comparing records
        parser.add_argument('--compare_by', help='compare records', action='store',
                            nargs='+', type=str,
                            metavar=('compare_type', 'value'))

        # Highscores
        parser.add_argument('--highscores', help='show highscores', action='store_true')

        args = parser.parse_args()

        commands = {'sort_by': args.sort_by,
                    'filter_by': args.filter_by,
                    'compare_by': args.compare_by,
                    'highscores': args.highscores}

        return commands
