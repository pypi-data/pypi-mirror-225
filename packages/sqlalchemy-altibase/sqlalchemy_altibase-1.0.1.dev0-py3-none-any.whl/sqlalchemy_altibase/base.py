# altibase/base.py
# Copyright (C) 2010-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
# get_select_precolumns(), limit_clause() implementation
# copyright (C) 2007 Fisch Asset Management
# AG http://www.fam.ch, with coding by Alexander Houben
# alexander.houben@thor-solutions.ch
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""

.. dialect:: altibase
    :name: Altibase
"""
from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy.dialects.oracle import base as oracle_base
from sqlalchemy.types import CHAR
from sqlalchemy.types import DATE
from sqlalchemy.types import FLOAT
from sqlalchemy.types import NCHAR
from sqlalchemy.types import NVARCHAR
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql import text

RESERVED_WORDS = set(
    [
        "_PROWID",
        "FIFO",
        "PRIMARY",
        "ACCESS",
        "FIXED",
        "PRIOR",
        "ADD",
        "FLASHBACK",
        "PROCEDURE",
        "AFTER",
        "FLUSH",
        "PURGE",
        "AGER",
        "FLUSHER",
        "QUEUE",
        "ALL",
        "FOLLOWING",
        "RAISE",
        "ALTER",
        "FOR",
        "READ",
        "AND",
        "FOREIGN",
        "REBUILD",
        "ANY",
        "FROM",
        "RECOVER",
        "APPLY",
        "FULL",
        "REMOVE",
        "ARCHIVE",
        "FUNCTION",
        "RENAME",
        "ARCHIVELOG",
        "GOTO",
        "REPLACE",
        "AS",
        "GRANT",
        "RETURN",
        "ASC",
        "GROUP",
        "RETURNING",
        "AT",
        "HAVING",
        "REVOKE",
        "AUDIT",
        "IF",
        "RIGHT",
        "AUTOEXTEND",
        "IN",
        "ROLLBACK",
        "BACKUP",
        "INDEX",
        "ROLLUP",
        "BEFORE",
        "INITRANS",
        "ROW",
        "BEGIN",
        "INNER",
        "ROWCOUNT",
        "BETWEEN",
        "INSERT",
        "ROWNUM",
        "BODY",
        "INSTEAD",
        "ROWTYPE",
        "BULK",
        "INTERSECT",
        "SAVEPOINT",
        "BY",
        "INTO",
        "SEGMENT",
        "CASCADE",
        "IS",
        "SELECT",
        "CASE",
        "ISOLATION",
        "SEQUENCE",
        "CAST",
        "JOIN",
        "SESSION",
        "CHECKPOINT",
        "KEY",
        "SET",
        "CLOSE",
        "LANGUAGE",
        "SHARD",
        "COALESCE",
        "LATERAL",
        "SOME",
        "COLUMN",
        "LEFT",
        "SPLIT",
        "COMMENT",
        "LESS",
        "SQLCODE",
        "COMMIT",
        "LEVEL",
        "SQLERRM",
        "COMPILE",
        "LIBRARY",
        "START",
        "COMPRESS",
        "LIFO",
        "STEP",
        "COMPRESSED",
        "LIKE",
        "STORAGE",
        "CONJOIN",
        "LIMIT",
        "STORE",
        "CONNECT",
        "LINK",
        "SYNONYM",
        "CONSTANT",
        "LINKER",
        "TABLE",
        "CONSTRAINTS",
        "LOB",
        "THAN",
        "CONTINUE",
        "LOCAL",
        "THEN",
        "CREATE",
        "LOCK",
        "TIMESTAMPADD",
        "CROSS",
        "LOGANCHOR",
        "TO",
        "CUBE",
        "LOGGING",
        "TOP",
        "CURSOR",
        "LOOP",
        "TRIGGER",
        "CYCLE",
        "MAXROWS",
        "TRUE",
        "DATABASE",
        "MAXTRANS",
        "TRUNCATE",
        "DECLARE",
        "MERGE",
        "TYPE",
        "DECRYPT",
        "MINUS",
        "TYPESET",
        "DEFAULT",
        "MODE",
        "UNION",
        "DELAUDIT",
        "MODIFY",
        "UNIQUE",
        "DELETE",
        "MOVE",
        "UNLOCK",
        "DEQUEUE",
        "MOVEMENT",
        "UNPIVOT",
        "DESC",
        "NEW",
        "UNTIL",
        "DETERMINISTIC",
        "NOAUDIT",
        "UPDATE",
        "DIRECTORY",
        "NOCOPY",
        "USING",
        "DISABLE",
        "NOCYCLE",
        "VALUES",
        "DISASTER",
        "NOLOGGING",
        "VARIABLE",
        "DISCONNECT",
        "NOT",
        "VC2COLL",
        "DISJOIN",
        "NULL",
        "VIEW",
        "DISTINCT",
        "NULLS",
        "VOLATILE",
        "DROP",
        "OF",
        "WAIT",
        "EACH",
        "OFF",
        "WHEN",
        "ELSE",
        "OFFLINE",
        "WHENEVER",
        "ELSEIF",
        "OLD",
        "WHERE",
        "ELSIF",
        "ON",
        "WHILE",
        "ENABLE",
        "ONLINE",
        "WITH",
        "END",
        "OPEN",
        "WITHIN",
        "ENQUEUE",
        "OR",
        "WORK",
        "ESCAPE",
        "ORDER",
        "WRAPPED",
        "EXCEPTION",
        "OTHERS",
        "WRITE",
        "EXEC",
        "OUT",
        "EXECUTE",
        "OUTER",
        "EXISTS",
        "OVER",
        "EXIT",
        "PACKAGE",
        "EXTENT",
        "PARALLEL",
        "EXTENTSIZE",
        "PARTITION",
        "FALSE",
        "PIVOT",
        "FETCH",
        "PRECEDING"
    ]
)


class _AltibaseUnitypeMixin(object):
    """these types appear to return a buffer object."""

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return str(value)  # decode("ucs-2")
            else:
                return None

        return process


class AltibaseTypeCompiler(oracle_base.OracleTypeCompiler):
    pass


ischema_names = {
    "VARCHAR2": VARCHAR,
    "NVARCHAR2": NVARCHAR,
    "CHAR": CHAR,
    "NCHAR": NCHAR,
    "DATE": DATE,
    "NUMBER": oracle_base.NUMBER,
    "BLOB": oracle_base.BLOB,
    "BFILE": oracle_base.BFILE,
    "CLOB": oracle_base.CLOB,
    "NCLOB": oracle_base.NCLOB,
    "TIMESTAMP": TIMESTAMP,
    "TIMESTAMP WITH TIME ZONE": TIMESTAMP,
    "INTERVAL DAY TO SECOND": oracle_base.INTERVAL,
    "RAW": oracle_base.RAW,
    "FLOAT": FLOAT,
    "DOUBLE PRECISION": oracle_base.DOUBLE_PRECISION,
    "LONG": oracle_base.LONG,
    "BINARY_DOUBLE": oracle_base.BINARY_DOUBLE,
    "BINARY_FLOAT": oracle_base.BINARY_FLOAT,
    "ROWID": oracle_base.ROWID,
}


class AltibaseInspector(reflection.Inspector):
    def __init__(self, conn):
        reflection.Inspector.__init__(self, conn)


class AltibaseExecutionContext(oracle_base.OracleExecutionContext):
    pass


class AltibaseSQLCompiler(oracle_base.OracleCompiler):
    pass


class AltibaseDDLCompiler(oracle_base.OracleDDLCompiler):
    pass


class AltibaseIdentifierPreparer(oracle_base.OracleIdentifierPreparer):
    # override LEGAL_CHARACTERS to add `#` for issue #1
    reserved_words = {x.lower() for x in RESERVED_WORDS}

    def __init__(self, dialect):
        super(AltibaseIdentifierPreparer, self).__init__(
            dialect,
            initial_quote="[",
            final_quote="]",
            escape_quote="",
            quote_case_sensitive_collations=False,
        )


class AltibaseDialect(default.DefaultDialect):
    name = "altibase"
    supports_statement_cache = True
    supports_alter = True
    supports_unicode_statements = False
    supports_unicode_binds = False
    max_identifier_length = 128

    supports_simple_order_by_label = False
    cte_follows_insert = True

    supports_sequences = True
    sequences_optional = False
    postfetch_lastrowid = False

    default_paramstyle = "named"
    colspecs = oracle_base.colspecs
    ischema_names = ischema_names
    requires_name_normalize = True

    supports_comments = True

    supports_default_values = False
    supports_default_metavalue = True
    supports_empty_insert = False
    supports_identity_columns = True

    type_compiler = AltibaseTypeCompiler
    statement_compiler = AltibaseSQLCompiler
    ddl_compiler = AltibaseDDLCompiler
    preparer = AltibaseIdentifierPreparer
    inspector = AltibaseInspector
    oracle_dialect = oracle_base.OracleDialect

    def __init__(
            self,
            use_ansi=True,
            optimize_limits=False,
            use_binds_for_limits=None,
            use_nchar_for_unicode=False,
            exclude_tablespaces=(),
            **kwargs
    ):
        default.DefaultDialect.__init__(self, **kwargs)
        self._use_nchar_for_unicode = use_nchar_for_unicode
        self.use_ansi = use_ansi
        self.optimize_limits = optimize_limits
        self.exclude_tablespaces = exclude_tablespaces

    def initialize(self, connection):
        super(AltibaseDialect, self).initialize(connection)

    @property
    def _supports_char_length(self):
        return True

    def _get_default_schema_name(self, connection):
        return self.normalize_name(
            connection.exec_driver_sql(
                "SELECT user_name FROM SYSTEM_.SYS_USERS_ ORDER BY user_name;"
            ).scalar()
        )

    def has_table(self, connection, table_name, schema=None):
        self._ensure_has_table_connection(connection)

        if not schema:
            schema = self.default_schema_name

        cursor = connection.execute(
            text(
                "SELECT T.TABLE_NAME 'TABLE_NAME' "
                "FROM SYSTEM_.SYS_TABLES_ T, SYSTEM_.SYS_USERS_ U "
                "WHERE T.TABLE_TYPE = 'T' "
                "AND T.TABLE_NAME = :name "
                "AND T.USER_ID = U.USER_ID "
                "AND U.USER_NAME = :schema_name "
                "ORDER BY T.TABLE_NAME;"
            ),
            dict(
                name=self.denormalize_name(table_name),
                schema_name=self.denormalize_name(schema),
            ),
        )
        return cursor.first() is not None

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        s = "SELECT user_name FROM SYSTEM_.SYS_USERS_ ORDER BY user_name;"
        cursor = connection.exec_driver_sql(s)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        # note that table_names() isn't loading DBLINKed or synonym'ed tables
        if schema is None:
            schema = self.default_schema_name

        sql_str = "SELECT T.TABLE_NAME 'TABLE_NAME' FROM SYSTEM_.SYS_TABLES_ T, SYSTEM_.SYS_USERS_ U WHERE "
        if self.exclude_tablespaces:
            sql_str += (
                    "NOT IN (%s) AND "
                    % (", ".join(["'%s'" % ts for ts in self.exclude_tablespaces]))
            )
        sql_str += (
            "T.TABLE_TYPE = 'T' "
            "AND T.USER_ID = U.USER_ID "
            "AND U.USER_NAME = :schema_name "
            "ORDER BY T.TABLE_NAME;"
        )
        cursor = connection.execute(text(sql_str), dict(schema_name=schema))
        return [self.normalize_name(row[0]) for row in cursor]


# If alembic is installed, register an alias in its dialect mapping.
try:
    import alembic.ddl.oracle
except ImportError:
    pass
else:

    class AltibaseDBImpl(alembic.ddl.oracle.OracleImpl):
        __dialect__ = "altibase"
        transactional_ddl = True

    # @compiles(alembic.ddl.postgresql.PostgresqlColumnType, "cockroachdb")
    # def visit_column_type(*args, **kwargs):
    #     return alembic.ddl.postgresql.visit_column_type(*args, **kwargs)
