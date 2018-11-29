import click


class AddressParamType(click.ParamType):
    name = 'address'

    def __call__(self, value, param=None, ctx=None):
        if value is None:
            return (None, None)
        return self.convert(value, param, ctx)

    def convert(self, value, param, ctx):
        if ':' in value:
            host, port = value.split(':', 1)
            port = int(port)
        else:
            host = value
            port = None
        return host, port


Address = AddressParamType()


@click.group()
def run():
    "Run a service."

@run.command()
@click.option(
    '--bind', '-b', default=None, help='Bind address.', type=Address
)
@click.option(
    '--workers', '-w', default=0,
    help='The number of worker process for handling requests'
)
@click.option(
    '--debug', '-d', default=False,
    help='The debug option for web'
)
def web(bind, workers, debug):
    from seed.services.app import SeedHttpServer
    from seed.runner.setting import discover_configs

    _, config_file, _ = discover_configs()
    http_server = SeedHttpServer(
        host=bind[0],
        port=bind[1],
        workers=workers,
        config_file=config_file
    )
    http_server.run()
