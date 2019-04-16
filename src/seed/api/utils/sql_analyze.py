import re

from flask import request
import sqlparse
from sqlparse.tokens import Keyword
from sqlparse.sql import IdentifierList, Identifier

from seed.api._base import RestfulBaseView, HttpMethods


class SqlFieldAnalysis(RestfulBaseView):
    url = 'sql_fields'

    access_methods = [HttpMethods.POST]

    def post(self):
        input_json = request.get_json()

        if 'sqls' not in input_json:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg='获取SQL失败')

        sqls = input_json['sqls']
        print("origin_sql:", sqls)
        sql_str = sqls.lower().replace('\n', ' ')

        # 去除注释信息,否则列名会被解析错误
        sql = sqlparse.format(sql_str, strip_comments=True)
        stmt = sqlparse.parse(sql)[0]
        tokens_list = stmt.tokens

        fields = []

        for token in tokens_list:
            if token.ttype is Keyword:
                continue
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    field_name = identifier.get_name()
                    fields.append(field_name)
            elif isinstance(token, Identifier):
                break

        return self.response_json(self.HttpErrorCode.SUCCESS, data={'fields': fields})
