from . import db, BaseModel

__all__ = ['Bussiness']


class Bussiness(BaseModel):
    """ bussiness model class
    """

    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    bmanager = db.relationship('BManager', cascade="all,delete", backref="bussiness")
    databases = db.relationship('Databases', cascade="all,delete", backref="bussiness")
    filters = db.relationship('Filters', cascade="all,delete", backref="bussiness")
    menu = db.relationship('Menu', cascade="all,delete", backref="bussiness")
    role = db.relationship('Role', cascade="all,delete", backref="bussiness")
    role_menu = db.relationship('RoleMenu', cascade="all,delete", backref="bussiness")