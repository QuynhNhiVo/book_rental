import re
import pymssql
import pyodbc
from .settings import settings

# Regex để chuẩn hóa tham số SQL (ví dụ: @username -> ?)
PARAMETER_PATTERN = re.compile(r"@([A-Za-z_][A-Za-z0-9_]*)")

def _normalize_server_name():
    return settings.DB_SERVER.replace('\\\\', '\\')

def _has_sql_login():
    return bool(settings.DB_USER and settings.DB_USER.strip())

def _select_odbc_driver():
    drivers = pyodbc.drivers()
    preferred_drivers = (
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server",
        "SQL Server",
    )
    for driver_name in preferred_drivers:
        if driver_name in drivers:
            return driver_name
    raise RuntimeError("Không tìm thấy driver ODBC cho SQL Server. Hãy cài đặt ODBC Driver 17 hoặc 18.")

def _prepare_pyodbc_query(query, params=None):
    if not params: return query, ()
    values = []
    def replace_match(match):
        param_name = match.group(1)
        if param_name not in params:
            raise KeyError(f"Thiếu tham số SQL: {param_name}")
        values.append(params[param_name])
        return "?"
    return PARAMETER_PATTERN.sub(replace_match, query), tuple(values)

def _row_to_dict(cursor, row):
    if row is None: return None
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

class PyodbcCursorAdapter:
    def __init__(self, cursor, as_dict=False):
        self._cursor = cursor
        self._as_dict = as_dict

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def execute(self, query, params=None):
        query, values = _prepare_pyodbc_query(query, params)
        if values: self._cursor.execute(query, values)
        else: self._cursor.execute(query)
        return self

    def fetchone(self):
        row = self._cursor.fetchone()
        return _row_to_dict(self._cursor, row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        return [_row_to_dict(self._cursor, row) for row in rows]

    def close(self):
        self._cursor.close()

class PyodbcConnectionAdapter:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self, as_dict=False):
        return PyodbcCursorAdapter(self._connection.cursor(), as_dict=as_dict)

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._connection.close()

def get_connection():
    """
    Khởi tạo kết nối tới SQL Server.
    Hỗ trợ cả Windows Authentication và SQL Server Authentication.
    """
    try:
        server = _normalize_server_name()
        db_user = settings.DB_USER.strip() if settings.DB_USER else None
        db_password = settings.DB_PASSWORD if settings.DB_PASSWORD else None

        # Sử dụng Windows Authentication nếu không có user/pass
        if not _has_sql_login():
            driver_name = _select_odbc_driver()
            connection_string = (
                f"DRIVER={{{driver_name}}};SERVER={server};"
                f"DATABASE={settings.DB_NAME};Trusted_Connection=yes;"
                "Encrypt=no;TrustServerCertificate=yes;Connection Timeout=5;"
            )
            return PyodbcConnectionAdapter(pyodbc.connect(connection_string, timeout=5))

        # Sử dụng SQL Server Authentication với pymssql
        return pymssql.connect(
            server=server, user=db_user, password=db_password,
            database=settings.DB_NAME, charset='utf8',
            login_timeout=5, timeout=10
        )
    except Exception as e:
        print(f"[ERROR] Database Connection Error: {e}")
        return None

def execute_query(connection, query, params=None):
    """Thực thi query INSERT, UPDATE, DELETE."""
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, params) if params else cursor.execute(query)
        connection.commit()
        return cursor.rowcount if cursor.rowcount >= 0 else True
    except Exception as e:
        connection.rollback()
        print(f"[ERROR] Query Execution Error: {e}")
        return None
    finally:
        if cursor: cursor.close()

def fetch_query(connection, query, params=None):
    """Lấy danh sách nhiều dòng dữ liệu."""
    cursor = None
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query, params) if params else cursor.execute(query)
        rows = cursor.fetchall()
        return rows if rows else []
    except Exception as e:
        print(f"[ERROR] Query Error: {e}")
        return []
    finally:
        if cursor: cursor.close()

def fetch_one(connection, query, params=None):
    """Lấy một dòng dữ liệu duy nhất."""
    cursor = None
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query, params) if params else cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        print(f"[ERROR] Query Error: {e}")
        return None
    finally:
        if cursor: cursor.close()
