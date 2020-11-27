from .base import *


live = False
try:
    from .local import *

except ImportError:
    live = True
    
if live:
    from .production import *