"""
Module contain enumerators
"""

from enum import Enum


class OrderBy(Enum):
    """
    Enum for order_by param in client search
    """
    fn = ('fn', 'first_name')
    ln = ('ln', 'last_name')
    dfb = ('dfb', 'date_of_birth')
    dfb_d = ('dfb_d', '-date_of_birth')

    @classmethod
    def get_value(cls, member):
        """
        Return enum value by it member
        :param member: short name enum
        :return: full name enum
        """
        return cls[member].value[1]
