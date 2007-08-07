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

#import psyco
#psyco.full()

import sys
import pygame
from GraphWidget import GraphWidget
from RowWidget import RowWidget
from App import AppWidget
from Lib.Point import Point

def main():
    pygame.init()
    a = AppWidget(800, 600)
    
    r = RowWidget(pos=Point((0,0)))
    r.add_widget_to_row(GraphWidget(size=Point((300,300))))
    r.add_widget_to_row(GraphWidget(size=Point((300,300))))
    
    #a.add_widget(GraphWidget(size=Point((800,600))))
    a.add_widget(r)
    r.transpose()
    a.run()

import time
real_time = time.time
cpu_time = time.clock

# Don't count sleeping-time and such
profile_time = cpu_time

def profile():
    from cProfile import Profile
    import time
    p = Profile(profile_time)
    p.runcall(main)
    import lsprofcalltree
    k = lsprofcalltree.KCacheGrind(p)
    k.output(open('prof.kgrind', 'w+b'))
    print "Profile results written to prof.kgrind"

if __name__=='__main__':
    if sys.argv[1:]:
        should_profile_str, = sys.argv[1:]
        should_profile = should_profile_str.lower() in ["y", "yes", "t", "true"]
    else:
        should_profile = False
    if should_profile:
        profile()
    else:
        main()
