import datetime
import bisect
import calendar
from typing import Union


def get_quarter(date: datetime):
    """
    获取日期所在的季度及季度区间
    :param date: 日期，datetime
    :return: tuple(quarter_start_date, quarter_end_date, quarter_n)
    """
    if isinstance(date, datetime.datetime):
        date = date.date()
    qbegins = [datetime.date(date.year, month, 1) for month in (1, 4, 7, 10)]
    qends = [datetime.date(date.year, month, calendar.monthrange(date.year, month)[1]) for month in (3, 6, 9, 12)]
    bidx = bisect.bisect(qbegins, date)
    return qbegins[bidx - 1], qends[bidx - 1], bidx


def get_date_range(date: datetime = None, period: int = 6, unit: int = 1):
    """
    按指定日期、周期数、周期单位计算出各日期区间
    :param date: 指定日期
    :param period: 周期数
    :param unit: 周期单位，支持 月=1，季=2，年=3
    :return:日期区间，如： 传参是 date=<datetime: 2020-07-01>, period=2, unit=1,
      return: [(<datetime: 2020-07-01>, <datetime: 2020-07-31>, '2020-07'), (<datetime: 2020-06-01>, <datetime: 2020-06-30>, '2020-06')]
    """
    periods = list()
    year = date is None and datetime.datetime.now().year or date.year
    month = date is None and datetime.datetime.now().month or date.month
    for n in range(int(period)):
        if unit == 1:
            _, day_num = calendar.monthrange(year, month)
            periods.append((datetime.datetime(year, month, 1), datetime.datetime(year, month, day_num), f'{year}-{month}'))
            year, month = calendar.prevmonth(year=year, month=month)
        elif unit == 2:
            first_day, last_day, date_str = get_quarter(date=datetime.date(year, month, 1))
            periods.append((first_day, last_day, date_str))
            year, month = calendar.prevmonth(year=first_day.year, month=first_day.month)
        elif unit == 3:
            periods.append((datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 31), f'{year}年'))
            year -= 1
    return periods[::-1]


def to_timestamp(date: Union[datetime.datetime, str], date_format='%Y-%m-%d %H:%M:%S') -> int:
    """将日期转换为时间戳
    :param date: 日期
    :param date_format: 日期格式，默认 'YYYY-MM-DD HH:mm:ss'
    :return: 时间戳
    """
    if isinstance(date, str) and date_format is not None:
        date = datetime.datetime.strptime(date, date_format)
    return int(date.timestamp() * 1000)


def timedelta_from_now(timedelta: int, timedelta_unit: str) -> int:
    """在当前时间基础上，加减指定的时间长度，并转成时间戳
    :param timedelta: 时间长度，单位为时间单位
    :param timedelta_unit: 时间单位，支持以下时间单位：
      - 'days'：天
      -'seconds'：秒
      -'minutes'：分
      - 'hours'：小时
      -'months'：月
      - 'years'：年
     :return: 时间戳
     """
    now = datetime.datetime.now()
    delta = datetime.timedelta(**{timedelta_unit: timedelta})
    result = now + delta
    ts = int(result.timestamp()) * 1000
    return ts
