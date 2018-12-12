from ._base import db, BaseModel

__all__ = ["BManager", ]


class BManager(BaseModel):
    """ 业务管理员模型
    """
    bussiness_id = db.Column(db.Integer, db.ForeignKey('bussiness.id'))
    user_id = db.Column(db.Integer, nullable=False)
