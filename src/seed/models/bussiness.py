from . import db, BaseModel

__all__ = ['Bussiness']


class Bussiness(BaseModel):
    """ bussiness model class
    """

    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    bmanager = db.relationship('BManager', cascade="all,delete", backref="bussiness")
    databases = db.relationship('Databases', cascade="all,delete", backref="bussiness")