""" Handling filter implementation template """

from abc import ABCMeta, abstractmethod


class GenericFilter:
    """ FilterTemplate interface for every filter """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.column_name = self.get_column_name()

    @abstractmethod
    def get_filter_function(self, *args):
        """
        Return filtering function
        :return: function that returns true if filtering conditions are met
        """

        raise NotImplementedError

    @abstractmethod
    def get_column_name(self):
        """ Every filter has to have its own column to filter"""

        raise NotImplementedError
