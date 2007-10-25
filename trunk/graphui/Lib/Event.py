# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

class Event(object):
    def __init__(self, typ):
        self.type = typ
    def __repr__(self):
        return '<Event: %r>' % (self.__dict__,)
    def copy(self):
        new = type(self)(self.type)
        new.__dict__.update(self.__dict__)
        return new

class EventTrigger(object):
    '''The name EventTrigger was chosen to prevent confusion with
    events that are simply passed between objects'''
    def __init__(self):
        self.handlers = []
    def trigger(self, event, only_forced=False):
        if not self.handlers:
            return False
        someone_handled = False
        for handler, forced in self.handlers:
            if only_forced and not forced:
                continue
            someone_handled = someone_handled or handler(event)
        return someone_handled
    
    def register(self, handler, forced=False):
        self.handlers.append((handler, forced))

# TODO implement unregister

class TriggerList(object):
    def __init__(self):
        self.triggers = {}
        
    def register_event_type(self, event_type, handler, forced=False):
        self.triggers.setdefault(event_type, EventTrigger()).register(handler, forced=forced)

    def handle_event(self, event, only_forced=False):
        if event.type not in self.triggers:
            return False
        return self.triggers[event.type].trigger(event, only_forced=only_forced)
                            
