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
        return cls[member].value[1]
