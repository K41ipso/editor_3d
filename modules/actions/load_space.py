from typing import Any

from modules.engine.core import Engine
from modules.engine.opengl_widget import OpenGLWidget


def load_saved_space(main_window: Any) -> None:
    """
    Загружает сохраненное пространство и отображает его.
    :param main_window: Экземпляр MainWindow.
    """
    engine = Engine()
    engine.load_space("saves/current_space.json")
    print("Пространство успешно загружено.")

    # Заменяем главное меню на OpenGL-виджет
    opengl_widget = OpenGLWidget(engine.get_space())
    main_window.setCentralWidget(opengl_widget)

    # Добавляем верхнее меню
    main_window.setup_main_menu()

    print("Пространство отображено.")
