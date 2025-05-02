from typing import Any

from modules.engine.core import Engine
from modules.engine.opengl_widget import OpenGLWidget


def continue_last_session(main_window: Any = None) -> None:
    """
    Продолжает работу с последним сохранением.
    :param main_window: Экземпляр MainWindow (опционально).
    """
    engine = main_window.engine if main_window else Engine()
    try:
        engine.continue_last_session()
        print("Продолжение работы с последним сохранением.")
    except FileNotFoundError:
        print("Ошибка: Файл последнего сохранения не найден.")
        return
    except Exception as e:
        print(f"Неожиданная ошибка при продолжении работы: {e}")
        return

    if main_window is not None:
        if hasattr(main_window, "keyboard_handler"):
            main_window.keyboard_handler.position = [0, 0, 0]

        print("Инициализация OpenGL...")
        opengl_widget = OpenGLWidget(engine.get_space(), keyboard_handler=main_window.keyboard_handler)
        print("OpenGL инициализирован.")
        main_window.setCentralWidget(opengl_widget)

        try:
            main_window.setup_main_menu()
        except AttributeError:
            print("Ошибка: Метод setup_main_menu не найден в классе MainWindow.")
        except Exception as e:
            print(f"Неожиданная ошибка при настройке верхнего меню: {e}")

        print("Пространство отображено.")
    else:
        print("Параметр main_window не передан. Продолжение работы без GUI.")