from typing import Any, List, Tuple

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout  # type: ignore


class PointsInputDialog(QDialog):
    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Рисование плоскости по трем точкам")
        self.layout = QVBoxLayout(self)

        # Добавляем поля для ввода координат
        self.point_labels = [QLabel(f"Точка {i + 1}:") for i in range(3)]
        self.point_inputs = [[QLineEdit(self) for _ in range(3)] for _ in range(3)]

        # Устанавливаем валидатор для ввода только чисел
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setRange(-999.0, 999.0)  # Установите диапазон значений по вашему усмотрению

        for i, (label, input_fields) in enumerate(zip(self.point_labels, self.point_inputs)):
            self.layout.addWidget(label)
            h_layout = QHBoxLayout()
            for input_field in input_fields:
                input_field.setValidator(validator)
                h_layout.addWidget(input_field)
            self.layout.addLayout(h_layout)

        # Добавляем выпадающий список для выбора цвета
        self.color_combo = QComboBox(self)
        self.color_combo.addItems(
            [
                "Красный",
                "Зеленый",
                "Синий",
                "Желтый",
                "Фиолетовый",
                "Оранжевый",
                "Розовый",
                "Коричневый",
                "Черный",
                "Белый",
            ]
        )
        self.layout.addWidget(QLabel("Выберите цвет:"))
        self.layout.addWidget(self.color_combo)

        # Кнопка подтверждения
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)  # type: ignore
        self.layout.addWidget(self.ok_button)

    def get_points_and_color(self) -> Tuple[List[Tuple[float, float, float]], Tuple[float, float, float]]:
        points = []
        for input_fields in self.point_inputs:
            x = float(input_fields[0].text())
            y = float(input_fields[1].text())
            z = float(input_fields[2].text())
            points.append((x, y, z))

        # Получаем цвет
        color_name = self.color_combo.currentText()
        color_map = {
            "Красный": (1.0, 0.0, 0.0),
            "Зеленый": (0.0, 1.0, 0.0),
            "Синий": (0.0, 0.0, 1.0),
            "Желтый": (1.0, 1.0, 0.0),
            "Фиолетовый": (0.5, 0.0, 0.5),
            "Оранжевый": (1.0, 0.5, 0.0),
            "Розовый": (1.0, 0.0, 1.0),
            "Коричневый": (0.6, 0.3, 0.0),
            "Черный": (0.0, 0.0, 0.0),
            "Белый": (1.0, 1.0, 1.0),
        }
        color = color_map[color_name]

        return points, color
