# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from __future__ import with_statement
from gui.main import pygame_display

import pygame

profile_filename = 'profile'

def clock():
    import os
    utime, stime, cutime, cstime, elapsed_time = os.times()
    return utime+stime

def profile_call(func, *args, **kw):
    from cProfile import Profile
    p = Profile() #clock)
    print "Profiling to", profile_filename
    p.runcall(func, *args, **kw)

    from pytools import lsprofcalltree
    k = lsprofcalltree.KCacheGrind(p)
    pdump_filename = profile_filename+'.pstats'
    p.dump_stats(pdump_filename)
    print "Profile dumped to", pdump_filename
    kcache_grind_filename = profile_filename+'.kcachegrind'
    with open(kcache_grind_filename, 'w+b') as f:
        k.output(f)
    print "Profile results written to", kcache_grind_filename

with pygame_display((1024, 768), pygame.DOUBLEBUF) as display:
    from codegui.loop import loop
    from codegui.BrowserWidget import BrowserWidget

    from codegui.Namer import Namer
    from codegui.widget_for import NormalWidgetMaker
    loop.namer = Namer()
    
    from example import example
    loop.browser = BrowserWidget(NormalWidgetMaker.make(example))

    import pygame
    pygame.key.set_repeat(250,10)

    loop.loop(display, loop.browser)
#    profile_call(loop.loop, display, loop.browser)
