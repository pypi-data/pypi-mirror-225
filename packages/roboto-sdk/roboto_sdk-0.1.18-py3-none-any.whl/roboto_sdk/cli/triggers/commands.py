#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import json
import sys
import textwrap

from ...domain.actions import Action
from ...domain.triggers import Trigger
from ..command import (
    RobotoCommand,
    RobotoCommandSet,
)
from ..common_args import (
    ParseError,
    add_compute_requirements_args,
    add_container_parameters_args,
    add_org_arg,
    parse_compute_requirements,
    parse_container_overrides,
)
from ..context import CLIContext

NAME_PARAM_HELP = "The unique name used to reference a trigger."
ACTION_NAME_PARAM_HELP = (
    "The unique name used to reference an action which a certain trigger invokes."
)


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    action = Action.from_name(
        name=args.action_name,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )

    try:
        compute_requirement_overrides = None
        if args.vcpu is not None or args.memory is not None or args.storage is not None:
            compute_requirement_overrides = parse_compute_requirements(
                args=args,
                default_vcpu=action.compute_requirements.vCPU,
                default_memory=action.compute_requirements.memory,
                default_storage=action.compute_requirements.storage,
            )

        container_overrides = None
        if (
            args.entry_point is not None
            or args.command is not None
            or args.env is not None
            or args.workdir is not None
        ):
            container_overrides = parse_container_overrides(
                args,
                default_entry_point=action.container_parameters.entry_point,
                default_command=action.container_parameters.command,
                default_env_vars=action.container_parameters.env_vars,
                default_workdir=action.container_parameters.workdir,
            )
    except ParseError as exc:
        print(exc.msg, file=sys.stderr)
        return

    record = Trigger.create(
        name=args.name,
        action_name=args.action_name,
        org_id=args.org,
        required_inputs=args.input_data,
        compute_requirement_overrides=compute_requirement_overrides,
        container_parameter_overrides=container_overrides,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        trigger_delegate=context.triggers,
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def create_setup_parser(parser):
    parser.add_argument("--name", type=str, required=True, help=NAME_PARAM_HELP)
    parser.add_argument(
        "--action-name", type=str, required=True, help=ACTION_NAME_PARAM_HELP
    )
    parser.add_argument(
        "--input-data",
        required=True,
        dest="input_data",
        type=str,
        nargs="+",
        action="extend",
        # fmt: off
        help=textwrap.dedent("""\
            One or many file patterns for data to download from the data source. Examples:
                front camera images, "--input-data '**/cam_front/*.jpg'";
                front and rear camera images, "--input-data '**/cam_front/*.jpg' --input-data '**/cam_rear/*.jpg'";
                all data, "--input-data '**/*'"
        """),
        # fmt: on
    )
    add_org_arg(parser=parser)
    add_compute_requirements_args(parser)
    add_container_parameters_args(parser)


def get(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Trigger.from_name(
        name=args.name,
        org_id=args.org,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        trigger_delegate=context.triggers,
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def get_setup_parser(parser):
    parser.add_argument("--name", type=str, required=True, help=NAME_PARAM_HELP)
    add_org_arg(parser=parser)


def search(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = Trigger.query(
        filters=dict(),
        org_id=args.org,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        trigger_delegate=context.triggers,
    )
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def search_setup_parser(parser):
    add_org_arg(parser=parser)


def delete(args, context: CLIContext, parser: argparse.ArgumentParser):
    Trigger.from_name(
        name=args.name,
        org_id=args.org,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        trigger_delegate=context.triggers,
    ).delete()
    sys.stdout.write("Successfully deleted!\n")


def delete_setup_parser(parser):
    parser.add_argument("--name", type=str, required=True, help=NAME_PARAM_HELP)
    add_org_arg(parser=parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={
        "help": "Creates a trigger to automatically invoke some action on datasets when certain criteria are met"
    },
)

get_command = RobotoCommand(
    name="get",
    logic=get,
    setup_parser=get_setup_parser,
    command_kwargs={"help": "Looks up a specific trigger by name"},
)

delete_command = RobotoCommand(
    name="delete",
    logic=delete,
    setup_parser=delete_setup_parser,
    command_kwargs={"help": "Deletes a trigger with a given name"},
)

search_command = RobotoCommand(
    name="search",
    logic=search,
    setup_parser=search_setup_parser,
    command_kwargs={
        "help": "Searches for triggers that match a given condition. Constrained to a single org."
    },
)

commands = [create_command, get_command, delete_command, search_command]

command_set = RobotoCommandSet(
    name="triggers",
    help="Commands for managing triggers which automatically invoke actions on datasets when certain criteria are met",
    commands=commands,
)
