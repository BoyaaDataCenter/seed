import os
import click

from seed.runner.commands.run import Address


@click.command()
@click.option(
    '--dev', default=False, is_flag=True, help='Use settings more conducive to local development'
)
@click.argument('directory', required=False)
@click.pass_context
def init(ctx, dev, directory):
    """ Initialize new configuration directory.
    """
    from seed.runner.setting import discover_configs, generate_settings

    if directory:
        os.environ['SEED_CONF'] = directory

    directory, py, yaml = discover_configs()

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    py_contents, yaml_contents = generate_settings(dev)

    if os.path.isfile(yaml):
        click.confirm(
            "File already exists at '%s', overwrite?" % click.format_filename(yaml),
            abort=True
        )

    with click.open_file(yaml, 'w') as fp:
        fp.write(yaml_contents)

    if os.path.isfile(py):
        click.confirm(
            "File already exists at '%s', overwrite?" % click.format_filename(py),
            abort=True
        )

    with click.open_file(py, 'w') as fp:
        fp.write(py_contents)
