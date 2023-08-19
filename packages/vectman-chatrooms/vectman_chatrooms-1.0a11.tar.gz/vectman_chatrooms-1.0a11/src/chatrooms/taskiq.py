# Copyright (C) I'm Create LLC
#
# This code is part of Vectman system. You are not allowed to distribute it.
from chatrooms_api_client import ChannelModel, ChannelPayload
from plans import SubscriptionId
from pydantic import AnyHttpUrl, BaseSettings, parse_obj_as
from taskiq import (
    AsyncBroker,
    TaskiqDepends,
    TaskiqEvents,
    TaskiqState,
)
from taskiq.brokers.shared_broker import AsyncSharedBroker

from .channels import ChannelsService
from .client import ChatroomsClient
from .exceptions import ChannelAlreadyExistsError, ChannelNotFoundError

_CHATROOMS_CLIENT_STATE_KEY = "__chatrooms_client__"
_tasks = AsyncSharedBroker()


class ChatroomsApiConfig(BaseSettings):
    """Configuration for the chatrooms API URL."""

    URL: AnyHttpUrl

    class Config(BaseSettings.Config):
        env_file = ".env"
        env_prefix = "CHATROOMS_"


def setup_chatrooms_client(broker: AsyncBroker) -> None:
    if isinstance(broker, AsyncSharedBroker):
        return setup_chatrooms_client(broker._default_broker)  # type: ignore

    async def _setup_api_client(state: TaskiqState) -> None:
        settings = ChatroomsApiConfig()  # type: ignore
        client = await ChatroomsClient.create(str(settings.URL)).__aenter__()
        state[_CHATROOMS_CLIENT_STATE_KEY] = client

    async def _shutdown_api_client(state: TaskiqState) -> None:
        client = _get_client(state)
        await client.close()

    broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, _setup_api_client)
    broker.add_event_handler(TaskiqEvents.WORKER_SHUTDOWN, _shutdown_api_client)
    _tasks.default_broker(broker)


def _get_client(state: TaskiqState = TaskiqDepends()) -> ChatroomsClient:
    client: ChatroomsClient = state[_CHATROOMS_CLIENT_STATE_KEY]
    return client


def _channels(api: ChatroomsClient = TaskiqDepends(_get_client)):
    return api.channels


@_tasks.task()
async def create_channel(
    payload: ChannelPayload, channels: ChannelsService = TaskiqDepends(_channels)
) -> ChannelModel | None:
    try:
        result = await channels.create(
            channel_key=payload.channel_key,
            description=payload.description,
            icon=parse_obj_as(str | None, payload.icon),  # type: ignore
            subscription_id=parse_obj_as(
                SubscriptionId | None, payload.subscription_id
            ),
            title=parse_obj_as(str, payload.title),  # type: ignore
        )
    except ChannelAlreadyExistsError:
        return None
    return result.data


@_tasks.task()
async def get_channel(
    channel_key: str,
    subscription_id: str | None,
    channels: ChannelsService = TaskiqDepends(_channels),
) -> ChannelModel | None:
    try:
        result = await channels.get_channel(channel_key, subscription_id)
    except ChannelNotFoundError:
        return None
    return result.data


@_tasks.task()
async def create_or_get_channel(payload: ChannelPayload) -> ChannelModel | None:
    find_task = await get_channel.kiq(payload.channel_key, payload.subscription_id)
    result = await find_task.wait_result()
    result.raise_for_error()
    if result.return_value is not None:
        return result.return_value

    create_task = await create_channel.kiq(payload)
    create_result = await create_task.wait_result()
    create_result.raise_for_error()
    return create_result.return_value


@_tasks.task()
async def remove_channel(
    channel_key: str,
    subscription_id: str | None,
    channels: ChannelsService = TaskiqDepends(_channels),
) -> bool:
    try:
        await channels.get_channel(channel_key, subscription_id)
    except ChannelNotFoundError:
        return False
    return True


@_tasks.task()
async def add_users_to_channel(
    channel_key: str,
    subscription_id: str | None,
    user_list: list[str],
    channels: ChannelsService = TaskiqDepends(_channels),
) -> None:
    await channels.get_channel(channel_key, subscription_id).join_users(set(user_list))


@_tasks.task()
async def remove_users_from_channel(
    channel_key: str,
    subscription_id: str | None,
    user_list: list[str],
    channels: ChannelsService = TaskiqDepends(_channels),
) -> None:
    await channels.get_channel(channel_key, subscription_id).join_users(set(user_list))
