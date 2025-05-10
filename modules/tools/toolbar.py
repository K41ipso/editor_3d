from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QLabel, QToolBar


class EditorToolBar(QToolBar):
    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Editor Toolbar")

        # Устанавливаем белый фон для всей панели инструментов
        self.setStyleSheet("background-color: white;")

        # Добавляем заголовки и кнопки
        self.add_label("Рисование плоскостей через")
        self.add_action("Три точки")
        self.add_action("Точку и отрезок")
        self.add_action("Точку и параллель")

        self.add_label("Рисование продвинутое")
        self.add_action("Многогранников")
        self.add_action("Сечение плоскости")

        self.add_label("Перемещение")
        self.add_action("Точек")
        self.add_action("Прямых")
        self.add_action("Плоскостей")

    def add_label(self, text: str) -> None:
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        label.setStyleSheet(
            """
            background-color: #555;  # Серый фон
            color: white;            # Белый текст
            font-weight: bold;       # Жирный шрифт
            font-size: 14px;         # Размер шрифта
            padding: 5px;            # Отступы
        """
        )
        self.addWidget(label)

    def add_action(self, text: str, callback: Any = None) -> None:
        action = QAction(text, self)
        if callback:
            action.triggered.connect(callback)  # type: ignore
        self.addAction(action)
