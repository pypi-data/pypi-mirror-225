# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from __future__ import annotations
from typing import Any, List, Tuple, Dict, Iterable, Optional, Literal, Union, ClassVar, NoReturn, overload
from re import findall
from sqlalchemy import create_engine as sqlalchemy_create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.exc import OperationalError
from pandas import DataFrame

from .rbase import get_first_notnull
from .rdata import objs_in
from .rmonkey import sqlalchemy_add_result_more_fetch, sqlalchemy_support_row_index_by_field
from .roption import ROption
from .rregular import search
from .rtable import Table, to_table
from .rtext import rprint
from .rwrap import runtime, retry


__all__ = (
    "RResult",
    "REngine",
    "RConnection",
    "RStatus",
    "RVariables",
    "RExecute"
)


# Add more fetch methods to CursorResult object.
RResult = sqlalchemy_add_result_more_fetch()

# Support Row object of package sqlalchemy index by field name.
sqlalchemy_support_row_index_by_field()


class REngine(object):
    """
    Rey's `database engine` type.
    """

    # Values to be converted to "NULL".
    null_values: ClassVar[List] = ["", " ", b"", [], (), {}, set()]


    @overload
    def __init__(
        self,
        host: None = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: None = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: None = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: None = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: Optional[Union[str, URL]] = None,
        engine: Optional[Union[Engine, Connection]] = None,
        **query: str
    ) -> None: ...

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: Optional[Union[str, URL]] = None,
        engine: Optional[Union[Engine, Connection]] = None,
        **query: str
    ) -> None:
        """
        Build `database engine` instance.

        Parameters
        ----------
        host : Server host.
        port : Server port.
        username : Server user name.
        password : Server password.
        database : Database name in the server.
        drivername : Database backend and driver name.
            - `None` : Auto select and try.
            - `str` : Use this value.

        pool_size : Number of connections `keep open`.
        max_overflow : Number of connections `allowed overflow`.
        pool_timeout : Number of seconds `wait create` connection.
        pool_recycle : Number of seconds `recycle` connection.
            - `None` : Use database variable `wait_timeout` value.
            - `Literal[-1]` : No recycle.
            - `int` : Use this value.

        url: Get parameters from server `URL`, but preferred input parameters.
            Parameters include `username`, `password`, `host`, `port`, `database`, `drivername`, `query`.
        engine : Use existing `Engine` or `Connection` object, and get parameters from it.
            Parameters include `username`, `password`, `host`, `port`, `database`, `drivername`, `query`,
            `pool_size`, `max_overflow`, `pool_timeout`, `pool_recycle`.
        query : Server parameters.
        """

        # From existing Engine or Connection object.
        if engine is not None:

            ## Extract Engine object from Connection boject.
            if engine.__class__ == Connection:
                engine = engine.engine

            ## Extract parameter.
            params = self.extract_from_engine(engine)

            ## Set.
            self.drivername = params["drivername"]
            self.username = params["username"]
            self.password = params["password"]
            self.host = params["host"]
            self.port = params["port"]
            self.database = params["database"]
            self.query = params["query"]
            self.pool_size = params["pool_size"]
            self.max_overflow = params["max_overflow"]
            self.pool_timeout = params["pool_timeout"]
            self.pool_recycle = params["pool_recycle"]
            self.engine = engine

        # From parameters create.
        else:

            ## Extract parameters from URL.
            if url is not None:
                params = self.extract_from_url(url)
            else:
                params = dict.fromkeys(
                    (
                        "drivername",
                        "username",
                        "password",
                        "host",
                        "port",
                        "database",
                        "query"
                    )
                )

            ## Set parameters by priority.
            self.drivername = get_first_notnull(drivername, params["drivername"])
            self.username = get_first_notnull(username, params["username"], default="exception")
            self.password = get_first_notnull(password, params["password"], default="exception")
            self.host = get_first_notnull(host, params["host"], default="exception")
            self.port = get_first_notnull(port, params["port"], default="exception")
            self.database = get_first_notnull(database, params["database"])
            self.query = get_first_notnull(query, params["query"], default={"charset": "utf8"}, null_values=[None, {}])
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.pool_timeout = pool_timeout

            ## Create Engine object.
            if pool_recycle is None:
                self.pool_recycle = -1
                self.engine = self.create_engine()
                wait_timeout = int(self.variables["wait_timeout"])
                self.pool_recycle = wait_timeout
                self.engine.pool._recycle = wait_timeout
            else:
                self.pool_recycle = pool_recycle
                self.engine = self.create_engine()


    def extract_from_url(self, url: Union[str, URL]) -> Dict[
        Literal["drivername", "username", "password", "host", "port", "database", "query"],
        Any
    ]:
        """
        Extract parameters from `URL` of string.

        Parameters
        ----------
        url : URL of string.

        Returns
        -------
        Extracted parameters.
        """

        # Extract.

        ## When str object.
        if url.__class__ == str:
            pattern = "^([\w\+]+)://(\w+):(\w+)@(\d+\.\d+\.\d+\.\d+):(\d+)[/]?([\w/]+)?[\?]?([\w&=]+)?$"
            result = search(pattern, url)
            if result is None:
                raise ValueError("the value of parameter 'url' is incorrect")
            (
                drivername,
                username,
                password,
                host,
                port,
                database,
                query_str
            ) = result
            if query_str is not None:
                pattern = "(\w+)=(\w+)"
                query_findall = findall(pattern, query_str)
                query = {key: value for key, value in query_findall}
            else:
                query = {}

        ## When URL object.
        elif url.__class__ == URL:
            drivername = url.drivername
            username = url.username
            password = url.password
            host = url.host
            port = url.port
            database = url.database
            query = dict(url.query)

        # Generate parameter.
        params = {
            "drivername": drivername,
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "query": query
        }

        return params


    def extract_from_engine(self, engine: Union[Engine, Connection]) -> Dict[
        Literal[
            "drivername", "username", "password", "host", "port", "database", "query",
            "pool_size", "max_overflow", "pool_timeout", "pool_recycle"
        ],
        Any
    ]:
        """
        Extract parameters from `Engine` or `Connection` object.

        Parameters
        ----------
        engine : Engine or Connection object.

        Returns
        -------
        Extracted parameters.
        """

        ## Extract Engine object from Connection boject.
        if engine.__class__ == Connection:
            engine = engine.engine

        ## Extract.
        drivername = engine.url.drivername
        username = engine.url.username
        password = engine.url.password
        host = engine.url.host
        port = engine.url.port
        database = engine.url.database
        query = dict(engine.url.query)
        pool_size = engine.pool._pool.maxsize
        max_overflow = engine.pool._max_overflow
        pool_timeout = engine.pool._timeout
        pool_recycle = engine.pool._recycle

        # Generate parameter.
        params = {
            "drivername": drivername,
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "query": query,
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_timeout": pool_timeout,
            "pool_recycle": pool_recycle
        }

        return params


    @property
    def url(self) -> str:
        """
        Generate server `URL`.

        Returns
        -------
        Server URL.
        """

        # Generate URL.
        _url = f"{self.drivername}://{self.username}:{self.password}@{self.host}:{self.port}"

        # Add database path.
        if self.database is not None:
            _url = f"{_url}/{self.database}"

        # Add Server parameter.
        if self.query != {}:
            query = "&".join(
                [
                    f"{key}={value}"
                    for key, value in self.query.items()
                ]
            )
            _url = f"{_url}?{query}"

        return _url


    def create_engine(self, **kwargs) -> Engine:
        """
        Create database `Engine` object.

        Parameters
        ----------
        kwargs : Keyword parameters of create engine method.

        Returns
        -------
        Engine object.
        """

        # Handle parameter.
        if self.drivername is None:
            drivernames = ("mysql+mysqldb", "mysql+pymysql")
        else:
            drivernames = (self.drivername,)

        # Create Engine object.
        for drivername in drivernames:

            ## Set engine parameter.
            self.drivername = drivername
            engine_params = {
                "url": self.url,
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
                **kwargs
            }

            ## Try create.
            try:
                engine = sqlalchemy_create_engine(**engine_params)
            except ModuleNotFoundError:
                pass
            else:
                return engine

        # Throw exception.
        drivernames_str = " and ".join(
            [
                dirvername.split("+", 1)[-1]
                for dirvername in drivernames
            ]
        )
        raise ModuleNotFoundError(f"module {drivernames_str} not fund")


    @property
    def count(self) -> Tuple[int, int]:
        """
        Count number of `keep open` and `allowed overflow` connection.

        Returns
        -------
        Number of keep open and allowed overflow connection.
        """

        # Count.
        _overflow = self.engine.pool._overflow
        if _overflow < 0:
            keep_n = self.pool_size + _overflow
            overflow_n = 0
        else:
            keep_n = self.pool_size
            overflow_n = _overflow

        return keep_n, overflow_n


    def fill_data(
        self,
        data: Table,
        sql: Union[str, TextClause],
    ) -> List[Dict]:
        """
        `Fill` missing data according to contents of `TextClause` object of package `sqlalchemy`, and filter out empty Dict.

        Parameters
        ----------
        data : Data set for filling.
        sql : SQL in method sqlalchemy.text format, or TextClause object.

        Returns
        -------
        Filled data.
        """

        # Handle parameter.
        if data.__class__ == dict:
            data = [data]
        elif data.__class__ != list:
            data = to_table(data)
        if sql.__class__ == TextClause:
            sql = sql.text

        # Extract fill field names.
        pattern = "(?<!\\\):(\w+)"
        sql_keys = findall(pattern, sql)

        # Fill data.
        for row in data:

            # Filter empty Dict.
            if row == {}:
                continue

            # Fill.
            for key in sql_keys:
                value = row.get(key)
                if (
                    value is None
                    or value in self.null_values
                ):
                    row[key] = None

        return data


    def get_syntax(self, sql: Union[str, TextClause]) -> List[str]:
        """
        Extract `SQL syntax` type for each segment form SQL.

        Parameters
        ----------
        sql : SQL text or TextClause object.

        Returns
        -------
        SQL syntax type for each segment.
        """

        # Handle parameter.
        if sql.__class__ == TextClause:
            sql = sql.text

        # Extract.
        syntax = [
            search("[a-zA-Z]+", sql_part).upper()
            for sql_part in sql.split(";")
        ]

        return syntax


    def is_multi_sql(self, sql: Union[str, TextClause]) -> bool:
        """
        Judge whether it is `multi segment SQL`.

        Parameters
        ----------
        sql : SQL text or TextClause object.

        Returns
        -------
        Judgment result.
        """

        # Handle parameter.
        if sql.__class__ == TextClause:
            sql = sql.text

        # Judge.
        if ";" in sql.rstrip()[:-1]:
            return True
        return False


    def executor(
        self,
        connection: Connection,
        sql: TextClause,
        data: List[Dict],
        report: bool
    ) -> RResult:
        """
        `SQL` executor.

        Parameters
        ----------
        connection : Connection object.
        sql : TextClause object.
        data : Data set for filling.
        report : Whether report SQL execute information.

        Returns
        -------
        Result object.
        """

        # Create Transaction object.
        with connection.begin():

            # Execute.

            ## Report.
            if report:
                result, report_runtime = runtime(connection.execute, sql, data, _return_report=True)
                report_info = (
                    f"{report_runtime}\n"
                    f"Row Count: {result.rowcount}"
                )
                sqls = [
                    sql_part.strip()
                    for sql_part in sql.text.split(";")
                ]
                if data == []:
                    rprint(report_info, *sqls, title="SQL")
                else:
                    rprint(report_info, *sqls, data, title="SQL")

            ## Not report.
            else:
                result = connection.execute(sql, data)

        return result


    def execute(
        self,
        sql: Union[str, TextClause],
        data: Optional[Table] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        Execute `SQL`.

        Parameters
        ----------
        sql : SQL in method `sqlalchemy.text` format, or `TextClause` object.
        data : Data set for filling.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameters by priority.
        report = get_first_notnull(report, ROption.report_execute_info)

        # Handle parameter.
        if sql.__class__ == str:
            sql = text(sql)
        if data is None:
            if kwdata == {}:
                data = []
            else:
                data = [kwdata]
        else:
            if data.__class__ == dict:
                data = [data]
            elif isinstance(data, CursorResult):
                data = to_table(data)
            elif data.__class__ == DataFrame:
                data = to_table(data)
            else:
                data = data.copy()
            for param in data:
                param.update(kwdata)

        # Fill missing data.
        data = self.fill_data(data, sql)

        # Execute.

        ## Create Connection object.
        with self.engine.connect() as connection:

            ## Can retry.
            if not self.is_multi_sql(sql):
                result = retry(
                    self.executor,
                    connection,
                    sql,
                    data,
                    report,
                    _report="Database execute operational error",
                    _exception=OperationalError
                )

            ## Cannot retry.
            else:
                result = self.executor(connection, sql, data, report)

        return result


    def execute_select(
            self,
            table: str,
            database: Optional[str] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            where: Optional[str] = None,
            group: Optional[str] = None,
            having: Optional[str] = None,
            order: Optional[str] = None,
            limit: Optional[Union[int, str, List, Tuple]] = None,
            report: bool = None,
            **kwdata: Any
        ) -> RResult:
        """
        Execute `select` SQL.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        fields : Select clause content.
            - `None` : Is `SELECT *`.
            - `str` : Join as `SELECT str`.
            - `Iterable[str]` : Join as `SELECT \`str\`, ...`.
                * `str and first character is ':'` : Use this syntax.
                * `str` : Use this field.

        where : Clause `WHERE` content, join as `WHERE str`.
        group : Clause `GROUP BY` content, join as `GROUP BY str`.
        having : Clause `HAVING` content, join as `HAVING str`.
        order : Clause `ORDER BY` content, join as `ORDER BY str`.
        limit : Clause `LIMIT` content.
            - `Union[int, str]` : Join as `LIMIT int/str`.
            - `Union[List, Tuple]` with length of 1 or 2 `int/str` : Join as `LIMIT int/str [, int/str]`.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `fields`.
        >>> fields = ['id', ':`id` + 1 AS `id_`']
        >>> result = REngine.execute_select('table', 'database', fields)
        >>> print(result.fetch_table())
        [{'id': 1, 'id_': 2}, ...]

        Parameter `kwdata`.
        >>> fields = '`id`, `id` + :value AS `id_`'
        >>> result = REngine.execute_select('table', 'database', fields, value=1)
        >>> print(result.fetch_table())
        [{'id': 1, 'id_': 2}, ...]
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Generate SQL.
        sql_list = []

        ## Part "SELECT" syntax.
        if fields is None:
            fields = "*"
        elif fields.__class__ != str:
            fields = ", ".join(
                [
                    field[1:]
                    if (
                        field[:1] == ":"
                        and field != ":"
                    )
                    else f"`{field}`"
                    for field in fields
                ]
            )
        sql_select = f"SELECT {fields}"
        sql_list.append(sql_select)

        ## Part "FROM" syntax.
        sql_from = f"FROM `{database}`.`{table}`"
        sql_list.append(sql_from)

        ## Part "WHERE" syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sql_list.append(sql_where)

        ## Part "GROUP BY" syntax.
        if group is not None:
            sql_group = f"GROUP BY {group}"
            sql_list.append(sql_group)

        ## Part "GROUP BY" syntax.
        if having is not None:
            sql_having = f"HAVING {having}"
            sql_list.append(sql_having)

        ## Part "ORDER BY" syntax.
        if order is not None:
            sql_order = f"ORDER BY {order}"
            sql_list.append(sql_order)

        ## Part "LIMIT" syntax.
        if limit is not None:
            if limit.__class__ in (str, int):
                sql_limit = f"LIMIT {limit}"
            else:
                if len(limit) in (1, 2):
                    limit_content = ", ".join([str(value) for value in limit])
                    sql_limit = f"LIMIT {limit_content}"
                else:
                    raise ValueError("The length of the parameter 'limit' value must be 1 or 2")
            sql_list.append(sql_limit)

        ## Join sql part.
        sql = "\n".join(sql_list)

        # Execute SQL.
        result = self.execute(sql, report=report, **kwdata)

        return result


    def execute_insert(
        self,
        data: Table,
        table: str,
        database: Optional[str] = None,
        duplicate: Optional[Literal["ignore", "update"]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Insert` the data of table in the datebase.

        Parameters
        ----------
        data : Insert data.
        table : Table name.
        database : Database name.
        duplicate : Handle method when constraint error.
            - `None` : Not handled.
            - `ignore` : Use `UPDATE IGNORE INTO` clause.
            - `update` : Use `ON DUPLICATE KEY UPDATE` clause.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.
            - `str and first character is ':'` : Use this syntax.
            - `Any` : Use this value.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `data` and `kwdata`.
        >>> data = [{'key': 'a'}, {'key': 'b'}]
        >>> kwdata = {'value1': 1, 'value2': ':(SELECT 2)'}
        >>> REngine.execute_insert(data, 'table', 'database', **kwdata)
        >>> result = REngine.execute_select('table', 'database')
        >>> print(result.fetch_table())
        [{'key': 'a', 'value1': 1, 'value2': 2}, {'key': 'b', 'value1': 1, 'value2': 2}]
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Handle parameter.

        ## Data.
        if data.__class__ == dict:
            data = [data]
        elif isinstance(data, CursorResult):
            data = to_table(data)
        elif data.__class__ == DataFrame:
            data = to_table(data)

        ## Check.
        if data in ([], [{}]):
            raise ValueError("parameter 'data' cannot both be empty")

        ## Keyword data.
        kwdata_method = {}
        kwdata_replace = {}
        for key, value in kwdata.items():
            if (
                value.__class__ == str
                and value[:1] == ":"
                and value != ":"
            ):
                kwdata_method[key] = value[1:]
            else:
                kwdata_replace[key] = value

        # Generate SQL.

        ## Part "fields" syntax.
        fields_replace = {
            field
            for row in data
            for field in row
        }
        fields_replace = {
            field
            for field in fields_replace
            if field not in kwdata
        }
        sql_fields_list = (
            *kwdata_method,
            *kwdata_replace,
            *fields_replace
        )
        sql_fields = ", ".join(
            [
                f"`{field}`"
                for field in sql_fields_list
            ]
        )

        ## Part "values" syntax.
        sql_values_list = (
            *kwdata_method.values(),
            *[
                ":" + field
                for field in (
                    *kwdata_replace,
                    *fields_replace
                )
            ]
        )
        sql_values = ", ".join(sql_values_list)

        ## Join sql part.

        ### Ignore.
        if duplicate == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{database}`.`{table}`({sql_fields})\n"
                f"VALUES({sql_values})"
            )

        ### Update.
        elif duplicate == "update":
            update_content = ",\n    ".join([f"`{field}` = VALUES(`{field}`)" for field in sql_fields_list])
            sql = (
                f"INSERT INTO `{database}`.`{table}`({sql_fields})\n"
                f"VALUES({sql_values})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"    {update_content}"
            )

        ### Not handle.
        else:
            sql = (
                f"INSERT INTO `{database}`.`{table}`({sql_fields})\n"
                f"VALUES({sql_values})"
            )

        # Execute SQL.
        result = self.execute(sql, data, report, **kwdata)

        return result


    def execute_update(
        self,
        data: Table,
        table: str,
        database: Optional[str] = None,
        where_fields: Optional[Union[str, Iterable[str]]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Update` the data of table in the datebase.

        Parameters
        ----------
        data : Update data, clause `WHERE` and `SET` content.
            - `Union[List, Tuple]` : Clause WHERE form is 'field IN :field'.
            - `Any` : Clause WHERE form is 'field = :field'.

        table : Table name.
        database : Database name.
        where_fields : Clause `WHERE` content fields.
            - `None` : The first key value pair of each item is judged.
            - `str` : This key value pair of each item is judged.
            - `Iterable[str]` : Multiple judged, `and` relationship.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.
            - `str and first character is ':'` : Use this syntax.
            - `Any` : Use this value.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `data` and `kwdata`.
        >>> data = [{'key': 'a'}, {'key': 'b'}]
        >>> kwdata = {'value': 1, 'name': ':`key`'}
        >>> REngine.execute_update(data, 'table', 'database', **kwdata)
        >>> result = REngine.execute_select('table', 'database')
        >>> print(result.fetch_table())
        [{'key': 'a', 'value': 1, 'name': 'a'}, {'key': 'b', 'value': 1, 'name': 'b'}]
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Handle parameter.

        ## Data.
        if data.__class__ == dict:
            data = [data]
        elif isinstance(data, CursorResult):
            data = to_table(data)
        elif data.__class__ == DataFrame:
            data = to_table(data)

        ## Check.
        if data in ([], [{}]):
            raise ValueError("parameter 'data' cannot both be empty")

        ## Keyword data.
        kwdata_method = {}
        kwdata_replace = {}
        for key, value in kwdata.items():
            if (
                value.__class__ == str
                and value[:1] == ":"
                and value != ":"
            ):
                kwdata_method[key] = value[1:]
            else:
                kwdata_replace[key] = value
        sql_set_list_kwdata = [
            f"`{key}` = {value}"
            for key, value in kwdata_method.items()
        ]
        sql_set_list_kwdata.extend(
            [
                f"`{key}` = :{key}"
                for key in kwdata_replace
            ]
        )

        # Generate SQL.
        data_flatten = kwdata_replace
        sqls_list = []
        if where_fields is None:
            no_where = True
        else:
            no_where = False
            if where_fields.__class__ == str:
                where_fields = [where_fields]
        for index, row in enumerate(data):
            for key, value in row.items():
                index_key = f"{index}_{key}"
                data_flatten[index_key] = value
            if no_where:
                for key in row:
                    where_fields = [key]
                    break

            ## Part "SET" syntax.
            sql_set_list = sql_set_list_kwdata.copy()
            sql_set_list.extend(
                [
                    f"`{key}` = :{index}_{key}"
                    for key in row
                    if (
                        key not in where_fields
                        and key not in kwdata
                    )
                ]
            )
            sql_set = ",\n    ".join(sql_set_list)

            ## Part "WHERE" syntax.
            sql_where_list = []
            for field in where_fields:
                index_field = f"{index}_{field}"
                index_value = data_flatten[index_field]
                if index_value.__class__ in (list, tuple):
                    sql_where_part = f"`{field}` IN :{index_field}"
                else:
                    sql_where_part = f"`{field}` = :{index_field}"
                sql_where_list.append(sql_where_part)
            sql_where = "\n    AND ".join(sql_where_list)

            ## Join sql part.
            sql = (
                f"UPDATE `{database}`.`{table}`\n"
                f"SET {sql_set}\n"
                f"WHERE {sql_where}"
            )
            sqls_list.append(sql)

        ## Join sqls.
        sqls = ";\n".join(sqls_list)

        # Execute SQL.
        result = self.execute(sqls, data_flatten, report)

        return result


    def execute_delete(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Delete` the data of table in the datebase.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        where : Clause `WHERE` content, join as `WHERE str`.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `where` and `kwdata`.
        >>> where = '`id` IN :ids'
        >>> ids = (1, 2)
        >>> result = REngine.execute_delete('table', 'database', where, ids=ids)
        >>> print(result.rowcount)
        2
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Generate SQL.
        sqls = []

        ## Part 'DELETE' syntax.
        sql_delete = f"DELETE FROM `{database}`.`{table}`"
        sqls.append(sql_delete)

        ## Part 'WHERE' syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sqls.append(sql_where)

        ## Join sqls.
        sqls = "\n".join(sqls)

        # Execute SQL.
        result = self.execute(sqls, report=report, **kwdata)

        return result


    @overload
    def execute_exist(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        count: Literal[False] = False,
        report: bool = None,
        **kwdata: Any
    ) -> bool: ...

    @overload
    def execute_exist(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        count: Literal[True] = False,
        report: bool = None,
        **kwdata: Any
    ) -> int: ...

    def execute_exist(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        count: bool = False,
        report: bool = None,
        **kwdata: Any
    ) -> Union[bool, int]:
        """
        `Count` records.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        where : Match condition, `WHERE` clause content, join as `WHERE str`.
            - `None` : Match all.
            - `str` : Match condition.

        count : Whether return match count, otherwise return whether it exist.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        CursorResult object of alsqlchemy package.

        Examples
        --------
        Parameter `where` and `kwdata`.
        >>> where = '`id` IN :ids'
        >>> ids = (1, 2)
        >>> result = REngine.execute_exist('table', 'database', where, True, ids=ids)
        >>> print(result)
        2
        """

        # Get parameter.
        if count:
            limit = None
        else:
            limit = 1

        # Execute.
        result = self.execute_select(table, database, "1", where=where, limit=limit, report=report, **kwdata)

        # Return.
        rowcount = result.rowcount
        if count:
            return rowcount
        else:
            return rowcount != 0


    @property
    def databases(self) -> Dict[str, List[str]]:
        """
        Get dictionary of `databases` and `tables`.

        Returns
        -------
        Dictionary of databases and tables
        """

        # Get database list.

        ## Generate SQL.
        sql = "SHOW DATABASES"

        ## Execute SQL.
        result = self.execute(sql)

        # Get table list of database.
        database_dict = {}
        for database, in result:
            sql = f"USE {database}"
            self.execute(sql)
            sql = "SHOW TABLES"
            result = self.execute(sql)
            database_dict[database] = [row for row, in result]

        return database_dict


    # @property
    # def variables(self) -> Dict[str, str]:
    #     """
    #     Get `variables` of database.

    #     Returns
    #     -------
    #     Variables of database.
    #     """

    #     # Generate SQL.
    #     sql = "SHOW VARIABLES"

    #     # Execute SQL.
    #     result = self.execute(sql)

    #     # Convert dictionary.
    #     variables = result.fetch_dict(val_field=1)

    #     return variables


    # @variables.setter
    # def variables(self, params: Dict[str, Union[str, float]]) -> None:
    #     """
    #     Update `variables` of database.

    #     Parameters
    #     ----------
    #     params : Update parameter key value pairs.
    #     """

    #     # Generate SQL.
    #     sql_set_list = [
    #         "%s = %s" % (
    #             key,
    #             (
    #                 value
    #                 if value.__class__ in (int, float)
    #                 else "'%s'" % value
    #             )
    #         )
    #         for key, value in params.items()
    #     ]
    #     sql_set = ",\n    ".join(sql_set_list)
    #     sql = (
    #         f"SET {sql_set}"
    #     )

    #     # Execute SQL.
    #     self.execute(sql)


    # @property
    # def global_variables(self) -> Dict[str, str]:
    #     """
    #     Get `global variables` of database.

    #     Returns
    #     -------
    #     Global variables of database.
    #     """

    #     # Generate SQL.
    #     sql = "SHOW GLOBAL VARIABLES"

    #     # Execute SQL.
    #     result = self.execute(sql)

    #     # Convert dictionary.
    #     variables = result.fetch_dict(val_field=1)

    #     return variables


    # @global_variables.setter
    # def global_variables(self, params: Dict[str, Union[str, float]]) -> None:
    #     """
    #     Update `global variables` of database.

    #     Parameters
    #     ----------
    #     params : Update parameter key value pairs.
    #     """

    #     # Generate SQL.
    #     sql_set_list = [
    #         "%s = %s" % (
    #             key,
    #             (
    #                 value
    #                 if value.__class__ in (int, float)
    #                 else "'%s'" % value
    #             )
    #         )
    #         for key, value in params.items()
    #     ]
    #     sql_set = ",\n    ".join(sql_set_list)
    #     sql = (
    #         f"SET GLOBAL {sql_set}"
    #     )

    #     # Execute SQL.
    #     self.execute(sql)


    # @property
    # def status(self) -> Dict[str, str]:
    #     """
    #     Get `status` of database.

    #     Returns
    #     -------
    #     Status of database.
    #     """

    #     # Generate SQL.
    #     sql = "SHOW STATUS"

    #     # Execute SQL.
    #     result = self.execute(sql)

    #     # Convert dictionary.
    #     status = result.fetch_dict(val_field=1)

    #     return status


    # @property
    # def global_status(self) -> Dict[str, str]:
    #     """
    #     Get `global status` of database.

    #     Returns
    #     -------
    #     Global status of database.
    #     """

    #     # Generate SQL.
    #     sql = "SHOW GLOBAL STATUS"

    #     # Execute SQL.
    #     result = self.execute(sql)

    #     # Convert dictionary.
    #     status = result.fetch_dict(val_field=1)

    #     return status


    def connect(self) -> RConnection:
        """
        Build `database connection` instance.
        """

        # Build.
        rconnection = RConnection(
            self.engine.connect(),
            self
        )

        return rconnection


    @property
    def status(self) -> RStatus:
        """
        Build `database status` instance.
        """

        # Build.
        rstatus = RStatus(self, False)

        return rstatus


    @property
    def global_status(self) -> RStatus:
        """
        Build global `database status` instance.
        """

        # Build.
        rstatus = RStatus(self, True)

        return rstatus


    @property
    def variables(self) -> RVariables:
        """
        Build `database variables` instance.
        """

        # Build.
        rvariables = RVariables(self, False)

        return rvariables


    @property
    def global_variables(self) -> RVariables:
        """
        Build global `database variables` instance.
        """

        # Build.
        rvariables = RVariables(self, True)

        return rvariables


    @property
    def exe(self) -> RExecute:
        """
        Build `database execute` instance.

        Examples
        --------
        Select.
        >>> where = '`id` in :ids'
        >>> kwdata = {'ids': [1, 2]}
        >>> result = RExecute.database.table(where, **kwdata)

        Insert.
        >>> data = [{'id': 1}, {'id': 2}]
        >>> kwdata = {'value': 'a'}
        >>> result = RExecute.database.table + (data, **kwdata)

        Update.
        >>> data = [{'id': 1}, {'id': 2}]
        >>> kwdata = {'value': 'a'}
        >>> result = RExecute.database.table & (data, **kwdata)

        Delete.
        >>> where = '`id` in :ids'
        >>> kwdata = {'ids': [1, 2]}
        >>> result = RExecute.database.table - (where, **kwdata)

        Exists.
        >>> where = '`id` in :ids'
        >>> kwdata = {'ids': [1, 2]}
        >>> result = RExecute.database.table * (where, **kwdata)

        Default database.
        >>> where = '`id` in :ids'
        >>> kwdata = {'ids': [1, 2]}
        >>> engine = REngine(**server, database)
        >>> result = engine.exe.table(where, **kwdata)
        """

        # Build.
        rexecute = RExecute(self)

        return rexecute


class RConnection(REngine):
    """
    Rey's `database connection` type.
    """


    def __init__(
            self,
            connection: Connection,
            rengine: REngine
        ) -> None:
        """
        Build `database connection` instance.

        Parameters
        ----------
        connection : Connection object.
        rengine : REngine object.
        """

        # Set parameter.
        self.connection = connection
        self.rengine = rengine
        self.begin = None
        self.begin_count = 0
        self.drivername = rengine.drivername
        self.username = rengine.username
        self.password = rengine.password
        self.host = rengine.host
        self.port = rengine.port
        self.database = rengine.database
        self.query = rengine.query
        self.pool_recycle = rengine.pool_recycle


    def executor(
        self,
        connection: Connection,
        sql: TextClause,
        data: List[Dict],
        report: bool
    ) -> RResult:
        """
        `SQL` executor.

        Parameters
        ----------
        connection : Connection object.
        sql : TextClause object.
        data : Data set for filling.
        report : Whether report SQL execute information.

        Returns
        -------
        Result object.
        """

        # Create Transaction object.
        if self.begin_count == 0:
            self.rollback()
            self.begin = connection.begin()

        # Execute.

        ## Report.
        if report:
            result, report_runtime = runtime(connection.execute, sql, data, _return_report=True)
            report_info = (
                f"{report_runtime}\n"
                f"Row Count: {result.rowcount}"
            )
            sqls = [
                sql_part.strip()
                for sql_part in sql.text.split(";")
            ]
            if data == []:
                rprint(report_info, *sqls, title="SQL")
            else:
                rprint(report_info, *sqls, data, title="SQL")

        ## Not report.
        else:
            result = connection.execute(sql, data)

        # Count.
        syntaxes = self.get_syntax(sql)
        if objs_in(syntaxes, "INSERT", "UPDATE", "DELETE"):
            self.begin_count += 1

        return result


    def execute(
        self,
        sql: Union[str, TextClause],
        data: Optional[Table] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        Execute `SQL`.

        Parameters
        ----------
        sql : SQL in method `sqlalchemy.text` format, or `TextClause` object.
        data : Data set for filling.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameters by priority.
        report = get_first_notnull(report, ROption.report_execute_info)

        # Handle parameter.
        if sql.__class__ == str:
            sql = text(sql)
        if data is None:
            if kwdata == {}:
                data = []
            else:
                data = [kwdata]
        else:
            if data.__class__ == dict:
                data = [data]
            elif isinstance(data, CursorResult):
                data = to_table(data)
            elif data.__class__ == DataFrame:
                data = to_table(data)
            else:
                data = data.copy()
            for param in data:
                param.update(kwdata)

        # Fill missing data.
        data = self.fill_data(data, sql)

        # Execute.

        ## Can retry.
        if self.begin_count == 0 and not self.is_multi_sql(sql):
            result = retry(
            self.executor,
            self.connection,
            sql,
            data,
            report,
            _report="Database execute operational error",
            _exception=OperationalError
        )

        ## Cannot retry.
        else:
            result = self.executor(self.connection, sql, data, report)

        return result


    def commit(self) -> None:
        """
        `Commit` cumulative executions.
        """

        # Commit.
        if self.begin is not None:
            self.begin.commit()
            self.begin = None
            self.begin_count = 0


    def rollback(self) -> None:
        """
        `Rollback` cumulative executions.
        """

        # Rollback.
        if self.begin is not None:
            self.begin.rollback()
            self.begin = None
            self.begin_count = 0


    def close(self) -> None:
        """
        `Close` database connection.
        """

        # Close.
        self.connection.close()


    def __del__(self) -> None:
        """
        `Close` database connection.
        """

        # Close.
        self.close()


class RParameter():
    """
    Rey's `database parameter` type.
    """


    def __init__(
        self,
        rengine: Union[REngine, RConnection],
        global_: bool
    ) -> None:
        """
        Build `database parameter` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        global_ : Whether base global.
        """

        # Set parameter.
        self.rengine = rengine
        self.global_ = global_


    def get(self) -> Dict[str, str]: ...


    def update(self, params: Dict[str, Union[str, float]]) -> None: ...


    def __getitem__(self, key: str) -> str:
        """
        Get item of parameter dictionary.

        Parameters
        ----------
        key : Parameter key.

        Returns
        -------
        Parameter value.
        """

        # Get.
        params = self.get()

        # Index.
        value = params[key]

        return value


    def __setitem__(self, key: str, value: Union[str, float]) -> None:
        """
        Set item of parameter dictionary.

        Parameters
        ----------
        key : Parameter key.
        value : Parameter value.
        """

        # Set.
        params = {key: value}

        # Update.
        self.update(params)


class RStatus(RParameter):
    """
    Rey's `database status` type.
    """


    def get(self) -> Dict[str, str]:
        """
        Get `database status`.

        Returns
        -------
        Status of database.
        """

        # Generate SQL.

        ## Global.
        if self.global_:
            sql = "SHOW GLOBAL STATUS"

        ## Not global.
        else:
            sql = "SHOW STATUS"

        # Execute SQL.
        result = self.rengine.execute(sql)

        # Convert dictionary.
        status = result.fetch_dict(val_field=1)

        return status


    def update(self, params: Dict[str, Union[str, float]]) -> None:
        """
        Update `database status`.

        Parameters
        ----------
        params : Update parameter key value pairs.
        """

        # Throw exception.
        raise AssertionError("database status not update")


class RVariables(RParameter):
    """
    Rey's `database variables` type.
    """


    def get(self) -> Dict[str, str]:
        """
        Get `database variables`.

        Returns
        -------
        Variables of database.
        """

        # Generate SQL.

        ## Global.
        if self.global_:
            sql = "SHOW GLOBAL VARIABLES"

        ## Not global.
        else:
            sql = "SHOW VARIABLES"

        # Execute SQL.
        result = self.rengine.execute(sql)

        # Convert dictionary.
        variables = result.fetch_dict(val_field=1)

        return variables


    def update(self, params: Dict[str, Union[str, float]]) -> None:
        """
        Update `database variables`.

        Parameters
        ----------
        params : Update parameter key value pairs.
        """

        # Generate SQL.
        sql_set_list = [
            "%s = %s" % (
                key,
                (
                    value
                    if value.__class__ in (int, float)
                    else "'%s'" % value
                )
            )
            for key, value in params.items()
        ]
        sql_set = ",\n    ".join(sql_set_list)

        # Global.
        if self.global_:
            sql = f"SET GLOBAL {sql_set}"

        ## Not global.
        else:
            sql = f"SET {sql_set}"

        # Execute SQL.
        self.rengine.execute(sql)


class RExecute(object):
    """
    Rey's `database execute` type.

    Examples
    --------
    Select.
    >>> where = '`id` in :ids'
    >>> kwdata = {'ids': [1, 2]}
    >>> result = RExecute.database.table(where, **kwdata)

    Insert.
    >>> data = [{'id': 1}, {'id': 2}]
    >>> kwdata = {'value': 'a'}
    >>> result = RExecute.database.table + (data, **kwdata)

    Update.
    >>> data = [{'id': 1}, {'id': 2}]
    >>> kwdata = {'value': 'a'}
    >>> result = RExecute.database.table & (data, **kwdata)

    Delete.
    >>> where = '`id` in :ids'
    >>> kwdata = {'ids': [1, 2]}
    >>> result = RExecute.database.table - (where, **kwdata)

    Exists.
    >>> where = '`id` in :ids'
    >>> kwdata = {'ids': [1, 2]}
    >>> result = RExecute.database.table * (where, **kwdata)

    Default database.
    >>> where = '`id` in :ids'
    >>> kwdata = {'ids': [1, 2]}
    >>> engine = REngine(**server, database)
    >>> result = engine.exe.table(where, **kwdata)
    """


    def __init__(self, rengine: Union[REngine, RConnection]) -> None:
        """
        Build `database execute` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        """

        # Set parameter.
        self._rengine = rengine
        self._path: List[str] = []


    @overload
    def __getattr__(self, key: Literal["_rengine"]) -> Union[REngine, RConnection]: ...

    @overload
    def __getattr__(self, key: Literal["_path"]) -> List[str]: ...

    @overload
    def __getattr__(self, key: str) -> RExecute: ...

    def __getattr__(self, key: str) -> Any:
        """
        Get attribute or set database name or set table name.

        Parameters
        ----------
        key : Attribute key or database name or table name.
        """

        # Filter private
        if key in ("_rengine", "_path"):
            return self.__dict__[key]

        # Check parameter.
        if len(self._path) not in (0, 1):
            raise AssertionError("usage error")

        # Set parameter.
        self._path.append(key)

        return self


    def _get_path(self) -> Tuple[str, str]:
        """
        Get database name and table name.

        Returns
        -------
        Database name and table name.
        """

        # Get.
        path_len = len(self._path)
        if path_len == 1:
            database = self._rengine.database
            table = self._path[0]
        elif path_len == 2:
            database = self._path[0]
            table = self._path[1]
        else:
            raise AssertionError("usage error")

        return database, table


    def __call__(
        self,
        where: Optional[str] = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Select` the data of table in the datebase.

        Parameters
        ----------
        where : Clause `WHERE` content, join as `WHERE str`.
        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        database, table = self._get_path()

        # Selete.
        result = self._rengine.execute_select(
            table,
            database,
            where=where,
            **kwdata
        )

        return result


    def __add__(
        self,
        data: Union[Table, Tuple[Table, Dict]]
    ) -> RResult:
        """
        `Insert` the data of table in the datebase.

        Parameters
        ----------
        data : Insert data.
            - `Table` : For table data.
            - `Tuple[Table, Dict]: For table data and keyword data.

        Returns
        -------
        Result object.
        """

        # Get parameter.

        ## Path.
        database, table = self._get_path()

        ## Data.
        if data.__class__ == tuple:
            data, kwdata = data
        else:
            kwdata = {}

        # Insert.
        result = self._rengine.execute_insert(
            data,
            table,
            database,
            **kwdata
        )

        return result


    def __and__(
        self,
        data: Union[Table, Tuple[Table, Dict]]
    ) -> RResult:
        """
        `Update` the data of table in the datebase.

        Parameters
        ----------
        data : Update data.
            - `Table` : For table data.
            - `Tuple[Table, Dict]: For table data and keyword data.

        Returns
        -------
        Result object.
        """

        # Get parameter.

        ## Path.
        database, table = self._get_path()

        ## Data.
        if data.__class__ == tuple:
            data, kwdata = data
        else:
            kwdata = {}

        # Insert.
        result = self._rengine.execute_update(
            data,
            table,
            database,
            **kwdata
        )

        return result


    def __sub__(
        self,
        where: Union[str, Tuple[str, Dict]]
    ) -> RResult:
        """
        `Delete` the data of table in the datebase.

        Parameters
        ----------
        where : Clause `WHERE` content, join as `WHERE str`.
            - `str` : For clause content.
            - `Tuple[str, Dict]: For clause content and keyword data.

        Returns
        -------
        Result object.
        """

        # Get parameter.

        ## Path.
        database, table = self._get_path()

        ## Where.
        if where.__class__ == tuple:
            where, kwdata = where
        else:
            kwdata = {}

        # Delete.
        result = self._rengine.execute_delete(
            table,
            database,
            where,
            **kwdata
        )

        return result


    def __mul__(
        self,
        where: Union[str, Tuple[str, Dict]]
    ) -> bool:
        """
        `Exist` the data of table in the datebase.

        Parameters
        ----------
        where : Clause `WHERE` content, join as `WHERE str`.
            - `str` : For clause content.
            - `Tuple[str, Dict]: For clause content and keyword data.

        Returns
        -------
        Exist result.
        """

        # Get parameter.

        ## Path.
        database, table = self._get_path()

        ## Where.
        if where.__class__ == tuple:
            where, kwdata = where
        else:
            kwdata = {}

        # Exist.
        result = self._rengine.execute_exist(
            table,
            database,
            where,
            **kwdata
        )

        return result