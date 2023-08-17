# MODULES
from typing import TypeVar, Generic
from logging import Logger

# MODELS
from session_repository.models.repository import SessionRepository


T = TypeVar("T", bound=SessionRepository)


class SessionService(Generic[T]):
    def __init__(
        self,
        repository: T,
        logger: Logger,
    ) -> None:
        self._repository = repository
        self._logger = logger

    def session_manager(self):
        return self._repository.session_manager()
