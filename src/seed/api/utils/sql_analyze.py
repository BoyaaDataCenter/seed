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

        sql_temp = sqls.lower().replace('\n', ' ')  #将换行符替换成空格
        temp = sql_temp[re.search("select\W+", sql_temp, re.I).end() : re.search("\W+from\W+", sql_temp, re.I).start()]   #截取字符串
        reg = re.compile(r'\(.*?\) ', re.I)    #查找‘（）’的内容，将他替换掉再来获取才正确
        temp = reg.sub(' ', temp)
        s = temp.split(',')  #分割字段
        fields = []
        for item in s:
            list = item.split(' ')   #再以空格分割
            i = len(list)
            while i>=0:
                i=i-1
                if list[i]:#获取最后一个不为空格的字段
                    fields.append(str(list[i]).strip())
                    break

        return self.response_json(self.HttpErrorCode.SUCCESS, data={'fields': fields})