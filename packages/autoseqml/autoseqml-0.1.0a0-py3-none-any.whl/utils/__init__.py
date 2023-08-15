import os
from configobj import ConfigObj

path = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(path, 'config.ini')

def check_ext(file, data_type=''):
    cfg = ConfigObj(CONFIG, encoding='utf8')
    ext = file.split('.')[-1]
    try:
        return ext in cfg['extensions'][data_type]
    except:
        exts = []
        for v in cfg['extensions'].values():
            exts.extend(list(v))
        return ext in exts