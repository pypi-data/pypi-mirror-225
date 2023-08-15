import os
import random
import numpy as np

import torch
import pytorch_lightning as pl

from .utils import exceptions
from .llm import LLM

class AutoSeqML:
    def __init__(self, path):
        self._path = path
        
    def __str__(self):
        return f'training data path: {self._path}'
    
    def is_path_available(self):
        return os.path.exists(self._path)
    
    def items(self):
        return os.listdir(self._path)
    
    def seed(self, seed):
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        pl.seed_everything(seed)
    
    def downstream(self):
        llm = LLM(self._path)
        
    
if __name__=='__main__':
    print('Auto sequential ML package loaded!')