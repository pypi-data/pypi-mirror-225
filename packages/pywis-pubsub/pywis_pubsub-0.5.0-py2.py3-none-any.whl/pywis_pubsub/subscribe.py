###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import json
import logging

import click

from pywis_pubsub import cli_options
from pywis_pubsub import util
from pywis_pubsub.geometry import is_message_within_bbox
from pywis_pubsub.hook import load_hook
from pywis_pubsub.message import get_canonical_link, get_data
from pywis_pubsub.mqtt import MQTTPubSubClient
from pywis_pubsub.storage import STORAGES
from pywis_pubsub.validation import validate_message
from pywis_pubsub.verification import data_verified


LOGGER = logging.getLogger(__name__)


def on_message_handler(client, userdata, msg):
    """message handler"""

    LOGGER.debug(f'Topic: {msg.topic}')
    LOGGER.debug(f'Message:\n{msg.payload}')

    msg_dict = json.loads(msg.payload)

    try:
        if userdata.get('validate_message', False):
            LOGGER.debug('Validating message')
            success, err = validate_message(msg_dict)
            if not success:
                LOGGER.error(f'Message is not a valid notification: {err}')
                return
    except RuntimeError as err:
        LOGGER.error(f'Cannot validate message: {err}')
        return

    if userdata.get('bbox') and msg_dict.get('geometry') is not None:
        LOGGER.debug('Performing spatial filtering')
        if not bool(msg_dict['geometry']):
            LOGGER.error(f"Invalid geometry: {msg_dict['geometry']}")
            return
        if is_message_within_bbox(msg_dict['geometry'], userdata['bbox']):
            LOGGER.debug('Message geometry is within bbox')
        else:
            LOGGER.debug('Message geometry not within bbox; skipping')
            return

    clink = get_canonical_link(msg_dict['links'])
    LOGGER.info(f"Received message with data URL: {clink['href']}")

    if userdata.get('storage') is not None:
        LOGGER.debug('Saving data')
        try:
            LOGGER.debug('Downloading data')
            data = get_data(msg_dict, userdata.get('verify_certs'))
        except Exception as err:
            LOGGER.error(err)
            return
        if ('integrity' in msg_dict['properties'] and
                userdata.get('verify_data', True)):
            LOGGER.debug('Verifying data')

            method = msg_dict['properties']['integrity']['method']
            value = msg_dict['properties']['integrity']['value']
            if 'content' in msg_dict['properties']:
                size = msg_dict['properties']['content']['size']
            else:
                size = clink['length']

            LOGGER.debug(method)
            if not data_verified(data, size, method, value):
                LOGGER.error('Data verification failed; not saving')
                return
            else:
                LOGGER.debug('Data verification passed')

        filename = msg_dict['properties']['data_id']

        storage_class = STORAGES[userdata.get('storage').get('type')]
        storage_object = storage_class(userdata['storage'])
        storage_object.save(data, filename)

    if userdata.get('hook') is not None:
        LOGGER.debug(f"Hook detected: {userdata['hook']}")
        try:
            hook = load_hook(userdata['hook'])
            LOGGER.debug('Executing hook')
            hook.execute(msg_dict)
        except Exception as err:
            msg = f'Hook failed: {err}'
            LOGGER.error(msg, exc_info=True)


@click.command()
@click.pass_context
@cli_options.OPTION_CONFIG
@cli_options.OPTION_VERBOSITY
@click.option('--bbox', '-b', help='Bounding box filter')
@click.option('--download', '-d', is_flag=True, help='Download data')
def subscribe(ctx, config, download, bbox=[], verbosity='NOTSET'):
    """Subscribe to a broker/topic and optionally download data"""

    if config is None:
        raise click.ClickException('missing --config')
    config = util.yaml_load(config)

    broker = config.get('broker')
    qos = int(config.get('qos', 1))
    subscribe_topics = config.get('subscribe_topics', [])
    verify_certs = config.get('verify_certs', True)

    options = {
        'verify_certs': verify_certs
    }

    if bbox:
        options['bbox'] = [float(i) for i in bbox.split(',')]

    if download:
        options['storage'] = config['storage']

    options['verify_data'] = config.get('verify_data', True)
    options['validate_message'] = config.get('validate_message', False)
    options['hook'] = config.get('hook')

    client = MQTTPubSubClient(broker, options)
    client.bind('on_message', on_message_handler)
    click.echo(f'Connected to broker {client.broker_safe_url}')
    click.echo(f'Subscribing to subscribe_topics {subscribe_topics}')
    client.sub(subscribe_topics, qos)
