# -*- coding: utf-8 -*-

import logging

from mkdocs.config.base import Config, _open_config_file
from mkdocs import exceptions
from mkdocs import utils

log = logging.getLogger('mkblog.config')


def load_config(config_file=None, **kwargs):
    """
    Load the configuration for a given file object or name
    The config_file can either be a file object, string or None. If it is None
    the default `mkdocs.yml` filename will loaded.
    Extra kwargs are passed to the configuration to replace any default values
    unless they themselves are None.
    """
    options = kwargs.copy()

    # Filter None values from the options. This usually happens with optional
    # parameters from Click.
    for key, value in options.copy().items():
        if value is None:
            options.pop(key)

    config_file = _open_config_file('mkblog.yml')
    options['config_file_path'] = getattr(config_file, 'name', '')

    # Initialise the config with the default schema .
    from mkblog import config
    cfg = Config(schema=config.DEFAULT_SCHEMA, config_file_path=options['config_file_path'])
    # First load the config file
    cfg.load_file(config_file)
    # Then load the options to overwrite anything in the config.
    cfg.load_dict(options)

    errors, warnings = cfg.validate()

    for config_name, warning in warnings:
        log.warning("Config value: '%s'. Warning: %s", config_name, warning)

    for config_name, error in errors:
        log.error("Config value: '%s'. Error: %s", config_name, error)

    for key, value in cfg.items():
        log.debug("Config value: '%s' = %r", key, value)

    if len(errors) > 0:
        raise exceptions.ConfigurationError(
            "Aborted with {0} Configuration Errors!".format(len(errors))
        )
    elif cfg['strict'] and len(warnings) > 0:
        raise exceptions.ConfigurationError(
            "Aborted with {0} Configuration Warnings in 'strict' mode!".format(len(warnings))
        )

    return cfg