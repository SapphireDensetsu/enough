## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
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

import socket
import select
import time


class Reactor(object):
    def __init__(self):
        self.handlers = {}
        self.time_handlers = []
        self.next_time = None

    def quit(self):
        self.stop = True
        
    def remove_file(self, f_obj):
        if f_obj in self.handlers:
            del self.handlers[f_obj]
        
    def register(self, f_obj, action, handler, one_shot=False):
        if action not in ('read', 'write'):
            raise ValueError('Invalid action', action)
        
        self.handlers.setdefault(f_obj, {'read':[], 'write':[]})[action].append((handler, one_shot))

    def register_timeout_from_now(self, time_from_now, handler):
        self.register_timeout(time.time() + time_from_now, handler)
        
    def register_timeout(self, t, handler):
        self.time_handlers.append((t, handler))
        self.time_handlers.sort()
        self.next_time = self.time_handlers[0][0]

    def single_loop_files(self):
        rds = []
        wts = []
        for f_obj in self.handlers.keys():
            if self.handlers[f_obj]['read']:
                rds.append(f_obj)
            if self.handlers[f_obj]['write']:
                wts.append(f_obj)
                
        if not rds and not wts:
            return
        
        if self.next_time is None:
            wait = None
        else:
            wait = max(time.time() - self.next_time, 0)

        try:
            rds, wts, garbage = select.select(rds, wts, [], wait)
        except KeyboardInterrupt:
            print 'Caught in select, wait=', wait
            raise
        
        for action, f_objs in (('read', rds), ('write', wts)):
            for f_obj in f_objs:
                if f_obj not in self.handlers:
                    continue # it got delete by another handler, probably
                handlers = self.handlers[f_obj][action]
                removed = 0
                for i, (handler, one_shot) in enumerate(handlers[:]):
                    if one_shot:
                        self.handlers[f_obj][action].pop(i - removed)
                        removed += 1
                    handler()

    def single_loop_times(self):
        now = time.time()
        i = 0
        while i < len(self.time_handlers):
            t, handler = self.time_handlers[i]
            if t > now:
                i += 1
                continue
            
            self.time_handlers.pop(i)
            handler()
            continue
        
        
    def run(self):
        self.single_loop_files()
        self.single_loop_times()

    def loop(self):
        self.stop = False
        while not self.stop:
            self.run()
            #time.sleep(0.01)
        


