import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QEvent
from modules.menu import MainWindow
import os

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = MainWindow()

    def tearDown(self):
        self.app.quit()

    @patch("modules.menu.QPixmap")
    def test_set_background_image(self, MockQPixmap):
        """Проверка установки фонового изображения."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.normpath(os.path.join(script_dir, "../resources/images/test_image.png"))

        self.window.set_background_image("test_image.png")

        MockQPixmap.assert_called_with(image_path)

    @patch("modules.menu.QIcon")
    def test_setup_window_icon(self, MockQIcon):
        """Проверка настройки иконки окна."""
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/images/app_icon_win.ico"))
        self.window.setup_window_icon()
        MockQIcon.assert_called_with(icon_path)

    @patch("modules.menu.MainWindow.resizeEvent")
    def test_resize_event(self, mock_update):
        """Проверка обновления размеров кнопок при изменении размера окна."""
        event = QEvent(QEvent.Resize)
        self.window.resizeEvent(event)

        mock_update.assert_called()

    @patch("modules.menu.MainWindow.create_button_handler")
    def test_setup_main_buttons(self, mock_create_button_handler):
        """Проверка создания кнопок главного меню."""
        self.window.setup_main_buttons()

        central_widget = self.window.centralWidget()
        layout = central_widget.layout()

        self.assertEqual(layout.count(), 5)

        expected_texts = [
            "Продолжить редактирование",
            "Новое пространство",
            "Загрузить пространство",
            "Настройки",
            "Выход",
        ]
        for i, text in enumerate(expected_texts):
            button = layout.itemAt(i).widget()
            self.assertIsInstance(button, QPushButton)
            self.assertEqual(button.text(), text)

        self.assertEqual(mock_create_button_handler.call_count, 5)

if __name__ == "__main__":
    unittest.main()