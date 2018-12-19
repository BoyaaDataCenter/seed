from ._base import db, BussinessModel
__all__ = ["BUser", ]


class BUser(BussinessModel):
    """ 业务用户权限模型
    """
    user_id = db.Column(db.Integer, nullable=False)