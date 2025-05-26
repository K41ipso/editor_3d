import unittest
from typing import Any
from unittest.mock import patch

from PyQt5.QtWidgets import QMainWindow

from modules.actions import continue_last_session, create_new_space, load_saved_space
from modules.engine.core import Engine


class TestActions(unittest.TestCase):
    def setUp(self) -> None:
        from PyQt5.QtWidgets import QApplication

        self.app = QApplication([])

        self.engine = Engine()
        self.main_window = QMainWindow()

    def tearDown(self) -> None:
        self.app.quit()

    @patch("modules.actions.new_space.Engine")
    def test_create_new_space(self, MockEngine: Any) -> None:
        """Проверка создания нового пространства."""
        create_new_space()  # type: ignore
        MockEngine.return_value.initialize_empty_space.assert_called_once()

    @patch("modules.actions.load_space.Engine")
    def test_load_saved_space(self, MockEngine: Any) -> None:
        """Проверка загрузки сохранённого пространства."""
        load_saved_space()
        MockEngine.return_value.load_space.assert_called_once()

    @patch("modules.actions.continues.Engine")
    def test_continue_last_session(self, MockEngine: Any) -> None:
        """Проверка продолжения последней сессии."""
        continue_last_session()

        MockEngine.return_value.continue_last_session.assert_called_once()


if __name__ == "__main__":
    unittest.main()
