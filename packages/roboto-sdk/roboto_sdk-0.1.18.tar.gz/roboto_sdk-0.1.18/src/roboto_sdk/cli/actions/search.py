#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.actions import Action
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import add_org_arg
from ..context import CLIContext


def search(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    filters = dict()
    if args.name:
        filters["name"] = args.name

    if args.metadata:
        filters["metadata"] = args.metadata

    if args.tag:
        filters["tags"] = args.tag

    matching_actions = Action.query(
        filters,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    print(json.dumps([action.to_dict() for action in matching_actions], indent=4))


def search_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=False,
        action="store",
        help="If querying by action name, must provide an exact match; patterns are not accepted.",
    )
    parser.add_argument(
        "--metadata",
        required=False,
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key=value' format key/value pairs which represent action metadata. "
            "`value` is parsed as JSON. "
        ),
    )
    parser.add_argument(
        "--tag",
        required=False,
        type=str,
        nargs="*",
        help="One or more tags associated with this action.",
        action="extend",
    )
    add_org_arg(parser=parser)


search_command = RobotoCommand(
    name="search",
    logic=search,
    setup_parser=search_parser,
    command_kwargs={"help": "Search for existing actions."},
)
