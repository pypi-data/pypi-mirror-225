import collections.abc
import datetime
from typing import Any, Optional

from ...http import PaginationToken
from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
    InvocationDataSource,
    InvocationRecord,
    InvocationStatus,
    InvocationStatusRecord,
    LogRecord,
)


class Invocation:
    __invocation_delegate: InvocationDelegate
    __record: InvocationRecord

    @classmethod
    def from_id(
        cls,
        invocation_id: str,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
    ) -> "Invocation":
        record = invocation_delegate.get_by_id(invocation_id, org_id)
        return cls(record, invocation_delegate)

    @classmethod
    def query(
        cls,
        filters: dict[str, Any],
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Invocation", None, None]:
        known_keys = set(InvocationRecord.__fields__.keys())
        actual_keys = set(filters.keys())
        unknown_keys = actual_keys - known_keys
        if unknown_keys:
            plural = len(unknown_keys) > 1
            msg = (
                "are not known attributes of Invocation"
                if plural
                else "is not a known attribute of Invocation"
            )
            raise ValueError(f"{unknown_keys} {msg}. Known attributes: {known_keys}")

        paginated_results = invocation_delegate.query_invocations(
            filters, org_id=org_id
        )
        while True:
            for record in paginated_results.items:
                yield cls(record, invocation_delegate)
            if paginated_results.next_token:
                paginated_results = invocation_delegate.query_invocations(
                    filters, org_id=org_id, page_token=paginated_results.next_token
                )
            else:
                break

    def __init__(
        self, record: InvocationRecord, invocation_delegate: InvocationDelegate
    ) -> None:
        self.__invocation_delegate = invocation_delegate
        self.__record = record

    def __str__(self) -> str:
        return str(self.__record)

    @property
    def action_name(self) -> str:
        return self.__record.action_name

    @property
    def compute_requirements(self) -> ComputeRequirements:
        return self.__record.compute_requirements

    @property
    def container_parameters(self) -> ContainerParameters:
        return self.__record.container_parameters

    @property
    def created(self) -> datetime.datetime:
        return self.__record.created

    @property
    def current_status(self) -> InvocationStatus:
        sorted_status_records = sorted(
            self.__record.status, key=lambda s: s.status.value
        )
        return sorted_status_records[-1].status

    @property
    def data_source(self) -> InvocationDataSource:
        return self.__record.data_source

    @property
    def id(self) -> str:
        return self.__record.invocation_id

    @property
    def input_data(self) -> list[str]:
        return self.__record.input_data

    @property
    def logs_location(self) -> Optional[tuple[str, str]]:
        if not self.__record.logs_bucket or not self.__record.logs_prefix:
            return None

        return self.__record.logs_bucket, self.__record.logs_prefix

    @property
    def org_id(self) -> str:
        return self.__record.org_id

    @property
    def record(self) -> InvocationRecord:
        return self.__record

    @property
    def reached_terminal_status(self) -> bool:
        return any(
            status_record.status.is_terminal() for status_record in self.__record.status
        )

    @property
    def status_log(self) -> list[InvocationStatusRecord]:
        return self.__record.status

    def is_queued_for_scheduling(self) -> bool:
        """
        An invocation is queued for scheduling if it has not yet reached the "Scheduled" status
        and it is not "Deadly".
        """
        previously_scheduled_or_deadly = (
            InvocationStatus.Scheduled,
            InvocationStatus.Deadly,
        )
        return all(
            status_record.status not in previously_scheduled_or_deadly
            for status_record in self.__record.status
        )

    def get_logs(
        self, page_token: Optional[PaginationToken] = None
    ) -> collections.abc.Generator[LogRecord, None, None]:
        paginated_results = self.__invocation_delegate.get_logs(
            self.id,
            self.__record.logs_bucket,
            self.__record.logs_prefix,
            page_token,
            self.org_id,
        )
        while True:
            for record in paginated_results.items:
                yield record
            if paginated_results.next_token:
                paginated_results = self.__invocation_delegate.get_logs(
                    self.id,
                    self.__record.logs_bucket,
                    self.__record.logs_prefix,
                    paginated_results.next_token,
                    self.org_id,
                )
            else:
                break

    def stream_logs(
        self, last_read: Optional[PaginationToken] = None
    ) -> collections.abc.Generator[LogRecord, None, Optional[PaginationToken]]:
        streamed_results = self.__invocation_delegate.stream_logs(
            self.id,
            self.__record.logs_bucket,
            self.__record.logs_prefix,
            last_read,
            self.org_id,
        )
        while True:
            for record in streamed_results.items:
                yield record
            if streamed_results.has_next and streamed_results.last_read:
                streamed_results = self.__invocation_delegate.stream_logs(
                    self.id,
                    self.__record.logs_bucket,
                    self.__record.logs_prefix,
                    streamed_results.last_read,
                    self.org_id,
                )
            else:
                break

        return streamed_results.last_read

    def set_logs_location(self, bucket: str, prefix: str) -> None:
        updated_record = self.__invocation_delegate.set_logs_location(
            self.__record, bucket, prefix
        )
        self.__record = updated_record

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def refresh(self) -> None:
        self.__record = self.__invocation_delegate.get_by_id(self.id, self.org_id)

    def update_status(
        self, next_status: InvocationStatus, detail: Optional[str] = "None"
    ) -> None:
        if next_status == InvocationStatus.Failed:
            # Heuristic: if this is the third time the invocation has failed, it is Deadly
            num_failures = len(
                [
                    status_record
                    for status_record in self.__record.status
                    if status_record.status == InvocationStatus.Failed
                ]
            )
            if num_failures >= 2:
                next_status = InvocationStatus.Deadly

        if not self.current_status.can_transition_to(next_status):
            raise ValueError(
                f"Cannot transition invocation from {self.current_status} to {next_status}"
            )

        updated_record = self.__invocation_delegate.update_invocation_status(
            self.__record, next_status, detail
        )
        self.__record = updated_record
