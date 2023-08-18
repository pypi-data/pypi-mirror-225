import time
import datetime
from datetime import date

year = '%Y'
month = '%Y-%m'
day = '%Y-%m-%d'
hours = '%Y-%m-%d %H'
minutes = '%Y-%m-%d %H:%M'
seconds = '%Y-%m-%d %H:%M:%S'


def unix_time(string: str, dateFormat: str) -> int:
    """
    将日期转换为时间戳
    :param string:
    :param dateFormat:
    :return:
    """
    # 转换成时间数组
    timeArray = time.strptime(string, dateFormat)
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    return timestamp


def custom_time(timestamp: int, dateFormat: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    将时间戳转为日期 dateFormat默认
    :param timestamp:
    :param dateFormat:
    :return:
    """
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime(dateFormat, time_local)
    return dt


def date_to_timestamp(date_: date) -> int:
    dayStr = date_.strftime(day)
    return unix_time(dayStr, day)


def get_curr_time() -> int:
    """
    获取当前时间戳 秒
    :return:
    """
    return int(time.time())


def get_curr_time_of_ms() -> int:
    """
    获取当前时间戳 毫秒
    :return:
    """
    return int(time.time() * 1000)


def get_curr_day() -> str:
    """
    获取当前日期
    :return:
    """
    return datetime.datetime.today().strftime(day)


def get_day(timeStamp: int = None) -> date:
    """
    获取日期对象 默认当天
    :param timeStamp: 时间戳 单位s
    :return:
    """
    return datetime.datetime.utcfromtimestamp(timeStamp) if timeStamp else datetime.datetime.today()


def get_start_of_day(timeStamp: int = None) -> int:
    """
    获取一天开始时间戳 默认当天
    :param timeStamp: 时间戳 单位s
    :return:
    """
    if timeStamp:
        return unix_time(custom_time(timeStamp, day), day)
    return unix_time(get_curr_day(), day)


def get_end_of_day(timeStamp: int = None) -> int:
    """
    获取一天结束时间戳 默认当天
    :param timeStamp: 时间戳 单位s
    :return:
    """
    return get_start_of_day(timeStamp) + 86399


def get_start_of_week(timeStamp: int = None, weekend_is_first: bool = False):
    """
    获取一周的开始时间戳  默认：本周
    :param timeStamp: 时间戳 单位s
    :param weekend_is_first: 默认周一是第一天
    :return:
    """
    data = get_day(timeStamp)
    days_ago = data.isoweekday() - 1
    if weekend_is_first:
        days_ago = days_ago + 1
    startWeek = data - datetime.timedelta(days=days_ago)
    return date_to_timestamp(startWeek)


def get_end_of_week(timeStamp: int = None, weekend_is_first: bool = False) -> int:
    """
    获取一周的结束时间戳 默认：本周
    :param timeStamp: 时间戳 单位s
    :param weekend_is_first: 默认周一是第一天
    :return:
    """
    return get_start_of_week(timeStamp, weekend_is_first) + 604799


def get_start_of_month(timeStamp: int = None) -> int:
    """
    获取本月的开始时间戳 默认本月
    :param timeStamp: 时间戳 单位s
    :return:
    """
    data = get_day(timeStamp)
    startMonth = datetime.date(data.year, data.month, 1)
    return date_to_timestamp(startMonth)


def get_ent_of_month(timeStamp: int = None) -> int:
    """
    获取一个月的结束时间戳 默认本月
    :param timeStamp: 时间戳 单位s
    :return:
    """
    data = get_day(timeStamp)
    if data.month == 12:
        yearInt, monthInt = data.year + 1, data.month
    else:
        yearInt, monthInt = data.year, data.month + 1
    startMonth = datetime.date(yearInt, monthInt, 1)
    return date_to_timestamp(startMonth) - 1


def get_start_of_year(timeStamp: int = None) -> int:
    """
    获取一年的开始时间戳 默认本年
    :param timeStamp: 时间戳 单位s
    :return:
    """
    data = get_day(timeStamp)
    startMonth = datetime.date(data.year, 1, 1)
    return date_to_timestamp(startMonth)


def get_end_of_year(timeStamp: int = None) -> int:
    """
    获取一年的结束时间戳 默认本年
    :param timeStamp: 时间戳 单位s
    :return:
    """
    data = get_day(timeStamp)
    startMonth = datetime.date(data.year + 1, 1, 1)
    return date_to_timestamp(startMonth) - 1
