import datetime

class convertTime_fablab:
    def convert_time_to_milliseconds(time_of_day=datetime.time(0, 0, 0, 0)):
        # This function is used to convert time to miliseconds
        time_as_timedelta = datetime.timedelta(hours=time_of_day.hour, minutes=time_of_day.minute, seconds=time_of_day.second)
        time_as_milliseconds = int(time_as_timedelta.total_seconds() * 1000)
        return time_as_milliseconds

    def convert_miliseconds_to_timeOfDay(time_as_milliseconds):
        # This function is used to convert time to miliseconds to timeofDay
        milliseconds = time_as_milliseconds
        time_as_timedelta = datetime.timedelta(milliseconds=milliseconds)
        hours, remainder = divmod(time_as_timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_of_day = datetime.time(hour=hours, minute=minutes, second=seconds)
        return time_of_day
