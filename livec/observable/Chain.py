from observer import Observable

class Chain(Observable):
    def __init__(self, *lists):
        Observable.__init__(self)
        self.lists = list(lists)
        for l in self.lists:
            l.add_observer(self)

    # TODO: Not nice:
    def chain_add(self, list):
        self.lists.append(list)
        list.add_observer(self)
        l = len(self)
        for observer in self.observers:
            for index, item in enumerate(list):
                observer.observe_insert(self, l+index, item)
    def chain_remove(self, list_):
        lindex = self.lists.index(list_)
        self.lists.pop(lindex)
        list_.remove_observer(self)
        
        l = sum(len(l) for l in self.lists[:lindex])
        for observer in self.observers:
            for item in list_:
                observer.observe_pop(self, l)

    def __getitem__(self, index):
        assert isinstance(index, int), "only ints supported as of yet.."
        offset = 0
        for l in self.lists:
            if offset <= index < offset+len(l):
                return l[index-offset]
            offset += len(l)

    def __len__(self):
        return sum(map(len, self.lists))

    def __iter__(self):
        for l in self.lists:
            for item in l:
                yield item

    def observe_insert(self, list_, index, item):
        lindex = self.lists.index(list_)
        l = sum(len(l) for l in self.lists[:lindex])
        for observer in self.observers:
            observer.observe_insert(self, l+index, item)

    def observe_pop(self, list_, index):
        lindex = self.lists.index(list_)
        l = sum(len(l) for l in self.lists[:lindex])
        for observer in self.observers:
            observer.observe_pop(self, l+index)
