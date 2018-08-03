from . import db, BaseModel

__all__ = ['Pages']

class Pages(BaseModel):
    """ Page model table
    """
    
    bussiness_id = db.Column(db.Integer, db.ForeignKey('bussiness.id'),
        nullable=False)
    
    name = db.Column(db.Text, nullable=False, comment='page name')

    creater = db.Column(db.Text, comment='The page create user')
    updater = db.Column(db.Text, comment='The last time update user')

    sort = db.Column(db.Integer, autoincrement=True, comment='Page sort')

    owner = db.Column(db.Text, comment='Page technical director id')
    description = db.Column(db.Text, comment='Page description')

    state = db.Column(db.Text, default=0, comment='Page on/off state')
