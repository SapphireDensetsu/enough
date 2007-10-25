# Copyright (c) 2007 Enough Project.
# See LICENSE for details.


class MovingPos(object):
    def __init__(self, target_pos=None):
        self.current_pos = None
        if target_pos is not None:
            self.set_target(target_pos)

    def set_target(self, target_pos):
        self.target_pos = list(target_pos)
        if self.current_pos is None:
            self.current_pos = list(target_pos)

    def update(self, step=0.1):
        if self.target_pos is None:
            raise ValueError('Target pos was not set')
        for i in xrange(len(self.target_pos)):
            self.current_pos[i] += (self.target_pos[i] - self.current_pos[i])*step


