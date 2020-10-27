import time
import datetime

from dateutil import parser, tz

def GetCountdownTime(stop_date, time_zone):

    #Gets the current time on the selected Time Zone
    selected_tz = tz.gettz(time_zone)
    current_datetime_tz = datetime.datetime.now(tz=selected_tz)

    difference = stop_date - current_datetime_tz

    count_hours, rem = divmod(difference.seconds, 3600)
    count_minutes, count_seconds = divmod(rem, 60)

    #count_hours = count_hours + 1

    count_down_str = f'{difference.days} Day(s) {count_hours} Hour(s) {count_minutes} Minute(s) {count_seconds} Second(s)'

    if difference.days <= 0 and count_hours <= 0 and count_minutes <= 0 and count_seconds <= 0:
        return "LAtEr SuCkeRsSSss!"

    if difference.days >= 0:
        return count_down_str