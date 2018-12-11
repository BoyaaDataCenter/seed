from ._base import db, BussinessModel

# from seed.models import Panels, Filters

__all__ = ["Menu",]


class Menu(BussinessModel):
    name = db.Column(db.Text, nullable=False)

    parent_id = db.Column(db.Integer, default=0)
    left_id = db.Column(db.Integer, default=0)

    panels = db.relationship('Panels', cascade="all,delete", backref="menu")
    filters = db.relationship('Filters', cascade="all,delete", backref="menu")