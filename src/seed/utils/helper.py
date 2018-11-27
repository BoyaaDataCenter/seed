from inspect import getmembers

from sqlalchemy.exc import InvalidRequestError


def get_module_members(modules, predicate):

    members = getmembers(modules, predicate)
    return map(lambda m: m[1], members)


def get_immediate_cls_attr(cls, attrname):
    if not issubclass(cls, object):
        return None

    for base in cls.__mro__:
        if attrname in base.__dict__ and base is cls:
            return getattr(base, attrname)

    return None


def get_package_members(package, predicate, pre_url=''):
    from pkgutil import iter_modules
    from importlib import import_module

    members = {}

    for _, name, ispkg in iter_modules(package.__path__, package.__name__+'.'):
        if ispkg:
            sub_members = get_package_members(
                import_module(name), predicate,
                '/'.join([pre_url, name.split('.')[-1]])
            )
            members.update(sub_members)

        members.setdefault(pre_url, []).extend(
            get_module_members(import_module(name), predicate)
        )

    return members


def common_batch_crud(schema, model, datas):
    """ 批量做增改删操作
    """
    # 删除多余的数据
    schema_instance = schema()
    delete_datas = [data for data in datas if data.get('status') == -1]
    delete_datas, errors = schema_instance.load(delete_datas, many=True)
    if errors:
        raise Exception(errors)

    for delete_data in delete_datas:
        try:
            delete_data.delete()
        except InvalidRequestError:
            pass

    # 新增和修改数据
    modify_datas = [data for data in datas if data.get('status') != -1]
    modify_datas, errors = schema_instance.load(modify_datas, many=True)
    if errors:
        raise Exception(errors)
    [modify_data.save() for modify_data in modify_datas]

    datas = schema(many=True, exclude=model.column_filter).dump(modify_datas)
    return datas
