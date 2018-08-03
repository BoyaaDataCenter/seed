from . import db, BaseModel

__all__ = ['Dropdowns']


class Dropdowns(BaseModel):
    """ Dropdown model class
    """

    model_id = db.Column(db.Integer, nullable=False)

    dtype = db.Column(db.Text, nullable=False,
        comment='Dropdown belong type, page or model')
    stype = db.Column(db.Text, nullable=False,
        default='radio', comment='Radio or mulitple choice')
    ename = db.Column(db.Text, nullable=False,
        comment='Field english name')
    cname = db.Column(db.Text, nullable=False,
        comment='Field chinese name')
    cascade_type = db.Column(db.Text, nullable=False,
        comment='The Dropdown field cascade type')
    codition_type = db.Column(db.Text, nullable=False,
        comment='The Dropdown condition setting type, manual or sql')
    conditions = db.Column(db.Text, nullable=False,
        comment='The Dropdown conditions, it will save as json string')