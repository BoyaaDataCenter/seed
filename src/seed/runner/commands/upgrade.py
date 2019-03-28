import os
import click


@click.command()
@click.option('--sql', is_flag=False,
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
        config_file=config_file
    ).upgrade(sql)
