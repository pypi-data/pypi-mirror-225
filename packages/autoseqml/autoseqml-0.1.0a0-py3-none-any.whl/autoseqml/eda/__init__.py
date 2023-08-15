from .csv import CSV
from .txt import TXT
from ..utils import check_ext

def EDA(file):
    if not check_ext(file): return 'file extension unacceptable'

    ext = file.split('.')[-1]
    if ext=='csv':
        return CSV(file)
    elif ext=='txt':
        return TXT(file)
        
# class EDA:
#     def __init__(self, file):
#         if not check_ext(file): return 'file extension unacceptable'
        
#         ext = file.split('.')[-1]
#         if ext=='csv':
#             self.eda = CSV(file)
#         elif ext=='txt':
#             self.eda = TXT(file)
        
