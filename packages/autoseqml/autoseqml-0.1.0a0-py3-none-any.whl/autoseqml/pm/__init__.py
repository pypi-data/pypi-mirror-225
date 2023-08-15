import os
from .weather import Weather

class PatternMining:
    def __init__(self, window_size=1):
        self.ws = window_size
    
    def split(self):
        pass
    
    def embed(self, content):
        lexicon = {}
        
    
    def encode(self, code:list):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'wordlist.txt'), 'r') as f:
            wl = [w.strip() for w in f.readlines()]
        
        return ' '.join([wl[c] for c in code])
    
if __name__=='__main__':
    print('test')