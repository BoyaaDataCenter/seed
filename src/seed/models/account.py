from datetime import datetime
# from flask.ext.sqlalchemy import Column
from ._base import db, BaseModel


__all__ = ['Account',]


class Account(BaseModel):
    column_filter = ['updated', 'password']

    sso_id = db.Column(db.Integer, default=-1)  # SSO_ID

    account = db.Column(db.String(40), unique=True, index=True, nullable=False)
    password = db.Column(db.String(256))
    email = db.Column(db.String(40), nullable=False)

    avatar = db.Column(db.Text)
    name = db.Column(db.String(40), nullable=False)
    sex = db.Column(db.String(20), nullable=False, default='male')
    depart_id = db.Column(db.Integer, default=-1)  # -1为未知

    role = db.Column(db.String(20), default='new')
    status = db.Column(db.Integer, default=0)  # -1:不可用 0: 未激活 1: 正常使用

    login_at = db.Column(
        db.DateTime, default=datetime.utcnow()
    )