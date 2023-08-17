# Copyright (c) 2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for the OpenTestFactory config."""


import argparse
import inspect
import os

from logging.config import dictConfig

import yaml


########################################################################

NOTIFICATION_LOGGER_EXCLUSIONS = 'eventbus'


########################################################################


class ConfigError(Exception):
    """Invalid configuration file."""


def make_argparser(description: str, configfile: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--manifest', help='alternate manifest file')
    parser.add_argument(
        '--config', help=f'alternate config file (default to {configfile})'
    )
    parser.add_argument('--context', help='alternative context')
    parser.add_argument('--host', help='alternative host')
    parser.add_argument('--port', help='alternative port')
    parser.add_argument(
        '--ssl_context', '--ssl-context', help='alternative ssl context'
    )
    parser.add_argument(
        '--trusted_authorities',
        '--trusted-authorities',
        help='alternative trusted authorities',
    )
    parser.add_argument(
        '--enable_insecure_login',
        '--enable-insecure-login',
        action='store_true',
        help='enable insecure login (disabled by default)',
    )
    parser.add_argument(
        '--insecure_bind_address',
        '--insecure-bind-address',
        help='insecure bind address (127.0.0.1 by default)',
        default='127.0.0.1',
    )
    parser.add_argument(
        '--authorization_mode',
        '--authorization-mode',
        help='authorization mode, JWT without RBAC if unspecified',
    )
    parser.add_argument(
        '--authorization_policy_file',
        '--authorization-policy-file',
        help='authorization policies for ABAC',
    )
    parser.add_argument(
        '--token_auth_file',
        '--token-auth-file',
        help='authenticated users for ABAC and RBAC',
    )
    parser.add_argument(
        '--trustedkeys_auth_file',
        '--trustedkeys-auth-file',
        help='authenticated trusted keys for ABAC and RBAC',
    )
    return parser


def configure_logging(name: str, debug_level: str) -> None:
    logging_conf = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in {name}: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            },
        },
        'root': {
            'level': debug_level,
            'handlers': ['wsgi'],
        },
    }
    if name not in NOTIFICATION_LOGGER_EXCLUSIONS:
        logging_conf['handlers']['eventbus'] = {
            'class': 'opentf.commons.EventbusLogger',
            'formatter': 'default',
        }
        logging_conf['root']['handlers'] += ['eventbus']
    dictConfig(logging_conf)


def read_configfile(argsconfig, configfile: str):
    try:
        configfile = argsconfig or configfile
        with open(configfile, 'r', encoding='utf-8') as cnf:
            config = yaml.safe_load(cnf)
        return configfile, config
    except Exception as err:
        raise ConfigError(f'Could not get configfile "{configfile}", aborting: {err}.')


def read_manifest(argsmanifest, manifest):
    try:
        if argsmanifest:
            manifestfile = argsmanifest
        else:
            for frame in inspect.stack():
                if frame.frame.f_code.co_name == '<module>':
                    break
            else:
                raise ConfigError('Could not get module location, aborting.')
            manifestfile = os.path.join(
                os.path.dirname(frame.filename),
                manifest or 'service.yaml',
            )
        with open(manifestfile, 'r', encoding='utf-8') as definition:
            manifest = list(yaml.safe_load_all(definition))
        return manifestfile, manifest
    except Exception as err:
        raise ConfigError(f'Could not get manifest "{manifestfile}", aborting: {err}.')
