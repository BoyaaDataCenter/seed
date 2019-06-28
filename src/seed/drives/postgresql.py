import decimal
from datetime import datetime, date

import psycopg2

from seed.drives.base import BaseDrive, DEFUALT_RETRY_COUNT

# 解决 pg TypeError: Decimal('30737') is not JSON serializable的问题
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)
# 解决DataTime is not Json serializable的问题
DATE2STR = psycopg2.extensions.new_type(
    psycopg2.extensions.PYDATE.values,
    'DATE2STR',
    lambda value, curs: value.split('.')[0] if value is not None else None)
psycopg2.extensions.register_type(DATE2STR)
DATETIME2STR = psycopg2.extensions.new_type(
    psycopg2.extensions.PYDATETIME.values,
    'DATETIME2STR',
    lambda value, curs: value.split('.')[0] if value is not None else None)
psycopg2.extensions.register_type(DATETIME2STR)


class PostgreSQL(BaseDrive):
    def query(self, sql, params=None, retry_count=DEFUALT_RETRY_COUNT):
        """ 查询SQL语句
        """
        self._raise_retry_count(retry_count)

        cursor = self._gen_cursor()
        try:
            query_datas = self._query(cursor, sql, params)
            return query_datas
        except (psycopg2.OperationalError, psycopg2.DatabaseError, psycopg2.InterfaceError) as e:
            # 可能数据库会主动断开连接
            # 尝试重新连接, 并重试
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

        return self._replace_type(query_datas)

    def _execute(self, cursor, sql, params=None):
        """ 执行SQL
        """
        try:
            cursor.execute(sql, params)
            self._commit()
        except psycopg2.ProgrammingError as e:
            # syntax error
            self._rollback()
            raise Exception(str(e))
        except psycopg2.extensions.QueryCanceledError as e:
            raise psycopg2.QueryCanceledError(str(e))
        except (psycopg2.OperationalError, psycopg2.DatabaseError, psycopg2.InterfaceError) as e:
            # server closed the connection unexpectedly
            raise
        except Exception as e:
            self._rollback()
            raise

    def _connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.name,
                user=self.user,
                password=self.password,
                host=self.ip,
                port=self.port,
                options='-c statement_timeout=60s',
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
                    data[key] = float(value)
        return datas


class Row(dict):

    """访问对象那样访问dict,行结果"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)