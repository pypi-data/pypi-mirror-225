from typing import Any, Optional
import urllib.parse

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    PaginationToken,
    StreamedList,
    headers_for_org_and_user,
)
from ...logging import default_logger
from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_record import ActionRecord
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_http_resources import (
    CreateInvocationRequest,
    QueryInvocationsRequest,
    SetLogsLocationRequest,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
    LogRecord,
)

logger = default_logger()


class InvocationHttpDelegate(InvocationDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def headers(
        self, org_id: Optional[str] = None, user_id: Optional[str] = None
    ) -> dict[str, str]:
        return headers_for_org_and_user(
            org_id=org_id,
            user_id=user_id,
            additional_headers={"Content-Type": "application/json"},
        )

    def create_invocation(
        self,
        action_record: ActionRecord,
        input_data: list[str],
        compute_requirements: ComputeRequirements,
        container_parameters: ContainerParameters,
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: Optional[str] = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{action_record.name}/invoke"
        request_body = CreateInvocationRequest(
            input_data=input_data,
            data_source_id=data_source_id,
            data_source_type=data_source_type,
            invocation_source=invocation_source,
            invocation_source_id=invocation_source_id,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(
                    org_id=action_record.org_id,
                    user_id=invocation_source_id
                    if invocation_source == InvocationSource.Manual
                    else None,
                ),
            )

        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_by_id(
        self, invocation_id: str, org_id: Optional[str] = None
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}"
        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers(org_id))

        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_logs(
        self,
        invocation_id: str,
        bucket: Optional[str],
        prefix: Optional[str],
        page_token: Optional[PaginationToken] = None,
        org_id: Optional[str] = None,
    ) -> PaginatedList[LogRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}/logs"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": str(page_token)})
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            http_response = self.__http_client.get(url, self.headers(org_id))
        data = http_response.from_json(json_path=["data"])

        return PaginatedList(
            items=[LogRecord.parse_obj(record) for record in data["items"]],
            next_token=PaginationToken.from_token(data["next_token"]),
        )

    def stream_logs(
        self,
        invocation_id: str,
        bucket: Optional[str],
        prefix: Optional[str],
        last_read: Optional[PaginationToken] = None,
        org_id: Optional[str] = None,
    ) -> StreamedList[LogRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}/logs/stream"
        if last_read:
            encoded_qs = urllib.parse.urlencode({"last_read": str(last_read)})
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            http_response = self.__http_client.get(url, self.headers(org_id))
        data = http_response.from_json(json_path=["data"])

        return StreamedList(
            items=[LogRecord.parse_obj(record) for record in data["items"]],
            has_next=data["has_next"],
            last_read=PaginationToken.from_token(data["last_read"]),
        )

    def set_logs_location(
        self, record: InvocationRecord, bucket: str, prefix: str
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.invocation_id}/logs"
        request_body = SetLogsLocationRequest(bucket=bucket, prefix=prefix)

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(record.org_id),
            )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def update_invocation_status(
        self,
        record: InvocationRecord,
        status: InvocationStatus,
        detail: Optional[str] = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.invocation_id}/status"

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data={"status": status.value, "detail": detail},
                headers=self.headers(record.org_id),
            )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_invocations(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[PaginationToken] = None,
    ) -> PaginatedList[InvocationRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/query"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": str(page_token)})
            url = f"{url}?{encoded_qs}"

        request_body = QueryInvocationsRequest(filters=filters)
        with RobotoHttpExceptionParse():
            res = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(org_id),
            )

        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                InvocationRecord.parse_obj(record) for record in unmarshalled["items"]
            ],
            next_token=PaginationToken.from_token(unmarshalled["next_token"]),
        )
