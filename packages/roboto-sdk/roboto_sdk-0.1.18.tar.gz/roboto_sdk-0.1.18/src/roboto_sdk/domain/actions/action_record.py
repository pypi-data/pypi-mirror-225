import datetime
import typing

import pydantic

from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)


class ActionRecord(pydantic.BaseModel):
    DISALLOWED_FOR_UPDATE: typing.ClassVar[set[str]] = {
        "name",
        "org_id",
        "uri",
        "created",
        "created_by",
        "modified",
        "modified_by",
    }

    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    created_by: str
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    modified_by: str
    name: str  # Sort key
    org_id: str  # Partition key

    compute_requirements: ComputeRequirements = pydantic.Field(
        default_factory=ComputeRequirements
    )
    container_parameters: ContainerParameters = pydantic.Field(
        default_factory=ContainerParameters
    )
    description: typing.Optional[str] = None
    metadata: typing.Optional[dict[str, typing.Any]] = None
    tags: typing.Optional[list[str]] = None
    uri: typing.Optional[str] = None
