# Copyright (C) I'm Create LLC
#
# This code is part of Vectman system. You are not allowed to distribute it.
from abc import ABC, abstractmethod
from asyncio import Future, InvalidStateError, ensure_future
from typing import Any, Generator, Generic, Self, TypeVar

from optional import Optional

_Value = TypeVar("_Value")


class DataNotLoadedError(Exception):
    """Raised if the data is not yet available."""


class Loadable(ABC, Generic[_Value]):
    def __init__(self, value: Optional[_Value] = Optional.empty()) -> None:
        super().__init__()

        self._load_future: Future[_Value] | None = None
        if value:
            self.data = value.value

    @abstractmethod
    async def load(self) -> _Value:
        raise NotImplementedError()

    @property
    def _future(self) -> Future[_Value]:
        if self._load_future is None:
            self._load_future = ensure_future(self.load())
        return self._load_future

    @_future.deleter
    def _future(self) -> None:
        self._load_future = None

    def __await__(self) -> Generator[Any, None, Self]:
        yield from self._future.__await__()
        return self

    def reload(self) -> Self:
        del self._future
        return self

    @property
    def data(self) -> _Value:
        try:
            return self._future.result()
        except InvalidStateError as exc:
            raise DataNotLoadedError() from exc

    @data.setter
    def data(self, value: _Value) -> None:
        new_future: Future[_Value] = Future()
        new_future.set_result(value)
        self._load_future = new_future

    @property
    def is_loaded(self):
        return (
            self._load_future is not None
            and self._load_future.done()
            and self._load_future.exception() is None
        )
