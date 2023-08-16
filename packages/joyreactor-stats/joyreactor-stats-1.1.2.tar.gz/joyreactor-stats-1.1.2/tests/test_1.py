import pytest
from urllib import request
from time import sleep
import re
from datetime import datetime, timedelta

from joyreactor_stats import JoyreactorStats


def test_defaults():
    joy_stats = JoyreactorStats('acc')

    assert joy_stats.account == 'acc'
    assert joy_stats.show_progress is True
    assert joy_stats.open_xls is True
    assert joy_stats.quiet is False


def test_init_params():
    joy_stats = JoyreactorStats(
        account = 'test_acc',
        open_xls = False,
        show_progress = False,
        quiet = True
        )

    assert joy_stats.account == 'test_acc'
    assert joy_stats.show_progress is False
    assert joy_stats.open_xls is False
    assert joy_stats.quiet is True


def test_get_len_date_str():
    start_date = datetime.strptime('10:00', '%H:%M')
    end_date = datetime.strptime('11:13:25', '%H:%M:%S')
    date_diff = end_date - start_date

    assert JoyreactorStats._get_len_date_str(date_diff) == '1 ч. 13 м. 25 сек.'

    end_date = datetime.strptime('23:00', '%H:%M')
    date_diff = end_date - start_date

    assert JoyreactorStats._get_len_date_str(date_diff) == '13 ч.'

    end_date = datetime.strptime('10:03', '%H:%M')
    date_diff = end_date - start_date

    assert JoyreactorStats._get_len_date_str(date_diff) == ' 3 м.'

    end_date = datetime.strptime('10:03:05', '%H:%M:%S')
    date_diff = end_date - start_date

    assert JoyreactorStats._get_len_date_str(date_diff) == ' 3 м. 5 сек.'

    end_date = datetime.strptime('13:00:16', '%H:%M:%S')
    date_diff = end_date - start_date

    assert JoyreactorStats._get_len_date_str(date_diff) == '3 ч. 16 сек.'

    end_date = datetime.strptime('10:00:52', '%H:%M:%S')
    date_diff = end_date - start_date

    assert JoyreactorStats._get_len_date_str(date_diff) == ' 52 сек.'
