
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

class MovingLine(MovingValue):
    # like MovingValue but for a list of points the represent a line
    def update(self):
        if not self.current:
            self.current = [Point(0,0) for p in self.final]
        else:
            len_diff = len(self.final) - len(self.current)
            if len_diff > 0:
                # delete intermediate points until they are the same length
                for i in xrange(len_diff):
                    self.current.pop(1)
            elif len_diff < 0:
                for i in xrange(len_diff):
                    self.current.insert(1, self.current[0].copy())
                    
        for current_p, final_p in zip (self.current, self.final):
            current_p += (final_p - current_p) * self.step
