
from Lib.Point import Point

def get_default(val, default):
    if val is None:
        return default
    return val


class MovingValue(object):
    def __init__(self, current, final, step=0.1):
        self.current = current
        self.final = final
        self.step = step

    def update(self):
        self.current += (self.final - self.current) * self.step
        
        
class ParamHolder(object):
    def __init__(self, allowed_names, name=None):
        self.__dict__['_allowed_names'] = allowed_names
        self.__dict__['_name'] = get_default(name, self.__class__.__name__)
        self.__dict__['_params'] = {}

    def verify_exists(self, name):
        if name not in self.__dict__['_allowed_names']:
            raise AttributeError("%s can not hold attribute %s" % (self.__dict__['_name'], name))
        
    def __getattr__(self, name):
        self.verify_exists(name)
        return self.__dict__['_params'][name]

    def __setattr__(self, name, value):
        self.verify_exists(name)
        self.__dict__['_params'][name] = value


