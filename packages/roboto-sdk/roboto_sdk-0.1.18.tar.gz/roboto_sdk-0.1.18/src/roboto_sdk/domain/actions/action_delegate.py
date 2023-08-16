import abc
from typing import Any, Optional

from ...http import PaginatedList, PaginationToken
from ...updates import UpdateCondition
from .action_container_resources import (
    ComputeRequirements,
    ContainerCredentials,
    ContainerParameters,
)
from .action_record import ActionRecord


class ActionDelegate(abc.ABC):
    @abc.abstractmethod
    def create_action(
        self,
        name: str,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,  # A Roboto user_id
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        compute_requirements: Optional[ComputeRequirements] = None,
        container_parameters: Optional[ContainerParameters] = None,
    ) -> ActionRecord:
        raise NotImplementedError("create_action")

    @abc.abstractmethod
    def get_action_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> ActionRecord:
        raise NotImplementedError("get_action_by_primary_key")

    @abc.abstractmethod
    def delete_action(self, record: ActionRecord) -> None:
        raise NotImplementedError("delete_action")

    @abc.abstractmethod
    def register_container(
        self,
        record: ActionRecord,
        image_name: str,
        image_tag: str,
        caller: Optional[str] = None,  # A Roboto user_id
    ) -> ActionRecord:
        raise NotImplementedError("register_container")

    @abc.abstractmethod
    def get_temp_container_credentials(
        self,
        record: ActionRecord,
        caller: Optional[str] = None,  # A Roboto user_id
    ) -> ContainerCredentials:
        raise NotImplementedError("get_temp_container_credentials")

    @abc.abstractmethod
    def query_actions(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[PaginationToken] = None,
    ) -> PaginatedList[ActionRecord]:
        raise NotImplementedError("query_actions")

    @abc.abstractmethod
    def update(
        self,
        record: ActionRecord,
        updates: dict[str, Any],
        conditions: Optional[list[UpdateCondition]],
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> ActionRecord:
        raise NotImplementedError("update")
