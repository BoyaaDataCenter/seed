from seed.models.bussiness import Bussiness
from seed.models.bmanager import BManager
from seed.models.buser import BUser
from seed.models._base import session


def get_permission_datas_by_user(user):
    all_datas = session.query(Bussiness).all()
    all_datas = [data.row2dict() for data in all_datas]

    if user.role == 'super_admin':
        # 所有权限
        for data in all_datas:
            data.update({'edit': True, 'delete': True})
        permission_datas = all_datas
        un_permission_datas = []

    else:
        # 管理的业务
        order_datas = session.query(Bussiness)\
            .join(BManager, Bussiness.id == BManager.bussiness_id)\
            .filter(BManager.user_id == user.id)\
            .all()
        order_ids = [data.id for data in order_datas]
        order_datas = [data.row2dict() for data in order_datas]
        for data in order_datas:
            data.update({'edit': True, 'delete': False})

        # 有权限的业务
        permission_datas = session.query(Bussiness)\
            .join(BUser, Bussiness.id == BUser.bussiness_id)\
            .filter(BUser.user_id == user.id)\
            .all()
        permission_ids = [data.id for data in permission_datas]
        permission_datas = [data.row2dict() for data in permission_datas]
        for data in permission_datas:
            data.update({'edit': False, 'delete': False})

        permission_datas = [
            data for data in permission_datas if data['id'] not in order_ids
        ]
        permission_datas = order_datas + permission_datas
        permission_ids = [data['id'] for data in permission_datas]

        un_permission_datas = [
            data for data in all_datas if data['id'] not in permission_ids
        ]
    return permission_datas, un_permission_datas


def has_bussiness_permission(user, bussiness_id):
    permission_datas, _ = get_permission_datas_by_user(user)
    return any([bussiness_id == bussiness['id'] for bussiness in permission_datas])
