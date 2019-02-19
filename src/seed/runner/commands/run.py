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
    '--debug', '-d', default=False,
    help='The debug option for web'
)
def web(debug):
    from seed.services.app import application
    from seed.services.wsgi import SeedWSGIHttpServer

    if debug:
        application.run()
    else:
        SeedWSGIHttpServer(application).run()
