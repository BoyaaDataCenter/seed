from inspect import isclass

from seed.libs.data_access.utils.auto_register import get_package_members, get_immediate_cls_attr


class FormatterFactory(object):
    registerd_charttypes = {}

    def __init__(self, charttype):
        self.charttype = charttype

    def formatter_class(self):
        from seed.libs.data_access.formatters.line import LineFormatter
        if self.charttype not in self.registerd_charttypes:
            self._register_charttypes()

        return self.registerd_charttypes.get(self.charttype.lower()+'formatter', LineFormatter)

    def _register_charttypes(self):
        from seed.libs.data_access import formatters
        predicate = lambda m: isclass(m) and issubclass(m, BaseFormatter) and not get_immediate_cls_attr(m, '__abstract__')
        members = get_package_members(formatters, predicate)
        self.registerd_charttypes = {member.__name__.lower(): member for member in members}


class BaseFormatter(object):
    __abstract__ = True

    def __init__(self, indexs, dimensions, data, format_args):
        self.indexs = indexs
        self.dimensions = dimensions
        self.data = data
        self.format_args = format_args
