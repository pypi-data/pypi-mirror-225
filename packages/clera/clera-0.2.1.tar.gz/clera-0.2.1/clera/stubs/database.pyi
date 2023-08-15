class Database:
    def __init__(self, name: str, PATH: str):
        '''
        The Clera Team - 0.0.1 

        Database is for easy configuration and data handling. "name" is the name of the database and "PATH" is the location of the database file or the location the database file should be created if it does not exist.
        '''
    def create(self, name: str, data: dict, commit: bool) -> bool:
        '''
        Create table in database with headers. name is the "name" of the table and "data" signifies the headers and the datatypes of their values.

        Data should be a dictionary where KEY is the header or column name and VALUE is the specified datatype for the column.

        Some datatypes are int, str, float, blob, null / None
        '''
    def insert(self, table: str, value: any, commit: bool) -> bool: ...
    def select(self, table: str, data: str, condition: str) -> list: ...
    def update(self, table: str, value: dict, condition: str) -> bool: ...
    def delete(self, table: str, condition: str) -> bool: 
        '''
        Delete row or data from table. "table" is the table name.
        '''
    def drop(self, table: str) -> bool: 
        '''
        Delete an entire table.
        '''
    def close(self) -> None: ...
    def commit(self) -> None:
        '''
        Make changes to the database
        '''

class database(Database): ...