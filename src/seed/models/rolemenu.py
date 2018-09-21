from ._base import db, BussinessModel

__all__ = ["RoleMenu",]


class RoleMenu(BussinessModel):
    role_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer)

    role_permission = db.Column(db.Boolean, default=True)