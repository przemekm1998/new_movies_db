""" Handling commands implementation template """

from abc import ABCMeta, abstractmethod
from modules.db_manager import DbManager


class CommandsHandler:
    """ Commands Handler interface for every handler """

    __metaclass__ = ABCMeta

    def __init__(self, database):
        self.database = database

    @abstractmethod
    def handle(self, *args):
        """ The main handle method used in main for every command handler """

        raise NotImplementedError

    @abstractmethod
    def get_keyword(self):
        """ Every handler has to have its own keyword like command """

        raise NotImplementedError
