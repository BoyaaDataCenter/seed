import json

# from seed.libs.data_access.formatters.base import BaseFormatter
from seed.libs.data_access.formatters.line import LineFormatter


class PieFormatter(LineFormatter):
    def __init__(self, *args, **kwargs):
        super(LineFormatter, self).__init__(*args, **kwargs)