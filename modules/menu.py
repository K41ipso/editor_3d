import os
import sys
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QMainWindow,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from modules.actions import continue_last_session, create_new_space
from modules.audio import play_background_music, play_sound_effect
from modules.engine import Engine, OpenGLWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.engine = Engine()  # Создаем экземпляр движка

        # Установка иконки приложения
        self.setup_window_icon()

        # Настройка иконки в трее
        self.setup_tray_icon()

        # Настройка главного окна
        self.setWindowTitle("3D Editor")

        # Установка размеров и позиции окна
        self.set_window_geometry(width_percent=0.8, height_percent=0.7)

        # Установка фонового изображения
        self.set_background_image("background.png")  # Передаем только имя файла

        # Настройка верхнего меню
        self.setup_main_menu()

        # Настройка главного меню с большими кнопками
        self.setup_main_buttons()

        # Обработка события по кнопке "Выход"
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.close)  # type: ignore[attr-defined]

        # Воспроизведение фоновой музыки
        play_background_music("menu_music_e1m1.mp3", volume=0)

    def setup_window_icon(self) -> None:
        """
        Настройка иконки главного окна приложения.
        """
        try:
            # Определяем путь к иконке в зависимости от платформы
            if sys.platform == "win32":  # Для Windows
                icon_path = os.path.join(os.path.dirname(__file__), "../resources/images/app_icon_win.ico")
            else:  # Для macOS/Linux
                icon_path = os.path.join(os.path.dirname(__file__), "../resources/images/app_icon_mac.png")

            # Проверяем существование файла
            if not os.path.exists(icon_path):
                raise FileNotFoundError(f"Иконка не найдена по пути {icon_path}")

            # Загружаем иконку
            icon = QIcon(icon_path)
            if icon.isNull():
                raise ValueError(f"Не удалось загрузить иконку из файла {icon_path}")

            # Устанавливаем иконку для главного окна
            self.setWindowIcon(icon)
            print("Иконка успешно загружена.")

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            print("Используется стандартная иконка.")
            # Можно установить дефолтную иконку, если пользовательская не найдена
            # Например:
            # self.setWindowIcon(QIcon(":/default_icon.png"))

        except ValueError as e:
            print(f"Ошибка: {e}")
            print("Используется стандартная иконка.")
            # Можно установить дефолтную иконку, если произошла ошибка загрузки
            # Например:
            # self.setWindowIcon(QIcon(":/default_icon.png"))

        except Exception as e:
            print(f"Неожиданная ошибка при загрузке иконки: {e}")
            print("Используется стандартная иконка.")
            # Можно установить дефолтную иконку, если произошла другая ошибка
            # Например:
            # self.setWindowIcon(QIcon(":/default_icon.png"))

    def setup_tray_icon(self) -> None:
        """
        Настройка иконки в системном трее.
        """
        try:
            # Абсолютный путь к иконке
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/images/app_icon_win.ico"))

            # Проверяем существование файла
            if not os.path.exists(icon_path):
                raise FileNotFoundError(f"Иконка не найдена по пути {icon_path}")

            # Загружаем иконку
            icon = QIcon(icon_path)
            if icon.isNull():
                raise ValueError("Не удалось загрузить иконку.")

            # Создаем иконку в трее
            self.tray_icon = QSystemTrayIcon(icon, self)
            self.tray_icon.show()

            # Создаем контекстное меню для иконки
            tray_menu = QMenu()
            exit_action = tray_menu.addAction("Exit")  # Добавляем действие "Exit"
            exit_action.triggered.connect(self.close)  # При нажатии на "Exit" закрываем приложение

            # Привязываем меню к иконке
            self.tray_icon.setContextMenu(tray_menu)

            print("Иконка в трее успешно загружена.")
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            print("Иконка в трее не будет отображаться.")
        except ValueError as e:
            print(f"Ошибка: {e}")
            print("Иконка в трее не будет отображаться.")
        except Exception as e:
            print(f"Неожиданная ошибка при настройке иконки в трее: {e}")
            print("Иконка в трее не будет отображаться.")

    def set_window_geometry(self, width_percent: float, height_percent: float) -> None:
        """
        Установка размеров и позиции окна в процентах от разрешения экрана.
        :param width_percent: Процент ширины экрана (например, 0.8 для 80%).
        :param height_percent: Процент высоты экрана (например, 0.7 для 70%).
        """
        # Получение разрешения экрана
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Размеры окна
        window_width = int(screen_width * width_percent)
        window_height = int(screen_height * height_percent)

        # Позиция окна (центр экрана)
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Установка геометрии окна
        self.setGeometry(x, y, window_width, window_height)

    def set_background_image(self, image_name: str = "background.png") -> None:
        """
        Установка фонового изображения.
        :param image_name: Имя файла фонового изображения (по умолчанию "background.png").
        """
        try:
            # Формируем путь к изображению
            image_path = os.path.join(os.path.dirname(__file__), "../resources/images", image_name)

            # Проверяем существование файла
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Фоновое изображение не найдено по пути {image_path}")

            # Загружаем изображение
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise ValueError(f"Не удалось загрузить фоновое изображение из файла {image_path}")

            # Устанавливаем фоновое изображение
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(pixmap))
            self.setPalette(palette)
            print("Фоновое изображение успешно загружено.")

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            print("Фоновое изображение не будет установлено.")

        except ValueError as e:
            print(f"Ошибка: {e}")
            print("Фоновое изображение не будет установлено.")

        except Exception as e:
            print(f"Неожиданная ошибка при загрузке фонового изображения: {e}")
            print("Фоновое изображение не будет установлено.")

    def resizeEvent(self, event: Any) -> None:
        """
        Обработка события изменения размера окна.
        Пересчитываем размеры кнопок и текста при изменении размера окна.
        """
        self.update_button_sizes()
        super().resizeEvent(event)  # type: ignore

    def update_button_sizes(self) -> None:
        """
        Обновление размеров кнопок и текста в зависимости от размера окна.
        """
        width = self.width()
        height = self.height()

        # Размер кнопок (50% ширины окна, высота 10% от высоты окна)
        button_width = int(width * 0.5)
        button_height = int(height * 0.08)

        # Размер шрифта (пропорционально высоте окна)
        font_size = max(12, int(height * 0.04))  # Минимальный размер шрифта: 12

        # Обновляем размеры и стиль всех кнопок
        for button in self.findChildren(QPushButton):
            button.setFixedSize(button_width, button_height)
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #404040;  /* Серый фон */
                    color: white;               /* Белый текст */
                    font-size: {font_size}px;   /* Размер шрифта */
                    border-radius: 10px;        /* Закругленные углы */
                    text-align: center;         /* Центрирование текста */
                }}
                QPushButton:hover {{
                    background-color: #303030;  /* Темнее при наведении */
                }}
                QPushButton:pressed {{
                    background-color: #202020;  /* Очень темный фон при нажатии */
                    color: gray;               /* Серый текст при нажатии */
                }}
            """
            )

    def keyPressEvent(self, event: Any) -> None:
        """
        Обработка нажатия клавиш.
        Переключение полноэкранного режима при нажатии F11.
        Возврат в главное меню при нажатии Esc.
        """
        if event.key() == Qt.Key_F11:  # Переключение полноэкранного режима при нажатии F11
            if self.isFullScreen():
                self.showNormal()  # Возвращение в обычный режим
            else:
                self.showFullScreen()  # Переключение на полноэкранный режим
        elif event.key() == Qt.Key_Escape:  # Возврат в главное меню при нажатии Esc
            self.return_to_main_menu()

    def setup_main_buttons(self) -> None:
        """Настройка главного меню с большими кнопками."""
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создание вертикального макета
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Центрирование кнопок
        layout.setSpacing(15)  # Расстояние между кнопками

        # Список кнопок с их действиями
        buttons_data = [
            ("Продолжить редактирование", lambda: self.continue_editing()),
            ("Новое пространство", lambda: self.create_new_space()),
            ("Загрузить пространство", lambda: self.load_space()),
            ("Настройки", lambda: self.open_settings()),
            ("Выход", self.close),
        ]

        # Добавление кнопок
        for text, action in buttons_data:
            button = QPushButton(text)
            # Подключение универсального обработчика
            button.clicked.connect(self.create_button_handler(action))  # type: ignore[attr-defined]
            layout.addWidget(button)

        # Установка макета
        central_widget.setLayout(layout)

        # Инициализация размеров кнопок
        self.update_button_sizes()

    def create_button_handler(self, action: Any) -> Any:
        """
        Создает обработчик для кнопки, который воспроизводит звук и выполняет основное действие.
        :param action: Основное действие кнопки.
        :return: Функция-обработчик.
        """

        def handler() -> None:
            # Воспроизведение звука нажатия
            play_sound_effect("pm_button_click.mp3")
            # Выполнение основного действия
            action()

        return handler

    def continue_editing(self) -> None:
        print("Продолжение редактирования...")
        continue_last_session()

    def create_new_space(self) -> None:
        print("Создание нового пространства...")
        create_new_space(self)

    def load_space(self) -> None:
        print("Загрузка пространства...")
        self.load_saved_space()

    def open_settings(self) -> None:
        print("Открытие настроек...")

    def setup_main_menu(self) -> None:
        """
        Настройка верхнего меню (маленькие кнопки).
        """
        # Удаляем существующее меню, если оно есть
        if hasattr(self, "menuBar") and self.menuBar():
            self.menuBar().clear()

        # Создаем новую панель меню
        menu_bar = self.menuBar()
        # Меню "File"
        file_menu = menu_bar.addMenu("File")
        save_action = QAction("Save", self)
        load_action = QAction("Load", self)
        exit_action = QAction("Exit", self)
        save_action.triggered.connect(self.save_current_space)  # type: ignore[attr-defined]
        load_action.triggered.connect(self.load_saved_space)  # type: ignore[attr-defined]
        exit_action.triggered.connect(self.close)  # type: ignore[attr-defined]
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        print("Верхнее меню успешно создано.")

    def save_current_space(self) -> None:
        """
        Сохраняет текущее состояние пространства.
        """
        try:
            save_path = "saves/current_space.json"
            self.engine.save_space(file_path=save_path)
            print(f"Текущее пространство успешно сохранено в {save_path}.")
        except Exception as e:
            print(f"Ошибка при сохранении пространства: {e}")

    def load_saved_space(self) -> None:
        """
        Загружает последнее сохраненное состояние пространства.
        """
        try:
            save_path = "saves/current_space.json"
            self.engine.load_space(file_path=save_path)
            print(f"Пространство успешно загружено из {save_path}.")
            self.update_opengl_widget()  # Обновляем OpenGL-виджет после загрузки
        except Exception as e:
            print(f"Ошибка при загрузке пространства: {e}")

    def update_opengl_widget(self) -> None:
        """
        Обновляет OpenGL-виджет после загрузки нового пространства.
        """
        try:
            # Удаляем старый виджет
            old_widget = self.centralWidget()
            if old_widget:
                old_widget.deleteLater()

            # Создаем новый OpenGL-виджет с загруженным пространством
            renderer = OpenGLWidget(self.engine.get_space())
            self.setCentralWidget(renderer)
            print("OpenGL-виджет успешно обновлен.")
        except Exception as e:
            print(f"Ошибка при обновлении OpenGL-виджета: {e}")

    def remove_main_menu(self) -> None:
        """
        Удаляет верхнее меню.
        """
        if hasattr(self, "menuBar"):
            self.menuBar().clear()
            print("Верхнее меню успешно удалено.")

    def return_to_main_menu(self) -> None:
        """
        Возвращает пользователя в главное меню.
        """
        self.remove_main_menu()  # Удаляем верхнее меню
        self.setup_main_buttons()  # Восстанавливаем главное меню с большими кнопками
        print("Возвращение в главное меню.")
