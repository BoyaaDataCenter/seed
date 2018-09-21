from ._base import db, BussinessModel

__all__ = ["Menu",]


class Menu(BussinessModel):
    name = db.Column(db.Text, nullable=False)

    parent_id = db.Column(db.Integer, default=0)
    left_id = db.Column(db.Integer, default=0)