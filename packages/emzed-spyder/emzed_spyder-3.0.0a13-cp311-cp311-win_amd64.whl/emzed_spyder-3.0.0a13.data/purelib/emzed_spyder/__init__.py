import os
import sys
from importlib.metadata import version

__version__ = version(__package__)

os.environ["QT_API"] = "pyqt5"

if sys.platform == "darwin":
    # https://sissource.ethz.ch/sispub/emzed/emzed-spyder/-/issues/23
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
