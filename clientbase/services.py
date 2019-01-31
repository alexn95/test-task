from app import settings
from datetime import datetime


# Parsing date from string, check all possible formats
def try_parsing_date(date):
    for fmt in settings.DATE_INPUT_FORMATS:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

