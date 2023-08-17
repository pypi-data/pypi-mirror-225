"""
This module contains useful developer tools that are packaged as functions.

Functions:
- date_today()
"""
from typing import Optional, Union
from datetime import datetime


def date_today(fmt='full_date') -> str:
    """
    Returns today's date in string format.
    <fmt> is an optional parameter that takes either of two valid str inputs:
        1. 'curr_date'
        2. 'curr_time'

    If <fmt> is left blank, then return both current date AND time.

    >>> print(date_today())
    ----------------
    Date: 2023-08-10
    Time: 23:35:06
    ----------------
    >>> print(date_today('curr_date'))
    2023-08-10
    >>> print(date_today('curr_time'))
    23:35:06
    >>> print(date_today('dat_boi_aint_right'))
    🚩----------------------------DEVTOOLS ERROR-----------------------------🚩
         <fmt> must be assigned 'curr_date', 'curr_time', or leave blank.
    🚩-----------------------------------------------------------------------🚩
    """
    now = datetime.now()
    if fmt == 'full_date':
        return now.strftime('\n\
----------------\n\
Date: %Y-%m-%d\n\
Time: %H:%M:%S\n\
----------------\n'
        )
    elif fmt == 'curr_date':
        return now.strftime('%Y-%m-%d')
    elif fmt == 'curr_time':
        return now.strftime('%H:%M:%S')
    else:
        return '\
🚩----------------------------DEVTOOLS ERROR-----------------------------🚩\n\
     <fmt> must be assigned \'curr_date\', \'curr_time\', or leave blank.\n\
🚩-----------------------------------------------------------------------🚩'


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(date_today(f'invalid_arg1'))
