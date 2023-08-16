from typing import Any, Optional

import pydantic

from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationSource,
    InvocationStatus,
)


class CreateInvocationRequest(pydantic.BaseModel):
    input_data: list[str]
    compute_requirements: ComputeRequirements
    container_parameters: ContainerParameters
    data_source_id: str
    data_source_type: InvocationDataSourceType
    invocation_source: InvocationSource
    invocation_source_id: Optional[str]


class QueryInvocationsRequest(pydantic.BaseModel):
    filters: dict[str, Any] = pydantic.Field(default_factory=dict)


class SetLogsLocationRequest(pydantic.BaseModel):
    bucket: str
    prefix: str


class UpdateInvocationStatus(pydantic.BaseModel):
    status: InvocationStatus
    detail: str
