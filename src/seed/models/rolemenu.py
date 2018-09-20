from ._base import db, BaseModel

__all__ = ["UserMenu",]


class RoleMenu(BaseModel):
    role_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer)