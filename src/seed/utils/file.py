import os
import time

from seed.utils.helper import local_file_path


class LocalFile(object):
    def save(self, file):
        filename = '_'.join([str(int(time.time())), file.filename])
        upload_path = os.path.join(local_file_path, filename)

        if not os.path.exists(local_file_path):
            os.makedirs(local_file_path)

        try:
            file.save(upload_path)
        except Exception as e:
            print(e)
            return None

        return os.path.join('files', filename)
