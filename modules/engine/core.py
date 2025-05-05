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
        self.space_data = {
            "point": {},
            "segment": {},
            "plane": {},
            "polyhedron": {}
        }
        self.initialize_empty_space_called = False
        self.load_space_called = False
        # Устанавливаем индекс
        self.props_index = 0
        print("Движок инициализирован.")

    def add_props_index(self) -> None:
        self.props_index += 1

    def initialize_empty_space(self) -> None:
        """
        Создает пустое пространство заданных размеров.
        :param dimensions: Размеры пространства (x, y, z).
        """
        try:
            self.space_data = {
                "point": {},
                "segment": {},
                "plane": {},
                "polyhedron": {}
            }
            self.initialize_empty_space_called = True
            print(f"Создано новое пространство.")
        except Exception as e:
            print(f"Ошибка при создании пространства: {e}")

    def add_point(self, id: str, coordinates: tuple, color: str) -> None:
        """
        Добавляет точку в пространство.
        :param id: Идентификатор точки.
        :param coordinates: Координаты точки.
        :param color: Цвет точки.
        """
        self.space_data["point"][id] = {
            "coordinates": coordinates,
            "color": color
        }
        self.add_props_index()

    def add_segment(self, id: str, start: tuple, end: tuple, color: str) -> None:
        """
        Добавляет сегмент в пространство.
        :param id: Идентификатор сегмента.
        :param start: Начальная точка сегмента.
        :param end: Конечная точка сегмента.
        :param color: Цвет сегмента.
        """
        self.space_data["segment"][id] = {
            "start": start,
            "end": end,
            "color": color
        }
        self.add_props_index()

    def add_plane(self, id: str, points: list, color: str) -> None:
        """
        Добавляет плоскость в пространство.
        :param id: Идентификатор плоскости.
        :param points: Список точек, определяющих плоскость.
        :param color: Цвет плоскости.
        """
        self.space_data["plane"][id] = {
            "points": points,
            "color": color
        }
        self.add_props_index()

    def add_polyhedron(self, id: str, faces: list, color: str) -> None:
        """
        Добавляет многогранник в пространство.
        :param id: Идентификатор многогранника.
        :param faces: Список граней многогранника.
        :param color: Цвет многогранника.
        """
        self.space_data["polyhedron"][id] = {
            "faces": faces,
            "color": color
        }
        self.add_props_index()

    def clear_space(self) -> None:
        """
        Очищает текущее пространство.
        """
        try:
            self.space_data = None
            print("Пространство очищено.")
        except Exception as e:
            print(f"Ошибка при очистке пространства: {e}")

    def save_space(self, parent_widget: Any, file_name: str | None = None) -> None:
        """
        Сохраняет текущее состояние пространства.
        :param parent_widget: Виджет, который будет родителем для диалога.
        """
        try:
            if self.space_data is None:
                raise ValueError("Нечего сохранять: пространство не инициализировано.")

            if not file_name:
                # Создаем уникальное имя файла с временной меткой
                file_name, _ = QInputDialog.getText(
                    parent_widget,  # Передаем виджет, а не self
                    "Сохранить пространство",
                    "Введите имя файла:"
                )
            if file_name:
                file_path = f"saves/{file_name}.json"
                # Создаем директорию, если она не существует
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Сохраняем данные в файл
                save_state(self.space_data, file_path)
                print(f"Пространство успешно сохранено в {file_path}.")
        except Exception as e:
            print(f"Ошибка при сохранении пространства: {e}")

    def load_space(self, file_path: str | None = None) -> None:
        """
        Загружает состояние пространства.
        :param file_path: Путь к файлу.
        """
        try:
            print(f"Попытка загрузить пространство из файла: {file_path}")
            loaded_data = load_state(file_path)
            print(f"loaded_data: {loaded_data}")
            if loaded_data is not None:
                self.load_space_called = True
                self.space_data = loaded_data
                self.props_index = (
                    len(self.space_data["point"]) +
                    len(self.space_data["segment"]) +
                    len(self.space_data["plane"]) +
                    len(self.space_data["polyhedron"])
                )
                print(f"Пространство успешно загружено из {file_path}.")
                print(f"что внутри: {self.space_data}")
            else:
                print("Не удалось загрузить пространство: данные не были загружены.")
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке пространства: {e}")

    def continue_last_session(self) -> None:
        """
        Продолжает работу с последним сохранением.
        """
        try:
            self.space_data = load_last_session()
            if self.space_data is not None:
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
        return self.space_data

    def exit_application(self) -> None:
        """
        Завершает работу приложения с автосохранением.
        """
        self.save_space()
        QApplication.quit()
