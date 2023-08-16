#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Optional

from .constants import (
    ORG_OVERRIDE_HEADER,
    USER_OVERRIDE_HEADER,
)


def headers_for_org_and_user(
    org_id: Optional[str] = None,
    user_id: Optional[str] = None,
    additional_headers: Optional[dict[str, str]] = None,
):
    headers = {}

    if org_id is not None:
        headers[ORG_OVERRIDE_HEADER] = org_id

    if user_id is not None:
        headers[USER_OVERRIDE_HEADER] = user_id

    if additional_headers is not None:
        headers.update(additional_headers)

    return headers
