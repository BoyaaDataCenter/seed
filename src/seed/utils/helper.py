from inspect import getmembers


def get_module_members(modules, predicate):

    members = getmembers(modules, predicate)
    return map(lambda m: m[1], members)


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
