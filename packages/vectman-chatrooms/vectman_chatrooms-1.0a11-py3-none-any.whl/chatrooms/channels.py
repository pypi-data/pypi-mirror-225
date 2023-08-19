# Copyright (C) I'm Create LLC
#
# This code is part of Vectman system. You are not allowed to distribute it.
from __future__ import annotations
from http import HTTPStatus

from typing import Iterable, cast
from chatrooms_api_client import ChannelUserModel
from chatrooms_api_client import ApiClient
from chatrooms_api_client import ChannelsApi
from chatrooms_api_client import ChannelPayload
from chatrooms_api_client import ChannelModel
from chatrooms_api_client import AddUsersPayload
from chatrooms_api_client import ApiException
from optional import Optional
from plans import SubscriptionId

from .exceptions import (
    ChannelAlreadyExistsError,
    ChannelNotFoundError,
    ChatroomsClientError,
)
from .utils import Loadable


def _channel_exc_map(
    channel_key: str, subscription_id: str | None
) -> dict[HTTPStatus, BaseException]:
    return {
        HTTPStatus.NOT_FOUND: ChannelNotFoundError(
            channel_key=channel_key, subscription_id=subscription_id
        ),
    }


class ChannelsService:
    def __init__(self, client: ApiClient) -> None:
        self._client = ChannelsApi(client)

    async def create(  # noqa: PLR0913
        self,
        *,
        channel_key: str,
        title: str,
        description: str | None = None,
        icon: str | None = None,
        subscription_id: SubscriptionId | None,
    ) -> Channel:
        try:
            result = await self._client.create_channel(  # type: ignore
                ChannelPayload(
                    channel_key=channel_key,
                    title=title,
                    description=description,
                    icon=icon,
                    subscription_id=str(subscription_id)
                    if subscription_id is not None
                    else None,
                ),
            )
        except ApiException as exc:
            raise _build_exc(
                exc=exc,
                exc_map={
                    HTTPStatus.BAD_REQUEST: ChannelAlreadyExistsError(
                        channel_key=channel_key, subscription_id=subscription_id
                    ),
                },
            ) from exc

        return Channel(
            data=result,
            client=self._client,
            channel_key=result.channel_key,
            subscription_id=result.subscription_id,
        )

    async def find_channels(
        self,
        *,
        offset: int | None = None,
        size: int | None = None,
        user_id: str | None = None,
        subscription_id: str | None,
    ) -> list[Channel]:
        page = await self._client.list_channels(  # type: ignore
            offset=offset,
            size=size,
            user_id=user_id,
            subscription_id=subscription_id,
        )

        return [
            self._map_channel(item)
            for item in cast(
                Iterable[ChannelModel],
                page.items,  # type: ignore
            )
        ]

    def _map_channel(self, item: ChannelModel) -> Channel:
        return Channel(
            data=item,
            client=self._client,
            channel_key=item.channel_key,
            subscription_id=item.subscription_id,
        )

    def get_channel(self, channel_key: str, subscription_id: str | None) -> Channel:
        return Channel(
            channel_key=channel_key,
            client=self._client,
            subscription_id=subscription_id,
        )


class Channel(Loadable[ChannelModel]):
    def __init__(
        self,
        *,
        data: ChannelModel | None = None,
        client: ChannelsApi,
        channel_key: str,
        subscription_id: str | None,
    ) -> None:
        super().__init__(Optional.of(data) if data is not None else Optional.empty())
        self._client = client
        self._key = channel_key
        self._subscription_id = subscription_id

    async def delete(self) -> None:
        await self._client.delete_channel(  # type: ignore
            key=self._key, subscription_id=self._subscription_id
        )

    async def join_users(self, user_ids: set[str]) -> None:
        await self._client.join_users_to_channel(  # type: ignore
            self._key,
            AddUsersPayload(user_ids=list(user_ids)),
            subscription_id=self._subscription_id,
        )

    async def remove_users(self, user_ids: set[str]):
        try:
            result = await self._client.remove_channel_users(  # type: ignore
                key=self._key,
                user_ids=list(user_ids),
                subscription_id=self._subscription_id,
            )
        except ApiException as exc:
            raise _build_exc(
                exc, _channel_exc_map(self._key, self._subscription_id)
            ) from exc

        return cast(set[str], result.user_ids)  # type: ignore

    async def load(self) -> ChannelModel:
        try:
            result = await self._client.retrieve_channel(  # type: ignore
                key=self._key, subscription_id=self._subscription_id
            )
        except ApiException as exc:
            raise _build_exc(
                exc, _channel_exc_map(self._key, self._subscription_id)
            ) from exc
        return result

    async def list_users(self) -> list[ChannelUser]:
        try:
            return [
                ChannelUser(self, item)
                for item in await self._client.get_channel_users(  # type: ignore
                    key=self._key,
                )
            ]
        except ApiException as exc:
            raise _build_exc(
                exc, _channel_exc_map(self._key, self._subscription_id)
            ) from exc

    def __str__(self) -> str:
        if self.is_loaded:
            return self.data.title
        return self._key

    def __repr__(self) -> str:
        return f"Channel({self})"


class ChannelUser:
    def __init__(self, client: Channel, data: ChannelUserModel) -> None:
        self._client = client
        self._data = data

    @property
    def data(self) -> ChannelUserModel:
        return self._data

    async def remove(self) -> bool:
        result = await self._client.remove_users(
            user_ids=[self.data.user_id],  # type: ignore
        )

        return self.data.user_id in cast(list[str], result.user_ids)  # type: ignore

    def __str__(self) -> str:
        return str(self.data.user_id)  # type: ignore


def _build_exc(
    exc: ApiException, exc_map: dict[HTTPStatus, BaseException]
) -> BaseException:
    match exc:
        case ApiException(status=int(status_code)):
            return exc_map.get(
                HTTPStatus(status_code),
                ChatroomsClientError(
                    "An unknown error was detected while calling the API."
                ),
            )
        case _:
            return RuntimeError("Exception not supported.")
