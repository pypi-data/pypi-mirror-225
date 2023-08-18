# Copyright 2021-2023 Henix, henix.fr
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

"""opentf-ctl"""

from typing import Any, Dict, List, Union

import json
import sys

from datetime import datetime

import jwt

from opentf.tools.ctlcommons import (
    _make_params_from_selectors,
    _ensure_options,
    _is_command,
    _error,
    _warning,
    generate_output,
    _get_arg,
    _ensure_uuid,
)
from opentf.tools.ctlconfig import (
    read_configuration,
    config_cmd,
    print_config_help,
    CONFIG,
)
from opentf.tools.ctlnetworking import (
    _eventbus,
    _agentchannel,
    _observer,
    _get,
    _delete,
)
from opentf.tools.ctlworkflows import print_workflow_help, workflow_cmd
from opentf.tools.ctlqualitygate import print_qualitygate_help, qualitygate_cmd

########################################################################

# pylint: disable=broad-except

DEFAULT_NAMESPACE = 'default'


########################################################################
# Help messages

GETNAMESPACES_COMMAND = 'get namespaces'
GETSUBSCRIPTIONS_COMMAND = 'get subscriptions'
DELETESUBSCRIPTION_COMMAND = 'delete subscription _'
GETAGENTS_COMMAND = 'get agents'
DELETEAGENT_COMMAND = 'delete agent _'
GETCHANNELS_COMMAND = 'get channels'

GENERAL_HELP = '''opentf-ctl controls the OpenTestFactory orchestrators.

Find more information at: https://opentestfactory.org/tools/running-commands

Basic Commands:
  get workflows                    List active and recent workflows
  run workflow {filename}          Start a workflow
  get workflow {workflow_id}       Get a workflow status
  kill workflow {workflow_id}      Cancel a running workflow

Agent Commands:
  get agents                       List registered agents
  delete agent {agent_id}          De-register an agent

Channel Commands:
  get channels                     List known channels

Qualitygate Commands:
  get qualitygate {workflow_id}    Get quality gate status for a workflow
  describe qualitygate {workflow_id}
                                   Get description of a quality gate status for a workflow

Token Commands:
  generate token using {key}       Interactively generate a signed token
  check token {token} using {key}  Check if token signature matches public key
  view token {token}               Show token payload

Advanced Commands:
  get namespaces                   List accessible namespaces
  get subscriptions                List active subscriptions
  delete subscription {sub_id}     Cancel an active subscription

Other Commands:
  config                           Modify current opentf-tools configuration
  version                          List the tools version

Usage:
  opentf-ctl <command> [options]

Use "opentf-ctl <command> --help" for more information about a given command.
Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

OPTIONS_HELP = '''
The following environment variables override the defaults, if not overridden by options:

  OPENTF_CONFIG: Path to the opentfconfig file to use for CLI requests
  OPENTF_TOKEN: Bearer token for authentication to the orchestrator

The following options can be passed to any command:

  --token='': Bearer token for authentication to the orchestrator
  --user='': The name of the opentfconfig user to use
  --orchestrator='': The name of the opentfconfig orchestrator to use
  --context='': The name of the opentfconfig context to use
  --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity.  This will make your HTTPS connections insecure
  --opentfconfig='': Path to the opentfconfig file to use for CLI requests
'''

VERSION_HELP = '''
List the tools version

Example:
  # Display the version of the tools
  opentf-ctl version

Usage:
  opentf-ctl version [options]

Options:
  --debug: show additional information.

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_SUBSCRIPTIONS_HELP = '''List active subscriptions on the eventbus

Example:
  # List the subscriptions
  opentf-ctl get subscriptions

  # List the subscriptions with more details
  opentf-ctl get subscriptions --output=wide

  # Get just the subscription names and IDs
  opentf-ctl get subscriptions --output=custom-columns=NAME:.metadata.name,ID:.metadata.subscription_id

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)

Usage:
  opentf-ctl get subscriptions [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DELETE_SUBSCRIPTION_HELP = '''Remove an active subscription from the eventbus

Example:
  # Delete a subscription
  opentf-ctl delete subscription 8947945a-a8ac-4c94-803a-6a226d74ce4a

Usage:
  opentf-ctl delete subscription SUBSCRIPTION_ID [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_CHANNELS_HELP = '''List known channels

Example:
  # List the channels
  opentf-ctl get channels

  # List the channels with more details
  opentf-ctl get channels --output=wide

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)

Usage:
  opentf-ctl get channels [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_NAMESPACES_HELP = '''List accessible namespaces

Example:
  # List the namespaces the current user can access
  opentf-ctl get namespaces

  # List the namespaces the current user can run workflows on
  opentf-ctl get namespaces --selector=resource==workflows,verb==create

Options:
  --selector= or -l=: selector (query) to filter on, supports 'resource==' and 'verb==', both required when specifying a selector.

Usage:
  opentf-ctl get namespaces [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_AGENTS_HELP = '''List registered agents

Example:
  # List the agents
  opentf-ctl get agents

  # List the agents with more details
  opentf-ctl get agents --output=wide

  # Get just the agent IDs
  opentf-ctl get agents --output=custom-columns=ID:.metadata.agent_id

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)

Usage:
  opentf-ctl get agents [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DELETE_AGENT_HELP = '''De-register an active agent

Example:
  # De-register the specified agent
  opentf-ctl delete agent 9ea3be45-ee90-4135-b47f-e66e4f793383

Usage:
  opentf-ctl delete agent AGENT_ID [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GENERATE_TOKEN_HELP = '''Generate a signed token

Example:
  # Generate token interactively
  opentf-ctl generate token using path/to/private.pem

Usage:
  opentf-ctl generate token using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

VIEW_TOKEN_HELP = '''View token payload

Example:
  # Display token payload
  opentf-ctl view token $TOKEN

Usage:
  opentf-ctl view token TOKEN [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

VALIDATE_TOKEN_HELP = '''Validate token signature

Example:
  # Validate token
  opentf-ctl check token $TOKEN using path/to/public.pum

Usage:
  opentf-ctl check token TOKEN using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Subscriptions


SUBSCRIPTION_COLUMNS = (
    'NAME:.metadata.name',
    'ENDPOINT:.spec.subscriber.endpoint',
    'CREATION:.metadata.creationTimestamp',
    'COUNT:.status.publicationCount',
    'SUBSCRIPTIONS:.metadata.annotations.*',
)

WIDE_SUBSCRIPTION_COLUMNS = (
    'ID:.metadata.subscription_id',
    'NAME:.metadata.name',
    'ENDPOINT:.spec.subscriber.endpoint',
    'CREATION:.metadata.creationTimestamp',
    'COUNT:.status.publicationCount',
    'SUBSCRIPTIONS:.metadata.annotations.*',
)


def _get_subscriptions() -> Dict[str, Any]:
    return _get(_eventbus(), '/subscriptions', 'Could not get subscriptions list')[
        'items'
    ]


def list_subscriptions() -> None:
    """List all active subscriptions.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    generate_output(
        list(_get_subscriptions().values()),
        SUBSCRIPTION_COLUMNS,
        WIDE_SUBSCRIPTION_COLUMNS,
    )


def delete_subscription(subscription_id: str) -> None:
    """Cancel a subscription."""
    subscription_id = _ensure_uuid(subscription_id, _get_subscriptions)
    what = _delete(
        _eventbus(),
        f'/subscriptions/{subscription_id}',
        'Could not delete subscription',
    )
    print(what['message'])


# Channels

CHANNEL_COLUMNS = (
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'LAST_REFRESH_TIMESTAMP:.status.lastCommunicationTimestamp',
    'STATUS:.status.phase',
)

WIDE_CHANNEL_COLUMNS = (
    'HANDLER_ID:.metadata.channelhandler_id',
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'LAST_REFRESH_TIMESTAMP:.status.lastCommunicationTimestamp',
    'STATUS:.status.phase',
)


def list_channels() -> None:
    """List all active agents.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    what = _get(
        _observer(),
        '/channels',
        'Could not get channels list',
        params=_make_params_from_selectors(),
    )

    generate_output(what['details']['items'], CHANNEL_COLUMNS, WIDE_CHANNEL_COLUMNS)


# Namepaces


def list_namespaces() -> None:
    """List namespaces.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    resource = verb = None
    selector = _get_arg('--selector=') or _get_arg('-l=')
    if selector:
        if len(selector.split(',')) != 2:
            _error(
                'Invalid selector, must be of form: "resource==resource,verb==verb", got: %s.',
                selector,
            )
            sys.exit(2)
        for item in selector.split(','):
            what, _, value = item.partition('=')
            if what == 'resource':
                resource = value.lstrip('=').strip()
            elif what == 'verb':
                verb = value.lstrip('=').strip()
            else:
                _error(
                    'Invalid selector, expecting "resource" or "verb", got: %s.', what
                )
                sys.exit(2)
    if (resource and not verb) or (verb and not resource):
        _error('Incomplete selector, expecting both "resource" and "verb".')
        sys.exit(2)

    url = '/namespaces'
    if resource and verb:
        url += f'?resource={resource}&verb={verb}'
    what = _get(_observer(), url, 'Could not get namespaces list')
    if 'details' not in what or 'items' not in what['details']:
        _error('Unexpected response: %s', what)
        sys.exit(2)
    namespaces = what['details']['items']
    print('NAMESPACE')
    if '*' in namespaces:
        print('*')
    else:
        for ns in namespaces:
            print(ns)


# Agents

AGENT_COLUMNS = (
    'AGENT_ID:.metadata.agent_id',
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'REGISTRATION_TIMESTAMP:.metadata.creationTimestamp',
    'LAST_SEEN_TIMESTAMP:.status.lastCommunicationTimestamp',
    'RUNNING_JOB:.status.currentJobID',
)


def _get_agents():
    what = _get(_agentchannel(), '/agents', 'Could not get agents list')
    data = what['items']

    # pre-2022-05 orchestrators where returning a dictionary, not a list
    # of manifests.
    if isinstance(data, dict):
        data = []
        for agent_id, manifest in what['items'].items():
            manifest['metadata']['agent_id'] = agent_id
            data.append(manifest)
    return data


def list_agents() -> None:
    """List all active agents.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    generate_output(_get_agents(), AGENT_COLUMNS, AGENT_COLUMNS)


def delete_agent(agent_id: str) -> None:
    """Deregister agent."""
    agent_id = _ensure_uuid(
        agent_id, lambda: [agent['metadata']['agent_id'] for agent in _get_agents()]
    )
    what = _delete(
        _agentchannel(), f'/agents/{agent_id}', f'Could not delete agent {agent_id}'
    )
    print(what['message'])


## JWT tokens

ALLOWED_ALGORITHMS = [
    'ES256',  # ECDSA signature algorithm using SHA-256 hash algorithm
    'ES384',  # ECDSA signature algorithm using SHA-384 hash algorithm
    'ES512',  # ECDSA signature algorithm using SHA-512 hash algorithm
    'RS256',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm
    'RS384',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm
    'RS512',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm
    'PS256',  # RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256
    'PS384',  # RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384
    'PS512',  # RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512
]


def generate_token(privatekey: str) -> None:
    """Generate JWT token.

    # Required parameters

    - privatekey: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        with open(privatekey, 'r', encoding='utf-8') as keyfile:
            pem = keyfile.read()
    except FileNotFoundError:
        _error('The specified private key could not be found: %s.', privatekey)
        sys.exit(2)

    algorithm = (
        input('Please specify an algorithm (RS512 if unspecified): ').strip() or 'RS512'
    )
    print('The specified algorithm is:', algorithm)
    while not (
        issuer := input(
            'Please enter the issuer (your company or department): '
        ).strip()
    ):
        _warning('The issuer cannot be empty.')
    while not (
        subject := input(
            'Please enter the subject (you or the person you are making this token for): '
        )
    ):
        _warning('The subject cannot be empty.')
    exp = (
        input(
            'Please specify an expiration date in YYYY/MM/DD format (never if unspecified): '
        ).strip()
        or None
    )
    if exp:
        try:
            exp = int(datetime.strptime(exp, '%Y/%m/%d').timestamp())
        except ValueError:
            _error('Invalid expiration date format, must be YYYY/MM/DD.')
            sys.exit(2)

    try:
        payload: Dict[str, Union[str, int]] = {'iss': issuer, 'sub': subject}
        if exp:
            payload['exp'] = exp
        token = jwt.encode(payload, pem, algorithm=algorithm)
    except NotImplementedError:
        _error('Algorithm not supported: %s.', algorithm)
        sys.exit(2)
    except Exception as err:
        _error('Could not generate token: %s.', err)
        sys.exit(2)

    print('The signed token is:')
    print(token)


def view_token(token: str) -> None:
    """View JWT token payload.

    # Required parameters

    - token: a non-empty string (a JWT token)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        print('The token payload is:')
        if 'exp' in payload:
            payload['exp'] = datetime.fromtimestamp(payload['exp']).strftime('%Y/%m/%d')
        print(payload)
    except Exception as err:
        _error('The specified token is invalid: %s', err)
        print(token)
        sys.exit(2)


def check_token(token: str, keyname: str) -> None:
    """Check JWT token signature.

    # Required parameters

    - token: a non-empty string (a JWT token)
    - keyname: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        with open(keyname, 'r', encoding='utf-8') as keyfile:
            key = keyfile.read()
    except FileNotFoundError:
        _error('The specified public key could not be found: %s.', keyname)
        sys.exit(2)

    try:
        payload = jwt.decode(token, key, algorithms=ALLOWED_ALGORITHMS)
        print(
            f'The token is signed by the {keyname} public key.  The token payload is:'
        )
        print(payload)
    except jwt.exceptions.InvalidSignatureError:
        _error('The token is not signed by %s.', keyname)
        sys.exit(102)
    except AttributeError as err:
        _error(
            'The specified key does not looks like a public key.'
            + '  Got "%s" while reading the provided key.',
            err,
        )
        sys.exit(2)
    except ValueError as err:
        _error(err.args[0])
        sys.exit(2)
    except Exception as err:
        _error('Could not validate token signature: %s.', err)
        sys.exit(2)


## version


def get_tools_version() -> None:
    """
    Prints in the console the current version details.
    """

    from importlib.metadata import version
    from pkg_resources import parse_version

    fullversion = parse_version(version('opentf-tools'))
    major = fullversion.base_version.split('.')[0]
    minor = fullversion.base_version.split('.')[1]
    print(
        f'Tools Version: version.Info{{Major:"{major}", Minor: "{minor}", FullVersion: "{fullversion}"}}'
    )


def get_orchestrator_version(debug: bool) -> None:
    """
    Parses and prints in console the content of orchestrator's image BOM
    (Bill of materials) file, namely components names and versions.
    """
    print('Orchestrator:')
    print(f'    Orchestrator server: {CONFIG["orchestrator"]["server"]}')
    bom = _get(_observer(), '/version', 'Could not get BOM details.')
    bom_items = bom['details']['items']
    if 'error' in bom_items.keys():
        _error(bom_items['error'])
        return
    print(f'Components of {bom_items["name"]} image:')
    if debug:
        print(json.dumps(bom_items, indent=2))
        return
    for version in [
        f"{item['name']}: {item['version']}"
        for key, value in bom_items.items()
        for item in value
        if key != 'name'
    ]:
        print('   ', version)


########################################################################
# Helpers


def print_help(args: List[str]) -> None:
    """Display help."""
    if _is_command('options', args):
        print(OPTIONS_HELP)
    if _is_command('version', args):
        print(VERSION_HELP)
    elif _is_command(GETSUBSCRIPTIONS_COMMAND, args):
        print(GET_SUBSCRIPTIONS_HELP)
    elif _is_command('delete subscription', args):
        print(DELETE_SUBSCRIPTION_HELP)
    elif _is_command('generate token', args):
        print(GENERATE_TOKEN_HELP)
    elif _is_command('view token', args):
        print(VIEW_TOKEN_HELP)
    elif _is_command('check token', args):
        print(VALIDATE_TOKEN_HELP)
    elif _is_command(GETAGENTS_COMMAND, args):
        print(GET_AGENTS_HELP)
    elif _is_command(GETCHANNELS_COMMAND, args):
        print(GET_CHANNELS_HELP)
    elif _is_command('delete agent', args):
        print(DELETE_AGENT_HELP)
    elif _is_command('config', args):
        print_config_help(args)
    elif _is_command('_ workflow', args) or _is_command('_ workflows', args):
        print_workflow_help(args)
    elif _is_command('get qualitygate', args) or _is_command(
        'describe qualitygate', args
    ):
        print_qualitygate_help(args)
    elif _is_command(GETNAMESPACES_COMMAND, args):
        print(GET_NAMESPACES_HELP)
    elif len(args) == 2:
        print(GENERAL_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


########################################################################
# Main


def main():
    """Process command."""
    if len(sys.argv) == 1:
        print(GENERAL_HELP)
        sys.exit(1)
    if sys.argv[-1] == '--help':
        print_help(sys.argv)
        sys.exit(0)

    if _is_command('options', sys.argv):
        print(OPTIONS_HELP)
        sys.exit(0)

    if _is_command('version', sys.argv):
        _ensure_options('version', sys.argv[1:], flags=[('--debug',)])
        get_tools_version()
        read_configuration()
        get_orchestrator_version('--debug' in sys.argv)
        sys.exit(0)

    if _is_command('generate token using _', sys.argv):
        if len(sys.argv) > 5:
            _error(
                f'"opentf-ctl generate token" does not take options.  Got "{" ".join(sys.argv[5:])}".'
            )
            sys.exit(2)
        generate_token(sys.argv[4])
        sys.exit(0)
    if _is_command('view token _', sys.argv):
        if len(sys.argv) > 4:
            _error(
                f'"opentf-ctl view token" does not take options.  Got "{" ".join(sys.argv[4:])}".'
            )
            sys.exit(2)
        view_token(sys.argv[3])
        sys.exit(0)
    if _is_command('check token _ using _', sys.argv):
        if len(sys.argv) > 6:
            _error(
                f'"opentf-ctl check token" does not take options.  Got "{" ".join(sys.argv[6:])}".'
            )
            sys.exit(2)
        check_token(sys.argv[3], sys.argv[5])
        sys.exit(0)
    if _is_command('check token _', sys.argv):
        _error('Missing required parameter.  Use "check token --help" for details.')
        sys.exit(2)
    if _is_command(GETNAMESPACES_COMMAND, sys.argv):
        _ensure_options(
            GETNAMESPACES_COMMAND, sys.argv[1:], extra=[('--selector', '-l')]
        )
        read_configuration()
        list_namespaces()
    elif _is_command(GETSUBSCRIPTIONS_COMMAND, sys.argv):
        _ensure_options(
            GETSUBSCRIPTIONS_COMMAND, sys.argv[1:], extra=[('--output', '-o')]
        )
        read_configuration()
        list_subscriptions()
    elif _is_command(DELETESUBSCRIPTION_COMMAND, sys.argv):
        subscription_id = _ensure_options(DELETESUBSCRIPTION_COMMAND, sys.argv[1:])
        read_configuration()
        delete_subscription(subscription_id)
    elif _is_command(GETAGENTS_COMMAND, sys.argv):
        _ensure_options(GETAGENTS_COMMAND, sys.argv[1:], extra=[('--output', '-o')])
        read_configuration()
        list_agents()
    elif _is_command(GETCHANNELS_COMMAND, sys.argv):
        _ensure_options(
            GETCHANNELS_COMMAND,
            sys.argv[1:],
            extra=[('--output', '-o'), ('--field-selector', '--selector', '-l')],
        )
        read_configuration()
        list_channels()
    elif _is_command(DELETEAGENT_COMMAND, sys.argv):
        agent_id = _ensure_options(DELETEAGENT_COMMAND, sys.argv[1:])
        read_configuration()
        delete_agent(agent_id)
    elif _is_command('_ workflow', sys.argv) or _is_command('_ workflows', sys.argv):
        workflow_cmd()
    elif _is_command('get qualitygate', sys.argv) or _is_command(
        'describe qualitygate', sys.argv
    ):
        qualitygate_cmd()
    elif _is_command('config', sys.argv):
        config_cmd()
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


if __name__ == '__main__':
    main()
