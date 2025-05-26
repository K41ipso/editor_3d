"""
Инициализация пакета engine.
"""

from .core import Engine
from .loader import load_state, save_state
from .opengl_widget import OpenGLWidget
from .render import Renderer

__all__ = ["Engine", "load_state", "save_state", "Renderer", "OpenGLWidget"]
