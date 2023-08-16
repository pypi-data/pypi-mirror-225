import logging
import sqlite3
from datetime import MAXYEAR, MINYEAR, datetime, timezone

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.elements import literal
from sqlalchemy.sql.functions import func

from dql.sql.functions import path as sql_path

logger = logging.getLogger("dql")

slash = literal("/")
empty_str = literal("")


def setup():
    # sqlite 3.31.1 is the earliest version tested in CI
    if sqlite3.sqlite_version_info < (3, 31, 1):
        logger.warning(
            "Possible sqlite incompatibility. The earliest tested version of "
            f"sqlite is 3.31.1 but you have {sqlite3.sqlite_version}"
        )

    sqlite3.register_adapter(datetime, adapt_datetime)
    sqlite3.register_converter("datetime", convert_datetime)

    compiles(sql_path.parent, "sqlite")(compile_path_parent)
    compiles(sql_path.name, "sqlite")(compile_path_name)


def adapt_datetime(val: datetime) -> str:
    if not (val.tzinfo is timezone.utc or val.tzname() == "UTC"):
        try:
            val = val.astimezone(timezone.utc)
        except (OverflowError, ValueError, OSError):
            if val.year == MAXYEAR:
                val = datetime.max
            elif val.year == MINYEAR:
                val = datetime.min
            else:
                raise
    return val.replace(tzinfo=None).isoformat(" ")


def convert_datetime(val: bytes) -> datetime:
    return datetime.fromisoformat(val.decode()).replace(tzinfo=timezone.utc)


def path_parent(path):
    return func.rtrim(func.rtrim(path, func.replace(path, slash, empty_str)), slash)


def path_name(path):
    return func.ltrim(func.substr(path, func.length(path_parent(path)) + 1), slash)


def compile_path_parent(element, compiler, **kwargs):
    return compiler.process(path_parent(*element.clauses.clauses), **kwargs)


def compile_path_name(element, compiler, **kwargs):
    return compiler.process(path_name(*element.clauses.clauses), **kwargs)
