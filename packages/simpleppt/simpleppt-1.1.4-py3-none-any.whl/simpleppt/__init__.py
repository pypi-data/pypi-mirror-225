try:
    from importlib_metadata import version
except:
    from importlib.metadata import version
__version__ = version(__name__)
del version

from .load_data import load_example
from .ppt import ppt
from .project_ppt import project_ppt
from .SimplePPT import SimplePPT
