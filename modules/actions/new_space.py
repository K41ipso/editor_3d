from typing import Any

from PyQt5.QtCore import QThread

from modules.engine.core import Engine
from modules.engine.opengl_widget import OpenGLWidget


class SpaceCreationThread(QThread):
    def __init__(self, engine: Any, dimensions: tuple[int, int, int], save_path: str) -> None:
        """
        Инициализация потока для создания нового пространства.
        :param engine: Экземпляр движка.
        :param dimensions: Размеры пространства (например, (10, 10, 10)).
        :param save_path: Путь для сохранения состояния.
        """
        super().__init__()
        self.engine = engine
        self.dimensions = dimensions
        self.save_path = save_path

    def run(self) -> None:
        """
        Основной метод потока.
        Создает новое пространство и сохраняет его состояние.
        """
        self.engine.initialize_empty_space(dimensions=self.dimensions)
        self.engine.save_space(self.save_path)


def create_new_space(main_window: Any = None) -> None:
    """
    Создает новое пространство, сохраняет его состояние и отображает его.
    :param main_window: Экземпляр MainWindow.
    """
    engine = Engine()
    engine.initialize_empty_space(dimensions=(10, 10, 10))
    print("Новое пространство создано.")


    # Сохраняем состояние в файл
    save_path = "saves/new_space.json"
    engine.save_space(save_path)
    print(f"Состояние сохранено в {save_path}.")

    # Проверяем, что main_window передан
    if main_window is not None:
        # Удаляем старый виджет
        old_widget = main_window.centralWidget()
        if old_widget:
            old_widget.deleteLater()

        # Заменяем главное меню на OpenGL-виджет
        print("Инициализация OpenGL...")
        renderer = OpenGLWidget(engine.get_space())
        print("OpenGL инициализирован.")
        main_window.setCentralWidget(renderer)
        print('setCentralWidget закончил свою работу.')

        # Добавляем верхнее меню
        try:
            main_window.setup_main_menu()
        except AttributeError:
            print("Ошибка: Метод setup_main_menu не найден в классе MainWindow.")
        except Exception as e:
            print(f"Неожиданная ошибка при настройке верхнего меню: {e}")

        print("Пространство отображено.")
    else:
        print("Параметр main_window не передан. Пространство создано без GUI.")


def on_space_created(main_window: Any, space_data: Any) -> None:
    """
    Вызывается после завершения создания пространства.
    :param main_window: Экземпляр MainWindow.
    :param space_data: Данные созданного пространства.
    """
    print("Новое пространство создано.")

    # Удаляем старый виджет
    old_widget = main_window.centralWidget()
    if old_widget:
        old_widget.deleteLater()

    # Заменяем главное меню на OpenGL-виджет
    from modules.engine.render import Renderer  # Импортируем Renderer

    renderer = Renderer(space_data)
    main_window.setCentralWidget(renderer)

    # Добавляем верхнее меню
    main_window.setup_main_menu()

    print("Пространство отображено.")
