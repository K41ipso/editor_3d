from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel, QComboBox

class PointsInputDialog(QDialog):
    def __init__(self, parent=None, ):
        super().__init__(parent)
        self.setWindowTitle("Введите координаты трех точек")
        self.layout = QVBoxLayout(self)

        self.point1_layout = QHBoxLayout()
        self.point2_layout = QHBoxLayout()
        self.point3_layout = QHBoxLayout()

        self.point1_x = QLineEdit(self)
        self.point1_x.setMaxLength(4)
        self.point1_x.setPlaceholderText("X1")
        self.point1_layout.addWidget(QLabel("Точка 1:"))
        self.point1_layout.addWidget(self.point1_x)

        self.point1_y = QLineEdit(self)
        self.point1_y.setMaxLength(4)
        self.point1_y.setPlaceholderText("Y1")
        self.point1_layout.addWidget(self.point1_y)

        self.point1_z = QLineEdit(self)
        self.point1_z.setMaxLength(4)
        self.point1_z.setPlaceholderText("Z1")
        self.point1_layout.addWidget(self.point1_z)

        self.layout.addLayout(self.point1_layout)

        self.point2_x = QLineEdit(self)
        self.point2_x.setMaxLength(4)
        self.point2_x.setPlaceholderText("X2")
        self.point2_layout.addWidget(QLabel("Точка 2:"))
        self.point2_layout.addWidget(self.point2_x)

        self.point2_y = QLineEdit(self)
        self.point2_y.setMaxLength(4)
        self.point2_y.setPlaceholderText("Y2")
        self.point2_layout.addWidget(self.point2_y)

        self.point2_z = QLineEdit(self)
        self.point2_z.setMaxLength(4)
        self.point2_z.setPlaceholderText("Z2")
        self.point2_layout.addWidget(self.point2_z)

        self.layout.addLayout(self.point2_layout)

        self.point3_x = QLineEdit(self)
        self.point3_x.setMaxLength(4)
        self.point3_x.setPlaceholderText("X3")
        self.point3_layout.addWidget(QLabel("Точка 3:"))
        self.point3_layout.addWidget(self.point3_x)

        self.point3_y = QLineEdit(self)
        self.point3_y.setMaxLength(4)
        self.point3_y.setPlaceholderText("Y3")
        self.point3_layout.addWidget(self.point3_y)

        self.point3_z = QLineEdit(self)
        self.point3_z.setMaxLength(4)
        self.point3_z.setPlaceholderText("Z3")
        self.point3_layout.addWidget(self.point3_z)

        self.layout.addLayout(self.point3_layout)

        self.submit_button = QPushButton("Отправить", self)
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

    def get_points(self):
        return (
            (float(self.point1_x.text()), float(self.point1_y.text()), float(self.point1_z.text())),
            (float(self.point2_x.text()), float(self.point2_y.text()), float(self.point2_z.text())),
            (float(self.point3_x.text()), float(self.point3_y.text()), float(self.point3_z.text()))
        )

class PointSegmentInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Рисование плоскости через точку и отрезок")
        self.layout = QVBoxLayout(self)

        # Валидатор для ввода чисел
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setRange(-999.0, 999.0)  # Установите диапазон значений по вашему усмотрению

        # Поле для первой точки (точка P)
        self.point_layout = QHBoxLayout()
        self.point_x = QLineEdit(self)
        self.point_y = QLineEdit(self)
        self.point_z = QLineEdit(self)
        for field in (self.point_x, self.point_y, self.point_z):
            field.setValidator(validator)
            field.setMaxLength(4)
        self.point_layout.addWidget(QLabel("Координаты точки:               "))
        self.point_layout.addWidget(self.point_x)
        self.point_layout.addWidget(self.point_y)
        self.point_layout.addWidget(self.point_z)
        self.layout.addLayout(self.point_layout)

        # Поле для начала отрезка (точка A)
        self.start_segment_layout = QHBoxLayout()
        self.start_x = QLineEdit(self)
        self.start_y = QLineEdit(self)
        self.start_z = QLineEdit(self)
        for field in (self.start_x, self.start_y, self.start_z):
            field.setValidator(validator)
            field.setMaxLength(4)
        self.start_segment_layout.addWidget(QLabel("Координаты начала отрезка:"))
        self.start_segment_layout.addWidget(self.start_x)
        self.start_segment_layout.addWidget(self.start_y)
        self.start_segment_layout.addWidget(self.start_z)
        self.layout.addLayout(self.start_segment_layout)

        # Поле для конца отрезка (точка B)
        self.end_segment_layout = QHBoxLayout()
        self.end_x = QLineEdit(self)
        self.end_y = QLineEdit(self)
        self.end_z = QLineEdit(self)
        for field in (self.end_x, self.end_y, self.end_z):
            field.setValidator(validator)
            field.setMaxLength(4)
        self.end_segment_layout.addWidget(QLabel("Координаты конца отрезка:  "))
        self.end_segment_layout.addWidget(self.end_x)
        self.end_segment_layout.addWidget(self.end_y)
        self.end_segment_layout.addWidget(self.end_z)
        self.layout.addLayout(self.end_segment_layout)

        # Выпадающий список для выбора цвета
        self.color_combo = QComboBox(self)
        self.color_combo.addItems([
            "Красный", "Зеленый", "Синий", "Желтый", "Фиолетовый",
            "Оранжевый", "Розовый", "Коричневый", "Черный", "Белый"
        ])
        self.layout.addWidget(QLabel("Выберите цвет:"))
        self.layout.addWidget(self.color_combo)

        # Кнопка подтверждения
        self.submit_button = QPushButton("Отправить", self)
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

    def get_data(self):
        # Получаем координаты точки P
        point = (
            float(self.point_x.text()),
            float(self.point_y.text()),
            float(self.point_z.text())
        )

        # Получаем координаты начала отрезка A
        start_segment = (
            float(self.start_x.text()),
            float(self.start_y.text()),
            float(self.start_z.text())
        )

        # Получаем координаты конца отрезка B
        end_segment = (
            float(self.end_x.text()),
            float(self.end_y.text()),
            float(self.end_z.text())
        )

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
            "Белый": (1.0, 1.0, 1.0)
        }
        color = color_map[color_name]

        return point, start_segment, end_segment, color