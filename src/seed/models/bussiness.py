from . import db, BaseModel
from sqlalchemy import event

__all__ = ['Bussiness']


class Bussiness(BaseModel):
    """ bussiness model class
    """

    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    # create_user_id = db.Column(db.Integer, nullable=False)

# @event.listens_for(Bussiness, 'first_init')
# def initial_default_bussiness(*args, **kwargs):
#     """ 添加默认数据
#     """
#     db.session.add(Bussiness(name='默认业务数据', description='展示初始化业务的业务数据'))
#     db.session.commit()