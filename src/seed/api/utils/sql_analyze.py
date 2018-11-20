import re

from flask import request

from seed.api.endpoints._base import RestfulBaseView, HttpMethods


class SqlFieldAnalysis(RestfulBaseView):
    url = 'sql_fields'

    access_methods = [HttpMethods.POST]

    def post(self):
        input_json = request.get_json()

        if 'sqls' not in input_json:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg='获取SQL失败')

        sqls = input_json['sqls']

        sql_str = sqls.lower().replace('\n', ' ')
        select_fileds = sql_str[
            re.search("select\W+", sql_str, re.I).end():
            re.search("\W+from\W+", sql_str, re.I).start()
        ]
        reg = re.compile(r'\(.*?\) ', re.I)
        select_fileds = reg.sub(' ', select_fileds)
        # 分割字段
        select_fileds = select_fileds.split(',')
        fields = []
        for select_filed in select_fileds:
            # 再以空格分割
            filed_split = select_filed.split(' ')
            i = len(filed_split)
            while i:
                i = i-1
                # 获取最后一个不为空格的字段
                if filed_split[i]:
                    fields.append(str(filed_split[i]).strip())
                    break
        return self.response_json(self.HttpErrorCode.SUCCESS, data={'fields': fields})
