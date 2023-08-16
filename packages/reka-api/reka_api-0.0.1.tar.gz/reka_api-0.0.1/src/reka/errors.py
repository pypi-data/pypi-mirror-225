"""Reka-specific exceptions."""

from typing import Any


class RekaError(Exception):
    """Something wrong happened with the request."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.underlying = kwargs.pop("underlying", None)
        self.reason = kwargs.pop("reason", None)
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"RekaError: Underlying={self.underlying}, Reason={self.reason}"


class DatasetError(RekaError):
    """Something wrong with processing datasets"""

    ...


class RetrievalError(RekaError):
    """Something wrong with retrieval"""

    ...


class AuthError(RekaError, ValueError):
    ...


class InvalidConversationError(RekaError):
    ...
