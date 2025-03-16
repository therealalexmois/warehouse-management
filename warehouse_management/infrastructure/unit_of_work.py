"""Реализация паттерна Unit of Work с использованием SQLAlchemy."""

from typing import TYPE_CHECKING

from warehouse_management.domain.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.orm import Session


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Реализация Unit of Work для работы с SQLAlchemy."""

    def __init__(self, session: 'Session') -> None:
        """Инициализирует Unit of Work.

        Args:
            session: Экземпляр SQLAlchemy-сессии.
        """
        self.session = session

    def __enter__(self) -> 'Self':
        """Входит в контекстный менеджер Unit of Work.

        Returns:
            Текущий экземпляр Unit of Work.
        """
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: object | None
    ) -> None:
        """Выходит из контекста Unit of Work, выполняя commit() или rollback().

        Args:
            exc_type: Тип исключения.
            exc_value: Объект исключения.
            traceback: Трассировка исключения.
        """
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        """Фиксирует изменения в базе данных."""
        self.session.commit()

    def rollback(self) -> None:
        """Откатывает изменения в базе данных."""
        self.session.rollback()
