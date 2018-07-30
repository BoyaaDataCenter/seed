import os
import click

from seed.utils.imports import import_string

version_string = '0.1'


@click.group()
@click.option(
    '--config',
    default='',
    envvar='SEED_CONF',
    help='Path to config file',
    metavar='PATH'
)
@click.version_option(version=version_string)
@click.pass_context
def cli(ctx, config):
    if config:
        os.environ['SEED_CONF'] = config
    else:
        os.environ['SEED_CONF'] = '~/.seed'


cmds = [
    'seed.runner.commands.run.run',
    'seed.runner.commands.init.init',
    'seed.runner.commands.upgrade.upgrade',
]

for cmd in cmds:
    cli.add_command(import_string(cmd))


def main():
    cli()
