import psycopg2

# 解决 pg TypeError: Decimal('30737') is not JSON serializable， 的bug
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)
# 解决DataTime is not Json serializable的bug
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

from seed.drives.base import BaseDrive, Row

class PostgreSQL(BaseDrive):

    def query(self, sql, params=[], retry_count=1):
        """ 查询SQL语句
        """
        self._raise_retry_count(retry_count)

        cursor = self._gen_cursor()
        # log.info("Logger_id: %s, postgres node get cursor." % self.logger_id)
        try:
            query_datas = self._query(cursor, sql, params)
            return query_datas
        except (psycopg2.OperationalError, psycopg2.DatabaseError, psycopg2.InterfaceError) as e:
            # 可能数据库会主动断开连接
            # 尝试重新连接, 并重试
            # log.warning('Logger_id: %s, the node try to connect database again' % self.logger_id)
            self._connect()
            return self.query(sql, params=params, retry_count=retry_count-1)
        finally:
            cursor.close()

        return []

    def _query(self, cursor, sql, params):
        # log.info('Logger_id: %s, the postgresql node begin to query' % self.logger_id) self._execute(cursor, sql, params=params)
        self._execute(cursor, sql, params=params)
        columns_name = [d[0] for d in cursor.description]
        query_datas = [Row(zip(columns_name, row)) for row in cursor]

        # log.info('Logger_id: %s, the postgresql node query finish and get data' % self.logger_id)

        return query_datas

    def _execute(self, cursor, sql, params=[]):
        """ 执行SQL
        """
        try:
            # log.info('Logger_id: %s, postgresql node execute sql start' % self.logger_id)
            cursor.execute(sql, params)
            self._commit()
            # log.info('Logger_id: %s, postgresql node execute sql normal' % self.logger_id)
        except psycopg2.ProgrammingError as e:
            # syntax error
            # log.error('Sql programming error:%s' % str(e))
            self._rollback()
            raise ProgrammingError(str(e))
        except psycopg2.extensions.QueryCanceledError as e:
            # log.error('The connection has been closed by db, the detail is %s' % str(e))
            raise QueryCanceledError(str(e))
        except (psycopg2.OperationalError, psycopg2.DatabaseError, psycopg2.InterfaceError) as e:
            # server closed the connection unexpectedly
            # log.error("The connection has been closed, the detail is %s" % str(e))
            raise
        except Exception as e:
            # log.error('Sql execute error:', str(e))
            self._rollback()
            raise
        # finally:
            # log.info('Logger_id: %s, postgresql node execute sql end' % self.logger_id)

    def _get_connection(self):
        if self.alive():
            self._connect()

    def _commit(self):
        """ 完成SQL执行
        """
        self.conn.commit()

    def _rollback(self):
        """ 回滚SQL
        """
        # log.debug('Postgresql node rollback')
        self.conn.rollback()

    def _connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.name,
                user=self.user,
                password=self.password,
                host=self.ip,
                port=self.port,
                options='-c statement_timeout=50s',
            )
        except Exception as e:
            # log.error('Logger_id: %s the postgresql node connection database error' % self.logger_id)
            raise

        # log.info('Postgresql node connected')

    def _gen_cursor(self):
        cursor = self.conn.cursor()
        return cursor

    def alive(self):
        """ 测试连接是否还存在
        """
        if self.conn:
            return True if self.conn.closed == 0 else False

        return False

    def close(self):
        """ 关闭连接
        """
        self.conn.close()
