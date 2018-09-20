from . import db, BaseModel

__all__ = ['Role', ]


class Role(BaseModel):
    role = db.Column(db.Text, default='new')