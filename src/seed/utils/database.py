from seed.drives import ALL_DRIVES


def get_db_instance(dtype, ip, port, name, user, password, **kwargs):
    # TODO 自动收集当前支持的驱动
    db = ALL_DRIVES[dtype](ip, int(port), name, user, password)
    return db
