#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Optional

from ..domain.actions import (
    ActionDelegate,
    InvocationDelegate,
)
from ..domain.datasets import DatasetDelegate
from ..domain.files import FileDelegate
from ..domain.orgs import OrgDelegate
from ..domain.tokens import TokenDelegate
from ..domain.triggers import TriggerDelegate
from ..domain.users import UserDelegate
from ..http import HttpClient


class CLIContext:
    _http: Optional[HttpClient]
    actions: ActionDelegate
    datasets: DatasetDelegate
    files: FileDelegate
    invocations: InvocationDelegate
    orgs: OrgDelegate
    tokens: TokenDelegate
    triggers: TriggerDelegate
    users: UserDelegate

    @property
    def http(self) -> HttpClient:
        # Necessary since http is lazy set after parsing args
        if self._http is None:
            raise ValueError("Unset HTTP client!")

        return self._http

    @http.setter
    def http(self, http: HttpClient) -> None:
        self._http = http
