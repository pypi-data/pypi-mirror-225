#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import typing

from ...domain.actions import Invocation
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def invocation_serializer(obj: typing.Any) -> typing.Any:
    if isinstance(obj, Invocation):
        return {
            "invocation_id": obj.id,
            "created": obj.created.isoformat(),
            "status": str(obj.current_status),
        }

    # The default behavior for json.dumps(default=) is to throw a TypeError
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def list_invocations(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    matching_invocations = Invocation.query(
        {"action_name": args.name},
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    sorted_invocations = sorted(
        matching_invocations, key=lambda invocation: invocation.created.timestamp()
    )
    print(json.dumps(sorted_invocations, indent=2, default=invocation_serializer))


def list_invocations_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=False,
        action="store",
        help="If querying by action name, must provide an exact match; patterns are not accepted.",
    )
    add_org_arg(parser=parser)


list_invocations_command = RobotoCommand(
    name="list-invocations",
    logic=list_invocations,
    setup_parser=list_invocations_parser,
    command_kwargs={"help": "List invocations for action."},
)
