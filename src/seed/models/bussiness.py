from . import db, BaseModel

__all__ = ['Bussiness']


class Bussiness(BaseModel):
    """ bussiness model class
    """

    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    # create_user_id = db.Column(db.Integer, nullable=False)
