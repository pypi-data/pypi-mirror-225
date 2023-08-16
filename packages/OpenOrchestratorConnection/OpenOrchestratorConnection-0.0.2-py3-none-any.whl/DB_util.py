import pyodbc
import os
import Crypto_util

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


def _load_sql_file(file_name):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'SQL', file_name)
    with open(path) as file:
        command = file.read()
    return command

@catch_db_error
def create_log(process_name:str, level:int, message:str):
    conn = _get_connection()

    command = _load_sql_file('Create_Log.sql')
    command = command.replace('{NAME}', str(process_name))
    command = command.replace('{LEVEL}', str(level))
    command = command.replace('{MESSAGE}', str(message))

    conn.execute(command)
    conn.commit()

@catch_db_error
def get_constant(constant_name:str):
    conn = _get_connection()

    command = _load_sql_file('Get_Constant.sql')
    command = command.replace('{NAME}', constant_name)

    result = conn.execute(command).fetchone()
    if result is not None:
        return result[0]
    else:
        raise ValueError(f"No constant with name '{constant_name}' found.")

@catch_db_error
def get_credential(credential_name:str) -> tuple[str, str]:
    conn = _get_connection()

    command = _load_sql_file('Get_Credential.sql')
    command = command.replace('{NAME}', credential_name)

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

    command = _load_sql_file('Update_Constant.sql')
    command = command.replace('{NAME}', str(constant_name))
    command = command.replace('{VALUE}', str(new_value))

    cursor = conn.execute(command)
    if cursor.rowcount == 0:
        raise ValueError(f"No constant with the name '{constant_name}' was found.")
    conn.commit()

@catch_db_error
def update_credential(credential_name:str, username:str, password:str):
    conn = _get_connection()

    password = Crypto_util.encrypt_string(password)

    command = _load_sql_file('Update_Credential.sql')
    command = command.replace('{USERNAME}', username)
    command = command.replace('{PASSWORD}', password)
    command = command.replace('{NAME}', credential_name)

    cursor = conn.execute(command)
    if cursor.rowcount == 0:
        raise ValueError(f"No credential with the name '{credential_name}' was found.")
    conn.commit()
