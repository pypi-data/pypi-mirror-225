import sqlite3

def connect(__file__: str, file_name: str = None) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    path = __file__.replace('\\', '/').split('/')
    path.pop(-1)
    path.pop(-1)
    if file_name is None:
        path.append('database.db')
    else:
        path.append(file_name)
    database = sqlite3.connect('/'.join(path))
    cursor = database.cursor()
    return database, cursor

def disconnect(database: sqlite3.Connection, cursor: sqlite3.Cursor):
    database.commit()
    cursor.close()
    database.close()

def add(table: str, data: str, values: list, __file__: str):
    database, cursor = connect(__file__=__file__)
    cursor.execute(f'INSERT INTO {table}({data}) VALUES({", ".join(["?"] * len(values))})', tuple(values))
    disconnect(database, cursor)

def get(table: str, data: str, __file__: str, where: str = None) -> str or None:
    database, cursor = connect(__file__=__file__)
    if where is None:
        data = cursor.execute(f'SELECT data FROM {table}').fetchone()
    else:
        data = cursor.execute(f'SELECT data FROM {table} WHERE ?', (where,)).fetchone()
    disconnect(database, cursor)
    return data if data is None else data[0]

def edit(table: str, data: str, new_data: str, __file__: str, where: str = None):
    database, cursor = connect(__file__=__file__)
    if where is None:
        cursor.execute(f'UPDATE {table} SET {data} = ?', (new_data,))
    else:
        cursor.execute(f'UPDATE {table} SET {data} = ? WHERE {where}', (new_data,))
    disconnect(database, cursor)

def remove(table: str, __file__: str, where: str = None):
    database, cursor = connect(__file__=__file__)
    if where is None:
        cursor.execute(f'DELETE FROM {table}')
    else:
        cursor.execute(f'DELETE FROM {table} WHERE {where.split(" = ")[0]} = ?', (where.split(" = ")[1],))
    disconnect(database, cursor)
