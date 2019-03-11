import datetime
from unittest import TestCase

from ..models import try_parsing_string_to_date
from ..services import try_parsing_date


class ServicesTestCase(TestCase):
    """
    Test cases of application services
    """
    def test_try_parsing_date(self):
        """
        Check try_parsing_date
        """
        self.assertIsInstance(try_parsing_date(datetime.datetime.now()), str)

    def test_try_parsing_string_to_date(self):
        """
        Check try_parsing_string_to_date with any available formats
        """
        date_list = (
            '2000-01-21', '21-01-2000',
            '2000/01/21', '21/01/2000',
            '2000.01.21', '21.01.2000',
            '2000 01 21', '21 01 2000',
        )
        for date in date_list:
            self.assertIsInstance(try_parsing_string_to_date(date),
                                  datetime.datetime)
