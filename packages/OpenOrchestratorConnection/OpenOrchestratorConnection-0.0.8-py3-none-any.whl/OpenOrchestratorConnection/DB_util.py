import pyodbc
from pypika import MSSQLQuery, Table
from . import Crypto_util

_connection_string = None
_connection = None

def connect(conn_string: str) -> bool:
    global _connection, _connection_string

    try:
        conn = pyodbc.connect(conn_string)
        _connection = conn
        _connection_string = conn_string
        return True
    except Exception as e:
        _connection = None
        _connection_string = None
    
    return False

def catch_db_error(func):
    """A decorator that catches errors in SQL queries"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pyodbc.DatabaseError as e:
            print(f"Query failed:\n{e}")
    return inner

def _get_connection():
    global _connection, _connection_string   
    
    if _connection:
        try:
            _connection.cursor()
            return _connection
        except pyodbc.ProgrammingError as e:
            if str(e) != 'Attempt to use a closed connection.':
                raise e
    
    _connection = pyodbc.connect(_connection_string)
    return _connection

@catch_db_error
def create_log(process_name:str, level:int, message:str):
    conn = _get_connection()

    logs = Table('Logs')
    command = (
        MSSQLQuery.into(logs)
        .columns(logs.log_level, logs.process_name, logs.log_message)
        .insert(level, process_name, message)
        .get_sql()
    )

    conn.execute(command)
    conn.commit()

@catch_db_error
def get_constant(constant_name:str):
    conn = _get_connection()

    constants = Table('Constants')
    command = (
        MSSQLQuery.from_(constants)
        .select(constants.constant_value)
        .where(constants.constant_name == constant_name)
        .get_sql()
    )

    result = conn.execute(command).fetchone()
    if result is not None:
        return result[0]
    else:
        raise ValueError(f"No constant with name '{constant_name}' found.")

@catch_db_error
def get_credential(credential_name:str) -> tuple[str, str]:
    conn = _get_connection()

    credentials = Table('Credentials')
    command = (
        MSSQLQuery.from_(credentials)
        .select(credentials.cred_username, credentials.cred_password)
        .where(credentials.cred_name == credential_name)
        .get_sql()
    )

    result = conn.execute(command).fetchone()
    if result is not None:
        username, password = result
        password = Crypto_util.decrypt_string(password)
        return username, password
    else:
        raise ValueError(f"No credential with name '{credential_name}' found.")

@catch_db_error
def update_constant(constant_name:str, new_value:str):
    conn = _get_connection()

    constants = Table('Constants')
    command = (
        MSSQLQuery.update(constants)
        .set(constants.constant_value, new_value)
        .where(constants.constant_name == constant_name)
        .get_sql()
    )

    cursor = conn.execute(command)
    if cursor.rowcount == 0:
        raise ValueError(f"No constant with the name '{constant_name}' was found.")
    conn.commit()

@catch_db_error
def update_credential(credential_name:str, username:str, password:str):
    conn = _get_connection()

    password = Crypto_util.encrypt_string(password)

    credentials = Table('Credentials')
    command = (
        MSSQLQuery.update(credentials)
        .set(credentials.cred_username, username)
        .set(credentials.cred_password, password)
        .where(credentials.cred_name == credential_name)
        .get_sql()
    )

    cursor = conn.execute(command)
    if cursor.rowcount == 0:
        raise ValueError(f"No credential with the name '{credential_name}' was found.")
    conn.commit()
