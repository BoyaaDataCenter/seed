from ._base import db, BussinessModel

__all__ = ["BManager", ]


class BManager(BussinessModel):
    """ 业务管理员模型
    """
    user_id = db.Column(db.Integer, nullable=False)
