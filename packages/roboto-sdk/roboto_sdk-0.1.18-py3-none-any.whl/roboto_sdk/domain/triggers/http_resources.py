#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Any, Optional

import pydantic

from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)


class CreateTriggerRequest(pydantic.BaseModel):
    # Required
    name: str = pydantic.Field(regex=r"[\w\-]{1,256}")
    action_name: str
    required_inputs: list[str]
    compute_requirement_overrides: Optional[ComputeRequirements] = None
    container_parameter_overrides: Optional[ContainerParameters] = None


class QueryTriggersRequest(pydantic.BaseModel):
    filters: dict[str, Any] = pydantic.Field(default_factory=dict)
