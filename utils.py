""" Utilities. """

import logging


def configure_logging(**options):

    """ Configure the root logger according to options.

    Mainly intended to be used by management commands to pass in the
    command line options to set the logger level according to the verbosity
    argument. Once raised the verbosity will not be reduced by subsequent
    calls to this method.

    """

    verbosity = int(options['verbosity'])
    if verbosity > 3:
        level = logging.DEBUG
    elif verbosity > 2:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.WARNING
    elif verbosity > 0:
        level = logging.ERROR
    else:
        level = logging.CRITICAL

    logger = logging.getLogger()
    if logger.level > level:
        logger.setLevel(level)
