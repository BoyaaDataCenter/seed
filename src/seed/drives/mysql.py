import decimal

import pymysql
from datetime import datetime, date

from seed.drives.postgresql import PostgreSQL


class MySQL(PostgreSQL):
    def query(self, sql, params=[], retry_count=1):
        """ 查询SQL语句
        """
        self._raise_retry_count(retry_count)

        cursor = self._gen_cursor()
        try:
            query_data = self._query(cursor, sql, params)
            return query_data
        except (pymysql.OperationalError, pymysql.DatabaseError, pymysql.InterfaceError) as e:
            if retry_count < 1:
                raise
            self._connect()
            return self.query(sql, params=params, retry_count=retry_count-1)
        finally:
            cursor.close()

        return []

    def _query(self, cursor, sql, params):
        self._execute(cursor, sql, params=params)
        datas = list(cursor.fetchall())
        return self._replace_type(datas)

    def _execute(self, cursor, sql, params=[]):
        """ 执行SQL
        """
        try:
            cursor.execute(sql, params)
            self._commit()
        except pymysql.ProgrammingError as e:
            self._rollback()
            raise Exception(str(e))
        except (pymysql.OperationalError, pymysql.DatabaseError, pymysql.InterfaceError) as e:
            raise
        except Exception as e:
            self._rollback()
            raise

    def _connect(self):
        try:
            self.conn = pymysql.connect(
                db=self.name,
                user=self.user,
                password=self.password,
                host=self.ip,
                port=self.port,
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            raise

    def _replace_type(self, datas):
        """ 替换数据类型
        """
        for data in datas:
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.strftime('%Y-%m-%d')
                if isinstance(value, date):
                    data[key] = value.strftime('%Y-%m-%d')
                if isinstance(value, decimal.Decimal):
                    data[key] = int(value)
        return datas
