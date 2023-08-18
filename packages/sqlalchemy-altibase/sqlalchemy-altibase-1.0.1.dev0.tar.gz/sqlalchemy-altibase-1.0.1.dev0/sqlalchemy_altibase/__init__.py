from sqlalchemy.dialects import registry as _registry
from . import base  # noqa
from . import pyodbc  # noqa
from .base import CHAR
from .base import DATE
from .base import FLOAT
from .base import NCHAR
from .base import NVARCHAR
from .base import VARCHAR
from .pyodbc import get_odbc_info

__version__ = "1.0.1.dev0"

# default (and only) dialect
base.dialect = dialect = pyodbc.dialect

_registry.register(
    "altibase.pyodbc", "sqlalchemy_altibase.pyodbc", "AltibaseDialect_pyodbc"
)

__all__ = (
    "VARCHAR",
    "NVARCHAR",
    "CHAR",
    "NCHAR",
    "DATE",
    "NUMBER",
    "BLOB",
    "BFILE",
    "CLOB",
    "NCLOB",
    "TIMESTAMP",
    "RAW",
    "FLOAT",
    "DOUBLE_PRECISION",
    "BINARY_DOUBLE",
    "BINARY_FLOAT",
    "LONG",
    "dialect",
    "INTERVAL",
    "VARCHAR2",
    "NVARCHAR2",
    "ROWID",
)
