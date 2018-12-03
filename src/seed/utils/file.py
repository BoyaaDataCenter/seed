import os
from pathlib import Path
import time

local_file_path = os.path.join(
    Path(os.path.dirname(os.path.realpath(__file__))).parent, 'static', 'files'
)


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
