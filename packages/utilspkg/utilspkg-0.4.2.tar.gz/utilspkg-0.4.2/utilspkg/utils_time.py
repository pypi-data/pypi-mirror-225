from datetime import timedelta, timezone, datetime
import pytz

class UtilsTime:
    ''' Set of functions to return useful datetime objects and strings from 
    slack timezone offsets, slack timestamps, and more'''

    @staticmethod
    def get_datetime_from_timezone(timezone_name='US/Eastern'):
        """
        Returns the current datetime object of a specific timezone.

        Args:
            timezone_name (str, optional): The timezone you want to get the current time from. Defaults to 'US/Eastern'.
        
        Returns:
            datetime: Current datetime object of the provided timezone.
        """
        tz = pytz.timezone(timezone_name)
        return datetime.now(tz)

    @staticmethod
    def get_day_name_from_dt(date_time):
        """
        Returns the day of the week from a datetime object.

        Args:
            date_time (datetime): Datetime object to get the day of the week from.
        
        Returns:
            str: Day of the week.
        """
        return date_time.strftime('%A')

    @staticmethod
    def get_time_string1(date_time):    
        """
        Returns a string like "Wednesday 15:00"

        Args:
            date_time (datetime): Datetime object to get the day and hour from.       
        """
        time_str = f'{UtilsTime.get_day_name_from_dt(date_time=date_time)}, {date_time.hour:02d}:00'

        return time_str

    @staticmethod
    def get_time_string2(date_time):    
        """
        Returns a formatted string containing the day of the week and the time.

        Args:
            date_time (datetime): Datetime object to get the day and time from.
        
        Returns:
            str: Formatted string.
        """
        return date_time.strftime('%A, %H:%M')

    @staticmethod
    def get_time_string3(date_time):    
        """
        Returns a string like: "Wednesday May 17"

        Args:
            date_time (datetime): Datetime object to get the day, month, and day from.
        
        Returns:
            str: Formatted string.
        """
        return date_time.strftime("%A %B %d")

    @staticmethod
    def get_datetime_from_slack_timestamp(slack_timestamp, tz_offset=0):
        """
        Converts a Slack timestamp and timezone offset into a datetime object.

        Args:
            slack_timestamp (str): Slack timestamp to convert.
            tz_offset (int, optional): Timezone offset in seconds. Defaults to 0.
        
        Returns:
            datetime: Corresponding datetime object.
        """
        unix_timestamp = float(slack_timestamp.split('.')[0])
        dt = datetime.fromtimestamp(unix_timestamp, timezone.utc)  # timezone-aware datetime
        return dt + timedelta(seconds=tz_offset)  


    @staticmethod
    def get_datetime_from_slack_tz_offset(tz_offset, date_time=None):
        """
        Adjusts a datetime object with a Slack timezone offset.

        Args:
            tz_offset (int, optional): Timezone offset in seconds. Defaults to 0.
            date_time (datetime, optional): Datetime object to adjust. If not provided, defaults to current UTC datetime.
        
        Returns:
            datetime: Adjusted datetime object.
        """
        date_time = date_time if date_time else datetime.now(timezone.utc)
        return date_time + timedelta(seconds=tz_offset)
