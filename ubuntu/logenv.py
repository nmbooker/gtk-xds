#! /usr/bin/env python

"""Set up logging based on environment variable.

Public functions:
    * configure_logging_module

Other functions should be considered private, use at your own risk.

Run as script for simple demonstration and test.
Sample code under "if __name__ == '__main__'".
"""

import logging
import os

def configure_logging_module(env_var, default_level='WARNING'):
    """Set the basicConfig level based on env_var if defined, or default_level

    The environment variable value, or the value of default_level,
    can be the names of any of the log level constants defined in the
    logging module.

    You may also use an integer value as default_level.

    At the moment, the environment variable must contain a constant name.

    If the name of the log level is invalid, ValueError is raised.
    """
    level = _get_configured_log_level(env_var, default_level)
    logging.basicConfig(level=level)


def _get_configured_log_level(env_var, default_level='WARNING'):
    """Implementation detail.
    Return the integer log level to be used.
    """
    level = os.getenv(env_var, default_level)
    if not isinstance(level, int):
        level = _log_level_from_string(level)
    return level


def _log_level_from_string(string):
    """Implementation detail.
    Return the log level corresponding to the constant named in STRING.
    """
    try:
        return getattr(logging, string)
    except AttributeError:
        raise ValueError('invalid log level: %r' % string)

if __name__ == "__main__":
    configure_logging_module('LOGENV_LOG_LEVEL')
    print "Set LOGENV_LOG_LEVEL to try out different levels"
    logging.debug('Variable x = 3 at the moment')
    logging.info('Starting to work on your data...')
    logging.warn('Something potentially dodgy going on here')
    logging.error('Part of the program failed')
    logging.critical('Something really bad happened, closing now')
