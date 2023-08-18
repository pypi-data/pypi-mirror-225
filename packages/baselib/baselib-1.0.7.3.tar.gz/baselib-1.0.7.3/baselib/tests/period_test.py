# -*- coding:utf-8 -*-
from baselib.time import Period
from datetime import datetime, timedelta


def test_get_recent_hour():
    """  测试获取近N个小时
    """
    # 测试点1：验证 小时的起止时间
    for i in [1, 2, 5, 10, 24, 25]:
        start_time, end_time = Period.get_recent_hour(i)
        now = datetime.now()
        del_time = end_time - start_time
        assert del_time.total_seconds() - 3600 * i < 0.1
    # print(end_time, now)
    del_time = now - end_time
    # print(del_time)
    assert del_time.total_seconds() < 1

    # 测试点2：验证截止统计时间
    start_time, end_time = Period.get_recent_hour(1, 10)
    now = datetime.now()
    del_time = end_time - start_time
    assert abs(del_time.total_seconds() - 3600) < 0.1
    del_time = now - end_time
    # print(now, end_time, del_time)
    assert abs(del_time.total_seconds() - 600) < 1


def test_get_recent_day():
    start_time, end_time = Period.get_recent_day(1)
    now = datetime.now()
    del_time = end_time - start_time

    assert abs(del_time.total_seconds() - 3600 * 24) < 0.1
    del_time = end_time - now
    # print(del_time.total_seconds())
    assert abs(del_time.total_seconds()) < 1
    # print(start_time, end_time)


def test_get_day_begin_end():
    start_time = Period.get_day_begin()
    end_time = Period.get_day_end()
    now = Period.now()
    assert start_time.day == now.day and \
        start_time.month == now.month and \
        start_time.year == now.year and \
        start_time.hour == 0 and \
        start_time.minute == 0 and \
        start_time.second == 0
    assert end_time.day == now.day and \
        end_time.month == now.month and \
        end_time.year == now.year and \
        end_time.hour == 23 and \
        end_time.minute == 59 and \
        end_time.second == 59

    yestorday, _ = Period.get_recent_day(1)
    start_time = Period.get_day_begin(yestorday)
    end_time = Period.get_day_end(yestorday)
    assert start_time.day == yestorday.day and \
        start_time.month == yestorday.month and \
        start_time.year == yestorday.year and \
        start_time.hour == 0 and \
        start_time.minute == 0 and \
        start_time.second == 0
    assert end_time.day == yestorday.day and \
        end_time.month == yestorday.month and \
        end_time.year == yestorday.year and \
        end_time.hour == 23 and \
        end_time.minute == 59 and \
        end_time.second == 59


def test_format_datetime():
    now = Period.get_day_end()
    assert Period.format_datetime(now) == now.strftime("%Y-%m-%d %H:%M:%S")
    assert Period.format_t_datetime(now) == now.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert Period.format_time(now) == now.strftime("%H:%M:%S")
    assert Period.format_date(now) == now.strftime("%Y-%m-%d")
