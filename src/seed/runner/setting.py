import os


DEFAULT_SETTINGS_CONF = 'config.yaml'
DEFAULT_SETTINGS_OVERRIDE = 'seed_conf.py'


def discover_configs():
    """ discover seed config files
    """

    try:
        config = os.environ['SEED_CONF']
    except KeyError:
        config = '~/.seed'

    config = os.path.expanduser(config)

    return (
        config, os.path.join(config, DEFAULT_SETTINGS_OVERRIDE),
        os.path.join(config, DEFAULT_SETTINGS_CONF)
    )


def load_config_template(path, version='default'):
    from pkg_resources import resource_string
    return resource_string('seed', 'data/config/%s.%s' % (path, version)).decode('utf-8')


def generate_settings(dev):
    """ generate default setting file contents
    """

    context = {
        'debug_flag': dev,
    }

    py = load_config_template(DEFAULT_SETTINGS_OVERRIDE, 'default') % context
    yaml = load_config_template(DEFAULT_SETTINGS_CONF, 'default') % context

    return py, yaml
