from typing import Any

from modules.engine.core import Engine
from modules.engine.opengl_widget import OpenGLWidget


def load_saved_space(main_window: Any = None) -> None:
    """
    Загружает сохраненное пространство и отображает его.
    :param main_window: Экземпляр MainWindow (опционально).
    """
    engine = Engine()
    try:
        engine.load_space("saves/current_space.json")
        print("Пространство успешно загружено.")
    except FileNotFoundError:
        print("Ошибка при загрузке состояния: Файл сохранения не найден по пути saves/current_space.json.")
        return
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке пространства: {e}")
        return

    # Проверяем, что main_window передан
    if main_window is not None:
        # Заменяем главное меню на OpenGL-виджет
        print("Инициализация OpenGL...")
        opengl_widget = OpenGLWidget(engine.get_space())
        print("OpenGL инициализирован.")
        main_window.setCentralWidget(opengl_widget)
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
        print("Параметр main_window не передан. Пространство загружено без GUI.")
