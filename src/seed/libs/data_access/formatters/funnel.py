import json
from seed.libs.data_access.formatters.line import LineFormatter


class FunnelFormatter(LineFormatter):
    def __init__(self, *args, **kwargs):
        super(LineFormatter, self).__init__(*args, **kwargs)

    def format_data(self):
        result = {"series": []}
        ret = {"data": []}
        for dimenstr, datas in self.data.items():
            info = {}
            dimendict = json.loads(dimenstr)
            namelist = [dimen.get("dimension", "") for dimen in self.dimensions]
            infoname = []
            for name in namelist:
                infoname.append(dimendict.get(name, ""))

            info["name"] = "-".join(infoname)
            info["value"] = 0
            for key, value in datas.items():
                if isinstance(value, (float, int)):
                    info["value"] += value
            ret["data"].append(info)

        result["series"].append(ret)

        return result
