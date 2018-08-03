# from flask.ext.sqlalchemy import Column
from ._base import db, BaseModel


__all__ = ['Account',]


class Account(BaseModel):
    role = db.Column(db.String(10), default='new')
    user_name = db.Column(db.String(40), unique=True, index=True, nullable=False)

    status = db.Column(db.Integer, default=1)
