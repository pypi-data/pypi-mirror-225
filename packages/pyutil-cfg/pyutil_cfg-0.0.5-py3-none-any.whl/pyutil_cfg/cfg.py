# -*- coding: utf-8 -*-

from configparser import SafeConfigParser
import logging
import logging.config

import json


def init(name, ini_filename, log_ini_filename='', params=None):
    logger = _init_logger(name, log_ini_filename, ini_filename)
    config = _init_ini_file(name, ini_filename, logger)
    config = _post_init_config(params, config, logger)

    logger.debug('pyutil_cfg: to return: name: %s logger: %s config: %s', name, logger, config)

    return logger, config


def _init_logger(name, log_ini_filename, ini_filename):
    logger = logging.getLogger(name)

    if not log_ini_filename:
        log_ini_filename = ini_filename

    if not log_ini_filename:
        return None

    try:
        logging.config.fileConfig(log_ini_filename, disable_existing_loggers=False)
    except:
        pass

    return logger


def _init_ini_file(name, ini_filename, logger):
    '''
    setup name:main config
    '''
    section = name + ':main'

    config = _init_ini_file_core(ini_filename, section, logger)

    return config


def _init_ini_file_core(ini_filename, section, logger):
    '''
    get ini conf from section
    return: config: {key: val} val: json_loaded
    '''
    if not ini_filename:
        return {}

    config_parser = SafeConfigParser()
    config_parser.read(ini_filename)
    sections = config_parser.sections()
    if section not in sections:
        return {}

    options = config_parser.options(section)
    config = {option: _init_ini_file_parse_option(option, section, config_parser, logger) for option in options}

    return config


def _init_ini_file_parse_option(option, section, config_parser, logger):
    try:
        val = config_parser.get(section, option)
    except Exception as e:
        logger.exception('unable to get option: section: %s option: %s e: %s', section, option, e)
        val = ''
    return _init_ini_file_val_to_json(option, val)


def _init_ini_file_val_to_json(option, val):
    '''
    try to do json load on value
    '''

    if val.__class__.__name__ != 'str':
        return val

    orig_v = val
    try:
        val = json.loads(val)
    except:
        val = orig_v

    if option.endswith('_set'):
        val = set(val)

    return val


def _post_init_config(params, config, logger):
    '''
    add additional parameters into config
    '''

    if not params:
        return config

    for (k, v) in params.items():
        if k in config:
            logger.warning('config will be overwritten by params: key: %s origin: %s new: %s', k, config[k], v)

    config.update(params)

    return config
