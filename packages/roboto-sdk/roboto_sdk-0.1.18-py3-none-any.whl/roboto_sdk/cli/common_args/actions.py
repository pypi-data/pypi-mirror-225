#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import enum
import shlex
import typing

import pydantic

from ...domain.actions import (
    ComputeRequirements,
    ContainerParameters,
)
from ..command import KeyValuePairsAction
from .exceptions import ParseError


class DockerInstructionForm(enum.Enum):
    """The form of a CMD instruction."""

    Exec = "exec"
    Shell = "shell"


null = object()


def parse_compute_requirements(
    args: argparse.Namespace,
    default_vcpu: typing.Optional[int] = None,
    default_memory: typing.Optional[int] = None,
    default_storage: typing.Optional[int] = None,
) -> typing.Optional[ComputeRequirements]:
    try:
        kwargs = {
            key: value
            for key, value in [
                ("vCPU", args.vcpu if args.vcpu else default_vcpu),
                ("memory", args.memory if args.memory else default_memory),
                ("storage", args.storage if args.storage else default_storage),
            ]
            if value is not None
        }
        if not kwargs:
            return None
        return ComputeRequirements.parse_obj(kwargs)
    except pydantic.ValidationError as exc:
        for err in exc.errors():
            err_msg = err.get("msg")
            msg = err_msg if err_msg else err
            raise ParseError(msg) from None

    return None


def add_compute_requirements_args(parser: argparse.ArgumentParser) -> None:
    resource_requirements_group = parser.add_argument_group(
        "Resource requirements",
        "Specify required compute resources.",
    )
    resource_requirements_group.add_argument(
        "--vcpu",
        required=False,
        type=int,
        choices=[256, 512, 1024, 2048, 4096, 8192, 16384],
        help="CPU units to dedicate to action invocation. Defaults to 512 (0.5vCPU).",
    )

    resource_requirements_group.add_argument(
        "--memory",
        required=False,
        type=int,
        help=(
            "Memory (in MiB) to dedicate to action invocation. Defaults to 1024 (1 GiB). "
            "Supported values range from 512 (0.5 GiB) to 122880 (120 GiB). "
            "Supported values are tied to selected vCPU resources. See documentation for more information."
        ),
    )

    resource_requirements_group.add_argument(
        "--storage",
        required=False,
        type=int,
        help=(
            "Ephemeral storage (in GiB) to dedicate to action invocation. Defaults to 21 GiB. "
            "Supported values range from 21 to 200, inclusive."
        ),
    )

    # Placeholder
    resource_requirements_group.add_argument(
        "--gpu",
        required=False,
        default=False,
        action="store_true",
        help=(
            "This is a placeholder; it currently does nothing. "
            "In the future, setting this option will invoke the action in a GPU-enabled compute environment."
        ),
    )


def parse_container_overrides(
    args: argparse.Namespace,
    default_entry_point: typing.Optional[list[str]] = None,
    default_command: typing.Optional[list[str]] = None,
    default_env_vars: typing.Optional[dict[str, str]] = None,
    default_workdir: typing.Optional[str] = None,
) -> typing.Optional[ContainerParameters]:
    try:
        entry_point: typing.Union[list[str], object] = default_entry_point
        if args.entry_point is null:
            entry_point = null
        elif args.entry_point is not None:
            entry_point = [args.entry_point]

        command: typing.Union[list[str], object] = default_command
        if args.command is null:
            command = null
        elif args.command is not None:
            command_form = DockerInstructionForm(args.command_form)
            command = []
            if command_form == DockerInstructionForm.Exec and len(args.command):
                lexxer = shlex.shlex(args.command, posix=True, punctuation_chars=True)
                lexxer.whitespace_split = True
                command = list(lexxer)
            else:
                command = [args.command]

        kwargs = {
            key: value
            for key, value in [
                ("entry_point", entry_point),
                ("command", command),
                ("workdir", args.workdir if args.workdir else default_workdir),
                ("env_vars", args.env if args.env else default_env_vars),
            ]
            if value is not None
        }
        if not kwargs:
            return None
        return ContainerParameters.parse_obj(
            {key: value if value is not null else None for key, value in kwargs.items()}
        )
    except pydantic.ValidationError as exc:
        for err in exc.errors():
            err_msg = err.get("msg")
            msg = err_msg if err_msg else err
            raise ParseError(msg) from None

    return None


def add_container_parameters_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group(
        "Container parameters",
        "Specify parameters to pass to the action's Docker container at runtime.",
    )

    group.add_argument(
        "--entrypoint",
        required=False,
        type=lambda s: s if s != "null" else null,
        dest="entry_point",
        help=(
            "Container ENTRYPOINT override."
            ' Supports passing empty string ("") as an override, which unsets the ENTRYPOINT specified in the docker image.'  # noqa: E501
            " If updating or invoking action which has existing ENTRYPOINT override, pass 'null' to remove the override."  # noqa: E501
            " Refer to docker documentation for more: "
            "https://docs.docker.com/engine/reference/builder/#entrypoint"
            " and https://docs.docker.com/engine/reference/run/#entrypoint-default-command-to-execute-at-runtime"
        ),
    )

    group.add_argument(
        "--command",
        required=False,
        type=lambda s: s if s != "null" else null,
        dest="command",
        help=(
            "Container CMD override."
            " If updating or invoking action which has existing CMD override, pass 'null' to remove the override."
            " Refer to docker documentation for more: "
            "https://docs.docker.com/engine/reference/builder/#cmd and"
            " https://docs.docker.com/engine/reference/run/#cmd-default-command-or-options"
        ),
    )

    group.add_argument(
        "--command-form",
        required=False,
        choices=[form.value for form in DockerInstructionForm],
        default=DockerInstructionForm.Exec.value,
        dest="command_form",
        help=(
            "In 'exec' form, the provided '--command' str is split into a list of strings"
            ' (e.g., \'--command "-c \'print(123)\'"\' is parsed as ["-c", "print(123)"]).'
            " In 'shell' form, the provided '--command' str is not split"
            " (e.g., '--command \"python -c 'print(123)'\"' is parsed as [\"python -c 'print(123)'\"])."
        ),
    )

    group.add_argument(
        "--workdir",
        required=False,
        type=lambda s: s if s != "null" else null,
        dest="workdir",
        help=(
            "If updating, pass 'null' to clear existing workdir."
            " Refer to docker documentation for more: https://docs.docker.com/engine/reference/run/#workdir"
        ),
    )

    group.add_argument(
        "--env",
        required=False,
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key=value' formatted pairs to set as container ENV vars. "
            "Do not use ENV vars for secrets (such as API keys). "
            "See documentation: https://docs.docker.com/engine/reference/run/#env-environment-variables"
        ),
    )
