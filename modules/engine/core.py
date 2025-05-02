import os
from typing import Any

import numpy as np

from PyQt5.QtWidgets import QApplication, QInputDialog

from .loader import load_last_session, load_state, save_state


class Engine:
    """
    Основной класс движка, управляющий состоянием пространства.
    """

    def __init__(self) -> None:
        """
        Инициализация движка.
        """
        self.space: Any = None  # Текущее состояние пространства
        self.state_file = "saves/current_space.json"  # Путь к файлу состояния
        self.initialize_empty_space_called = False
        self.load_space_called = False
        print("Движок инициализирован.")

    def initialize_empty_space(self, dimensions: tuple[int, int, int] = (10, 10, 10)) -> None:
        """
        Создает пустое пространство заданных размеров.
        :param dimensions: Размеры пространства (x, y, z).
        """
        try:
            self.space = np.zeros(dimensions, dtype=int)  # Пустое пространство (массив нулей)
            self.initialize_empty_space_called = True
            print(f"Создано новое пространство размером {dimensions}.")
        except Exception as e:
            print(f"Ошибка при создании пространства: {e}")

    def update_space(self, position: Any, value: int) -> None:
        """
        Обновляет значение в определенной позиции пространства.
        :param position: Координаты (x, y, z).
        :param value: Новое значение.
        """
        try:
            if self.space is None:
                raise ValueError("Пространство не инициализировано.")
            self.space[position] = value
            print(f"Обновлено значение в позиции {position}: {value}")
        except IndexError:
            print(f"Ошибка: Позиция {position} выходит за пределы пространства.")
        except Exception as e:
            print(f"Неожиданная ошибка при обновлении пространства: {e}")

    def clear_space(self) -> None:
        """
        Очищает текущее пространство.
        """
        try:
            self.space = None
            print("Пространство очищено.")
        except Exception as e:
            print(f"Ошибка при очистке пространства: {e}")

    def save_space(self, parent_widget: Any, file_path: str | None = None) -> None:
        """
        Сохраняет текущее состояние пространства.
        :param parent_widget: Виджет, который будет родителем для диалога.
        :param file_path: Путь к файлу (если не указан, используется уникальное имя).
        """
        try:
            if self.space is None:
                raise ValueError("Нечего сохранять: пространство не инициализировано.")

            # Создаем уникальное имя файла с временной меткой
            file_name, ok = QInputDialog.getText(
                parent_widget,  # Передаем виджет, а не self
                "Сохранить пространство",
                "Введите имя файла:"
            )
            if ok and file_name:
                file_path = f"saves/{file_name}.json"
                # Создаем директорию, если она не существует
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Сохраняем данные в файл
                save_state(self.space, file_path)
                print(f"Пространство успешно сохранено в {file_path}.")
        except Exception as e:
            print(f"Ошибка при сохранении пространства: {e}")

    def exit_application(self) -> None:
        """
        Завершает работу приложения с автосохранением.
        """
        self.save_space()
        QApplication.quit()

    def load_space(self, file_path: str | None = None) -> None:
        """
        Загружает состояние пространства.
        :param file_path: Путь к файлу (если не указан, используется self.state_file).
        """
        try:
            file_path = file_path or self.state_file
            self.space = load_state(file_path)
            if self.space is not None:
                self.load_space_called = True
                print(f"Пространство успешно загружено из {file_path}.")
            else:
                print("Не удалось загрузить пространство.")
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке пространства: {e}")

    def continue_last_session(self) -> None:
        """
        Продолжает работу с последним сохранением.
        """
        try:
            self.space = load_last_session()
            if self.space is not None:
                print("Продолжение работы с последним сохранением.")
            else:
                print("Последнее сохранение не найдено.")
        except Exception as e:
            print(f"Ошибка при продолжении последней сессии: {e}")

    def get_space(self) -> Any:
        """
        Возвращает текущее состояние пространства.
        :return: Текущее пространство (NumPy массив).
        """
        return self.space
