from .__confutil__ import confutil
from .__log__ import *

__all__ = ['__version__', 'check_config']
__version__ = '1.2.1'


def check_config(_object=None, _filename='config'):
    return confutil.check_config(_object, _filename)
