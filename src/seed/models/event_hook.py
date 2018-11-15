from sqlalchemy import event

from seed.models.bussiness import Bussiness
from seed.models.menu import Menu
from seed.models.role import Role
from seed.models.buser import BUser
from seed.models.bmanager import BManager
from seed.models.buserrole import BUserRole
from seed.models.menu import Menu
from seed.models.rolemenu import RoleMenu
from seed.models.filters import Filters
from seed.models.panels import Panels


@event.listens_for(Bussiness, 'after_insert')
def bussiness_after_insert_hook(mapper, connection, target):
    """ 创建业务之后, 默认添加菜单和角色
    """
    # 新增默认菜单
    default_first_menu = connection.execute(
        Menu.__table__.insert(),
        bussiness_id=target.id,
        name='游戏概况'
    )
    connection.execute(
        Menu.__table__.insert(),
        bussiness_id=target.id,
        name='活跃用户',
        parent_id=default_first_menu.lastrowid
    )

    # 新增默认角色
    connection.execute(
        Role.__table__.insert(),
        bussiness_id=target.id,
        role='商务'
    )

    # TODO 新增默认图表数据


@event.listens_for(Menu, 'after_insert')
def menu_after_insert_hook(mapper, connection, target):
    """ 创建页面之后, 默认添加菜单和角色
    """
    pass


@event.listens_for(BUser, 'after_delete')
def buser_after_delete_hook(mapper, connection, target):
    """  删除业务用户之后，尝试删除该用户在当前业务之下的角色 和 管理员权限
    """
    connection.execute(
        BManager.__table__.delete(),
        bussiness_id=target.bussiness_id,
        user_id=target.id
    )

@event.listens_for(Bussiness, 'after_delete')
def bussiness_after_delete_hook(mapper, connection, target):
    """ 删除业务之后， 尝试删除业务相关的 业务用户，业务菜单，业务图表， 业务过滤组件， 业务角色
    """
    # 删除业务相关的用户权限
    connection.execute(
        BUser.__table__.delete(),
        bussiness_id=target.id
    )

    connection.execute(
        Role.__table__.delete(),
        bussiness_id=target.id
    )

    # 删除业务相关的用户角色权限
    connection.execute(
        BUserRole.__table__.delete(),
        bussiness_id=target.id
    )

    # 删除业务相关的角色菜单
    connection.execute(
        RoleMenu.__table__.delete(),
        bussiness_id=target.id
    )


    # 删除业务相关的菜单
    connection.execute(
        Menu.__table__.delete(),
        bussiness_id=target.id
    )

    # 删除业务相关的数据图表
    connection.execute(
        Panels.__table__.delete(),
        bussiness_id=target.id
    )

    # 删除业务相关的过滤组件
    connection.execute(
        Filters.__table__.delete(),
        bussiness_id=target.id
    )


@event.listens_for(Menu, 'after_delete')
def menu_after_delete_hook(mapper, connection, target):
    """ 删除菜单之后，尝试删除菜单对应的 角色菜单映射，菜单对应的业务图标，业务对应的过滤组件
    """
    # 删除业务相关的角色菜单
    # TODO menu和page不统一
    connection.execute(
        RoleMenu.__table__.delete(),
        bussiness_id=target.bussiness_id,
        menu_id=target.id
    )

    # 删除业务相关的数据图表
    connection.execute(
        Panels.__table__.delete(),
        bussiness_id=target.bussiness_id,
        page_id=target.id
    )

    # 删除业务相关的过滤组件
    connection.execute(
        Filters.__table__.delete(),
        bussiness_id=target.bussiness_id,
        page_id=target.id
    )
