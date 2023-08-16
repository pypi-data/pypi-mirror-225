#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import sys

from ...domain.actions import Action
from ...updates import UpdateCondition
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


def update(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    if (args.docker_image_name and not args.docker_image_tag) or (
        args.docker_image_tag and not args.docker_image_name
    ):
        raise argparse.ArgumentError(
            argument=None,
            message="Must define both --image-name and --image-tag if either is provided",
        )

    action = Action.from_name(
        name=args.name,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    updates = dict()
    if args.description:
        updates["description"] = args.description

    if args.metadata:
        updates["metadata"] = args.metadata

    if args.tag:
        updates["tags"] = args.tag

    try:
        compute_requirements = parse_compute_requirements(
            args,
            default_vcpu=action.compute_requirements.vCPU,
            default_memory=action.compute_requirements.memory,
            default_storage=action.compute_requirements.storage,
        )
        if compute_requirements:
            updates["compute_requirements"] = compute_requirements
        container_parameters = parse_container_overrides(
            args,
            default_env_vars=action.container_parameters.env_vars,
            default_entry_point=action.container_parameters.entry_point,
            default_command=action.container_parameters.command,
            default_workdir=action.container_parameters.workdir,
        )
        if container_parameters:
            updates["container_parameters"] = container_parameters
    except ParseError as exc:
        print(exc.msg, file=sys.stderr)
        return

    action.update(
        updates,
        conditions=[
            # Avoid a race
            UpdateCondition(
                key="modified", value=action.last_modified.isoformat(), comparator="eq"
            )
        ],
    )

    if args.docker_image_name:
        action.register_container(args.docker_image_name, args.docker_image_tag)

    print(f"Successfully updated action '{action.name}'. Record: ")
    print(json.dumps(action.to_dict(), indent=4))

    if args.docker_image_name or action.uri:
        print(finalize_docker_image_registration_instructions(action))


def update_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=True,
        action="store",
        help="Name of the action to update.",
    )
    parser.add_argument(
        "--description",
        required=False,
        action="store",
        help="Optional description of action.",
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
            "Updating metadata will overwrite any existing metadata already associated with the action."
        ),
    )
    parser.add_argument(
        "--tag",
        required=False,
        type=str,
        nargs="*",
        help=(
            "One or more tags to annotate this action. "
            "Updating tags will overwrite any existing tags already associated with this action."
        ),
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
            "Name of Docker image to associate with this action. "
            "If defined, must provide --image-tag as well."
        ),
    )
    docker_image_group.add_argument(
        "--image-tag",
        required=False,
        action="store",
        dest="docker_image_tag",
        help="Tag of Docker image to associate with this action.",
    )

    add_compute_requirements_args(parser)
    add_container_parameters_args(parser)


update_command = RobotoCommand(
    name="update",
    logic=update,
    setup_parser=update_parser,
    command_kwargs={"help": "Update an existing action."},
)
