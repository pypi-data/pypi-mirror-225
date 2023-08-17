import pickle

import aiosqlite

class Taper:
    """
        Main class. Its instances correspond to a single table in the database.
        Use:
        table1 = Taper("table_name", "file.db")
    """

    class _Value:
        def __init__(self):
            pass

    class _ColumnCountError(Exception):
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None

    class _TooMuchColumnError(_ColumnCountError):
        def __init__(self):
            super().__init__()

        def __str__(self):
            if self.message:
                return f"Передано значений больше, чем столбцов в таблице. {self.message}"
            else:
                return f"Передано значений больше, чем столбцов в таблице."

    class _TooFewColumnError(_ColumnCountError):
        def __init__(self):
            super().__init__()

        def __str__(self):
            if self.message:
                return f"Передано значений меньше, чем столбцов в таблице. {self.message}"
            else:
                return f"Передано значений меньше, чем столбцов в таблице."

    def __init__(self, table_name: str, file_name: str):
        self._table_name: str = table_name
        self._file_name: str = file_name
        self.obj = self._Value()
        self._columns = {}

    async def write(self, values: list | tuple, table_name: str = None):
        if table_name is None:
            table_name = self._table_name

            if len(values) > len(self._columns):
                raise self._TooMuchColumnError
            if len(values) < len(self._columns):
                raise self._TooFewColumnError

        conn = await aiosqlite.connect(self._file_name)
        questions = "?"
        for x in range(len(values) - 1):
            questions += ", ?"

        await conn.execute(f"INSERT or REPLACE into {table_name} VALUES({questions});", values)
        await conn.commit()
        await conn.close()
        return values

    async def read(self, column_name: str, key: str | int):
        conn = await aiosqlite.connect(self._file_name)
        cur = await conn.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
        result = await cur.fetchall()

        if len(result) == 1:
            result = result[0]

            # pickle check
            result = list(result)
            for n, val in enumerate(result):
                if type(val) in (bytes, bytearray):
                    result[n] = pickle.loads(val)
            # /pickle check

        else:
            # pickle check
            for n, row in enumerate(result):
                row = list(row)
                for m, val in enumerate(row):
                    if type(val) in (bytes, bytearray):
                        row[m] = pickle.loads(val)
                result[n] = row


        await conn.close()
        return result

    async def read_obj(self, column_name: str, key: str | int):
        conn = await aiosqlite.connect(self._file_name)
        cur = await conn.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
        result = await cur.fetchone()

        # pickle check
        result = list(result)
        for n, val in enumerate(result):
            if type(val) in (bytes, bytearray):
                result[n] = pickle.loads(val)
        # /pickle check

        index = 0
        for key in self._columns:
            self.obj.__setattr__(key, result[index])
            index += 1
        return self.obj

    async def read_all(self, table_name: str = None):
        if table_name is None:
            table_name = self._table_name
        conn = await aiosqlite.connect(self._file_name)
        cur = await conn.execute(f"SELECT * from {table_name}")
        result = await cur.fetchall()

        # pickle check
        if len(result) <= 1000:
            for n, row in enumerate(result):
                row = list(row)
                for m, val in enumerate(row):
                    if type(val) in (bytes, bytearray):
                        row[m] = pickle.loads(val)
                result[n] = row
        # /pickle check

        await conn.close()
        return result

    async def delete_row(self, column_name: str = None, key: str | int = None, all_rows: bool = None):
        """
        Func uses to deleting rows from the table.

        :param column_name: Column name to delete the row in which the key is found in the current column
        :param key: Key which looks in column
        :param all_rows: If True func delete all rows in the table
        """

        conn = await aiosqlite.connect(self._file_name)
        if all_rows:
            await conn.execute(f'DELETE FROM {self._table_name}')
        else:
            await conn.execute(f'DELETE FROM {self._table_name} WHERE {column_name} = ?', (key,))
        await conn.commit()
        await conn.close()

    async def create_table(self, table: dict, table_name: str = None):
        """
        table - {
                    "table1": "type",
                    and so on
                }

        """
        if table_name is None:
            table_name = self._table_name
        conn = await aiosqlite.connect(self._file_name)
        task = f"CREATE TABLE IF NOT EXISTS {table_name}("
        n = 0
        for key in table:
            n += 1
            task += f"{key} {table[key]}"
            if n != len(table):
                task += ", "
            else:
                task += ");"
        await conn.execute(task)
        await conn.commit()
        await conn.close()
        self._columns = table
        self.__create_obj__()

    async def pop_table(self, table_name: str = None):
        if not table_name:
            table_name = self._table_name
        conn = await aiosqlite.connect(self._file_name)
        await conn.execute(f"DROP TABLE {table_name}")
        await conn.commit()
        await conn.close()

    def __create_obj__(self):
        for key in self._columns:
            self.obj.__setattr__(key, None)


    async def execute(self, sql: str):
        conn = await aiosqlite.connect(self._file_name)
        await conn.execute(sql)
        await conn.commit()
        await conn.close()