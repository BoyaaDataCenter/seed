from ._base import db, BaseModel

__all__ = ["Menu",]


class Menu(BaseModel):
    name = db.Column(db.Text, nullable=False)

    parent_id = db.Column(db.Integer, default=0)
    left_id = db.Column(db.Integer, default=0)