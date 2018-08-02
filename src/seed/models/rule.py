from ._base import db, BaseModel

__all__ = ['Rule', ]


class Rule(BaseModel):
    rule = db.Column(db.Text, default='new')