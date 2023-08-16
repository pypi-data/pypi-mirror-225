#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc
from typing import Any, Optional

from ...http import PaginatedList, PaginationToken
from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)
from .trigger_record import TriggerRecord


class TriggerDelegate(abc.ABC):
    @abc.abstractmethod
    def create_trigger(
        self,
        name: str,
        action_name: str,
        required_inputs: list[str],
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,  # A Roboto user_id
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
    ) -> TriggerRecord:
        raise NotImplementedError("create_trigger")

    @abc.abstractmethod
    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> TriggerRecord:
        raise NotImplementedError("get_trigger_by_primary_key")

    @abc.abstractmethod
    def query_triggers(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[PaginationToken] = None,
    ) -> PaginatedList[TriggerRecord]:
        raise NotImplementedError("query_triggers")

    @abc.abstractmethod
    def delete_trigger(self, name: str, org_id: str) -> None:
        raise NotImplementedError("delete_trigger")
