# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-05-09 15:30:10
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : File methods.
"""


from typing import Any, Union, Literal, Optional, overload
from json import dumps as json_dumps, JSONDecodeError

from .rbase import check_target


__all__ = (
    "read_file",
    "write_file"
)


@overload
def read_file(path: str, type_: Literal["bytes"] = "bytes") -> bytes: ...

@overload
def read_file(path: str, type_: Literal["str"] = "bytes") -> str: ...

def read_file(path: str, type_: Literal["str", "bytes"] = "bytes") -> Union[bytes, str]:
    """
    `Read` file data.

    Parameters
    ----------
    path : Read file path.
    type_ : File data type.
        - `Literal['bytes']` : Return file bytes data.
        - `Literal['str']` : Return file string data.

    Returns
    -------
    File bytes data or string data.
    """

    # Handle parameter.
    if type_ == "bytes":
        mode = "rb"
    elif type_ == "str":
        mode = "r"

    # Read.
    with open(path, mode) as file:
        content = file.read()

    return content


def write_file(path: str, data: Optional[Any] = "", append: bool = False) -> None:
    """
    `Write` file data.

    Parameters
    ----------
    path : Write File path. When path not exist, then cerate file.
    data : Write data.
        - `bytes` : File bytes data.
        - `str` : File text.
        - `Any` : Try.

    append : Whether append data, otherwise overwrite data.
    """

    # Handle parameter.

    ## Write mode.
    if append:
        mode = "a"
    else:
        mode = "w"
    if data.__class__ == bytes:
        mode += "b"

    ## Convert data to string.
    if data.__class__ not in (str, bytes):
        try:
            data = json_dumps(data, ensure_ascii=False)
        except (JSONDecodeError, TypeError):
            data = str(data)

    # Write.
    with open(path, mode) as file:
        file.write(data)