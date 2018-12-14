from seed.models._base import db

__all__ = ['AnalogdataDimensions', 'AnalogdataGamedatas']


class AnalogdataDimensions(db.Model):
    """ 测试数据-维度表
    """
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    game_name = db.Column(db.Text)
    platform_id = db.Column(db.Integer)
    platform_name = db.Column(db.Text)
    version_id = db.Column(db.Integer)
    version_name = db.Column(db.Text)


class AnalogdataGamedatas(db.Model):
    """ 测试数据-数据表
    """
    id = db.Column(db.Integer, primary_key=True)
    fdate = db.Column(db.Text)
    game_id = db.Column(db.Integer)
    platform_id = db.Column(db.Integer)
    version_id = db.Column(db.Integer)
    fregucnt = db.Column(db.Integer)
    factucnt = db.Column(db.Integer)
    fpayucnt = db.Column(db.Integer)
    fincome = db.Column(db.Float)
