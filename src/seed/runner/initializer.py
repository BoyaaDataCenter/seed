import logging


def initialize_app(config):
    """
    initialize a application
    """

    configure_logging()


def configure_logging():
    """
    configure logging
    """
    from seed.conf import server
    logging.config.dictConfig(server.LOGGING)