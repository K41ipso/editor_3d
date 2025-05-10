from typing import Any

from PyQt5.QtWidgets import QFileDialog  # type: ignore

from modules.engine.opengl_widget import OpenGLWidget


def load_saved_space(main_window: Any = None) -> None:
    """
    Загружает сохраненное пространство и отображает его.
    :param main_window: Экземпляр MainWindow (опционально).
    """
    try:
        # Открываем диалог выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            main_window,  # Передаем main_window как родительский виджет
            "Выберите файл сохранения",
            "saves/",  # Директория по умолчанию
            "JSON Files (*.json);;All Files (*)",  # Фильтр файлов
            options=options,
        )

        if not file_path:
            print("Файл не выбран.")
            return

        # Загружаем пространство из выбранного файла
        main_window.engine.load_space(file_path)
        print(f"Пространство успешно загружено из {file_path}.")

        # Обновляем дату редактирования файла
        with open(file_path, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(content + ' ')  # Добавляем пробел
            file.truncate()  # Удаляем пробел
            print(f"Дата редактирования файла {file_path} обновлена.")

    except FileNotFoundError:
        print(f"Ошибка при загрузке состояния: Файл сохранения не найден по пути {file_path}.")
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке пространства: {e}")

    # Проверяем, что main_window передан
    if main_window is not None:
        # Сброс позиции камеры
        if hasattr(main_window, "keyboard_handler"):
            main_window.keyboard_handler.position = [0, 0, 0]

        # Заменяем главное меню на OpenGL-виджет
        print("Инициализация OpenGL...")
        opengl_widget = OpenGLWidget(main_window.engine.get_space(), keyboard_handler=main_window.keyboard_handler)
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
