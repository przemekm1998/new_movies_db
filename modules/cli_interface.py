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
        parser.add_argument('--sort_by', help='sort records', action='store', nargs=1,
                            choices=['id', 'title', 'year', 'runtime', 'genre',
                                     'director', 'cast', 'writer', 'language',
                                     'country',
                                     'awards', 'imdb_rating', 'imdb_votes',
                                     'box_office'],
                            type=str)

        # Filtering records
        parser.add_argument('--filter_by', help='filter records', action='store',
                            nargs='+', type=str,
                            metavar=('column', 'value'))

        args = parser.parse_args()

        commands = {'sort_by': args.sort_by,
                    'filter_by': args.filter_by}

        return commands
