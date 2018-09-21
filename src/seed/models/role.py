from . import db, BussinessModel

__all__ = ['Role', ]


class Role(BussinessModel):
    role = db.Column(db.Text, default='new')