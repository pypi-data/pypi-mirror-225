"""GUI Interface for Appy.
    Provides Interface to GUI elements and screens. 
"""


from . import style
from .gui import GUI
from .tkgui import TKGUI
from .screens import *
from .elements import *

pack_defaults = {**style.paddings, "expand": True}
WIDTH = 1280
HEIGHT = 720
