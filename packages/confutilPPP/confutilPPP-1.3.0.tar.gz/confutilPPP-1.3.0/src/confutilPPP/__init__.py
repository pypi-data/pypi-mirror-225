from .__confutil__ import confutil

__all__ = ['__version__', 'check_config']
__version__ = '1.3.0'


def check_config(_object=None, _filename='config'):
    return confutil.check_config(_object, _filename)
