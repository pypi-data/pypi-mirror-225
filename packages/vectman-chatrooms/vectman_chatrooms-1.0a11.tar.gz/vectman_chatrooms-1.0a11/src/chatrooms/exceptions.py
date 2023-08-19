# Copyright (C) I'm Create LLC
#
# This code is part of Vectman system. You are not allowed to distribute it.
from typing import Any, ClassVar


class TemplatedError(Exception):
    template_str: ClassVar[str | None] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)
        self._kwargs = kwargs

    @property
    def template(self) -> str:
        template = type(self).template_str
        if template is None:
            error_msg = "Message template not set."
            raise NotImplementedError(error_msg)
        return template

    @property
    def message(self) -> str:
        return self.template.format(*self.args, **self.kwargs)

    @property
    def kwargs(self):
        return self._kwargs.copy()

    def __str__(self) -> str:
        return self.message


class ChatroomsClientError(Exception):
    pass


class ValidationError(ChatroomsClientError):
    pass


class ChannelNotFoundError(TemplatedError, ChatroomsClientError):
    template_str = (
        "Channel key '{channel_key}' not found in subscription '{subscription_id}'."
    )


class ChannelAlreadyExistsError(TemplatedError, ChatroomsClientError):
    template_str = "Channel key '{channel_key}' is already being used."
