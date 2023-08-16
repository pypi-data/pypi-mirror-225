#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.datasets import Dataset
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import add_org_arg
from ..context import CLIContext


def search(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = Dataset.query(
        args.filter, context.datasets, context.files, org_id=args.org
    )
    print(json.dumps([record.to_dict() for record in records], indent=4))


def search_setup_parser(parser):
    add_org_arg(parser=parser)
    parser.add_argument(
        "-f",
        "--filter",
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help="Zero or more 'key=value' formatted conditions which will perform equality checks against "
        + "datasets and filter results accordingly.",
        default={},
    )


search_command = RobotoCommand(
    name="search",
    logic=search,
    setup_parser=search_setup_parser,
    command_kwargs={"help": "Query dataset matching filter criteria."},
)
