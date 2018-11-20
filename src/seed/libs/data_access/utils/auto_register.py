from inspect import getmembers


def get_module_members(modules, predicate):
    members = getmembers(modules, predicate)
    return map(lambda m: m[1], members)


def get_package_members(package, predicate):
    from pkgutil import iter_modules
    from importlib import import_module

    members = []
    for _, name, ispkg in iter_modules(package.__path__, package.__name__+'.'):
        if ispkg:
            sub_members = get_package_members(
                import_module(name), predicate
            )
            members.append(sub_members)

        members.extend(get_module_members(import_module(name), predicate))

    return members


def get_immediate_cls_attr(cls, attrname):
    if not issubclass(cls, object):
        return None

    for base in cls.__mro__:
        if attrname in base.__dict__ and base is cls:
            return getattr(base, attrname)

    return None
