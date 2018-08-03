from . import db, BaseModel

__all__ = ['Dims']


class Dims(BaseModel):
    """ Dims or index model setting
    """

    model_id = db.Column(db.Integer, db.ForeignKey('report_model.id'))

    ename = db.Column(db.Text, nullable=False,
        comment='The dims english name')
    cname = db.Column(db.Text, nullable=False,
        comment='The dims chinese name')
    
    show_type = db.Column(db.Text, nullable=False, default='original',
        comment='The dims show type')
    
    state = db.Column(db.Text, nullable=False, default='on',
        comment='The dims show on or off')
    
    description = db.Column(db.Text, comment='The dims description')
