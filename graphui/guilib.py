## /* Copyright 2007, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

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
