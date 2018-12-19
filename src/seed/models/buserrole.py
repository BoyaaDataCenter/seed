from ._base import db, BussinessModel

__all__ = ["BUserRole", ]


class BUserRole(BussinessModel):
    """ 用户权限模型
    """
    user_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)