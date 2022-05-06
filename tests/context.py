import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mwsimpleedittypes.mwsimpleedittypes import EditTypes
from mwsimpleedittypes.differ import parse_change_text
