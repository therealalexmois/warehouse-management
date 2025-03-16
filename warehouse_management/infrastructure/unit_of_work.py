from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from warehouse_management.domain.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from typing import Self


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session) -> None:
        self.session = session

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
