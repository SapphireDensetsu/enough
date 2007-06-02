class DisjointSets(object):
    def __init__(self):
        self.sets = []

    def _set_of(self, item):
        for s in self.sets:
            for s_item in s:
                if item == s_item:
                    return s
        return None

    def set_of(self, item):
        s = self._set_of(item)
        if s is None:
            s = set((item,))
        return s
    
    def union(self, a, b):
        set_a = self._set_of(a)
        set_b = self._set_of(b)
        if set_a is not None and set_b is not None:
            if set_a == set_b:
                return
            else:
                set_a.update(set_b)
                self.sets.remove(set_b)
                return
        if set_a is None and set_b is not None:
            set_b.add(a)
            return
        if set_b is None and set_a is not None:
            set_a.add(b)
            return

        # both sets are None
        # none exist
        self.sets.append(set((a,b)))

    def split(self, item):
        s = self._set_of(item)
        if s is None:
            return
        s.remove(item)
        if len(s) == 1:
            # a one item set is meaningless, we are only interseted in groups
            self.sets.remove(s)
                
                
