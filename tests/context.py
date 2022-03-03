import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mwedittypes.mwedittypes import EditTypes
from mwedittypes.node_differ import parse_change_text
