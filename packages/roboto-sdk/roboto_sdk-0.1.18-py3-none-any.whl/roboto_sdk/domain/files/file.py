import collections.abc
import hashlib
import pathlib
from typing import Any, Optional

from ...serde import pydantic_jsonable_dict
from .delegate import FileDelegate, S3Credentials
from .progress import (
    NoopProgressMonitorFactory,
    ProgressMonitorFactory,
)
from .record import FileRecord


class File:
    __delegate: FileDelegate
    __record: FileRecord

    @staticmethod
    def compute_file_id(uri: str) -> str:
        """
        Return a fixed size (32 character), unique ID deterministically from an Object's bucket and key.
        Versioned objects will have the same ID.
        """
        return hashlib.blake2b(uri.encode("utf-8"), digest_size=16).hexdigest()

    @staticmethod
    def construct_s3_obj_uri(
        bucket: str, key: str, version: Optional[str] = None
    ) -> str:
        base_uri = f"s3://{bucket}/{key}"
        if version:
            base_uri += f"?versionId={version}"
        return base_uri

    @classmethod
    def from_id(
        cls,
        file_id: str,
        delegate: FileDelegate,
        org_id: Optional[str] = None,
    ) -> "File":
        record = delegate.get_record_by_primary_key(file_id, org_id)
        return cls(record, delegate)

    @classmethod
    def query(
        cls,
        filters: dict[str, Any],
        delegate: FileDelegate,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["File", None, None]:
        known_keys = set(FileRecord.__fields__.keys())
        actual_keys = set(filters.keys())
        unknown_keys = actual_keys - known_keys
        if unknown_keys:
            plural = len(unknown_keys) > 1
            msg = (
                "are not known attributes of File"
                if plural
                else "is not a known attribute of File"
            )
            raise ValueError(f"{unknown_keys} {msg}. Known attributes: {known_keys}")

        paginated_results = delegate.query_files(filters, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, delegate)
            if paginated_results.next_token:
                paginated_results = delegate.query_files(
                    filters, org_id=org_id, page_token=paginated_results.next_token
                )
            else:
                break

    def __init__(self, record: FileRecord, delegate: FileDelegate):
        self.__record = record
        self.__delegate = delegate

    @property
    def file_id(self) -> str:
        return self.__record.file_id

    @property
    def uri(self) -> str:
        return self.__record.uri

    @property
    def record(self) -> FileRecord:
        return self.__record

    @property
    def relative_path(self) -> str:
        return self.__record.relative_path

    def delete(self) -> None:
        self.__delegate.delete_file(self.__record)

    def download(
        self,
        local_path: pathlib.Path,
        credentials: S3Credentials,
        progress_monitor_factory: ProgressMonitorFactory = NoopProgressMonitorFactory(),
    ):
        self.__delegate.download_file(
            self.__record,
            local_path,
            credentials,
            progress_monitor_factory=progress_monitor_factory,
        )

    def get_signed_url(self) -> str:
        return self.__delegate.get_signed_url(self.__record)

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)
