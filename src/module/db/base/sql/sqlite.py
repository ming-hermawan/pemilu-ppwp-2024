import sqlite3

from g import DB_FOLDER_PATH


class BaseDbSqlite:

    # Constructor
    def __init__(self,
                 db_filename: str):
        db_path = self.__get_db_path(db_filename)
        self.__conn = sqlite3.connect(db_path)
        self.__cur = self.__conn.cursor()

    # Destructor
    def __del__(self):
        self.__conn.close()

    # PROTECTED Begin

    def __get_db_path(self,
                      db_filename: str) -> str:
        return "{0}/{1}.db".format(
          DB_FOLDER_PATH,
          db_filename)

    # PROTECTED End

    # PRIVATE Begin

    def _execute(self,
                 sql: str,
                 parameters: dict = None):
        if parameters is None:
            self.__cur.execute(sql)
        else:
            self.__cur.execute(sql,
                               parameters)

    def _executemany(self,
                     sql: str,
                     parameters: list = None):
        if parameters is None:
            self.__cur.executemany(sql)
        else:
            self.__cur.executemany(sql,
                                   parameters)

    def _fetchone(self,
                  sql: str,
                  parameters: dict = None):
        self._execute(
          sql=sql,
          parameters=parameters)
        return self.__cur.fetchone()

    def _fetchall(self,
                  sql: str,
                  parameters: dict = None):
        self._execute(
          sql=sql,
          parameters=parameters)
        return self.__cur.fetchall()

    def _commit(self):
        self.__conn.commit()

    def _close(self):
        self.__conn.close()

    # PRIVATE End
