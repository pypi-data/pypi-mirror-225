#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import sys

from ...domain.actions import Action
from ...exceptions import RobotoNotFoundException
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
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
from .shared import (
    finalize_docker_image_registration_instructions,
)


def create(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    if (args.docker_image_name and not args.docker_image_tag) or (
        args.docker_image_tag and not args.docker_image_name
    ):
        raise argparse.ArgumentError(
            argument=None,
            message="Must define both --image-name and --image-tag if either is provided",
        )

    try:
        action = Action.from_name(
            name=args.name,
            action_delegate=context.actions,
            invocation_delegate=context.invocations,
            org_id=args.org,
        )
        print(
            f"Action with name '{args.name}' already exists. To update it, use the 'roboto actions update' command.",
            file=sys.stderr,
        )
        return None
    except RobotoNotFoundException:
        pass  # Swallow

    try:
        compute_requirements = parse_compute_requirements(args)
        container_parameters = parse_container_overrides(args)
    except ParseError as exc:
        print(exc.msg, file=sys.stderr)
    else:
        action = Action.create(
            name=args.name,
            action_delegate=context.actions,
            invocation_delegate=context.invocations,
            description=args.description,
            org_id=args.org,
            metadata=args.metadata,
            tags=args.tag,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )

        if args.docker_image_name:
            action.register_container(args.docker_image_name, args.docker_image_tag)

        print(f"Successfully created action '{action.name}'. Record: ")
        print(json.dumps(action.to_dict(), indent=4))
        if args.docker_image_name or action.uri:
            print(finalize_docker_image_registration_instructions(action))


def create_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=True,
        action="store",
        help=(
            "Name of the action. Not modifiable after creation. "
            "An action is considered unique by its (name, docker_image_name, docker_image_tag) tuple."
        ),
    )
    parser.add_argument(
        "--description",
        required=False,
        action="store",
        help="Optional description of action. Modifiable after creation.",
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
            "Metadata can be modified after creation."
        ),
    )
    parser.add_argument(
        "--tag",
        required=False,
        type=str,
        nargs="*",
        help="One or more tags to annotate this action. Modifiable after creation.",
        action="extend",
    )
    add_org_arg(parser=parser)

    docker_image_group = parser.add_argument_group(
        "Docker image",
        "Register a Docker image with this action.",
    )
    docker_image_group.add_argument(
        "--image-name",
        required=False,
        action="store",
        dest="docker_image_name",
        help=(
            "Name of Docker image to associate with this action. Modifiable after creation. "
            "Required if '--image-tag' is provided."
        ),
    )
    docker_image_group.add_argument(
        "--image-tag",
        required=False,
        action="store",
        dest="docker_image_tag",
        help=(
            "Tag of Docker image to associate with this action. Modifiable after creation. "
            "Required if '--image-name' is provided."
        ),
    )

    add_compute_requirements_args(parser)
    add_container_parameters_args(parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_parser,
    command_kwargs={"help": "Create a new action."},
)
