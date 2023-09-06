import pyodbc


def connect_sql_server(configs: dict) -> pyodbc.Cursor:
    connection = pyodbc.connect(
        f'DRIVER={configs["driver"]};'
        f'SERVER={configs["server"]};'
        f'PORT={configs["port"]};'
        f'DATABASE={configs["database"]};'
        f'UID={configs["user"]};'
        f'PWD={configs["password"]}'
    )

    return connection.cursor()