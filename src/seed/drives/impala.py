import decimal
from datetime import datetime, date

from impala import dbapi

from seed.drives.base import BaseDrive, DEFUALT_RETRY_COUNT


class Impala(BaseDrive):
    def query(self, sql, params=None, retry_count=DEFUALT_RETRY_COUNT):
        """ 查询SQL语句
        """
        self._raise_retry_count(retry_count)

        cursor = self._gen_cursor()
        try:
            query_data = self._query(cursor, sql, params)
            return query_data
        except (dbapi.OperationalError, dbapi.DatabaseError, dbapi.InterfaceError):
            if not retry_count:
                raise

            self._connect()
            return self.query(sql, params=params, retry_count=retry_count-1)
        finally:
            cursor.close()

    def _query(self, cursor, sql, params):
        self._execute(cursor, sql, params=params)
        columns_name = [d[0] for d in cursor.description]
        query_datas = [Row(zip(columns_name, row)) for row in cursor]

        return query_datas

    def _execute(self, cursor, sql, params=None):
        """ 执行SQL
        """
        try:
            try:
                cursor.execute(sql, params)
            except Exception:
                cursor.execute("INVALIDATE METADATA;")
                cursor.execute(sql, params)
            self._commit()
        except dbapi.ProgrammingError as e:
            self._rollback()
            raise Exception(str(e))
        except (dbapi.OperationalError, dbapi.DatabaseError, dbapi.InterfaceError) as e:
            raise
        except Exception:
            self._rollback()
            raise

    def _connect(self):
        try:
            self.conn = dbapi.connect(
                database=self.name,
                user=self.user,
                password=self.password,
                host=self.ip,
                port=self.port,
            )
        except Exception:
            raise


class Row(dict):
    """访问对象那样访问dict,行结果"""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)