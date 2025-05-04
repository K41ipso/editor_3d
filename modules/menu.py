import os
import sys
from typing import Any, List, Tuple
import math

from functools import partial

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
    QFileDialog,
    QDialog
)

from modules.actions import continue_last_session, create_new_space, load_saved_space
from modules.audio import play_background_music, play_sound_effect
from modules.engine import Engine, OpenGLWidget
from modules.input_handler.keyboard import KeyboardHandler
from modules.tools.input_dialog import PointsInputDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.engine = Engine()  # Создаем экземпляр движка
        self.opengl = OpenGLWidget(space_data=self.engine.get_space()) # Создаем экземпляр рендера

        # Инициализация обработчика клавиатуры
        self.keyboard_handler = KeyboardHandler(main_window=self)

        # Привязка клавиш
        self.keyboard_handler.bind_key("W", self.keyboard_handler.move_forward)
        self.keyboard_handler.bind_key("A", self.keyboard_handler.move_left)
        self.keyboard_handler.bind_key("S", self.keyboard_handler.move_backward)
        self.keyboard_handler.bind_key("D", self.keyboard_handler.move_right)
        self.keyboard_handler.bind_key("Q", self.keyboard_handler.move_up)
        self.keyboard_handler.bind_key("E", self.keyboard_handler.move_down)
        self.keyboard_handler.bind_key("Z", lambda: self.close())
        self.keyboard_handler.bind_key("Ц", self.keyboard_handler.move_forward)
        self.keyboard_handler.bind_key("Ф", self.keyboard_handler.move_left)
        self.keyboard_handler.bind_key("Ы", self.keyboard_handler.move_backward)
        self.keyboard_handler.bind_key("В", self.keyboard_handler.move_right)
        self.keyboard_handler.bind_key("Й", self.keyboard_handler.move_up)
        self.keyboard_handler.bind_key("У", self.keyboard_handler.move_down)
        self.keyboard_handler.bind_key("Я", lambda: self.close())

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
                icon_path = os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "resources",
                        "images",
                        "app_icon_win.ico"
                    )
                )
            else:  # Для macOS/Linux
                icon_path = (
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "resources",
                        "images",
                        "app_icon_mac.png"
                    )
                )

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
            icon_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../resources/images/app_icon_win.ico"
                )
            )

            # Проверяем существование файла
            if not os.path.exists(icon_path):
                raise FileNotFoundError(
                    f"Иконка не найдена по пути {icon_path}"
                )

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
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.normpath(
                os.path.join(
                    script_dir,
                    "..",
                    "resources",
                    "images",
                    image_name
                )
            )

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

        """Обработка нажатия клавиш."""
        key = event.text().upper()  # Преобразуем символ в верхний регистр
        if key:
            renderer = OpenGLWidget(space_data=self.engine.get_space(), keyboard_handler=self.keyboard_handler)
            self.keyboard_handler.set_opengl_widget(renderer)
            self.keyboard_handler.handle_key_press(key)
        super().keyPressEvent(event)  # Вызываем базовый метод для дальнейшей обработки

    def set_is_edit_mode_true(self):
        self.is_edit_mode = True

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
        continue_last_session(self)

    def create_new_space(self) -> None:
        print("Создание нового пространства...")
        self.set_is_edit_mode_true()
        create_new_space(self)

    def load_space(self) -> None:
        print("Загрузка пространства...")
        load_saved_space(self)

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
        save_action.triggered.connect(partial(self.engine.save_space, self))

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_space)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.engine.exit_application)

        draw_planes_menu = menu_bar.addMenu("Рисование плоскостей через")
        draw_planes_menu.addAction("Три точки", self.on_draw_plane_three_points)
        draw_planes_menu.addAction("Точку и отрезок", self.on_draw_plane_point_segment)
        draw_planes_menu.addAction("Точку и параллель", self.on_draw_plane_point_parallel)

        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        print("Верхнее меню успешно создано.")

    @staticmethod
    def sort_points(points: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
        # Вычисляем центр
        centroid = (
            sum(p[0] for p in points) / len(points),
            sum(p[1] for p in points) / len(points),
            sum(p[2] for p in points) / len(points)
        )

        # Сортируем точки по углу относительно центра
        def angle_from_centroid(point):
            return math.atan2(point[1] - centroid[1], point[0] - centroid[0])

        sorted_points = sorted(points, key=angle_from_centroid)
        return sorted_points

    def on_draw_plane_three_points(self):
        try:
            print("Рисование плоскости через три точки")
            dialog = PointsInputDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                points, color = dialog.get_points_and_color()
                print(f"Полученные координаты: {points}, цвет: {color}")
                sorted_points = self.sort_points(points)

                # Добавляем плоскость в движок
                self.engine.add_plane("plane_id", sorted_points, color)
                self.opengl.data_space_reload(self.engine.get_space())
        except Exception as e:
            print(f"Ошибка при рисовании плоскости: {e}")

    def on_draw_plane_point_segment(self):
        pass
        # try:
        #     self.update_opengl_widget()
        #     print("Рисование плоскости через точку и отрезок")
        #     current_widget = self.centralWidget()
        #     if isinstance(current_widget, OpenGLWidget):
        #         current_widget.draw_cube()
        #         current_widget.update()
        #         print("Куб успешно отрисован")
        #     else:
        #         print("Текущий центральный виджет не является OpenGLWidget.")
        # except Exception as e:
        #     print(f"Ошибка при рисовании куба: {e}")

    def on_draw_plane_point_parallel(self):
        # Логика для "Точку и параллель"
        print("Рисование плоскости через точку и параллель")

    def load_space_from_file(self) -> None:
        """
        Загружает пространство из выбранного файла.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл сохранения",
            "saves/",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        if file_name:
            self.engine.load_space(file_path=file_name)
            print(f"Пространство загружено из {file_name}.")
            self.setup_main_menu()  # Восстанавливаем меню после загрузки

    def update_opengl_widget(self) -> None:
        """
        Обновляет OpenGL-виджет после загрузки нового пространства.
        """
        rotation_x = 0.0
        rotation_y = 0.0
        last_mouse_pos = None
        mouse_pressed = False
        try:
            # Удаляем старый виджет и сохраняем его состояние
            old_widget = self.centralWidget()
            if isinstance(old_widget, OpenGLWidget):
                # Сохраняем углы поворота и положение мыши
                rotation_x = old_widget.rotation_x
                rotation_y = old_widget.rotation_y
                last_mouse_pos = old_widget.last_mouse_pos
                mouse_pressed = old_widget.mouse_pressed
                old_widget.deleteLater()

            # Создаем новый OpenGL-виджет с загруженным пространством
            renderer = OpenGLWidget(
                space_data=self.engine.get_space(),
                keyboard_handler=self.keyboard_handler,
                rotation_x=rotation_x,
                rotation_y=rotation_y,
                last_mouse_pos=last_mouse_pos,
                mouse_pressed=True
            )
            self.keyboard_handler.set_opengl_widget(renderer)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
