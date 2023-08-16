#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import shlex
import subprocess

from ...domain.actions import Action
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def docker_login(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    action = Action.from_name(
        name=args.name,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    credentials = action.get_temporary_container_credentials()
    cmd = f"docker login --username {credentials.username} --password-stdin {credentials.registry_url}"
    docker_login_completed_process = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        check=True,
        input=credentials.password,
        text=True,
    )
    print(docker_login_completed_process.stdout)


def docker_login_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--name",
        required=True,
        action="store",
        help="Name of an action with an associated Docker image.",
    )
    add_org_arg(parser)


docker_login_command = RobotoCommand(
    name="docker-login",
    logic=docker_login,
    setup_parser=docker_login_parser,
    command_kwargs={
        "help": (
            "Temporarily login to Roboto's private, secured Docker image registry. "
            "Requires Docker CLI. Login is valid for 12 hours."
        )
    },
)
