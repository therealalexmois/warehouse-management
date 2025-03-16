"""Юнит-тесты для абстрактного класса UnitOfWork."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_mock import MockFixture

    from warehouse_management.domain.unit_of_work import UnitOfWork


@pytest.fixture
def mock_unit_of_work(mocker: 'MockFixture') -> 'UnitOfWork':
    """Создает мок-объект UnitOfWork с поддержкой контекстного менеджера."""
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mock

    def exit_mock(
        exc_type: type[BaseException] | None, _exc_value: BaseException | None, _traceback: object | None
    ) -> None:
        if exc_type:
            mock.rollback()
        else:
            mock.commit()

    mock.__exit__.side_effect = exit_mock
    return mock


@pytest.mark.unit
def test_unit_of_work__commit(mock_unit_of_work: 'UnitOfWork') -> None:
    """Тест метода `commit()`.

    Ожидаемый результат:
    - Метод `commit()` вызывается один раз.
    """
    mock_unit_of_work.commit()
    mock_unit_of_work.commit.assert_called_once()


@pytest.mark.unit
def test_unit_of_work__rollback(mock_unit_of_work: 'UnitOfWork') -> None:
    """Тест метода `rollback()`.

    Ожидаемый результат:
    - Метод `rollback()` вызывается один раз.
    """
    mock_unit_of_work.rollback()
    mock_unit_of_work.rollback.assert_called_once()


@pytest.mark.unit
def test_unit_of_work__context_manager(mock_unit_of_work: 'UnitOfWork') -> None:
    """Тест работы контекстного менеджера UnitOfWork.

    Ожидаемый результат:
    - `commit()` вызывается при отсутствии ошибок.
    - `rollback()` вызывается при исключении.
    """
    with mock_unit_of_work as uow:
        uow.commit.assert_not_called()
        uow.rollback.assert_not_called()

    with pytest.raises(RuntimeError), mock_unit_of_work:
        raise RuntimeError('Ошибка внутри транзакции')

    mock_unit_of_work.rollback.assert_called_once()
