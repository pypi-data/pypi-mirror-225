from typing import Any, Optional

import pydantic

from ...updates import UpdateCondition
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)


class CreateActionRequest(pydantic.BaseModel):
    # Required
    name: str

    # Optional
    description: Optional[str] = None
    metadata: Optional[dict[str, Any]] = pydantic.Field(default_factory=dict)
    tags: Optional[list[str]] = pydantic.Field(default_factory=list)
    compute_requirements: Optional[ComputeRequirements] = None
    container_parameters: Optional[ContainerParameters] = None


class ContainerUploadCredentials(pydantic.BaseModel):
    username: str
    password: str
    registry_url: str
    image_uri: str


class RegisterContainerRequest(pydantic.BaseModel):
    image_name: str
    image_tag: str


class QueryActionsRequest(pydantic.BaseModel):
    filters: dict[str, Any] = pydantic.Field(default_factory=dict)


class ActionRecordUpdates(pydantic.BaseModel):
    description: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    tags: Optional[list[str]] = None
    compute_requirements: Optional[ComputeRequirements] = None
    container_parameters: Optional[ContainerParameters] = None


class UpdateActionRequest(pydantic.BaseModel):
    updates: ActionRecordUpdates
    conditions: Optional[list[UpdateCondition]] = None
