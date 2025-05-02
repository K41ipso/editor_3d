from PyQt5.QtWidgets import QToolBar, QAction, QLabel
from PyQt5.QtCore import Qt

class EditorToolBar(QToolBar):
    def __init__(self, parent=None):
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

    def add_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        label.setStyleSheet("""
            background-color: #555;  # Серый фон
            color: white;            # Белый текст
            font-weight: bold;       # Жирный шрифт
            font-size: 14px;         # Размер шрифта
            padding: 5px;            # Отступы
        """)
        self.addWidget(label)

    def add_action(self, text, callback=None):
        action = QAction(text, self)
        if callback:
            action.triggered.connect(callback)
        self.addAction(action)