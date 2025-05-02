import random
from typing import Any

import numpy as np
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LINES,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_QUADS,
    glBegin,
    glClear,
    glClearColor,
    glColor3f,
    glEnable,
    glEnd,
    glLoadIdentity,
    glMatrixMode,
    glRotatef,
    glTranslatef,
    glVertex3f,
    glViewport
)
from OpenGL.GLU import gluPerspective
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QOpenGLWidget, QDialog

from modules.tools.modal_dialogs import PointsInputDialog


class OpenGLWidget(QOpenGLWidget):
    def __init__(
            self,
            space_data: Any = None,
            parent: Any = None,
            keyboard_handler: Any = None,
            rotation_x: float = 0.0,
            rotation_y: float = 0.0,
            last_mouse_pos: Any = None,
            mouse_pressed: bool = False
    ) -> None:
        super().__init__(parent)
        self.space_data = space_data
        self.rotation_x = rotation_x  # Угол поворота по оси X
        self.rotation_y = rotation_y  # Угол поворота по оси Y
        self.last_mouse_pos = last_mouse_pos  # Последняя позиция мыши
        self.keyboard_handler = keyboard_handler  # Ссылка на KeyboardHandler для доступа к координатам
        self.mouse_pressed = mouse_pressed  # Флаг для отслеживания состояния кнопки мыши

    def initializeGL(self) -> None:
        """
        Инициализация OpenGL.
        """
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Темно-серый фон
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width: int, height: int) -> None:
        """
        Настройка проекции при изменении размеров окна.
        """
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self) -> None:
        """
        Отрисовка OpenGL.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Применение координат из KeyboardHandler
        if self.keyboard_handler:
            x, y, z = self.keyboard_handler.position
            glTranslatef(x, y, z - 5.0)  # Перемещение камеры (z - 5.0 для отдаления от объектов)
        else:
            glTranslatef(0.0, 0.0, -5.0)  # Задний план, если KeyboardHandler не задан

        glRotatef(self.rotation_x, 1, 0, 0)  # Поворот по оси X
        glRotatef(self.rotation_y, 0, 1, 0)  # Поворот по оси Y

        self.draw_coordinate_grid() # Рисуем координатную сетку

    def draw_cube(self) -> None:
        """
        Рисует куб (пример примитивного объекта).
        """
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)  # Красный
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)

        glColor3f(0.0, 1.0, 0.0)  # Зеленый
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glEnd()
        #self.update()

    def draw_coordinate_grid(self) -> None:
        """
        Рисует бесконечную координатную сетку.
        """
        try:
            print("Начало рисования бесконечной координатной сетки...")

            # Установка цвета сетки
            glColor3f(0.5, 0.5, 0.5)  # Серый цвет для сетки
            print("Цвет сетки успешно установлен.")

            # Начало рисования линий
            glBegin(GL_LINES)
            print("Начало рисования линий (glBegin).")

            # Получаем текущую позицию камеры
            if self.keyboard_handler:
                x, y, z = self.keyboard_handler.position
            else:
                x, y, z = 0, 0, 0

            grid_size = 100  # Размер сетки
            step = 1  # Шаг между линиями

            # Рисуем линии сетки
            for i in range(-grid_size, grid_size + 1, step):
                # Линии по оси X
                glVertex3f(i, 0, -grid_size + z)
                glVertex3f(i, 0, grid_size + z)

                # Линии по оси Z
                glVertex3f(-grid_size + x, 0, i)
                glVertex3f(grid_size + x, 0, i)

            glEnd()
            print("Рисование линий завершено (glEnd).")
            print("Бесконечная координатная сетка успешно нарисована.")
        except Exception as e:
            print(f"Неожиданная ошибка при рисовании координатной сетки: {e}")

    def mousePressEvent(self, event: Any) -> None:
        """
        Обработка нажатия кнопки мыши.
        """
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: Any) -> None:
        """
        Обработка движения мыши.
        """
        #print(f"мышь зажата : {self.mouse_pressed}")
        if self.mouse_pressed or self.last_mouse_pos is not None:
            dx = event.x() - self.last_mouse_pos.x()  # type: ignore
            dy = event.y() - self.last_mouse_pos.y()
            self.rotation_x += dy  # Изменяем угол поворота по оси X
            self.rotation_y += dx  # Изменяем угол поворота по оси Y
            self.last_mouse_pos = event.pos()
            self.update()  # Перерисовываем виджет

    def mouseReleaseEvent(self, event: Any) -> None:
        """
        Обработка отпускания кнопки мыши.
        """
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            self.last_mouse_pos = None

    def on_draw_plane(self):
        dialog = PointsInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            points = dialog.get_points()
            print(f"Полученные координаты: {points}")  # Отладочный вывод
            self.draw_plane(points)

    def draw_plane(self, points):
        try:
            # Преобразуйте строки в числа
            p1 = tuple(map(float, points[0]))
            p2 = tuple(map(float, points[1]))
            p3 = tuple(map(float, points[2]))

            print(f"Координаты для отрисовки: {p1}, {p2}, {p3}")  # Отладочный вывод

            try:
                # Установите цвет для плоскости
                glColor3f(0.0, 0.0, 1.0)  # Синий цвет
                print("Цвет плоскости установлен.")
            except Exception as e:
                print(f"Ошибка при установке цвета плоскости: {e}")

            # Найдите четвертую точку для завершения квадрата
            try:
                # Вектор от p1 до p2
                v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
                # Вектор от p1 до p3
                v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
                # Векторное произведение для нахождения нормали
                normal = (
                    v1[1] * v2[2] - v1[2] * v2[1],
                    v1[2] * v2[0] - v1[0] * v2[2],
                    v1[0] * v2[1] - v1[1] * v2[0]
                )
                # Нормализация нормали
                length = (normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2) ** 0.5
                normal = (normal[0] / length, normal[1] / length, normal[2] / length)

                # Определяем четвертую точку, смещая p3 вдоль нормали
                # Здесь мы должны использовать правильное смещение, чтобы p4 находилась на плоскости
                # Например, можно использовать среднее значение координат для нахождения p4
                p4 = (
                    p1[0] + v1[0] + v2[0],
                    p1[1] + v1[1] + v2[1],
                    p1[2] + v1[2] + v2[2]
                )
                print(f"Четвертая точка определена: {p4}")
            except Exception as e:
                print(f"Ошибка при вычислении четвертой точки: {e}")

            try:
                glBegin(GL_QUADS)
                glVertex3f(*p1)
                glVertex3f(*p2)
                glVertex3f(*p3)
                glVertex3f(*p4)
                glEnd()
                print("Плоскость успешно нарисована.")
            except Exception as e:
                print(f"Ошибка при отрисовке плоскости: {e}")

            try:
                self.update()  # Перерисовываем виджет
                print("Виджет обновлен.")
            except Exception as e:
                print(f"Ошибка при обновлении виджета: {e}")

        except Exception as e:
            print(f"Ошибка при отрисовке плоскости: {e}")
