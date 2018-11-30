from flask import request

# from seed.api.common import _MethodView
from seed.utils.file import LocalFile
from seed.api.endpoints._base import RestfulBaseView, HttpMethods


class Files(RestfulBaseView):

    access_methods = [HttpMethods.POST]

    def post(self):
        upload_file = request.files['file']
        local_file = LocalFile()
        file_path = local_file.save(upload_file)
        if file_path:
            file_url = request.host_url + file_path.replace('\\', '/')
            return self.response_json(self.HttpErrorCode.SUCCESS, '上传成功', {'file_url': file_url})
        return self.response_json(self.HttpErrorCode.ERROR, '上传失败')
