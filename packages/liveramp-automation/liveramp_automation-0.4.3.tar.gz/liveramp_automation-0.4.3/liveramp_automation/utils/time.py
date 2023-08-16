import time
from datetime import date, timedelta, datetime

"""
The MACROS() API prepared some expected time format.
You could invole the time format like: yesterday.format(**MACROS) at any code snippet.
"""
MACROS = {
    "yesterday": (date.today() - timedelta(days=1)).strftime("%Y%m%d"),
    "today": date.today().strftime("%Y%m%d"),
    "dayOfYear": (date.today().timetuple()).tm_yday,
    "now": datetime.now().strftime("%Y%m%d%H%M%S"),
    "now_format": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "nowconnect": datetime.now().strftime("%Y%m%d-%H%M%S"),  # data ingestion must be in yyyymmdd-hhmmss format
    "three_days_ago": (date.today() - timedelta(days=0)).strftime("%Y%m%d"),
    "two_hours_from_now": (datetime.now() + timedelta(hours=2)).strftime("%Y%m%d-%H%M%S"),
    "24hours_before_now": (datetime.now() - timedelta(hours=24)).strftime("%Y%m%d%H%M%S")
}


def fixed_wait(value=3):
    """The fixed_wait() defined the default=3 seconds wait time.

    :param value: The number of seconds to wait (default is 3 seconds).
    :return: None
    """
    time.sleep(value)
