#import psyco
#psyco.full()

import sys
import pygame
from GraphApp import GraphApp

def main():
    pygame.init()
    a = GraphApp(800, 600)
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
