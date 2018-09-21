from ._base import db, BussinessModel

__all__ = ["UserRole", ]

class UserRole(BussinessModel):
    """ 用户菜单模型
    """

    user_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)