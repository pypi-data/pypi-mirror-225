import collections.abc
import datetime
from typing import Any, Optional

from ...serde import pydantic_jsonable_dict
from ...updates import UpdateCondition
from .action_container_resources import (
    ComputeRequirements,
    ContainerCredentials,
    ContainerParameters,
)
from .action_delegate import ActionDelegate
from .action_record import ActionRecord
from .invocation import Invocation
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationSource,
)


class Action:
    __action_delegate: ActionDelegate
    __invocation_delegate: InvocationDelegate
    __record: ActionRecord
    __temp_container_credentials: Optional[ContainerCredentials] = None

    @classmethod
    def create(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        created_by: Optional[str] = None,
        compute_requirements: Optional[ComputeRequirements] = None,
        container_parameters: Optional[ContainerParameters] = None,
    ) -> "Action":
        record = action_delegate.create_action(
            name,
            org_id,
            created_by,
            description,
            metadata,
            tags,
            compute_requirements,
            container_parameters,
        )
        return cls(record, action_delegate, invocation_delegate)

    @classmethod
    def from_name(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
    ) -> "Action":
        record = action_delegate.get_action_by_primary_key(name, org_id)
        return cls(record, action_delegate, invocation_delegate)

    @classmethod
    def query(
        cls,
        filters: dict[str, Any],
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Action", None, None]:
        known_keys = set(ActionRecord.__fields__.keys())
        actual_keys = set(filters.keys())
        unknown_keys = actual_keys - known_keys
        if unknown_keys:
            plural = len(unknown_keys) > 1
            msg = (
                "are not known attributes of Action"
                if plural
                else "is not a known attribute of Action"
            )
            raise ValueError(f"{unknown_keys} {msg}. Known attributes: {known_keys}")

        paginated_results = action_delegate.query_actions(filters, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, action_delegate, invocation_delegate)
            if paginated_results.next_token:
                paginated_results = action_delegate.query_actions(
                    filters, org_id=org_id, page_token=paginated_results.next_token
                )
            else:
                break

    def __init__(
        self,
        record: ActionRecord,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
    ) -> None:
        self.__action_delegate = action_delegate
        self.__invocation_delegate = invocation_delegate
        self.__record = record

    @property
    def compute_requirements(self) -> ComputeRequirements:
        return self.__record.compute_requirements

    @property
    def container_parameters(self) -> ContainerParameters:
        return self.__record.container_parameters

    @property
    def last_modified(self) -> datetime.datetime:
        return self.__record.modified

    @property
    def name(self) -> str:
        return self.__record.name

    @property
    def org_id(self) -> str:
        return self.__record.org_id

    @property
    def record(self) -> ActionRecord:
        return self.__record

    @property
    def uri(self) -> Optional[str]:
        return self.__record.uri

    def get_temporary_container_credentials(
        self, caller: Optional[str] = None  # A Roboto user_id
    ) -> ContainerCredentials:
        if (
            self.__temp_container_credentials is None
            or self.__temp_container_credentials.is_expired()
        ):
            creds = self.__action_delegate.get_temp_container_credentials(
                self.__record, caller
            )
            self.__temp_container_credentials = creds

        return self.__temp_container_credentials

    def delete(self) -> None:
        self.__action_delegate.delete_action(self.__record)

    def invoke(
        self,
        input_data: list[str],
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: Optional[str] = None,
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
    ) -> Invocation:
        compute_reqs = self.__record.compute_requirements.copy(
            deep=True,
            update=compute_requirement_overrides.dict(
                exclude_none=True, exclude_defaults=True, exclude_unset=True
            )
            if compute_requirement_overrides
            else dict(),
        )
        container_params = self.__record.container_parameters.copy(
            deep=True,
            update=container_parameter_overrides.dict(
                exclude_none=True, exclude_defaults=True, exclude_unset=True
            )
            if container_parameter_overrides
            else dict(),
        )
        record = self.__invocation_delegate.create_invocation(
            self.__record,
            input_data,
            compute_reqs,
            container_params,
            data_source_id,
            data_source_type,
            invocation_source,
            invocation_source_id,
        )
        return Invocation(
            record,
            self.__invocation_delegate,
        )

    def register_container(
        self,
        image_name: str,
        image_tag: str,
        caller: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """
        Idempotent get or create container repository for this Action, and associate it with the Action as its URI.
        Use this to associate an Action with a container image that has yet to be pushed,
        or with a container image that has already been pushed to an existing repository.

        A container may be pushed to the reposistory using credentials returned by
        `get_temporary_container_credentials`.
        Its tag does not need to equal `image_tag`, but without calling this method with the associated tag,
        the Action will not be able to invoke the pushed container.

        Side-effects:
            * If a container repository for given `image_name`:`image_tag` does not exist, it will be created.
            * If a container repository was previously created for this Action for a different `image_name`,
              AND that repository is empty, it will be deleted.
            * Sets the `uri` attribute of this Action to the URI of the image expected to be pushed to the repository.

        `caller` is ignored on the client. It is determined server-side via the identity/access mechanism.
        """
        updated = self.__action_delegate.register_container(
            self.__record, image_name, image_tag, caller
        )
        self.__record = updated

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def update(
        self,
        updates: dict[str, Any],
        conditions: Optional[list[UpdateCondition]] = None,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        known_keys = set(ActionRecord.__fields__.keys())
        allowed_keys = known_keys - ActionRecord.DISALLOWED_FOR_UPDATE
        unallowed = set(updates.keys()) - allowed_keys
        if len(unallowed):
            plural = len(unallowed) > 1
            msg = (
                "are not updateable attributes"
                if plural
                else "is not an updateable attribute"
            )
            raise ValueError(
                f"{unallowed} {msg}. Updateable attributes: {allowed_keys}"
            )

        updated = self.__action_delegate.update(
            self.__record, updates, conditions, updated_by
        )
        self.__record = updated
