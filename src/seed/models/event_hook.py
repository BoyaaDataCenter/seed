from sqlalchemy import event

from seed.models.bussiness import Bussiness
from seed.models.menu import Menu
from seed.models.role import Role


@event.listens_for(Bussiness, 'after_insert')
def bussiness_after_insert_hook(mapper, connection, target):
    """ 创建业务之后, 默认添加菜单和角色
    """
    connection.execute(Menu.__table__.insert(), bussiness_id=target.id, name='活跃用户分析')
    connection.execute(Role.__table__.insert(), bussiness_id=target.id, role='商务')