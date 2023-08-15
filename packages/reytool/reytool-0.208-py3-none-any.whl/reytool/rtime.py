# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:11:50
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Time methods.
"""


from typing import Any, List, Dict, Literal, Optional, Union, overload, NoReturn
from pandas import DataFrame, concat as pd_concat
from time import time as time_time, sleep as time_sleep
from datetime import (
    datetime as datetime_datetime,
    date as datetime_date,
    time as datetime_time,
    timedelta as datetime_timedelta
)

from .rbase import check_target, is_number_str
from .rnumber import randn
from .rtext import rprint


__all__ = (
    "now",
    "time2str",
    "str2time",
    "sleep",
    "RTimeMark"
)


@overload
def now(format: Literal["datetime"] = "datetime_str") -> datetime_datetime: ...

@overload
def now(format: Literal["date"] = "datetime_str") -> datetime_date: ...

@overload
def now(format: Literal["time"] = "datetime_str") -> datetime_time: ...

@overload
def now(format: Literal["datetime_str", "date_str", "time_str"] = "datetime_str") -> str: ...

@overload
def now(format: Literal["timestamp"] = "datetime_str") -> int: ...

def now(
    format: Literal["datetime", "date", "time", "datetime_str", "date_str", "time_str", "timestamp"] = "datetime_str"
) -> Union[datetime_datetime, datetime_date, datetime_time, str, int]:
    """
    Get `current` time string or intger or object.

    Parameters
    ----------
    format : Format type.
        - `Literal['datetime']` : Return datetime object of datetime package.
        - `Literal['date']` : Return date object of datetime package.
        - `Literal['time']` : Return time object of datetime package.
        - `Literal['datetime_str']` : Return string in format `%Y-%m-%d %H:%M:%S`.
        - `Literal['date_str']` : Return string in format `%Y-%m-%d`.
        - `Literal['time_str']` : Return string in foramt `%H:%M:%S`.
        - `Literal['timestamp']` : Return time stamp in milliseconds.

    Returns
    -------
    Time string or object of datetime package.
    """

    # Return time object by parameter format.
    if format == "datetime":
        return datetime_datetime.now()
    elif format == "date":
        return datetime_datetime.now().date()
    elif format == "time":
        return datetime_datetime.now().time()
    elif format == "datetime_str":
        return datetime_datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif format == "date_str":
        return datetime_datetime.now().strftime("%Y-%m-%d")
    elif format == "time_str":
        return datetime_datetime.now().strftime("%H:%M:%S")
    elif format == "timestamp":
        return int(time_time() * 1000)


@overload
def time2str(
    object_: Union[datetime_datetime, datetime_date, datetime_time, datetime_timedelta, int],
    format: Optional[str] = None,
    throw_e: bool = False
) -> str: ...

@overload
def time2str(
    object_: Any,
    format: Optional[str] = None,
    throw_e: Literal[False] = False
) -> Any: ...

@overload
def time2str(
    object_: Any,
    format: Optional[str] = None,
    throw_e: Literal[True] = False
) -> NoReturn: ...

def time2str(
    object_: Union[datetime_datetime, datetime_date, datetime_time, datetime_timedelta, int, Any],
    format: Optional[str] = None,
    throw_e: bool = False
) -> Union[str, Any]:
    """
    Format time object of package `datetime` to string.

    Parameters
    ----------
    object_ : Object of `datetime` package or int.
    format : Format string.
        - `None` : Automatic by type.
            * Parameter `object_` is datetime_datetime : Is `%Y-%m-%d %H:%M:%S`.
            * Parameter `object_` is datetime_date : Is `%Y-%m-%d`.
            * Parameter `object_` is datetime_time : Is `%H:%M:%S`.
            * Parameter `object_` is datetime_timedelta : Is f`{days} %H:%M:%S`.
            * Parameter `object_` is time stamp : Is `%Y-%m-%d %H:%M:%S`.
        - `str` : Format by this value.

    throw_e : Whether throw exception, when parameter `object_` value error, otherwise return original value.

    Returns
    -------
    String after foramt or original value.
    """

    # Check parameter.
    if throw_e:
        check_target(object_, datetime_datetime, datetime_date, datetime_time, datetime_timedelta, int)

    # Convert to time string.

    ## From datetime object.
    if object_.__class__ == datetime_datetime:
        if format is None:
            string = str(object_)[:19]
        else:
            string = object_.strftime(format)

    ## From date object.
    elif object_.__class__ == datetime_date:
        if format is None:
            string = str(object_)[:10]
        else:
            string = object_.strftime(format)

    ## From time object.
    elif object_.__class__ == datetime_time:
        if format is None:
            string = str(object_)[:8]
        else:
            string = object_.strftime(format)

    ## From timedelta object.
    elif object_.__class__ == datetime_timedelta:
        if format is None:
            string = str(object_)
            if "day" in string:
                day, char, string = string.split(" ")
            else:
                day = "0"
            if string[1] == ":":
                string = "0" + string
            string = f"{day} {string[:8]}"
        else:
            seconds = object_.microseconds / 1000_000
            datetime_obj = datetime_datetime.fromtimestamp(seconds)
            string = datetime_obj.strftime(format)

    ## From int object.
    elif object_.__class__ == int:
        int_len = len(str(object_))
        if int_len > 10:
            divisor = 10 ** (int_len - 10)
            seconds = object_ / divisor
        else:
            seconds = object_
        datetime_obj = datetime_datetime.fromtimestamp(seconds)
        if format is None:
            format = "%Y-%m-%d %H:%M:%S"
        string = datetime_obj.strftime(format)

    ## From other object.
    else:
        return object_

    return string


@overload
def str2time(
    string: str,
    type_: None = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> Union[datetime_datetime, datetime_date, datetime_time, datetime_timedelta, int]: ...

@overload
def str2time(
    string: str,
    type_: Literal["datetime"] = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> datetime_datetime: ...

@overload
def str2time(
    string: str,
    type_: Literal["date"] = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> datetime_date: ...

@overload
def str2time(
    string: str,
    type_: Literal["time"] = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> datetime_time: ...

@overload
def str2time(
    string: str,
    type_: Literal["timedelta"] = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> datetime_timedelta: ...

@overload
def str2time(
    string: str,
    type_: Literal["timestamp"] = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> int: ...

@overload
def str2time(
    string: Any,
    type_: Optional[Literal["datetime", "date", "time", "timedelta", "timestamp"]] = None,
    format: Optional[str] = None,
    throw_e: Literal[False] = False
) -> Any: ...

@overload
def str2time(
    string: Any,
    type_: Optional[Literal["datetime", "date", "time", "timedelta", "timestamp"]] = None,
    format: Optional[str] = None,
    throw_e: Literal[True] = False
) -> NoReturn: ...

def str2time(
    string: Union[str, Any],
    type_: Optional[Literal["datetime", "date", "time", "timedelta", "timestamp"]] = None,
    format: Optional[str] = None,
    throw_e: bool = False
) -> Union[datetime_datetime, datetime_date, datetime_time, datetime_timedelta, int, Any]:
    """
    Format string to time object of package `datetime`.

    Parameters
    ----------
    string : Time string.
    type_ : Format type.
        - `None` : Automatic judgment.
        - `Literal['datetime']` : Return datetime object of package datetime.
        - `Literal['date']` : Return date object of package datetime.
        - `Literal['time']` : Return time object of package datetime.
        - `Literal['timedelta']` : Return timedelta object of package datetime.
        - `Literal['timestamp']` : Return time stamp in milliseconds.

    format : Format string.
        - `None` : Default format method.
            * Parameter `type_` is `datetime` : Is `%Y-%m-%d %H:%M:%S`.
            * Parameter `type_` is `date` : Is `%Y-%m-%d`.
            * Parameter `type_` is `time` : Is `%H:%M:%S`.
            * Parameter `type_` is `timedelta` : Is `days %H:%M:%S`.
            * Parameter `type_` is `timestamp` : Is `%Y-%m-%d %H:%M:%S`.
            * Parameter `type_` is `None` : automatic judgment.
        - `str` : Format by this value.

    throw_e : Whether throw exception, when parameter `time_obj` value error, otherwise return original value.

    Returns
    -------
    Time object of datetime package or time stamp or original value.
    """

    # Check parameter.
    if string.__class__ != str:
        return string

    # Get time format by automatic judgment.
    if type_ is None:
        str_len = len(string)
        if "年" == string[4:5]:
            if str_len > 11:
                format = "%Y年%m月%d日 %H时%M分%S秒"
                type_ = "datetime"
            else:
                format = "%Y年%m月%d日"
                type_ = "date"
        elif "时" in string[1:3]:
            format = "%H时%M分%S秒"
            type_ = "time"
        elif " " in string and "-" not in string:
            format = "%H:%M:%S"
            type_ = "timedelta"
        elif str_len == 19:
            format = "%Y-%m-%d %H:%M:%S"
            type_ = "datetime"
        elif str_len == 14:
            format = "%Y%m%d%H%M%S"
            type_ = "datetime"
        elif str_len == 10:
            format = "%Y-%m-%d"
            type_ = "date"
        elif str_len == 8:
            if string[2] == ":":
                format = "%H:%M:%S"
                type_ = "time"
            else:
                format = "%Y%m%d"
                type_ = "date"
        elif str_len == 6:
            format = "%H%M%S"
            type_ = "time"
        elif str_len == 4:
            format = "%Y"
            type_ = "date"
        else:
            return string

    # Get time format by parameter `type_`.
    else:
        if format is None:
            format_dir = {
                "datetime": "%Y-%m-%d %H:%M:%S",
                "date": "%Y-%m-%d",
                "time": "%H:%M:%S",
                "timestamp": "%Y-%m-%d %H:%M:%S",
                "timedelta": "%H:%M:%S"
            }
            format = format_dir[type_]

    # Additional processing timedelta type.
    if type_ == "timedelta":
        if " " in string:
            strings = string.split(" ")
            day_str, string = strings[0], strings[-1]
        else:
            day = "0"
        try:
            day = int(day_str)
        except ValueError:
            if throw_e:
                raise ValueError("failed to format string as time object")
            return string

    # Convert to time type.
    try:
        time_obj = datetime_datetime.strptime(string, format)
    except ValueError:
        if throw_e:
            raise ValueError("failed to format string as time object")
        return string
    if type_ == "date":
        time_obj = time_obj.date()
    elif type_ == "time":
        time_obj = time_obj.time()
    elif type_ == "timestamp":
        time_obj = int(time_obj.timestamp() * 1000)
    elif type_ == "timedelta":
        second = time_obj.second
        second += day * 86400
        time_obj = datetime_timedelta(seconds=second)

    return time_obj


def sleep(*thresholds: float, precision: Optional[int] = None) -> float:
    """
    `Sleep` random seconds.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When `length is 0`, then low and high thresholds is `0` and `10`.
        - When `length is 1`, then sleep this value.
        - When `length is 2`, then low and high thresholds is `thresholds[0]` and `thresholds[1]`.
    
    precision : Precision of random range, that is maximum decimal digits of sleep seconds.
        - `None` : Set to Maximum decimal digits of element of parameter `thresholds`.
        - `int` : Set to this value.
    
    Returns
    -------
    Random seconds.
        - When parameters `precision` is `0`, then return int.
        - When parameters `precision` is `greater than 0`, then return float.
    """

    # Handle parameter.
    if len(thresholds) == 1:
        second = float(thresholds[0])
    else:
        second = randn(*thresholds, precision=precision)

    # Sleep.
    time_sleep(second)

    return second


class RTimeMark():
    """
    Rey`s `time mark` type.
    """


    def __init__(self) -> None:
        """
        Build `time mark` instance.
        """

        # Record table.
        self.record: List[Dict[
            Literal["index", "timestamp", "datetime", "datetime_str", "interval_timestamp", "interval_timedelta", "interval_timedelta_str"],
            Any
        ]] = []


    def mark(self, note: Optional[str] = None) -> None:
        """
        `Mark` now time.

        Parameters
        ----------
        note : Mark note.
        """

        # Get parametes.
        record_len = len(self.record)
        mark_info = {
            "index": record_len,
            "timestamp": now("timestamp"),
            "datetime": now("datetime"),
            "datetime_str": now()
        }

        # Mark.

        ## First.
        if record_len == 0:
            mark_info["interval_timestamp"] = None
            mark_info["interval_timedelta"] = None
            mark_info["interval_timedelta_str"] = None

        ## Non first.
        else:
            last_datetime = self.record[-1]["datetime"]
            last_timestamp = self.record[-1]["timestamp"]
            mark_info["interval_timestamp"] = mark_info["timestamp"] - last_timestamp
            mark_info["interval_timedelta"] = mark_info["datetime"] - last_datetime
            mark_info["interval_timedelta_str"] = time2str(mark_info["interval_timedelta"])

        mark_info["note"] = note
        self.record.append(mark_info)


    def report(self, title: Optional[str] = None) -> DataFrame:
        """
        `Print` and `return` time mark information.

        Parameters
        ----------
        title : Print title.
            - `None` : Not print.
            - `str` : Print and use this title.

        Returns
        -------
        DataFrame object of pandas package with time mark information.
        """

        # Get parameter.
        data = [
            {
                "timestamp": row["timestamp"],
                "datetime": row["datetime_str"],
                "interval": row["interval_timedelta_str"],
                "note": row["note"]
            }
            for row in self.record
        ]

        # Generate report.
        report_df = DataFrame(data, dtype=str)
        interval_timedelta = self.record[-1]["datetime"] - self.record[0]["datetime"]
        interval = time2str(interval_timedelta)
        sum_df = DataFrame({"interval": interval}, index = ["sum"])
        report_df = pd_concat([report_df, sum_df])
        report_df.fillna("-", inplace=True)

        # Print.
        if title is not None:
            rprint(report_df, title=title)

        return report_df