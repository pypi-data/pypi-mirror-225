import openai

class Forecast:
    
    def __init__(self, api_key=''):
        self.api_key = api_key
        
    def set_key(self, key):
        self.api_key = api_key
            