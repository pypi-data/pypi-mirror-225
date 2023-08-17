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

"""Helpers for the OpenTestFactory subscription and publication API."""

from typing import Any, Dict, Optional

import sys

from datetime import datetime


import requests


########################################################################
# Publishers & Subscribers Helpers

DEFAULT_TIMEOUT_SECONDS = 10


def make_event(schema: str, **kwargs) -> Dict[str, Any]:
    """Return a new event dictionary.

    # Required parameters

    - schema: a string

    # Optional parameters

    A series of key=values

    # Returned value

    A dictionary.
    """
    apiversion, kind = schema.rsplit('/', 1)
    return {'apiVersion': apiversion, 'kind': kind, **kwargs}


def make_subscription(
    name: str, selector: Dict[str, Any], target: str, context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a subscription manifest.

    # Required parameter

    - name: a string
    - selector: a dictionary
    - target: a string
    - context: a dictionary

    # Returned value

    A _subscription manifest_.  A subscription manifest is a dictionary
    with the following entries:

    - apiVersion: a string
    - kind: a string
    - metadata: a dictionary
    - spec: a dictionary

    `metadata` has two entries: `name` and `timestamp`.

    `spec` has two entries: `selector` and `subscriber`.
    """
    protocol = 'https' if context.get('ssl_context') != 'disabled' else 'http'
    hostname = context['eventbus'].get('hostname', context['host'])
    subscriber = {'endpoint': f'{protocol}://{hostname}:{context["port"]}/{target}'}
    return {
        'apiVersion': 'opentestfactory.org/v1alpha1',
        'kind': 'Subscription',
        'metadata': {'name': name, 'creationTimestamp': datetime.now().isoformat()},
        'spec': {'selector': selector, 'subscriber': subscriber},
    }


def subscribe(
    kind: str,
    target: str,
    app,
    labels: Optional[Dict[str, Any]] = None,
    fields: Optional[Dict[str, Any]] = None,
) -> str:
    """Subscribe on specified endpoint.

    `kind` is of form `[apiVersion/]kind`.

    # Required parameters

    - kind: a string
    - target: a string
    - app: a flask app

    # Optional parameters

    - labels: a dictionary
    - fields: a dictionary

    # Returned value

    A _uuid_ (a string).

    # Raised exceptions

    Raise a _SystemExit_ exception (with exit code 1) if the
    subscription fails.
    """
    if '/' in kind:
        apiversion, kind = kind.rsplit('/', 1)
        if fields is None:
            fields = {}
        fields['apiVersion'] = apiversion
    selector: Dict[str, Any] = {'matchKind': kind}
    if labels:
        selector['matchLabels'] = labels
    if fields:
        selector['matchFields'] = fields
    context = app.config['CONTEXT']
    try:
        response = requests.post(
            context['eventbus']['endpoint'] + '/subscriptions',
            json=make_subscription(
                app.name, selector=selector, target=target, context=context
            ),
            headers={'Authorization': f'Bearer {context["eventbus"]["token"]}'},
            verify=not context['eventbus'].get('insecure-skip-tls-verify', False),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
    except Exception as err:
        app.logger.error('Could not subscribe to eventbus: %s.', err)
        sys.exit(1)

    if response.status_code == 201:
        return response.json()['details']['uuid']

    app.logger.error(
        'Could not subscribe to eventbus: got status %d: %s.',
        response.status_code,
        response.text,
    )
    sys.exit(1)


def unsubscribe(subscription_id: str, app) -> requests.Response:
    """Cancel specified subscription

    #  Required parameters

    - subscription_id: a string (an uuid)
    - app: a flask app

    # Returned value

    A `requests.Response` object.
    """
    context = app.config['CONTEXT']
    return requests.delete(
        context['eventbus']['endpoint'] + '/subscriptions/' + subscription_id,
        headers={'Authorization': f'Bearer {context["eventbus"]["token"]}'},
        verify=not context['eventbus'].get('insecure-skip-tls-verify', False),
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )


def publish(publication: Any, context: Dict[str, Any]) -> requests.Response:
    """Publish publication on specified endpoint.

    If `publication` is a dictionary, and if it has a `metadata` entry,
    a `creationTimestamp` sub-entry will be created (or overwritten if
    it already exists).

    # Required parameters

    - publication: an object
    - context: a dictionary

    # Returned value

    A `requests.Response` object.
    """
    if isinstance(publication, dict) and 'metadata' in publication:
        publication['metadata']['creationTimestamp'] = datetime.now().isoformat()
    return requests.post(
        context['eventbus']['endpoint'] + '/publications',
        json=publication,
        headers={'Authorization': f'Bearer {context["eventbus"]["token"]}'},
        verify=not context['eventbus'].get('insecure-skip-tls-verify', False),
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
