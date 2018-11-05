from seed.drives.postgresql import PostgreSQL


def get_db_instance(dtype, ip, port, name, user, password, **kwargs):
    # TODO 自动收集当前支持的驱动
    db = PostgreSQL(ip, port, name, user, password)
    return db