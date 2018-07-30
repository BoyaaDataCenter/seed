import os
import click


@click.command()
@click.pass_context
def upgrade(ctx):
    """ Upgrade database data and strcuct
    """
    from seed.services.app import SeedHttpServer
    from seed.runner.setting import discover_configs

    # Monkey Patch
    import flask_migrate

    _, config_file, _ = discover_configs()
    http_server = SeedHttpServer(
        host='127.0.0.1',
        port='5000',
        workers=1,
        config_file=config_file
    )
    flask_migrate.current_app = http_server.app

    http_server.upgrade()
