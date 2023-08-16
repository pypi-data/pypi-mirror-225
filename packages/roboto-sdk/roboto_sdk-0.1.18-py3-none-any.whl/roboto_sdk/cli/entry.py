#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import logging
import pathlib
import sys
from typing import Any, Optional

from ..domain.actions import (
    ActionHttpDelegate,
    InvocationHttpDelegate,
)
from ..domain.datasets import DatasetHttpDelegate
from ..domain.files import FileClientDelegate
from ..domain.orgs import OrgHttpDelegate
from ..domain.tokens import TokenHttpDelegate
from ..domain.triggers import TriggerHttpDelegate
from ..domain.users import UserHttpDelegate
from ..http import (
    HttpClient,
    LocalAuthDecorator,
    PATAuthDecorator,
)
from ..profile import RobotoProfile
from .actions import (
    command_set as actions_command_set,
)
from .context import CLIContext
from .datasets import (
    command_set as datasets_command_set,
)
from .invocations import (
    command_set as invocations_command_set,
)
from .orgs import command_set as orgs_command_set
from .tokens import (
    command_set as tokens_command_set,
)
from .triggers import (
    command_set as triggers_command_set,
)
from .users import (
    command_set as users_command_set,
)

COMMAND_SETS = [
    actions_command_set,
    datasets_command_set,
    invocations_command_set,
    orgs_command_set,
    users_command_set,
    tokens_command_set,
    triggers_command_set,
]

BETA_USER_POOL_CLIENT_ID = "7p2e45lijin58tuaairtflf3m8"
PROD_USER_POOL_CLIENT_ID = "1gricmdmh0vv582qdd84phab5"


def __populate_context(args, context: CLIContext):
    profile = (
        RobotoProfile(default_profile_name=args.profile)
        if args.config_file is None
        else RobotoProfile(
            config_file=args.config_file, default_profile_name=args.profile
        )
    )

    profile_entry = profile.get_entry()

    http_client_args: dict[str, Any] = {
        "default_endpoint": profile_entry.default_endpoint
    }

    if "localhost" not in profile_entry.default_endpoint:
        http_client_args["default_auth"] = PATAuthDecorator.for_client(
            client_id=profile_entry.default_client_id, profile=profile
        )
    else:
        http_client_args["default_auth"] = LocalAuthDecorator(
            user_id=profile_entry.user_id
        )

    http = HttpClient(**http_client_args)  # type: ignore[arg-type]

    context.actions = ActionHttpDelegate(
        http_client=http, roboto_service_base_url=profile_entry.default_endpoint
    )
    context.datasets = DatasetHttpDelegate(
        http_client=http, roboto_service_base_url=profile_entry.default_endpoint
    )
    context.files = FileClientDelegate(
        http_client=http, roboto_service_base_url=profile_entry.default_endpoint
    )
    context.invocations = InvocationHttpDelegate(
        http_client=http, roboto_service_base_url=profile_entry.default_endpoint
    )
    context.orgs = OrgHttpDelegate(http_client=http)
    context.triggers = TriggerHttpDelegate(http_client=http)
    context.users = UserHttpDelegate(http_client=http)
    context.http = http
    context.tokens = TokenHttpDelegate(http_client=http)


def construct_parser(context: Optional[CLIContext] = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="roboto",
        description=(
            "Top level CLI for interacting with Roboto's public API."
            "These are a combination of thin wrappers around REST calls, and higher level conveinence utilities which "
            "compose multiple calls and may have some additional client side logic."
            "Each of the command groups listed below have their own set of supported actions and their own help pages."
        ),
    )

    parser.add_argument(
        "--debug", help="Sets the log level to DEBUG", action="store_true"
    )

    parser.add_argument(
        "--profile",
        help="Which Roboto profile to use; must match a section within the Roboto config.json.",
        required=False,
    )

    parser.add_argument(
        "--config-file",
        help="Overrides the location of the roboto config.json file. Defaults to ~/.roboto/config.json",
        type=pathlib.Path,
        required=False,
    )

    # https://bugs.python.org/issue29298
    subcommands = parser.add_subparsers(dest="function")
    subcommands.required = True

    for command_set in COMMAND_SETS:
        command_set.add_to_subparsers(subcommands, context)

    return parser


def entry():
    logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

    context = CLIContext()
    parser = construct_parser(context)

    args = parser.parse_args()
    __populate_context(args, context)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.ERROR)

    args.func(args)
