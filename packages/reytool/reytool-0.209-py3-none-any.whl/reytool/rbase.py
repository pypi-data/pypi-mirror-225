# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Basic methods.
"""


from typing import Any, List, Tuple, Iterable, Type, Literal, Optional, Union
from types import TracebackType
from sys import exc_info
from traceback import format_exc
from warnings import warn as warnings_warn
from varname import argname


__all__ = (
    "warn",
    "exc",
    "check_target",
    "check_least_one",
    "check_most_one",
    "is_iterable",
    "is_table",
    "is_number_str",
    "get_first_notnull",
    "get_name"
)


def warn(*warn_infos: Any, warn_type: Type[BaseException] = UserWarning, stacklevel: int = 3) -> None:
    """
    Throw `warning`.

    Parameters
    ----------
    warn_info : Warn informations.
    warn_type : Warn type.
    stacklevel : Warning code location, number of recursions up the code level.
    """

    # Handle parameter.
    if warn_infos == ():
        warn_infos = "Warning!"
    elif len(warn_infos) == 1:
        if warn_infos[0].__class__ == str:
            warn_infos = warn_infos[0]
        else:
            warn_infos = str(warn_infos[0])
    else:
        warn_infos = str(warn_infos)

    # Throw warning.
    warnings_warn(warn_infos, warn_type, stacklevel)


def exc(title: Optional[str] = None) -> Tuple[str, Type[BaseException], BaseException, TracebackType]:
    """
    Return exception information and print, must used in `except` syntax.

    Parameters
    ----------
    title : Print title.
        - `None` : Not print.
        - `str` : Print and use this title.

    Returns
    -------
    Exception report text and exception type and exception instance and exception position instance.
    """

    # Get parameter.
    exception_report = format_exc()
    exception_report = exception_report.strip()
    exception_type, exception, traceback = exc_info()

    # Print.
    if title is not None:

        ## Import.
        from .rtext import rprint

        ## Execute.
        rprint(exception_report, title=title, frame="half")

    return exception_report, exception_type, exception, traceback


def check_target(value: Any, *targets: Union[Any, Literal["_iterable"]], check_element: bool = False) -> None:
    """
    Check the content or type of the value, when check fail, then throw `exception`.

    Parameters
    ---------
    value : Check object.
    targets : Correct target, can be type.
        - `Any` : Check whether it is the target.
        - `Literal['_iterable']` : Check whether it can be iterable.

    check_element : Whether check element in value.
    """

    # Handle parameter.
    if check_element:
        values = value
    else:
        values = [value]

    # Check.
    for element in values:

        ## Check sub elements.
        if "_iterable" in targets and is_iterable(element):
            continue

        ## Right target.
        if element.__class__ in targets:
            continue
        for target in targets:
            if element is target:
                continue

        ## Throw exception.
        var_name = get_name(value)
        if var_name is not None:
            var_name = f" '{var_name}'"
        else:
            var_name = ""
        correct_targets_str = ", ".join([repr(target) for target in targets])
        if check_element:
            raise ValueError(f"parameter{var_name} the elements content or type must in [{correct_targets_str}], now: {repr(value)}")
        else:
            raise ValueError(f"parameter{var_name} the content or type must in [{correct_targets_str}], now: {repr(value)}")


def check_least_one(*values: Any) -> None:
    """
    Check that at least one of multiple values is not `None`, when check fail, then throw `exception`.

    Parameters
    ----------
    values : Check values.
    """

    # Check.
    for value in values:
        if value is not None:
            return

    # Throw exception.
    vars_name = get_name(values)
    if vars_name is not None:
        vars_name_de_dup = list(set(vars_name))
        vars_name_de_dup.sort(key=vars_name.index)
        vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
    else:
        vars_name_str = ""
    raise ValueError(f"at least one of parameters{vars_name_str} is not None")


def check_most_one(*values: Any) -> None:
    """
    Check that at most one of multiple values is not `None`, when check fail, then throw `exception`.

    Parameters
    ----------
    values : Check values.
    """

    # Check.
    none_count = 0
    for value in values:
        if value is not None:
            none_count += 1

    # Throw exception.
    if none_count > 1:
        vars_name = get_name(values)
        if vars_name is not None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError(f"at most one of parameters{vars_name_str} is not None")


def is_iterable(obj: Any, exclude_types: Iterable[Type] = [str, bytes]) -> bool:
    """
    Judge whether it is `iterable`.

    Parameters
    ----------
    obj : Judge object.
    exclude_types : Non iterative types.

    Returns
    -------
    Judgment result.
    """

    # Exclude types.
    if obj.__class__ in exclude_types:
        return False

    # Judge.
    try:
        obj_dir = obj.__dir__()
    except TypeError:
        return False
    if "__iter__" in obj_dir:
        return True
    else:
        return False


def is_table(obj: Any, check_fields: bool = True) -> bool:
    """
    Judge whether it is `List[Dict]` table format and keys and keys sort of the Dict are the same.

    Parameters
    ----------
    obj : Judge object.
    check_fields : Do you want to check the keys and keys sort of the Dict are the same.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    if obj.__class__ != list:
        return False
    for element in obj:
        if element.__class__ != dict:
            return False

    ## Check fields of table.
    if check_fields:
        keys_strs = [
            ":".join([str(key) for key in element.keys()])
            for element in obj
        ]
        keys_strs_only = set(keys_strs)
        if len(keys_strs_only) != 1:
            return False

    return True


def is_number_str(string: str) -> bool:
    """
    Judge whether it is `number` string.

    Parameters
    ----------
    string : String.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    try:
        int(string)
    except (ValueError, TypeError):
        return False

    return True


def get_first_notnull(
    *values: Any,
    default: Union[None, Any, Literal["exception"]] = None,
    null_values: List = [None]) -> Any:
    """
    Get the first value that is not `None`.

    Parameters
    ----------
    values : Check values.
    default : When all are null, then return this is value, or throw exception.
        - `Any` : Return this is value.
        - `Literal['exception']` : Throw `exception`.

    null_values : Range of null values.

    Returns
    -------
    Return first not null value, when all are `None`, then return default value.
    """

    # Get value.
    for value in values:
        if value not in null_values:
            return value

    # Throw exception.
    if default == "exception":
        vars_name = get_name(values)
        if vars_name is not None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError(f"at least one of parameters{vars_name_str} is not None")

    return default


def get_name(obj: Any, frame: int = 2) -> Optional[Union[str, Tuple[str, ...]]]:
    """
    Get object `name`.

    Parameters
    ----------
    obj : Object.
    frame : Number of code to upper level.

    Returns
    -------
    Object name or None.
    """

    # Get name using built in method.
    try:
        name = obj.__name__
    except AttributeError:

        # Get name using module method.
        name = "obj"
        try:
            for _frame in range(1, frame + 1):
                name = argname(name, frame=_frame)
            if name.__class__ != str:
                if "".join(name) == "":
                    name = None
        except:
            name = None

    return name