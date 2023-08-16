#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse

from ...domain.actions import Action
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def delete(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    action = Action.from_name(
        name=args.name,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    action.delete()
    print(f"Deleted action {args.name}")


def delete_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=True,
        action="store",
        help="Exact name of action.",
    )
    add_org_arg(parser=parser)


delete_command = RobotoCommand(
    name="delete",
    logic=delete,
    setup_parser=delete_parser,
    command_kwargs={"help": "Delete action and all of its related subresources."},
)
