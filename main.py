import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
import os
from modules.menu import setup_main_menu
from modules.audio import play_background_music


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("3D Editor")
        self.setGeometry(100, 100, 800, 600)

        # Установка фонового изображения
        image_path = os.path.join(os.path.dirname(__file__), "resources/images/background_doom.png")
        self.set_background_image(image_path)

        # Настройка главного меню
        setup_main_menu(self)

    def set_background_image(self, image_path):
        """Установка фонового изображения."""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Ошибка: Не удалось загрузить изображение по пути {image_path}")
        else:
            print("Изображение успешно загружено.")

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)


def main():
    # Создание приложения PyQt5
    app = QApplication(sys.argv)

    # Загрузка фоновой музыки
    music_path = os.path.join(os.path.dirname(__file__), "resources/sounds/menu_music_e1m1.mp3")
    play_background_music(music_path)

    # Создание главного окна
    window = MainWindow()
    window.show()

    # Запуск основного цикла
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()