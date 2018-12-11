import os
import click


@click.command()
@click.option('--sql', default=False,
              help=("Don't emit SQL to database - dump to standard "
                    "output instead"))
@click.pass_context
def upgrade(ctx, sql=False):
    """ Upgrade database data and strcuct
    """
    from seed.services.app import SeedHttpServer
    from seed.runner.setting import discover_configs

    _, config_file, _ = discover_configs()
    SeedHttpServer(
        host='127.0.0.1',
        port='5000',
        workers=1,
        config_file=config_file
    ).upgrade(sql)
