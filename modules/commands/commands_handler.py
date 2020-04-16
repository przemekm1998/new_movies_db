""" Handling commands implementation template """

from abc import ABCMeta, abstractmethod


class CommandHandler:
    """ Commands Handler interface for every handler """

    __metaclass__ = ABCMeta

    keyword = None

    @abstractmethod
    def handle(self, *args):
        """ The main handle method used in main for every command handler """

        raise NotImplementedError
