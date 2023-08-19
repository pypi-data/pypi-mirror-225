# Copyright (C) I'm Create LLC
#
# This code is part of Vectman system. You are not allowed to distribute it.
from __future__ import annotations
from functools import cached_property
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from chatrooms_api_client.api_client import ApiClient
from chatrooms_api_client.configuration import Configuration

from .channels import ChannelsService


class ChatroomsClient(AbstractAsyncContextManager["ChatroomsClient"]):
    def __init__(self, client: ApiClient) -> None:
        self._client = client

    @cached_property
    def channels(self):
        return ChannelsService(self._client)

    @staticmethod
    def create(server_url: str):
        config = Configuration(f"{server_url}/api/v1")
        client = ApiClient(config)
        return ChatroomsClient(client)

    async def __aenter__(self) -> ChatroomsClient:
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        await self._client.__aexit__(  # type: ignore
            exc_type=__exc_type, exc_value=__exc_value, traceback=__traceback
        )

    async def close(self) -> None:
        await self._client.close()
