from . import db, BaseModel

__all__ = ['Bussiness']


class Bussiness(BaseModel):
    """ bussiness model class
    """

    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)