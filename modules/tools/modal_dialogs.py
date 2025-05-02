from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel

class PointsInputDialog(QDialog):
    def __init__(self, parent=None):
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
            (self.point1_x.text(), self.point1_y.text(), self.point1_z.text()),
            (self.point2_x.text(), self.point2_y.text(), self.point2_z.text()),
            (self.point3_x.text(), self.point3_y.text(), self.point3_z.text())
        )
