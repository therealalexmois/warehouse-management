"""Абстрактный интерфейс Unit of Work для управления транзакциями."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self


class UnitOfWork(ABC):
    """Абстрактный класс Unit of Work.

    Используется для управления транзакциями при работе с базой данных.
    """

    @abstractmethod
    def __enter__(self) -> 'Self':
        """Начинает контекст управления транзакцией.

        Returns:
            UnitOfWork: Текущий экземпляр Unit of Work.
        """
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """Завершает контекст управления транзакцией.

        Args:
            exc_type (Type[BaseException] | None): Тип исключения, если оно произошло.
            exc_val (BaseException | None): Значение исключения.
            exc_tb (object | None): Трассировка исключения.
        """
        pass

    @abstractmethod
    def commit(self) -> None:
        """Фиксирует текущую транзакцию."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Откатывает текущую транзакцию."""
        pass
