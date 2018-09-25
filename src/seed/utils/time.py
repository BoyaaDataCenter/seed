from dateutil import tz


def convert_utc_to_local(utc_datetime, time_zone):
    zone = tz.gettz(time_zone)
    return utc_datetime.replace(tzinfo=zone)