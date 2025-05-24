from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout

import os

class ScreenshotNotification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Основной горизонтальный layout
        layout = QHBoxLayout()
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(18)

        # --- Квадратик для иконки ---
        icon_square = QWidget()
        icon_square.setFixedSize(64, 64)  # Квадрат 64x64
        icon_square.setStyleSheet("""
            background-color: rgba(60, 60, 60, 200);
            border-radius: 12px;
        """)
        # Внутри квадрата — QLabel с иконкой, по центру
        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.normpath(os.path.join(script_dir, "..", "..", "resources", "images", "screen_logo.png"))
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        icon_square.setLayout(icon_layout)
        layout.addWidget(icon_square)

        # --- Текст справа ---
        self.text_label = QLabel("Скриншот сохранен")
        self.text_label.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding-left: 8px;
        """)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

        # Стилизация всего уведомления
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 14px;
            }
        """)

        self.setWindowFlags(
            Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_with_animation)

    def show_notification(self, parent_window):
        # Позиционируем в правом нижнем углу главного окна
        parent_geom = parent_window.geometry()
        notif_width = 400  # Сделаем шире, чтобы текст не сливался с иконкой
        notif_height = 100
        x = parent_geom.x() + parent_geom.width() - notif_width - 40
        y = parent_geom.y() + parent_geom.height() - notif_height - 40
        self.setGeometry(x, y, notif_width, notif_height)
        self.setWindowOpacity(1.0)
        self.show()
        self.raise_()
        self.timer.start(2000)

    def hide_with_animation(self):
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.hide)
        self.animation.start()
