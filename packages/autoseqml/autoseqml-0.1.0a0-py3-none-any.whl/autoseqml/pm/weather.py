import pandas as pd

from ..utils import check_ext

class Weather:
    def __init__(self, file):
        if not check_ext(file, 'weather'): return 'Invalid extensions or wrong data type'
        else:
            pass
    
    