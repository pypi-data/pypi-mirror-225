# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-04-22 22:32:34
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Other methods.
"""


from typing import List, Literal, Optional
from os import (
    walk as os_walk,
    listdir as os_listdir
)
from os.path import (
    abspath as os_abspath,
    join as os_join,
    isfile as os_isfile,
    isdir as os_isdir
)


__all__ = (
    "get_paths",
)


def get_paths(path: Optional[str] = None, target: Literal["all", "file", "folder"] = "all", recursion: bool = True) -> List:
    """
    `Get` the path of files and folders in the `path`.

    Parameters
    ----------
    path : When None, then work path.
    target : Target data.
        - `Literal['all']` : Return file and folder path.
        - `Literal['file']` : Return file path.
        - `Literal['folder']` : Return folder path.

    recursion : Is recursion directory.

    Returns
    -------
    String is path.
    """

    # Handle parameter.
    if path is None:
        path = ""
    path = os_abspath(path)

    # Get paths.
    paths = []

    ## Recursive.
    if recursion:
        obj_walk = os_walk(path)
        if target == "all":
            targets_path = [
                os_join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name + folders_name
            ]
            paths.extend(targets_path)
        elif target == "file":
            targets_path = [
                os_join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name
            ]
            paths.extend(targets_path)
        elif target in ("all", "folder"):
            targets_path = [
                os_join(path, folder_name)
                for path, folders_name, files_name in obj_walk
                for folder_name in folders_name
            ]
            paths.extend(targets_path)

    ## Non recursive.
    else:
        names = os_listdir(path)
        if target == "all":
            for name in names:
                target_path = os_join(path, name)
                paths.append(target_path)
        elif target == "file":
            for name in names:
                target_path = os_join(path, name)
                is_file = os_isfile(target_path)
                if is_file:
                    paths.append(target_path)
        elif target == "folder":
            for name in names:
                target_path = os_join(path, name)
                is_dir = os_isdir(target_path)
                if is_dir:
                    paths.append(target_path)

    return paths