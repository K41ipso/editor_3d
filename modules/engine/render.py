from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *


class Renderer(QOpenGLWidget):
    def __init__(self, space_data=None, parent=None):
        super().__init__(parent)
        self.space_data = space_data

    def initializeGL(self):
        """
        Инициализация OpenGL.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        """
        Настройка проекции при изменении размеров окна.
        """
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """
        Отрисовка OpenGL.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)  # Перемещение камеры
        self.draw_cube()

    def draw_cube(self):
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